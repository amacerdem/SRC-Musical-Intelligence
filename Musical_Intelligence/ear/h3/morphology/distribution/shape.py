"""Distribution shape morphs: M4 max, M6 skewness, M7 kurtosis.

All functions are pure (torch only, no project dependencies).
"""
from __future__ import annotations

import torch
from torch import Tensor


def m4_max(window: Tensor, weights: Tensor) -> Tensor:
    """M4: Maximum value.

    Formula: max(window, dim=-1).values

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Unsigned, min window = 1.
    """
    return torch.max(window, dim=-1).values


def m6_skewness(window: Tensor, weights: Tensor) -> Tensor:
    """M6: Skewness (third standardized moment).

    Formula: E[(x - mu)^3] / sigma^3

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Signed, min window = 3.
        - Returns zeros(B) for constant window (sigma == 0).
    """
    B, W = window.shape
    if W < 3:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    mu = torch.mean(window, dim=-1, keepdim=True)          # (B, 1)
    diff = window - mu                                       # (B, W)
    sigma = torch.std(window, dim=-1)                         # (B,)

    # Constant window guard: return 0.0 where sigma is negligible
    is_const = sigma < 1e-8
    sigma_safe = sigma.clamp(min=1e-8)

    m3 = torch.mean(diff ** 3, dim=-1)                       # (B,)
    s3 = sigma_safe ** 3                                      # (B,)
    result = m3 / s3
    return torch.where(is_const, torch.zeros_like(result), result)


def m7_kurtosis(window: Tensor, weights: Tensor) -> Tensor:
    """M7: Excess kurtosis (fourth standardized moment minus 3).

    Formula: E[(x - mu)^4] / sigma^4 - 3

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Unsigned, min window = 4.
        - Returns zeros(B) for constant window (sigma == 0).
    """
    B, W = window.shape
    if W < 4:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    mu = torch.mean(window, dim=-1, keepdim=True)          # (B, 1)
    diff = window - mu                                       # (B, W)
    sigma = torch.std(window, dim=-1)                         # (B,)

    # Constant window guard: return 0.0 where sigma is negligible
    is_const = sigma < 1e-8
    sigma_safe = sigma.clamp(min=1e-8)

    m4 = torch.mean(diff ** 4, dim=-1)                       # (B,)
    s4 = sigma_safe ** 4                                      # (B,)
    result = m4 / s4 - 3.0
    return torch.where(is_const, torch.zeros_like(result), result)
