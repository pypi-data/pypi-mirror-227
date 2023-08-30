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
    'version': '1.1.0',
    'description': "Wraps MAX IV's dsconfig JSON generator to let the user use Python to generate the config",
    'long_description': '# dsconfig-wrapper\n\n[![pipeline status](https://gitlab.desy.de/cfel-sc-public/dsconfig-wrapper/badges/main/pipeline.svg)](https://gitlab.desy.de/cfel-sc-public/dsconfig-wrapper/-/commits/main) \n[![coverage report](https://gitlab.desy.de/cfel-sc-public/dsconfig-wrapper/badges/main/coverage.svg)](https://gitlab.desy.de/cfel-sc-public/dsconfig-wrapper/-/commits/main)\n\nThis is a small Python library to complement [MAX IV\'s](https://www.maxiv.lu.se/) excellent [dsconfig](https://gitlab.com/MaxIV/lib-maxiv-dsconfig) library, which can make the database for the [Tango](https://www.tango-controls.org/) controls system *declarative* by updating it from a JSON file.\n\nUsually, it looks like this:\n\n```mermaid\nflowchart TD\n    DatabaseDs[(Tango Database)]\n    DatabaseDs -->|dsconfig.dump| JsonFile[JSON file]\n    Human -->|vim/emacs| JsonFile\n    JsonFile -->|json2tango| DatabaseDs\n```\n\nWith this tool, it looks like this:\n\n```mermaid\nflowchart TD\n    DatabaseDs[(Tango Database)]\n    Human -->|vim/emacs| PythonFile[Python file]\n    DsconfigWrapper[dsconfig-wrapper] -->|import| PythonFile\n    PythonFile -->|dsconfig-wrapper| JsonFile\n    JsonFile -->|json2tango| DatabaseDs\n```\n\nThis way, we can have our configuration not in JSON, but in Python! And in Python, we can have, for instance, `argparse`, to create a little program that can generate a configuration with parameters. You can also use Python DRY elements in your configuration (say, you have the same motor, but with various different properties set).\n\n## Usage\n\nJust do\n\n```\npip install dsconfig-wrapper\n```\n\nand then use it to create a config JSON. Example:\n\n```python\ntest_servers = [\n    Server(\n        instance_name="my_instance_name",\n        class_name="my_class_name",\n        devices=[\n            Device(\n                identifier=Identifier(\n                    domain="my_domain",\n                    family="my_family",\n                    member="my_member",\n                    host="my_host:10000",\n                ),\n                properties={\n                    "prop_str": "strvalue",\n                    "prop_list_str": ["value1", "value2"],\n                    "prop_list_int": [2000, 3000],\n                    "prop_int": 2000,\n                },\n                polled_commands={"update": 1000},\n                attribute_properties={\n                    "State": AttributeProperties(archive_period_ms=1001),\n                    "velocity_mm_per_s": AttributeProperties(\n                        archive_abs_change=(-0.5, 0.5),\n                        archive_period_ms=5000,\n                        rel_change=(-0.05, 0.05),\n                    ),\n                },\n            )\n        ],\n    )\n]\ntest_config = Config(servers=test_servers)\nprint(config_to_json(test_config))\n```\n\nHere, we create a config for a device server with class `my_class_name` and one instance running at `tango://myhost:10000/my_domain/my_family/my_member`. The `update` command is polled every second, and we also set some properties and attribute properties.\n\nWe now run this program (say it\'s stored in `main.py`) and pipe it into dsconfig:\n\n```\npython main.py | json2tango\n```\n\nVoila!\n',
    'author': 'CFEL-SC',
    'author_email': 'sc@cfel.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.desy.de/cfel-sc-public/dsconfig-wrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
