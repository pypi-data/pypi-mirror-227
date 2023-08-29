# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geminix']

package_data = \
{'': ['*']}

install_requires = \
['torch']

setup_kwargs = {
    'name': 'geminix',
    'version': '0.0.1',
    'description': 'Gemini - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Gemini\nThe open source implementation of Gemini, the model that will "eclipse ChatGPT", \n\n\n\n# References\n* Combine Reinforcment learning with modular pretrained transformer, multi-modal capabilities, image, audio, \n* self improving mechanisms like robocat\n* PPO? or MPO\n* get good at backtracking and exploring alternative paths\n* speculative decoding\n*',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Gemini',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
