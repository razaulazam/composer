# Copyright 2022 MosaicML Composer authors
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import pytest
import torch

from composer.utils import ensure_tuple


def test_none_to_tuple():
    assert ensure_tuple(None) == ()


@pytest.mark.parametrize("x", ['test', b'test', bytearray(b'test')])
def test_str_to_tuple(x):
    assert ensure_tuple(x) == (x,)


@pytest.mark.parametrize("x", [(0, 1, 2), [0, 1, 2], range(3)])
def test_seq_to_tuple(x):
    assert ensure_tuple(x) == (0, 1, 2)


@pytest.mark.parametrize("x", [{'t': 1, 'e': 2, 's': 3}])
def test_dict_to_tuple(x):
    assert ensure_tuple(x) == (1, 2, 3)


@pytest.mark.parametrize("x", [torch.arange(3), np.arange(3)])
def test_obj_to_tuple(x):
    assert ensure_tuple(x) == (x,)
