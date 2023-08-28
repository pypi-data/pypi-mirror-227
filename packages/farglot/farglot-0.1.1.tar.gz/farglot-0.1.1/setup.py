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

entry_points = \
{'console_scripts': ['farglot = farglot.cli:app']}

setup_kwargs = {
    'name': 'farglot',
    'version': '0.1.1',
    'description': 'A Transformer-based SocialNLP toolkit for Farcaster',
    'long_description': '# FarGlot\n\nA Transformer-based SocialNLP toolkit for [Farcaster](https://www.farcaster.xyz/).\n\n## Installation\n\n```\npip install farglot\n```\n\n## Examples\n\n```python\nfrom farglot import CastAnalyzer\n\nsentiment_analyzer=CastAnalyzer.sequence_analzyer_from_model_name(\n    hub_address="nemes.farcaster.xyz:2283",\n    model_name="pysentimiento/robertuito-sentiment-analysis"\n)\n\nsentiment_analyzer.predict_cast(fid=2, hash_hex="0x0bcdcbf006ec22b79f37f2cf2a09c33413883937")\n# ...\nsentiment_analyzer.predict_casts_by_fid(fid=2)\n# [...]\n```\n\n## Generate a Training Set from a [Hub](https://github.com/farcasterxyz/hub-monorepo/tree/main/apps/hubble)\n\n### Install the FarGlot CLI\n\n```\npip install farglot[cli]\n```\n\n### Define Training Set Columns\n\n```json\n{\n  "name": "labels",\n  "default_value": 1 // optional\n}\n```\n\nFor multilabel classfication:\n\n```json\n[\n  {\n    "name": "column_one",\n    "default_value": 1 // optional\n  },\n  {\n    "name": "column_two",\n    "default_value": 2 // optional\n  },\n  {\n    "name": "column_three",\n    "default_value": 3 // optional\n  }\n]\n```\n\n### Usage\n\n```sh\nfarglot init\nfarglot set-columns-path /path/to/column_configs.json\nfarglot set-hub-db-path /path/to/.rocks/rocks.hub._default\nfarglot new-training-set --out ./data/training-set.csv\n```\n\nThis largely is largely adapted off of [pysentimiento](https://github.com/pysentimiento/pysentimiento).\n',
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
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
