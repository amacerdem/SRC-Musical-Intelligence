"""Neurochemical accumulation — (B, T, 4) modulatory overlay.

Implements the neuro tensor lifecycle (TERMINOLOGY.md Section 15.2):
    1. Initialize at baseline (0.5)
    2. Per depth level, each nucleus's NeuroLinks update the tensor
    3. Final state clamped to [0, 1]

Channel order: [DA, NE, OPI, 5HT] (TERMINOLOGY.md Section 15.1)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import torch

from Musical_Intelligence.contracts.dataclasses import (
    DA,
    NE,
    NUM_CHANNELS,
    OPI,
    _5HT,
)

# Import channel metadata from individual files
from . import dopamine, norepinephrine, opioid, serotonin  # noqa: F401

if TYPE_CHECKING:
    from torch import Tensor

    from Musical_Intelligence.contracts.bases.nucleus import Nucleus

__all__ = [
    "DA", "NE", "OPI", "_5HT", "NUM_CHANNELS",
    "BASELINE", "init_neuro", "accumulate_neuro",
]

BASELINE = 0.5


def init_neuro(batch: int, time: int, device: torch.device | None = None) -> Tensor:
    """Create a baseline neurochemical state tensor.

    Returns:
        ``(B, T, 4)`` tensor filled with ``BASELINE`` (0.5).
    """
    return torch.full(
        (batch, time, NUM_CHANNELS),
        BASELINE,
        device=device,
    )


def accumulate_neuro(
    neuro: Tensor,
    nucleus: Nucleus,
    output: Tensor,
) -> Tensor:
    """Apply a nucleus's NeuroLinks to the neurochemical state.

    For each NeuroLink declared by the nucleus:
        - ``produce``: Set channel to dim_value * weight
        - ``amplify``: Scale channel upward: ch += dim_value * weight * (1 - ch)
        - ``inhibit``: Scale channel downward: ch -= dim_value * weight * ch

    The output is clamped to [0, 1].

    Args:
        neuro:  Current ``(B, T, 4)`` neurochemical state (modified in-place).
        nucleus: The nucleus whose NeuroLinks to apply.
        output: The nucleus's ``(B, T, OUTPUT_DIM)`` output tensor.

    Returns:
        Updated ``(B, T, 4)`` neurochemical state (same tensor, clamped).
    """
    dim_names = nucleus.dimension_names
    name_to_idx = {name: i for i, name in enumerate(dim_names)}

    for nl in nucleus.neuro_links:
        dim_idx = name_to_idx.get(nl.dim_name)
        if dim_idx is None:
            continue

        # (B, T) value of the driving dimension
        dim_value = output[:, :, dim_idx]
        ch = nl.channel

        if nl.effect == "produce":
            neuro[:, :, ch] = dim_value * nl.weight
        elif nl.effect == "amplify":
            # Additive scaling toward 1.0
            neuro[:, :, ch] = neuro[:, :, ch] + dim_value * nl.weight * (1.0 - neuro[:, :, ch])
        elif nl.effect == "inhibit":
            # Subtractive scaling toward 0.0
            neuro[:, :, ch] = neuro[:, :, ch] - dim_value * nl.weight * neuro[:, :, ch]

    neuro.clamp_(0.0, 1.0)
    return neuro
