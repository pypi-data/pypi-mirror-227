# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torch_uncertainty',
 'torch_uncertainty.baselines',
 'torch_uncertainty.baselines.classification',
 'torch_uncertainty.baselines.regression',
 'torch_uncertainty.baselines.utils',
 'torch_uncertainty.datamodules',
 'torch_uncertainty.datasets',
 'torch_uncertainty.datasets.cifar',
 'torch_uncertainty.datasets.imagenet',
 'torch_uncertainty.layers',
 'torch_uncertainty.layers.bayesian_layers',
 'torch_uncertainty.metrics',
 'torch_uncertainty.models',
 'torch_uncertainty.models.resnet',
 'torch_uncertainty.models.vgg',
 'torch_uncertainty.models.wideresnet',
 'torch_uncertainty.post_processing',
 'torch_uncertainty.post_processing.calibration',
 'torch_uncertainty.routines',
 'torch_uncertainty.transforms',
 'torch_uncertainty.utils']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.6.0',
 'huggingface-hub>=0.14.1,<0.15.0',
 'pandas>=2.0.3,<3.0.0',
 'pytorch-lightning>=1.9.0,<2.0.0',
 'scipy>=1.10.0,<2.0.0',
 'tensorboard>=2.11.2',
 'timm>=0.6.12',
 'torch>=2.0.0,!=2.0.1',
 'torchinfo>=1.7.1']

setup_kwargs = {
    'name': 'torch-uncertainty',
    'version': '0.1.4',
    'description': 'TorchUncertainty: A maintained and collaborative PyTorch Library for benchmarking and leveraging predictive uncertainty quantification techniques.',
    'long_description': '<div align="center">\n\n![Torch Uncertainty Logo](https://github.com/ENSTA-U2IS/torch-uncertainty/blob/main/docs/source/_static/images/torch_uncertainty.png)\n\n[![pypi](https://img.shields.io/pypi/v/torch_uncertainty.svg)](https://pypi.python.org/pypi/torch_uncertainty)\n[![tests](https://github.com/ENSTA-U2IS/torch-uncertainty/actions/workflows/run-tests.yml/badge.svg?branch=main&event=push)](https://github.com/ENSTA-U2IS/torch-uncertainty/actions/workflows/run-tests.yml)\n[![Docs](https://github.com/ENSTA-U2IS/torch-uncertainty/actions/workflows/build-docs.yml/badge.svg)](https://torch-uncertainty.github.io/)\n[![Code Coverage](https://codecov.io/github/ENSTA-U2IS/torch-uncertainty/coverage.svg?branch=master)](https://codecov.io/gh/ENSTA-U2IS/torch-uncertainty)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)\n</div>\n\n_TorchUncertainty_ is a package designed to help you leverage uncertainty quantification techniques and make your deep neural networks more reliable. It aims at being collaborative and including as many methods as possible, so reach out to add yours!\n\n:construction: _TorchUncertainty_ is in early development :construction: - expect massive changes, but reach out and contribute if you are interested in the project! **Please raise an issue if you have any bugs or difficulties.**\n\n---\n\nThis package provides a multi-level API, including:\n\n- ready-to-train baselines on research datasets, such as ImageNet and CIFAR\n- deep learning baselines available for training on your datasets\n- [pretrained weights](https://huggingface.co/torch-uncertainty) for these baselines on ImageNet and CIFAR (work in progress 🚧).\n- layers available for use in your networks\n- scikit-learn style post-processing methods such as Temperature Scaling\n\nSee the [Reference page](https://torch-uncertainty.github.io/references.html) or the [API reference](https://torch-uncertainty.github.io/api.html) for a more exhaustive list of the implemented methods, datasets, metrics, etc.\n\n## Installation\n\nThe package can be installed from PyPI:\n\n```sh\npip install torch-uncertainty\n```\n\nThen, install the desired PyTorch version in your environment.\n\nIf you aim to contribute (thank you!), have a look at the [contribution page](https://torch-uncertainty.github.io/contributing.html).\n\n## Getting Started and Documentation\n\nPlease find the documentation at [torch-uncertainty.github.io](https://torch-uncertainty.github.io).\n\nA quickstart is available at [torch-uncertainty.github.io/quickstart](https://torch-uncertainty.github.io/quickstart.html).\n\n## Implemented methods\n\n### Baselines\n\nTo date, the following deep learning baselines have been implemented:\n\n- Deep Ensembles\n- BatchEnsemble\n- Masksembles\n- MIMO\n- Packed-Ensembles (see [blog post](https://medium.com/@adrien.lafage/make-your-neural-networks-more-reliable-with-packed-ensembles-7ad0b737a873))\n- Bayesian Neural Networks\n\n### Post-processing methods\n\nTo date, the following post-processing methods have been implemented:\n\n- Temperature, Vector, & Matrix scaling\n\n## Tutorials\n\nWe provide the following tutorials in our documentation:\n\n- [From a Vanilla Classifier to a Packed-Ensemble](https://torch-uncertainty.github.io/auto_tutorials/tutorial_pe_cifar10.html)\n- [Training a Bayesian Neural Network in 3 minutes](https://torch-uncertainty.github.io/auto_tutorials/tutorial_bayesian.html)\n- [Improve Top-label Calibration with Temperature Scaling](https://torch-uncertainty.github.io/auto_tutorials/tutorial_scaler.html)\n  \n## Awesome Uncertainty repositories\n\nYou may find a lot of papers about modern uncertainty estimation techniques on the [Awesome Uncertainty in Deep Learning](https://github.com/ENSTA-U2IS/awesome-uncertainty-deeplearning).\n\n## Other References\n\nThis package also contains the official implementation of Packed-Ensembles.\n\nIf you find the corresponding models interesting, please consider citing our [paper](https://arxiv.org/abs/2210.09184):\n\n```text\n@inproceedings{laurent2023packed,\n    title={Packed-Ensembles for Efficient Uncertainty Estimation},\n    author={Laurent, Olivier and Lafage, Adrien and Tartaglione, Enzo and Daniel, Geoffrey and Martinez, Jean-Marc and Bursuc, Andrei and Franchi, Gianni},\n    booktitle={ICLR},\n    year={2023}\n}\n```\n',
    'author': 'ENSTA U2IS',
    'author_email': 'olivier.laurent@ensta-paris.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
