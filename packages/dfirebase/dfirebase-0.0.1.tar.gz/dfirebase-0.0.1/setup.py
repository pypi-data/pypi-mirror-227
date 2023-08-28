# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dfirebase']

package_data = \
{'': ['*']}

install_requires = \
['blinker[signals]>=1.6.2,<2.0.0',
 'cryptography[rsa,signedtoken]>=41.0.3,<42.0.0',
 'gcloud>=0.18.3,<0.19.0',
 'google-api-python-client>=2.97.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=1.0.0,<2.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pycryptodome>=3.18.0,<4.0.0',
 'pyjwt[signedtoken]>=2.8.0,<3.0.0',
 'requests-toolbelt>=1.0.0,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'urllib3>=2.0.4,<3.0.0']

setup_kwargs = {
    'name': 'dfirebase',
    'version': '0.0.1',
    'description': '',
    'long_description': 'pip install DFirebase',
    'author': 'Antoni Oktha Fernandes',
    'author_email': '37358597+DesKaOne@users.noreply.github.com',
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
