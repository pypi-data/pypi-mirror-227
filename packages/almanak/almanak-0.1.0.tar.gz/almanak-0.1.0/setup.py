# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['almanak']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'almanak',
    'version': '0.1.0',
    'description': 'A placeholder for the incoming Almanak package',
    'long_description': '# Almanak\n\nA placeholder for the incoming Almanak package.',
    'author': 'Lars',
    'author_email': 'lars@suanet.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
