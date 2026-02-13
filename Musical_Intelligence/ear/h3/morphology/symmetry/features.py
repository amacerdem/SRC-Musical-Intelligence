"""Symmetry morphs: M16 curvature, M19 stability, M23 symmetry.

All functions are pure (torch only, no project dependencies).
"""
from __future__ import annotations

import torch
from torch import Tensor


def m16_curvature(window: Tensor, weights: Tensor) -> Tensor:
    """M16: Mean absolute second difference (curvature).

    Formula: mean(|diff(diff(x, dim=-1), dim=-1)|, dim=-1)

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) Mean absolute curvature. One scalar per batch item.

    Properties:
        - Signed (per scaling convention; raw value is non-negative).
        - Min window = 3.
        - Returns zeros(B) for win_len < 3.
    """
    B, W = window.shape
    if W < 3:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    d2 = torch.diff(torch.diff(window, dim=-1), dim=-1)  # (B, W-2)
    return torch.mean(torch.abs(d2), dim=-1)


def m19_stability(window: Tensor, weights: Tensor) -> Tensor:
    """M19: Stability (inverse standard deviation).

    Formula: 1 / (1 + std(x, dim=-1))

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) Stability in (0, 1]. One scalar per batch item.

    Properties:
        - Unsigned, min window = 2.
        - Returns 1.0 for constant input (perfect stability).
        - Returns zeros(B) for win_len < 2 (safe default).
    """
    B, W = window.shape
    if W < 2:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    sigma = torch.std(window, dim=-1)  # (B,)
    return 1.0 / (1.0 + sigma)


def m23_symmetry(window: Tensor, weights: Tensor) -> Tensor:
    """M23: Time-reversal symmetry (Pearson correlation of first half vs reversed second half).

    Computes the Pearson correlation between the first half of the window
    and the reversed second half.

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) Correlation in [-1, 1]. One scalar per batch item.

    Properties:
        - Signed, min window = 4.
        - Returns zeros(B) for win_len < 4.
        - Returns zeros(B) for constant input (undefined correlation).
    """
    B, W = window.shape
    if W < 4:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    # Split into first half and reversed second half
    half = W // 2
    first_half = window[:, :half]                          # (B, half)
    second_half = window[:, -half:]                         # (B, half)
    second_half_rev = second_half.flip(dims=[-1])           # (B, half)

    # Pearson correlation
    mu_a = torch.mean(first_half, dim=-1, keepdim=True)     # (B, 1)
    mu_b = torch.mean(second_half_rev, dim=-1, keepdim=True)  # (B, 1)

    a_dev = first_half - mu_a                               # (B, half)
    b_dev = second_half_rev - mu_b                          # (B, half)

    numerator = torch.sum(a_dev * b_dev, dim=-1)            # (B,)
    denom_a = torch.sqrt(torch.sum(a_dev ** 2, dim=-1))     # (B,)
    denom_b = torch.sqrt(torch.sum(b_dev ** 2, dim=-1))     # (B,)

    denominator = (denom_a * denom_b).clamp(min=1e-8)       # guard div-by-zero
    return numerator / denominator
