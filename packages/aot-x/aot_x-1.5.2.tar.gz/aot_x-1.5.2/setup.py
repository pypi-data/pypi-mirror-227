# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aot']

package_data = \
{'': ['*']}

install_requires = \
['swarms']

setup_kwargs = {
    'name': 'aot-x',
    'version': '1.5.2',
    'description': 'Algorithm of thoughts - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Algorithm-Of-Thoughts\nMy implementation of "Algorithm of Thoughts: Enhancing Exploration of Ideas in Large Language Models"\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Algorithm-Of-Thoughts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
