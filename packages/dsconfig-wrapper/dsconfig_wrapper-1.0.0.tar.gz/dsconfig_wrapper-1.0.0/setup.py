# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dsconfig_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['dsconfig==1.6.7', 'pytango==9.4.2']

setup_kwargs = {
    'name': 'dsconfig-wrapper',
    'version': '1.0.0',
    'description': "Wraps MAX IV's dsconfig JSON generator to let the user use Python to generate the config",
    'long_description': 'None',
    'author': 'CFEL-SC',
    'author_email': 'sc@cfel.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
