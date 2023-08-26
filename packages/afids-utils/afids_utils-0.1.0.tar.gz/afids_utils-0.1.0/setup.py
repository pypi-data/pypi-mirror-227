# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afids_utils', 'afids_utils.ext', 'afids_utils.resources']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=23.1.0,<24.0.0', 'numpy>=1.24.3,<2.0.0']

setup_kwargs = {
    'name': 'afids-utils',
    'version': '0.1.0',
    'description': 'Utility functions for working with AFIDs data / workflows',
    'long_description': '# Anatomical Fiducials (AFIDs) Utility Tools\n\n[![Documentation Status](https://readthedocs.org/projects/afids-utils/badge/?version=latest)](https://afids-utils.readthedocs.io/en/latest/?badge=latest)\n\nThe `afids_utils` package provides common utilities for projects involving \nanatomical fiducials (AFIDs). For a comprehensive list of available utilities \nrefer to the [documentation](https://afids-utils.readthedocs.io/en/stable) \npage.',
    'author': 'Jason Kai',
    'author_email': 'tkai@uwo.ca',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
