# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webthing_client']

package_data = \
{'': ['*']}

install_requires = \
['rdflib==6.2.0',
 'requests==2.28.2',
 'stomper==0.4.3',
 'websocket-client==1.5.0']

setup_kwargs = {
    'name': 'webthing-client',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Emile Deman',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
