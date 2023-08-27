# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neurobench',
 'neurobench.accumulators',
 'neurobench.benchmarks',
 'neurobench.benchmarks.utils',
 'neurobench.datasets',
 'neurobench.examples',
 'neurobench.examples.model_data',
 'neurobench.models',
 'neurobench.preprocessing']

package_data = \
{'': ['*']}

install_requires = \
['llvmlite>=0.40.1,<0.41.0',
 'numba>=0.57.1,<0.58.0',
 'numpy>=1.24.3,<2.0.0',
 'tonic>=1.4.0,<2.0.0',
 'torch>=2.0.1,<3.0.0',
 'torchaudio>=2.0.2,<3.0.0',
 'tqdm>=4.65.0,<5.0.0']

extras_require = \
{'snntorch': ['snntorch>=0.7.0,<0.8.0']}

setup_kwargs = {
    'name': 'neurobench',
    'version': '0.1.0',
    'description': 'Collaborative, Fair, and Representative Benchmarks for Neuromorphic Computing',
    'long_description': '# NeuroBench Algorithm Benchmarks Harness\nA harness for running evaluations on [NeuroBench](https://neurobench.ai) algorithm benchmarks.\n\nThis framework is in a beta state and is still under active development. Currently, only pytorch-based models and frameworks are supported.\nExtension of the harness to cover system track benchmarks in the future is planned.\n\nNeuroBench is a community-driven project, and we welcome further development from the community. If you are interested in developing extensions to features, programming frameworks, or metrics and tasks, please see the [contributing guidelines](CONTRIBUTING.md).\n\n## Installation\nInstall from PyPI:\n```\npip install neurobench\n```\n\n### Development\nIf you clone the repo directly for development, poetry can be used to maintain a virtualenv consistent with a deployment environment. In the `algorithms_benchmarks` folder run:\n```\npoetry install\npoetry run pytest tests/\n```\n\nCurrently the end-to-end examples can be run from the `algorithms_benchmarks` folder via:\n```\npoetry run python neurobench/examples/dvs_gesture.py\npoetry run python neurobench/examples/gsc.py\npoetry run python neurobench/examples/mackey_glass.py\npoetry run python neurobench/examples/primate_reaching.py\n```\nThe examples may not yet have trained models or a full set of metrics.\n\n\n## Getting started\nExample benchmark scripts can be found under the `neurobench/examples` folder. \n\nIn general, the design flow for using the framework is as follows:\n      \n1. Train a network using the train split from a particular dataset.\n2. Wrap the network in a `NeuroBenchModel`.\n3. Pass the model, evaluation split dataloader, pre-/post-processors, and a list of metrics to the `Benchmark` and `run()`.\n\nDocumentation for the framework interfaces can found in [API.md](API.md).\n\n## Developers\nNeuroBench is a collaboration between industry and academic engineers and researchers. This framework is currently maintained by [Jason Yik](https://www.linkedin.com/in/jasonlyik/), [Noah Pacik-Nelson](https://www.linkedin.com/in/noah-pacik-nelson/), and [Korneel Van den Berghe](https://www.linkedin.com/in/korneel-van-den-berghe/), and there have been technical contributions from many others. A non-exhaustive list includes Gregor Lenz, Denis Kleyko, Younes Bouhadjar, Paul Hueber, Vincent Sun, Biyan Zhou, George Vathakkattil Joseph, Douwe den Blanken, Maxime Fabre, Shenqi Wang, Guangzhi Tang, Anurag Kumar Mishra, Soikat Hasan Ahmed.\n\n## Contributing\nIf you are interested in helping to build this framework, please see the [contributing guidelines](CONTRIBUTING.md).\n\n## Citation\nIf you use this framework in your research, please cite the following whitepaper:\n\n```\n@misc{neurobench_arxiv2023,\n      title={NeuroBench: Advancing Neuromorphic Computing through Collaborative, Fair and Representative Benchmarking}, \n      author={Jason Yik and Soikat Hasan Ahmed and Zergham Ahmed and Brian Anderson and Andreas G. Andreou and Chiara Bartolozzi and Arindam Basu and Douwe den Blanken and Petrut Bogdan and Sander Bohte and Younes Bouhadjar and Sonia Buckley and Gert Cauwenberghs and Federico Corradi and Guido de Croon and Andreea Danielescu and Anurag Daram and Mike Davies and Yigit Demirag and Jason Eshraghian and Jeremy Forest and Steve Furber and Michael Furlong and Aditya Gilra and Giacomo Indiveri and Siddharth Joshi and Vedant Karia and Lyes Khacef and James C. Knight and Laura Kriener and Rajkumar Kubendran and Dhireesha Kudithipudi and Gregor Lenz and Rajit Manohar and Christian Mayr and Konstantinos Michmizos and Dylan Muir and Emre Neftci and Thomas Nowotny and Fabrizio Ottati and Ayca Ozcelikkale and Noah Pacik-Nelson and Priyadarshini Panda and Sun Pao-Sheng and Melika Payvand and Christian Pehle and Mihai A. Petrovici and Christoph Posch and Alpha Renner and Yulia Sandamirskaya and Clemens JS Schaefer and André van Schaik and Johannes Schemmel and Catherine Schuman and Jae-sun Seo and Sadique Sheik and Sumit Bam Shrestha and Manolis Sifalakis and Amos Sironi and Kenneth Stewart and Terrence C. Stewart and Philipp Stratmann and Guangzhi Tang and Jonathan Timcheck and Marian Verhelst and Craig M. Vineyard and Bernhard Vogginger and Amirreza Yousefzadeh and Biyan Zhou and Fatima Tuz Zohora and Charlotte Frenkel and Vijay Janapa Reddi},\n      year={2023},\n      eprint={2304.04640},\n      archivePrefix={arXiv},\n      primaryClass={cs.AI}\n}\n```\n',
    'author': 'NeuroBench Team',
    'author_email': 'neurobench@googlegroups.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
