"""Batch morph computation -- vectorized versions of all 24 morphs.

Each function takes ``(B, F, W)`` windows and ``(W,)`` weights and returns
``(B, F)`` results, enabling computation across all frames at once
instead of per-frame iteration.

This module is the vectorized counterpart of the per-frame dispatch in
:class:`~ear.h3.morphology.computer.MorphComputer`.
"""
from __future__ import annotations

from typing import Callable, Dict

import torch
from torch import Tensor

# Type alias: (windows, weights) -> result
BatchMorphFn = Callable[[Tensor, Tensor], Tensor]


# ── Distribution ─────────────────────────────────────────────────────────

def batch_m0_weighted_mean(windows: Tensor, weights: Tensor) -> Tensor:
    """M0: Attention-weighted mean.  (B,F,W),(W,) -> (B,F)."""
    return (windows * weights).sum(-1)


def batch_m1_mean(windows: Tensor, weights: Tensor) -> Tensor:
    """M1: Unweighted mean.  (B,F,W),(W,) -> (B,F)."""
    return windows.mean(-1)


def batch_m2_std(windows: Tensor, weights: Tensor) -> Tensor:
    """M2: Standard deviation.  (B,F,W),(W,) -> (B,F)."""
    W = windows.shape[-1]
    if W < 2:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    return windows.std(-1)


def batch_m3_median(windows: Tensor, weights: Tensor) -> Tensor:
    """M3: Median.  (B,F,W),(W,) -> (B,F)."""
    return windows.median(-1).values


def batch_m4_max(windows: Tensor, weights: Tensor) -> Tensor:
    """M4: Maximum.  (B,F,W),(W,) -> (B,F)."""
    return windows.max(-1).values


def batch_m5_range(windows: Tensor, weights: Tensor) -> Tensor:
    """M5: Range (max - min).  (B,F,W),(W,) -> (B,F)."""
    W = windows.shape[-1]
    if W < 2:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    return windows.max(-1).values - windows.min(-1).values


# ── Shape ────────────────────────────────────────────────────────────────

def batch_m6_skewness(windows: Tensor, weights: Tensor) -> Tensor:
    """M6: Skewness.  (B,F,W),(W,) -> (B,F)."""
    W = windows.shape[-1]
    if W < 3:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    mu = windows.mean(-1, keepdim=True)            # (B, F, 1)
    diff = windows - mu                             # (B, F, W)
    sigma = windows.std(-1)                          # (B, F)
    is_const = sigma < 1e-8
    sigma_safe = sigma.clamp(min=1e-8)
    m3 = (diff ** 3).mean(-1)                        # (B, F)
    result = m3 / (sigma_safe ** 3)
    return torch.where(is_const, torch.zeros_like(result), result)


def batch_m7_kurtosis(windows: Tensor, weights: Tensor) -> Tensor:
    """M7: Excess kurtosis.  (B,F,W),(W,) -> (B,F)."""
    W = windows.shape[-1]
    if W < 4:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    mu = windows.mean(-1, keepdim=True)
    diff = windows - mu
    sigma = windows.std(-1)
    is_const = sigma < 1e-8
    sigma_safe = sigma.clamp(min=1e-8)
    m4 = (diff ** 4).mean(-1)
    result = m4 / (sigma_safe ** 4) - 3.0
    return torch.where(is_const, torch.zeros_like(result), result)


# ── Dynamics: Derivatives ────────────────────────────────────────────────

def batch_m8_velocity(windows: Tensor, weights: Tensor) -> Tensor:
    """M8: Instantaneous velocity (last first-difference).  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 2:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    return windows[..., -1] - windows[..., -2]


def batch_m9_velocity_mean(windows: Tensor, weights: Tensor) -> Tensor:
    """M9: Mean velocity.  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 2:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    d1 = torch.diff(windows, dim=-1)     # (B, F, W-1)
    return d1.mean(-1)


def batch_m10_velocity_std(windows: Tensor, weights: Tensor) -> Tensor:
    """M10: Velocity std.  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 3:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    d1 = torch.diff(windows, dim=-1)
    return d1.std(-1)


def batch_m11_acceleration(windows: Tensor, weights: Tensor) -> Tensor:
    """M11: Instantaneous acceleration (last second-difference).  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 3:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    d2 = torch.diff(torch.diff(windows, dim=-1), dim=-1)  # (B, F, W-2)
    return d2[..., -1]


