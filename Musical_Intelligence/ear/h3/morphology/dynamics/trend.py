"""Dynamics trend morphs: M18 trend, M21 zero_crossings.

All functions are pure (torch only, no project dependencies).
"""
from __future__ import annotations

import torch
from torch import Tensor


def m18_trend(window: Tensor, weights: Tensor) -> Tensor:
    """M18: Weighted linear regression slope (trend).

    Formula:
        t = linspace(0, 1, W)
        slope = sum(w * (x - x_mean) * (t - t_mean)) / sum(w * (t - t_mean)^2)

    where w = weights (pre-normalized attention kernel).

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Pre-normalized attention weights (sum to 1.0).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Signed, min window = 2.
        - Returns zeros(B) for win_len < 2.
    """
    B, W = window.shape
    if W < 2:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    # Time axis normalized to [0, 1]
    t = torch.linspace(0.0, 1.0, W, device=window.device, dtype=window.dtype)

    # Weighted means
    t_mean = torch.sum(weights * t)                          # scalar
    x_mean = torch.sum(weights * window, dim=-1, keepdim=True)  # (B, 1)

    # Deviations
    t_dev = t - t_mean                                       # (W,)
    x_dev = window - x_mean                                  # (B, W)

    # Weighted covariance and variance
    numerator = torch.sum(weights * x_dev * t_dev, dim=-1)   # (B,)
    denominator = torch.sum(weights * t_dev ** 2)             # scalar

    # Guard division by zero (all weights at same time point)
    denominator = denominator.clamp(min=1e-12)
    return numerator / denominator


def m21_zero_crossings(window: Tensor, weights: Tensor) -> Tensor:
    """M21: Count of mean-crossings.

    Counts sign changes in (x - mean(x)) for consecutive pairs.

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) Raw count of crossings (not normalized).

    Properties:
        - Unsigned, min window = 2.
        - Returns zeros(B) for win_len < 2.
    """
    B, W = window.shape
    if W < 2:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    mu = torch.mean(window, dim=-1, keepdim=True)            # (B, 1)
    centered = window - mu                                    # (B, W)

    # Sign changes: product of consecutive centered values is negative
    products = centered[:, :-1] * centered[:, 1:]             # (B, W-1)
    crossings = (products < 0).float().sum(dim=-1)            # (B,)
    return crossings
