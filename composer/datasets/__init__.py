# Copyright 2022 MosaicML Composer authors
# SPDX-License-Identifier: Apache-2.0

"""Natively supported datasets.

Modules in datasets namespace define utilities and mechanisms to create dataloaders from the given hyperparameters.  Two
of the important classes in this module are described below:

* All datasets derive from the abstract base class :class:`~.DatasetHparams` and it contains common parameters such as
  ``shuffle``. :class:`~.DatasetHparams` returns a dataloader (a :class:`torch.utils.data.DataLoader` or a
  :class:`~.DataSpec`) for the trainer.

* :class:`~.DataLoaderHparams` contains the :class:`torch.utils.data.DataLoader` settings that are common across
  both training and eval datasets. See the documentation of :class:`~.DataLoaderHparams` for more details on these
  settings.
"""

from composer.datasets.ade20k import ADE20kDatasetHparams, StreamingADE20kHparams
from composer.datasets.brats import BratsDatasetHparams
from composer.datasets.c4 import C4DatasetHparams
from composer.datasets.cifar import CIFAR10DatasetHparams
from composer.datasets.coco import COCODatasetHparams, StreamingCOCOHparams
from composer.datasets.dataloader import DataLoaderHparams
from composer.datasets.dataset_registry import get_dataset_registry
from composer.datasets.evaluator import EvaluatorHparams
from composer.datasets.glue import GLUEHparams
from composer.datasets.hparams import DatasetHparams, SyntheticHparamsMixin
from composer.datasets.imagenet import ImagenetDatasetHparams, StreamingImageNet1kHparams
from composer.datasets.lm_datasets import LMDatasetHparams
from composer.datasets.mnist import MNISTDatasetHparams
from composer.datasets.synthetic import (MemoryFormat, SyntheticBatchPairDataset, SyntheticDataLabelType,
                                         SyntheticDataType, SyntheticPILDataset)

__all__ = [
    "ADE20kDatasetHparams", "StreamingADE20kHparams", "BratsDatasetHparams", "C4DatasetHparams",
    "CIFAR10DatasetHparams", "COCODatasetHparams", "StreamingCOCOHparams", "DataLoaderHparams", "get_dataset_registry",
    "EvaluatorHparams", "GLUEHparams", "DatasetHparams", "SyntheticHparamsMixin", "ImagenetDatasetHparams",
    "StreamingImageNet1kHparams", "LMDatasetHparams", "MNISTDatasetHparams", "MemoryFormat",
    "SyntheticBatchPairDataset", "SyntheticDataLabelType", "SyntheticDataType", "SyntheticPILDataset"
]
