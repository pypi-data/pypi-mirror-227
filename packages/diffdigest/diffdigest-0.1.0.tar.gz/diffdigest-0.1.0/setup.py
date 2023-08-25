# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['diffdigest']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.32,<4.0.0',
 'k-means-constrained>=0.7.3,<0.8.0',
 'numpy>=1.25.2,<2.0.0',
 'openai>=0.27.9,<0.28.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'tiktoken>=0.4.0,<0.5.0',
 'unidiff>=0.7.5,<0.8.0']

entry_points = \
{'console_scripts': ['diffdigest = diffdigest.cli:main']}

setup_kwargs = {
    'name': 'diffdigest',
    'version': '0.1.0',
    'description': 'Generate commit messages from git diffs of any size using LLMs to cluster and summarize',
    'long_description': '# diffdigest\n\nGenerate commit messages from git diffs of any size using LLMs to cluster and summarize\n',
    'author': 'Max Johnson',
    'author_email': 'maxdjohnson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
