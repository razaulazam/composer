# Copyright 2022 MosaicML Composer authors
# SPDX-License-Identifier: Apache-2.0

"""This file provides the canonical settings (dataset, model, algorithms, arguments)
for each algorithm to be tested. This can be used throughout the codebase for
functional tests, serialization tests, etc.

Each algorithm is keyed based on its name in the algorithm registry.
"""

from typing import Any, Dict, Optional, Type

import pytest
from torch.utils.data import Dataset

import composer
from composer import Algorithm
from composer.algorithms import (AGC, EMA, SAM, SWA, Alibi, AugMix, BlurPool, ChannelsLast, ColOut, CutMix, CutOut,
                                 Factorize, GhostBatchNorm, LabelSmoothing, LayerFreezing, MixUp, NoOpModel,
                                 ProgressiveResizing, RandAugment, SelectiveBackprop, SeqLengthWarmup, SqueezeExcite,
                                 StochasticDepth)
from composer.models import ComposerResNet
from composer.models.base import ComposerModel
from tests import common

simple_vision_settings = {
    'model': common.SimpleConvModel,
    'dataset': common.RandomImageDataset,
    'kwargs': {},
}

simple_vision_pil_settings = {
    'model': common.SimpleConvModel,
    'dataset': (common.RandomImageDataset, {
        'is_PIL': True
    }),
    'kwargs': {},
}

simple_resnet_settings = {
    'model': (ComposerResNet, {
        'model_name': 'resnet18',
        'num_classes': 2
    }),
    'dataset': (common.RandomImageDataset, {
        'shape': (3, 224, 224),
    }),
    'kwargs': {},
}

_settings: Dict[Type[Algorithm], Optional[Dict[str, Any]]] = {
    AGC: simple_vision_settings,
    Alibi: None,  # NLP settings needed
    AugMix: simple_vision_settings,
    BlurPool: {
        'model': common.SimpleConvModel,
        'dataset': common.RandomImageDataset,
        'kwargs': {
            'min_channels': 0,
        },
    },
    ChannelsLast: simple_vision_settings,
    ColOut: simple_vision_settings,
    CutMix: {
        'model': common.SimpleConvModel,
        'dataset': common.RandomImageDataset,
        'kwargs': {
            'num_classes': 2
        }
    },
    CutOut: simple_vision_settings,
    EMA: {
        'model': common.SimpleConvModel,
        'dataset': common.RandomImageDataset,
        'kwargs': {
            'half_life': "1ba",
        },
    },
    Factorize: simple_resnet_settings,
    GhostBatchNorm: {
        'model': (ComposerResNet, {
            'model_name': 'resnet18',
            'num_classes': 2
        }),
        'dataset': (common.RandomImageDataset, {
            'shape': (3, 224, 224)
        }),
        'kwargs': {
            'ghost_batch_size': 2,
        }
    },
    LabelSmoothing: simple_vision_settings,
    LayerFreezing: simple_vision_settings,
    MixUp: simple_vision_settings,
    ProgressiveResizing: simple_vision_settings,
    RandAugment: simple_vision_settings,
    NoOpModel: simple_vision_settings,
    SAM: simple_vision_settings,
    SelectiveBackprop: simple_vision_settings,
    SeqLengthWarmup: None,  # NLP settings needed
    SqueezeExcite: simple_resnet_settings,
    StochasticDepth: {
        'model': (ComposerResNet, {
            'model_name': 'resnet50',
            'num_classes': 2
        }),
        'dataset': (common.RandomImageDataset, {
            'shape': (3, 224, 224),
        }),
        'kwargs': {
            'stochastic_method': 'block',
            'target_layer_name': 'ResNetBottleneck',
            'drop_rate': 0.2,
            'drop_distribution': 'linear',
            'drop_warmup': "0.0dur",
            'use_same_gpu_seed': False,
        }
    },
    SWA: {
        'model': common.SimpleConvModel,
        'dataset': common.RandomImageDataset,
        'kwargs': {
            'swa_start': "0.2dur",
            'swa_end': "0.97dur",
            'update_interval': '1ep',
            'schedule_swa_lr': True,
        }
    },
}


def _get_alg_settings(alg_cls: Type[Algorithm]):
    if alg_cls not in _settings or _settings[alg_cls] is None:
        raise ValueError(f"Algorithm {alg_cls.__name__} not in the settings dictionary.")
    settings = _settings[alg_cls]
    assert settings is not None
    return settings


def get_alg_kwargs(alg_cls: Type[Algorithm]) -> Dict[str, Any]:
    """Return the kwargs for an algorithm."""
    return _get_alg_settings(alg_cls)['kwargs']


def get_alg_model(alg_cls: Type[Algorithm]) -> ComposerModel:
    """Return an instance of the model for an algorithm."""
    settings = _get_alg_settings(alg_cls)['model']
    if isinstance(settings, tuple):
        (cls, kwargs) = settings
    else:
        (cls, kwargs) = (settings, {})
    return cls(**kwargs)


def get_alg_dataset(alg_cls: Type[Algorithm]) -> Dataset:
    """Return an instance of the dataset for an algorithm."""
    settings = _get_alg_settings(alg_cls)['dataset']
    if isinstance(settings, tuple):
        (cls, kwargs) = settings
    else:
        (cls, kwargs) = (settings, {})
    return cls(**kwargs)


def get_algs_with_marks():
    """Returns a list of algorithms appropriate markers for a subsequent call to pytest.mark.parameterize.
    It applies markers as appropriate (e.g. XFAIL for algs missing config)
    It reads from the algorithm registry

    E.g. @pytest.mark.parametrize("alg_class", get_algs_with_marks())
    """
    ans = []
    for alg_cls in common.get_module_subclasses(composer.algorithms, Algorithm):
        marks = []
        settings = _settings[alg_cls]

        if alg_cls in (CutMix, MixUp, LabelSmoothing):
            # see: https://github.com/mosaicml/composer/issues/362
            pytest.importorskip("torch", minversion="1.10", reason="Pytorch 1.10 required.")

        if alg_cls == SWA:
            # TODO(matthew): Fix
            marks.append(
                pytest.mark.filterwarnings(
                    r'ignore:Detected call of `lr_scheduler.step\(\)` before `optimizer.step\(\)`:UserWarning'))

        if alg_cls == MixUp:
            # TODO(Landen): Fix
            marks.append(
                pytest.mark.filterwarnings(r"ignore:Some targets have less than 1 total probability:UserWarning"))

        if settings is None:
            marks.append(pytest.mark.xfail(reason=f"Algorithm {alg_cls.__name__} is missing settings."))

        ans.append(pytest.param(alg_cls, marks=marks, id=alg_cls.__name__))

    return ans
