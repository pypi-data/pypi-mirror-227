import argparse
import copy
import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime
from io import StringIO
from logging.handlers import RotatingFileHandler
from pathlib import Path

import dotenv
import numpy as np
import openai
import tiktoken
from git import Repo
from k_means_constrained import KMeansConstrained
from unidiff import PatchSet

BIN_NAME = "diffdigest"
XDG_STATE_HOME = Path(
    os.environ.get("XDG_STATE_HOME") or os.path.join(os.environ["HOME"], ".local", "state")
)
XDG_CONFIG_HOME = Path(
    os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.environ["HOME"], ".config")
)

RE_WHITESPACE = re.compile(r"\s+")
TOKEN_ENCODER = tiktoken.get_encoding("cl100k_base")
EMBEDDING_TOKEN_LIMIT = 8191
LLM_TOKEN_LIMIT = 4096
RESPONSE_TOKEN_ALLOWANCE = 150

# Prompts
PROMPT_SYSTEM = """
You are an expert software engineer contributing to a large open-source project.
Do not use vague language like "improve usability", "logic improvements", or "enhance functionality".
Do not include any author information or other placeholders.
Do not repeat the same information multiple times.
""".replace(
    "\n", " "
).strip()
PROMPT_SUMMARIZE_DIFF = """
Given the following Git diff, please generate a bulleted list of key changes.
Group related changes (including changes to a single function) into a single bullet point.
Incorporate new code comment text verbatim in the summary.
Include the purpose and intent of each change.
""".replace(
    "\n", " "
).strip()
PROMPT_COMMIT_MESSAGE = """
Given the following summary of code changes, please generate a short commit message that accurately describes the changes.
The commit message should have a subject and body separated by a blank line.
The subject should be a one-line summary of the high-level purpose and intent of the commit.
The body should summarize a few of the most relevant technical details.
""".replace(
    "\n", " "
).strip()


def main():
    # Set up environment
    config_path = XDG_CONFIG_HOME / BIN_NAME / f"{BIN_NAME}.env"
    dotenv.load_dotenv(config_path)
    if os.getenv("OPENAI_API_KEY", "") == "":
        sys.exit("OPENAI_API_KEY not set. Please set in the environment, or in " + str(config_path))
    openai.api_key = os.getenv("OPENAI_API_KEY")

    os.makedirs(XDG_STATE_HOME / BIN_NAME, exist_ok=True)
    init_logging(XDG_STATE_HOME / BIN_NAME / "log.jsonl")

    parser = argparse.ArgumentParser(description="Generate a commit message using GPT-3.5.")
    parser.add_argument("repo", help="Path to the Git repository", nargs="?", default=".")
    parser.add_argument("--ref", "-r", help="Git ref to use, otherwise uses working directory")
    parser.add_argument(
        "--commit",
        "-c",
        help="Automatically commit the changes to the repo",
        action="store_true",
    )

    args = parser.parse_args()
    if args.commit and args.ref is not None:
        sys.exit("Cannot specify --commit and --ref at the same time")

    diff_text = get_diff(args.repo, args.ref)
    if diff_text.strip() == "":
        sys.exit("Empty diff")
    diffs = split_diff(diff_text)
    summaries = [summarize_diff(diff) for diff in diffs]
    # TODO sort summaries so that the most relevant (code) ones are first
    commit_message = generate_commit_message(summaries)
    if args.commit:
        repo = Repo(args.repo)
        res = subprocess.run(
            ["git", "apply", "--cached"],
            input=diff_text + "\n",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=Path(args.repo).resolve(),
            text=True,
        )
        if res.returncode != 0:
            sys.exit(res.stdout)
        repo.index.commit(commit_message)
    else:
        print(commit_message)


def get_diff(repopath, ref=None):
    """Returns a textual diff of either the working directory or a specific commit."""
    repo = Repo(repopath)
    if ref is None:
        return repo.git.diff(ignore_blank_lines=True, ignore_all_space=True)
    else:
        return repo.git.diff(ref + "~1", ref, ignore_blank_lines=True, ignore_all_space=True)