def batch_m12_acceleration_mean(windows: Tensor, weights: Tensor) -> Tensor:
    """M12: Mean acceleration.  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 3:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    d2 = torch.diff(torch.diff(windows, dim=-1), dim=-1)
    return d2.mean(-1)


def batch_m13_acceleration_std(windows: Tensor, weights: Tensor) -> Tensor:
    """M13: Acceleration std.  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 4:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    d2 = torch.diff(torch.diff(windows, dim=-1), dim=-1)
    return d2.std(-1)


# ── Dynamics: Smoothness ─────────────────────────────────────────────────

def batch_m15_smoothness(windows: Tensor, weights: Tensor) -> Tensor:
    """M15: Smoothness (inverse velocity variability).  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 3:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    d1 = torch.diff(windows, dim=-1)
    vel_std = d1.std(-1)
    return 1.0 / (1.0 + vel_std)


# ── Dynamics: Trend ──────────────────────────────────────────────────────

def batch_m18_trend(windows: Tensor, weights: Tensor) -> Tensor:
    """M18: Weighted linear regression slope.  (B,F,W),(W,) -> (B,F)."""
    B, F, W = windows.shape
    if W < 2:
        return torch.zeros(B, F, device=windows.device, dtype=windows.dtype)
    t = torch.linspace(0.0, 1.0, W, device=windows.device, dtype=windows.dtype)
    t_mean = (weights * t).sum()                                    # scalar
    x_mean = (weights * windows).sum(-1, keepdim=True)              # (B, F, 1)
    t_dev = t - t_mean                                               # (W,)
    x_dev = windows - x_mean                                        # (B, F, W)
    numer = (weights * x_dev * t_dev).sum(-1)                       # (B, F)
    denom = (weights * t_dev ** 2).sum().clamp(min=1e-12)           # scalar
    return numer / denom


def batch_m21_zero_crossings(windows: Tensor, weights: Tensor) -> Tensor:
    """M21: Mean-crossing count.  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 2:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    mu = windows.mean(-1, keepdim=True)              # (B, F, 1)
    centered = windows - mu                           # (B, F, W)
    products = centered[..., :-1] * centered[..., 1:]  # (B, F, W-1)
    return (products < 0).float().sum(-1)             # (B, F)


# ── Rhythm ───────────────────────────────────────────────────────────────

def batch_m14_periodicity(windows: Tensor, weights: Tensor) -> Tensor:
    """M14: Periodicity (autocorrelation peak ratio).  (B,F,W) -> (B,F)."""
    B, F, W = windows.shape
    if W < 8:
        return torch.zeros(B, F, device=windows.device, dtype=windows.dtype)
    mu = windows.mean(-1, keepdim=True)       # (B, F, 1)
    centered = windows - mu                    # (B, F, W)
    r0 = (centered ** 2).sum(-1).clamp(min=1e-12)  # (B, F)
    max_lag = W // 2
    result = torch.zeros(B, F, device=windows.device, dtype=windows.dtype)
    for lag in range(2, max_lag + 1):
        r_lag = (centered[..., :W - lag] * centered[..., lag:]).sum(-1)
        ratio = r_lag / r0
        result = torch.maximum(result, ratio)
    return result


def batch_m17_shape_period(windows: Tensor, weights: Tensor) -> Tensor:
    """M17: Dominant period in frames.  (B,F,W) -> (B,F)."""
    B, F, W = windows.shape
    if W < 8:
        return torch.zeros(B, F, device=windows.device, dtype=windows.dtype)
    mu = windows.mean(-1, keepdim=True)
    centered = windows - mu
    r0 = (centered ** 2).sum(-1).clamp(min=1e-12)
    max_lag = W // 2
    best_ratio = torch.full((B, F), -1.0, device=windows.device,
                            dtype=windows.dtype)
    best_lag = torch.zeros(B, F, device=windows.device, dtype=windows.dtype)
    for lag in range(2, max_lag + 1):
        r_lag = (centered[..., :W - lag] * centered[..., lag:]).sum(-1)
        ratio = r_lag / r0
        mask = ratio > best_ratio
        best_ratio = torch.where(mask, ratio, best_ratio)
        lag_val = torch.tensor(float(lag), device=windows.device,
                               dtype=windows.dtype)
        best_lag = torch.where(mask, lag_val, best_lag)
    return best_lag


