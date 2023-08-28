# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dfirebase']

package_data = \
{'': ['*']}

install_requires = \
['blinker>=1.4.0',
 'bs4>=0.0.1,<0.0.2',
 'cryptography>=3.0.0',
 'deskaone-requests>=0.0.6,<0.0.7',
 'gcloud>=0.18.3',
 'google-api-python-client>=2.97.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=1.0.0,<2.0.0',
 'oauth2client>=4.1.2',
 'pycryptodome>=3.6.4',
 'pyjwt>=2.0.0,<3',
 'python-jwt>=2.0.1',
 'requests-toolbelt>=0.7.1,<1.0',
 'requests[socks]>=2.11.1,<3.0.0',
 'urllib3>=1.21.1,<2']

setup_kwargs = {
    'name': 'dfirebase',
    'version': '0.0.4',
    'description': '',
    'long_description': 'pip install DFirebase',
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