def split_diff(diff_text):
    """splits a diff into chunks based on the model's token limit"""
    diff_token_limit = (
        LLM_TOKEN_LIMIT
        - len(TOKEN_ENCODER.encode(PROMPT_SYSTEM + " " + PROMPT_SUMMARIZE_DIFF))
        - RESPONSE_TOKEN_ALLOWANCE
    )
    diff_token_limit = 100 * int(np.floor(diff_token_limit / 100))

    # If the diff is short enough, then there is no need to split it
    diff_toklen = len(TOKEN_ENCODER.encode(diff_text))
    logging.info(f"total diff token length: {diff_toklen} (limit: {diff_token_limit})")
    if diff_toklen < diff_token_limit:
        return [diff_text]

    patch_set = PatchSet(StringIO(diff_text))
    compute_embeddings(patch_set)
    n_clusters = compute_clusters(patch_set, diff_token_limit)
    return diff_by_cluster(patch_set, n_clusters)


def compute_embeddings(patch_set):
    """Computes embeddings and token length for each hunk in a patch set."""
    hunks = []
    formatted = []
    embed_token_count = 0
    for changed_file in patch_set:
        if len(changed_file.patch_info) > 1 and changed_file.patch_info[1].startswith("index"):
            changed_file.patch_info[1] = "index\n"
        header_toklen = get_header_toklen(changed_file)
        for hunk in changed_file:
            hunk.toklen = header_toklen + len(TOKEN_ENCODER.encode(str(hunk)))
            hunks.append(hunk)
            hunk_formatted = fmt_plain_flip(changed_file.path, hunk)
            hunk_formatted_toklen = len(TOKEN_ENCODER.encode(hunk_formatted))
            # truncate long hunks by removing 10% of the text at a time until it fits
            # TODO: something smarter (add lines incrementally)
            while hunk_formatted_toklen > EMBEDDING_TOKEN_LIMIT:
                hunk_formatted = hunk_formatted[: int(len(hunk_formatted) * 0.9)]
                hunk_formatted_toklen = len(TOKEN_ENCODER.encode(hunk_formatted))
            embed_token_count += hunk_formatted_toklen
            formatted.append(hunk_formatted)
    cost = round(embed_token_count * 0.0001) / 1000
    logging.info(f"embedding {len(formatted)} hunks", dict(tokens=embed_token_count, cost=cost))
    embedding = get_embeddings(formatted, engine="text-embedding-ada-002")
    for hunk, embedding in zip(hunks, embedding):
        hunk.embedding = embedding
    return patch_set


def get_embeddings(list_of_text, engine, **kwargs):
    assert len(list_of_text) <= 2048, "The batch size should not be larger than 2048."

    # replace newlines, which can negatively affect performance.
    list_of_text = [text.replace("\n", " ") for text in list_of_text]

    data = openai.Embedding.create(input=list_of_text, engine=engine, **kwargs).data
    return [d["embedding"] for d in data]


def get_header_toklen(patched_file):
    f = copy.copy(patched_file)
    f.clear()
    return len(TOKEN_ENCODER.encode(str(f)))


def fmt_plain_flip(path, hunk):
    """
    Formats a hunk as plain-text suitable for embedding using openai's ada model. This is the best
    performing format among several I tested.
    """
    added = "\n".join([RE_WHITESPACE.sub(" ", l.value.strip()) for l in hunk if l.is_added])
    removed = "\n".join([RE_WHITESPACE.sub(" ", l.value.strip()) for l in hunk if l.is_removed])
    return f"""Path: {path}

Added:
```
{added}
```

Removed:
```
{removed}
```"""


