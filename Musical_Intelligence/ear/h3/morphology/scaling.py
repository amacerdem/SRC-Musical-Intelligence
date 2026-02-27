"""Morph normalization dispatch: maps raw morph outputs to [0, 1] or [-1, 1].

Imports MORPH_SCALE and SIGNED_MORPHS from ear.h3.constants and applies
the appropriate unsigned or signed normalization formula.
"""
from __future__ import annotations

import torch
from torch import Tensor

from ..constants.scaling import MORPH_SCALE
from ..constants.morphs import SIGNED_MORPHS


def normalize_morph(raw: Tensor, morph_idx: int) -> Tensor:
    """Normalize a raw morph value to [0, 1] or [-1, 1].

    Dispatches between signed and unsigned normalization based on
    whether ``morph_idx`` is in ``SIGNED_MORPHS``.

    Unsigned:
        clamp(raw / scale, 0, 1)

    Signed:
        clamp(raw / scale, -1, 1)

    Args:
        raw: Raw morph output tensor (any shape).
        morph_idx: Morph index (0-23).

    Returns:
        Unsigned morphs: tensor in [0, 1].
        Signed morphs: tensor in [-1, 1] with zero at origin.
    """
    scale = MORPH_SCALE[morph_idx]

    if morph_idx in SIGNED_MORPHS:
        return torch.clamp(raw / scale, -1.0, 1.0)
    else:
        return torch.clamp(raw / scale, 0.0, 1.0)
