# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dutils']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'bs4>=0.0.1,<0.0.2',
 'colorama>=0.4.6,<0.5.0',
 'pycryptodome>=3.18.0,<4.0.0',
 'random-user-agent>=1.0.1,<2.0.0',
 'requests[socks]>=2.19.1,<2.30',
 'sqlalchemy>=2.0.20,<3.0.0']

setup_kwargs = {
    'name': 'sal-dutils',
    'version': '0.1.2',
    'description': '',
    'long_description': 'pip install sal-dutils',
    'author': 'DesKaOne',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