def compute_clusters(patch_set, diff_token_limit):
    """Assigns each hunk in a patch set to a cluster."""
    hunks = []
    points = []
    for changed_file in patch_set:
        for hunk in changed_file:
            cost_100 = min(int(np.ceil(hunk.toklen / 100)), diff_token_limit // 100)
            for _ in range(cost_100):
                hunks.append(hunk)
                points.append(hunk.embedding)
    len(points) * 100

    n_clusters = int(np.ceil(len(points) * 100 / diff_token_limit))
    logging.info(f"computing {n_clusters} clusters")
    clf = KMeansConstrained(
        n_clusters=n_clusters,
        size_min=int(diff_token_limit / 200),
        size_max=int(diff_token_limit / 100),
        random_state=0,
    )
    clf.fit_predict(np.array(points))

    for hunk, cluster in zip(hunks, clf.labels_):
        hunk.cluster = cluster

    return n_clusters


def diff_by_cluster(patch_set, n_clusters):
    """splits a patch set into chunks based on the assigned hunk clusters, and returns them as text."""
    splitdiffs = [list() for _ in range(n_clusters)]

    for changed_file in patch_set:
        for i in range(len(splitdiffs)):
            ff = copy.copy(changed_file)
            ff.clear()
            for hunk in changed_file:
                if hunk.cluster == i:
                    ff.append(hunk)
            if len(ff) > 0:
                splitdiffs[i].append(ff)

    difftexts = ["\n".join(str(f) for f in ps) for ps in splitdiffs]
    [len(TOKEN_ENCODER.encode(diff)) for diff in difftexts]
    return difftexts


def summarize_diff(diff_text):
    user_input = PROMPT_SUMMARIZE_DIFF + "\n\n" + diff_text
    # truncate long diffs by removing 10% of the text at a time until it fits
    # TODO: something smarter (add lines incrementally)
    token_limit = (
        LLM_TOKEN_LIMIT - RESPONSE_TOKEN_ALLOWANCE - len(TOKEN_ENCODER.encode(PROMPT_SYSTEM))
    )
    user_input_tokens = len(TOKEN_ENCODER.encode(user_input))
    while user_input_tokens > token_limit:
        user_input = user_input[: int(len(user_input) * 0.9)]
        user_input_tokens = len(TOKEN_ENCODER.encode(user_input))
    logging.info(
        "gpt input",
        dict(system=PROMPT_SYSTEM, user=user_input, tokens=user_input_tokens),
    )
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT_SYSTEM},
            {"role": "user", "content": user_input},
        ],
        temperature=0.3,
        presence_penalty=0.2,
    )
    out = res["choices"][0]["message"]["content"]
    tokens = len(TOKEN_ENCODER.encode(" ".join([PROMPT_SYSTEM, user_input, out])))
    cost = round(tokens * 0.0015) / 1000
    logging.info(
        "gpt result",
        dict(system=PROMPT_SYSTEM, user=user_input, agent=out, tokens=tokens, cost=cost),
    )
    return out


def generate_commit_message(summaries):
    user_input = PROMPT_COMMIT_MESSAGE + "\n\n" + "\n".join(summaries)
    # truncate long diffs by removing 10% of the text at a time until it fits
    # TODO: something smarter (add lines incrementally)
    token_limit = (
        LLM_TOKEN_LIMIT - RESPONSE_TOKEN_ALLOWANCE - len(TOKEN_ENCODER.encode(PROMPT_SYSTEM))
    )
    user_input_tokens = len(TOKEN_ENCODER.encode(user_input))
    while user_input_tokens > token_limit:
        user_input = user_input[: int(len(user_input) * 0.9)]
        user_input_tokens = len(TOKEN_ENCODER.encode(user_input))
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT_SYSTEM},
            {"role": "user", "content": user_input},
        ],
        temperature=0.6,
    )
    out = res["choices"][0]["message"]["content"]
    tokens = len(TOKEN_ENCODER.encode(" ".join([PROMPT_SYSTEM, user_input, out])))
    cost = round(tokens * 0.0015) / 1000
    logging.info(
        "gpt result",
        dict(system=PROMPT_SYSTEM, user=user_input, agent=out, tokens=tokens, cost=cost),
    )
    return out


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "message": record.getMessage(),
        }
        log_entry.update(record.args)
        return json.dumps(log_entry)


def init_logging(path):
    file_handler = RotatingFileHandler(path, maxBytes=1000000, backupCount=10)
    file_handler.setFormatter(JsonFormatter())
    file_handler.doRollover()

    # Configure the root logger
    logging.basicConfig(level=logging.INFO, handlers=[file_handler], format="%(message)s")


if __name__ == "__main__":
    main()
