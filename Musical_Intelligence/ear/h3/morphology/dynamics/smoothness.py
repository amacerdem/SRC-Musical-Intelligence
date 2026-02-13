"""Dynamics smoothness morph: M15.

All functions are pure (torch only, no project dependencies).
"""
from __future__ import annotations

import torch
from torch import Tensor


def m15_smoothness(window: Tensor, weights: Tensor) -> Tensor:
    """M15: Smoothness (inverse velocity variability).

    Formula: 1 / (1 + std(diff(window, dim=-1), dim=-1))

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item, in range (0, 1].

    Properties:
        - Unsigned, min window = 3.
        - Returns 1.0 for constant input (perfect smoothness).
        - Returns zeros(B) for win_len < 3 (safe default).
    """
    B, W = window.shape
    if W < 3:
        return torch.zeros(B, device=window.device, dtype=window.dtype)
    d1 = torch.diff(window, dim=-1)  # (B, W-1)
    vel_std = torch.std(d1, dim=-1)  # (B,)
    return 1.0 / (1.0 + vel_std)
