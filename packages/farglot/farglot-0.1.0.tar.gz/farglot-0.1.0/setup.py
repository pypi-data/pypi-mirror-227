# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['examples',
 'examples.classifiers',
 'farglot',
 'farglot.__farcaster',
 'farglot.__farcaster.generated']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.14.3,<3.0.0',
 'torch>=2.0.1,<3.0.0',
 'transformers>=4.31.0,<5.0.0']

extras_require = \
{'cli': ['typer[all]>=0.9.0,<0.10.0',
         'PyNaCl>=1.5.0,<2.0.0',
         'blake3>=0.3.3,<0.4.0',
         'protobuf==4.22.1',
         'faust-streaming-rocksdb>=0.9.2,<0.10.0',
         'grpcio==1.53.0']}

setup_kwargs = {
    'name': 'farglot',
    'version': '0.1.0',
    'description': 'A Transformer-based SocialNLP toolkit for Farcaster',
    'long_description': '# FarSent\n\nAdaption of [pysentimiento](https://github.com/pysentimiento/pysentimiento) for [farcaster](https://www.farcaster.xyz/).\n',
    'author': 'michaelhly',
    'author_email': 'michaelhly@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/michaelhly/FarGlot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
