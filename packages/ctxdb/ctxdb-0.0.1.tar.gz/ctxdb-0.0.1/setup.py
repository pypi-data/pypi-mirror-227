# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctxdb',
 'ctxdb.ctxdb',
 'ctxdb.ctxdb.api',
 'ctxdb.ctxdb.core',
 'ctxdb.ctxdb.models',
 'ctxdb.ctxdb.utils',
 'ctxdb.examples',
 'ctxdb.tests']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'docarray[redis]>=0.37.0,<0.38.0',
 'fastapi>=0.101.1,<0.102.0',
 'numpy>=1.22.2,<2.0.0',
 'sentence-transformers>=2.2.2,<3.0.0',
 'uvicorn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'ctxdb',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Philip Solarz',
    'author_email': 'philipsolarz@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11',
}


setup(**setup_kwargs)
