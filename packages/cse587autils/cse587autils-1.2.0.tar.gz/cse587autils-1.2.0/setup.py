# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cse587Autils', 'cse587Autils.DiceObjects', 'cse587Autils.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.25.1,<2.0.0', 'pandas>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'cse587autils',
    'version': '1.2.0',
    'description': 'A set of classes and functions to be used in CSE 587A',
    'long_description': "[![Build](https://github.com/Chase-Mateusiak/cse587Autils/actions/workflows/python-package.yml/badge.svg)](https://github.com/Chase-Mateusiak/cse587Autils/actions/workflows/python-package.yml)\n\n# Introduction\n\nThis package stores objects, functions and at some point possibly data for\nMichael Brent's CSE 587A: Algorithms for Computational Biology at Washington\nUniversity.  \n\n[See the documentation here](https://chase-mateusiak.github.io/cse587Autils/)\n\n# Installation\n\n## Typical User\n\nThis is on PyPI and may be installed with pip:\n\n```bash\npip install cse587Autils\n```\n\n## Cutting edge version\n\nIt is possible that the `dev` branch is ahead of `main` and the `pypi` version.\nHowever, `dev` is not necessarily as stable. Install the `dev` version at your\nown risk:\n\n```bash\npip install https://github.com/Chase-Mateusiak/cse587Autils.git@dev\n```\n\n# Developers\n\nIf you want to participate in improving this repository, then fork the repo\ninto your own profile. Issue pull requests against `dev`.  \n\n## codespace\n\nA development container is configured such that after you fork the repo, you\ncan launch a codespace with a pre-configured environment and start coding\nright away. Changes you make will be pushed to your fork, and from there you \ncan issue pull requests against this repo.",
    'author': 'chase mateusiak',
    'author_email': 'chase.mateusiak@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