def batch_m22_peaks(windows: Tensor, weights: Tensor) -> Tensor:
    """M22: Count of local maxima.  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 3:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    left = windows[..., :-2]
    center = windows[..., 1:-1]
    right = windows[..., 2:]
    is_peak = (center > left) & (center > right)
    return is_peak.float().sum(-1)


# ── Information ──────────────────────────────────────────────────────────

def batch_m20_entropy(windows: Tensor, weights: Tensor) -> Tensor:
    """M20: Shannon entropy over 16-bin histogram.  (B,F,W) -> (B,F)."""
    B, F, W = windows.shape
    NUM_BINS = 16
    if W < 4:
        return torch.zeros(B, F, device=windows.device, dtype=windows.dtype)
    x = windows.clamp(0.0, 1.0)
    bin_idx = (x * NUM_BINS).long().clamp(0, NUM_BINS - 1)  # (B, F, W)
    one_hot = torch.nn.functional.one_hot(bin_idx, NUM_BINS).float()  # (B,F,W,16)
    counts = one_hot.sum(dim=-2)                             # (B, F, 16)
    p = counts / W
    log_p = torch.log2(p.clamp(min=1e-10))
    entropy = -((p * log_p) * (p > 0).float()).sum(-1)       # (B, F)
    return entropy.abs()


# ── Symmetry ─────────────────────────────────────────────────────────────

def batch_m16_curvature(windows: Tensor, weights: Tensor) -> Tensor:
    """M16: Mean absolute second difference.  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 3:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    d2 = torch.diff(torch.diff(windows, dim=-1), dim=-1)
    return d2.abs().mean(-1)


def batch_m19_stability(windows: Tensor, weights: Tensor) -> Tensor:
    """M19: Stability (inverse std).  (B,F,W) -> (B,F)."""
    W = windows.shape[-1]
    if W < 2:
        return torch.zeros(windows.shape[:2], device=windows.device,
                           dtype=windows.dtype)
    sigma = windows.std(-1)
    return 1.0 / (1.0 + sigma)


def batch_m23_symmetry(windows: Tensor, weights: Tensor) -> Tensor:
    """M23: Time-reversal symmetry (Pearson r of halves).  (B,F,W) -> (B,F)."""
    B, F, W = windows.shape
    if W < 4:
        return torch.zeros(B, F, device=windows.device, dtype=windows.dtype)
    half = W // 2
    first_half = windows[..., :half]               # (B, F, half)
    second_half_rev = windows[..., -half:].flip(-1)  # (B, F, half)
    mu_a = first_half.mean(-1, keepdim=True)
    mu_b = second_half_rev.mean(-1, keepdim=True)
    a_dev = first_half - mu_a
    b_dev = second_half_rev - mu_b
    numer = (a_dev * b_dev).sum(-1)
    denom_a = (a_dev ** 2).sum(-1).sqrt()
    denom_b = (b_dev ** 2).sum(-1).sqrt()
    denom = (denom_a * denom_b).clamp(min=1e-8)
    return numer / denom


# ── Dispatch Table ───────────────────────────────────────────────────────

BATCH_DISPATCH: Dict[int, BatchMorphFn] = {
    0:  batch_m0_weighted_mean,
    1:  batch_m1_mean,
    2:  batch_m2_std,
    3:  batch_m3_median,
    4:  batch_m4_max,
    5:  batch_m5_range,
    6:  batch_m6_skewness,
    7:  batch_m7_kurtosis,
    8:  batch_m8_velocity,
    9:  batch_m9_velocity_mean,
    10: batch_m10_velocity_std,
    11: batch_m11_acceleration,
    12: batch_m12_acceleration_mean,
    13: batch_m13_acceleration_std,
    14: batch_m14_periodicity,
    15: batch_m15_smoothness,
    16: batch_m16_curvature,
    17: batch_m17_shape_period,
    18: batch_m18_trend,
    19: batch_m19_stability,
    20: batch_m20_entropy,
    21: batch_m21_zero_crossings,
    22: batch_m22_peaks,
    23: batch_m23_symmetry,
}


def batch_morph(
    windows: Tensor,
    weights: Tensor,
    morph_idx: int,
) -> Tensor:
    """Compute a morph across all frames in batch.

    Args:
        windows: ``(B, F, W)`` -- batched time windows for F frames.
        weights: ``(W,)`` -- pre-normalized attention weights.
        morph_idx: Integer in ``[0, 23]`` selecting the morph.

    Returns:
        ``(B, F)`` -- raw (un-normalized) morph values.
    """
    if morph_idx not in BATCH_DISPATCH:
        raise ValueError(f"Invalid morph_idx={morph_idx}; must be in [0, 23].")
    return BATCH_DISPATCH[morph_idx](windows, weights)
