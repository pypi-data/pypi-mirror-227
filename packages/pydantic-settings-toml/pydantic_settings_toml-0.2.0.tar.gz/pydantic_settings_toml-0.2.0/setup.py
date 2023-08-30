# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_settings_toml']

package_data = \
{'': ['*']}

install_requires = \
['pydantic-settings>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'pydantic-settings-toml',
    'version': '0.2.0',
    'description': 'Custom pydantic setting source for loading settings from toml files',
    'long_description': '',
    'author': 'Simone Dalla',
    'author_email': 'simodalla@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/simodalla/pydantic-settings-toml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
