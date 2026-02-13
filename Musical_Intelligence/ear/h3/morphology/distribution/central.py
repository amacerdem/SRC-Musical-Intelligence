"""Distribution central tendency morphs: M0 weighted_mean, M1 mean, M3 median.

All functions are pure (torch only, no project dependencies).
"""
from __future__ import annotations

import torch
from torch import Tensor


def m0_weighted_mean(window: Tensor, weights: Tensor) -> Tensor:
    """M0: Attention-weighted mean.

    Formula: sum(weights * window, dim=-1)

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Pre-normalized attention weights (sum to 1.0).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Unsigned, min window = 1.
        - Single-frame: returns the value itself.
    """
    # weights is (W,), broadcast over batch dim
    return torch.sum(weights * window, dim=-1)


def m1_mean(window: Tensor, weights: Tensor) -> Tensor:
    """M1: Unweighted mean.

    Formula: mean(window, dim=-1)

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Unsigned, min window = 1.
        - Single-frame: returns the value itself.
    """
    return torch.mean(window, dim=-1)


def m3_median(window: Tensor, weights: Tensor) -> Tensor:
    """M3: Median.

    Formula: median(window, dim=-1).values

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Unsigned, min window = 1.
        - Single-frame: returns the value itself.
    """
    return torch.median(window, dim=-1).values
