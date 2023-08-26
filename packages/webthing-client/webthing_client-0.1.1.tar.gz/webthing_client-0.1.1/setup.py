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
    'version': '0.1.1',
    'description': 'Client for the Dynamic Dashboard Web Things',
    'long_description': '# Webthing Client Python\n\nA package for performing data operations on remote Webthing and listening to Observations.\n\n## Installation\n\nInstall the package `webthing-client` using your Python package manager of choice.\nYou can import the client class itself as:\n```python\nfrom webthing_client.client import WebthingClient\n```\n',
    'author': 'Emile Deman',
    'author_email': 'None',
    'maintainer': 'Stef Pletinck',
    'maintainer_email': 's@stefpletinck.be',
    'url': 'https://github.com/predict-idlab/webthing-client-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
