# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['examples',
 'examples.classifiers',
 'farglot',
 'farglot.__farcaster',
 'farglot.__farcaster.generated',
 'farglot.analyzer']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.14.3,<3.0.0',
 'torch>=2.0.1,<3.0.0',
 'transformers>=4.31.0,<5.0.0']

extras_require = \
{':extra == "cli"': ['grpcio==1.53.0', 'protobuf==4.22.1'],
 'cli': ['typer[all]>=0.9.0,<0.10.0',
         'PyNaCl>=1.5.0,<2.0.0',
         'blake3>=0.3.3,<0.4.0',
         'faust-streaming-rocksdb>=0.9.2,<0.10.0']}

entry_points = \
{'console_scripts': ['farglot = farglot.cli:app']}

setup_kwargs = {
    'name': 'farglot',
    'version': '0.1.3',
    'description': 'A Transformer-based SocialNLP toolkit for Farcaster',
    'long_description': '# FarGlot\n\nA Transformer-based SocialNLP toolkit for [Farcaster](https://www.farcaster.xyz/).\n\n## Installation\n\n```\npip install farglot\n```\n\n## Examples\n\n```python\nfrom farglot import CastAnalyzer\n\nsentiment_analyzer=CastAnalyzer.sequence_analzyer_from_model_name(\n    hub_address="nemes.farcaster.xyz:2283",\n    model_name="pysentimiento/robertuito-sentiment-analysis"\n)\n\nsentiment_analyzer.predict_cast(fid=2, hash_hex="0bcdcbf006ec22b79f37f2cf2a09c33413883937")\n# {\'NEG\': 0.051998768001794815, \'NEU\': 0.22470703721046448, \'POS\': 0.7232941389083862}\nsentiment_analyzer.predict_casts_by_fid(fid=2)\n# {\'NEG\': 0.03734538331627846, \'NEU\': 0.505352795124054, \'POS\': 0.4573018550872803}\n```\n\n## Generate a Training Corpus from a [Hub](https://github.com/farcasterxyz/hub-monorepo/tree/main/apps/hubble)\n\n### Install the FarGlot CLI\n\n```\npip install "farglot[cli]"\n```\n\n### Define Training Set Classifier(s)\n\n```json\n{\n  "name": "labels",\n  "default_value": 1 // optional\n}\n```\n\nFor multi-label classfication:\n\n```json\n[\n  {\n    "name": "class_one",\n    "default_value": 1 // optional\n  },\n  {\n    "name": "class_two",\n    "default_value": 2 // optional\n  },\n  {\n    "name": "class_three",\n    "default_value": 3 // optional\n  }\n]\n```\n\n### Usage\n\n```sh\nfarglot init\nfarglot set-classifers-path /path/to/class_configs.json\nfarglot set-hub-db-path /path/to/.rocks/rocks.hub._default\nfarglot new-training-set --out ./data/training-set.csv\n```\n\n### Tuning\n\nTODO: Example of fine-tuning and uploading dataset and model to [Hugging Face](https://huggingface.co/)\n\n### Tuning Resources\n\nNot sure how to where to start? Check out the following blog posts on tuning an LLM:\n\n- [Datasets and Preprocessing](https://michaelhly.com/posts/tune-llm-one)\n- [Hyperparameters and Metrics](https://michaelhly.com/posts/tune-llm-two)\n\nThis largely is largely adapted off of [pysentimiento](https://github.com/pysentimiento/pysentimiento).\n',
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
