"""Distribution spread morphs: M2 std, M5 range.

All functions are pure (torch only, no project dependencies).
"""
from __future__ import annotations

import torch
from torch import Tensor


def m2_std(window: Tensor, weights: Tensor) -> Tensor:
    """M2: Standard deviation.

    Formula: std(window, dim=-1)

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Unsigned, min window = 2.
        - Returns zeros(B) for win_len < 2 or constant input.
    """
    B, W = window.shape
    if W < 2:
        return torch.zeros(B, device=window.device, dtype=window.dtype)
    return torch.std(window, dim=-1)


def m5_range(window: Tensor, weights: Tensor) -> Tensor:
    """M5: Range (max - min).

    Formula: max(window, dim=-1) - min(window, dim=-1)

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Unsigned, min window = 2.
        - Returns zeros(B) for win_len < 2 or constant input.
    """
    B, W = window.shape
    if W < 2:
        return torch.zeros(B, device=window.device, dtype=window.dtype)
    return torch.max(window, dim=-1).values - torch.min(window, dim=-1).values
