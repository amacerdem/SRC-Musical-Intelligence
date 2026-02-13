"""Rhythm morphs: M14 periodicity, M17 shape_period, M22 peaks.

All functions are pure (torch only, no project dependencies).
"""
from __future__ import annotations

import torch
from torch import Tensor


def m14_periodicity(window: Tensor, weights: Tensor) -> Tensor:
    """M14: Periodicity (autocorrelation peak ratio).

    Computes normalized autocorrelation, finds the maximum peak in the
    lag range [2, W//2], and returns peak / autocorr[0].

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) Peak ratio in [0, 1]. One scalar per batch item.

    Properties:
        - Unsigned, min window = 8.
        - Returns zeros(B) for win_len < 8.
    """
    B, W = window.shape
    if W < 8:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    # Center the signal
    mu = torch.mean(window, dim=-1, keepdim=True)    # (B, 1)
    centered = window - mu                             # (B, W)

    # Autocorrelation at lag 0
    r0 = torch.sum(centered ** 2, dim=-1)              # (B,)
    r0 = r0.clamp(min=1e-12)                           # guard constant signal

    # Compute autocorrelation for lags [2, W//2]
    max_lag = W // 2
    result = torch.zeros(B, device=window.device, dtype=window.dtype)

    for lag in range(2, max_lag + 1):
        r_lag = torch.sum(centered[:, :W - lag] * centered[:, lag:], dim=-1)
        ratio = r_lag / r0
        result = torch.maximum(result, ratio)

    return result


def m17_shape_period(window: Tensor, weights: Tensor) -> Tensor:
    """M17: Dominant period in frames (lag of max autocorrelation peak).

    Finds the lag (in range [2, W//2]) with the highest normalized
    autocorrelation value.

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) Dominant period in frames. One scalar per batch item.

    Properties:
        - Unsigned, min window = 8.
        - Returns zeros(B) for win_len < 8.
    """
    B, W = window.shape
    if W < 8:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    # Center the signal
    mu = torch.mean(window, dim=-1, keepdim=True)    # (B, 1)
    centered = window - mu                             # (B, W)

    # Autocorrelation at lag 0
    r0 = torch.sum(centered ** 2, dim=-1)              # (B,)
    r0 = r0.clamp(min=1e-12)

    # Find lag with maximum autocorrelation in [2, W//2]
    max_lag = W // 2
    best_ratio = torch.full((B,), -1.0, device=window.device, dtype=window.dtype)
    best_lag = torch.zeros(B, device=window.device, dtype=window.dtype)

    for lag in range(2, max_lag + 1):
        r_lag = torch.sum(centered[:, :W - lag] * centered[:, lag:], dim=-1)
        ratio = r_lag / r0

        # Update where this lag has a higher ratio
        mask = ratio > best_ratio
        best_ratio = torch.where(mask, ratio, best_ratio)
        best_lag = torch.where(mask, torch.tensor(float(lag), device=window.device, dtype=window.dtype), best_lag)

    return best_lag


def m22_peaks(window: Tensor, weights: Tensor) -> Tensor:
    """M22: Count of local maxima.

    A frame x[i] is a local maximum if x[i-1] < x[i] > x[i+1].

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) Raw count of peaks. One scalar per batch item.

    Properties:
        - Unsigned, min window = 3.
        - Returns zeros(B) for win_len < 3.
    """
    B, W = window.shape
    if W < 3:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    left = window[:, :-2]    # (B, W-2)
    center = window[:, 1:-1]  # (B, W-2)
    right = window[:, 2:]     # (B, W-2)

    is_peak = (center > left) & (center > right)  # (B, W-2)
    return is_peak.float().sum(dim=-1)             # (B,)
