"""MorphComputer: 24 morphological feature computations."""

from __future__ import annotations

import torch
from torch import Tensor


class MorphComputer:
    """Dispatches to 24 morphological feature methods."""

    def compute(self, window: Tensor, weights: Tensor, morph_idx: int) -> Tensor:
        """(B, win_len), (win_len,), int → (B,)"""
        method = getattr(self, f"_m{morph_idx}_{_MORPH_METHODS[morph_idx]}")
        return method(window, weights)

    # ── M0-M5: Basic statistics ────────────────────────────────────────────

    def _m0_value(self, w: Tensor, wt: Tensor) -> Tensor:
        return (w * wt).sum(dim=-1)

    def _m1_mean(self, w: Tensor, wt: Tensor) -> Tensor:
        return w.mean(dim=-1)

    def _m2_std(self, w: Tensor, wt: Tensor) -> Tensor:
        return w.std(dim=-1) if w.shape[-1] > 1 else torch.zeros(w.shape[0], device=w.device)

    def _m3_median(self, w: Tensor, wt: Tensor) -> Tensor:
        return w.median(dim=-1).values

    def _m4_max(self, w: Tensor, wt: Tensor) -> Tensor:
        return w.max(dim=-1).values

    def _m5_range(self, w: Tensor, wt: Tensor) -> Tensor:
        return w.max(dim=-1).values - w.min(dim=-1).values

    # ── M6-M7: Distribution shape ─────────────────────────────────────────

    def _m6_skewness(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device)
        mean = w.mean(dim=-1, keepdim=True)
        std = w.std(dim=-1, keepdim=True).clamp(min=1e-8)
        return (((w - mean) / std) ** 3).mean(dim=-1)

    def _m7_kurtosis(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 4:
            return torch.zeros(w.shape[0], device=w.device)
        mean = w.mean(dim=-1, keepdim=True)
        std = w.std(dim=-1, keepdim=True).clamp(min=1e-8)
        return (((w - mean) / std) ** 4).mean(dim=-1) - 3.0

    # ── M8-M10: Velocity ──────────────────────────────────────────────────

    def _m8_velocity(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device)
        return w[:, -1] - w[:, -2]

    def _m9_velocity_mean(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device)
        diff = w[:, 1:] - w[:, :-1]
        return diff.mean(dim=-1)

    def _m10_velocity_std(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device)
        diff = w[:, 1:] - w[:, :-1]
        return diff.std(dim=-1)

    # ── M11-M13: Acceleration ─────────────────────────────────────────────

    def _m11_acceleration(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device)
        vel = w[:, 1:] - w[:, :-1]
        return vel[:, -1] - vel[:, -2]

    def _m12_acceleration_mean(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device)
        vel = w[:, 1:] - w[:, :-1]
        acc = vel[:, 1:] - vel[:, :-1]
        return acc.mean(dim=-1)

    def _m13_acceleration_std(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 4:
            return torch.zeros(w.shape[0], device=w.device)
        vel = w[:, 1:] - w[:, :-1]
        acc = vel[:, 1:] - vel[:, :-1]
        return acc.std(dim=-1)

    # ── M14-M17: Shape ────────────────────────────────────────────────────

    def _m14_periodicity(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device)
        mean = w.mean(dim=-1, keepdim=True)
        centered = w - mean
        auto = (centered[:, :-1] * centered[:, 1:]).mean(dim=-1)
        var = (centered ** 2).mean(dim=-1).clamp(min=1e-8)
        return (auto / var).clamp(0.0, 1.0)

    def _m15_smoothness(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 4:
            return torch.ones(w.shape[0], device=w.device)
        vel = w[:, 1:] - w[:, :-1]
        jerk = vel[:, 1:] - vel[:, :-1]
        sigma = w.std(dim=-1).clamp(min=1e-8)
        return 1.0 / (1.0 + jerk.abs().mean(dim=-1) / sigma)

    def _m16_curvature(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device)
        vel = w[:, 1:] - w[:, :-1]
        acc = vel[:, 1:] - vel[:, :-1]
        return acc.abs().mean(dim=-1)

    def _m17_shape_period(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device)
        n = w.shape[-1]
        mean = w.mean(dim=-1, keepdim=True)
        zc = ((w[:, 1:] - mean) * (w[:, :-1] - mean) < 0).float().sum(dim=-1)
        zc = zc.clamp(min=1.0)
        return torch.sigmoid(2 * n / zc / n - 0.5)

    # ── M18-M19: Trend & Stability ────────────────────────────────────────

    def _m18_trend(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device)
        n = w.shape[-1]
        x = torch.arange(n, device=w.device, dtype=w.dtype)
        x_mean = x.mean()
        y_mean = w.mean(dim=-1, keepdim=True)
        numer = ((x - x_mean) * (w - y_mean)).sum(dim=-1)
        denom = ((x - x_mean) ** 2).sum().clamp(min=1e-8)
        return numer / denom

    def _m19_stability(self, w: Tensor, wt: Tensor) -> Tensor:
        mean = w.mean(dim=-1).clamp(min=1e-8)
        var = w.var(dim=-1) if w.shape[-1] > 1 else torch.zeros(w.shape[0], device=w.device)
        return 1.0 / (1.0 + var / (mean ** 2))

    # ── M20-M23: Information ──────────────────────────────────────────────

    def _m20_entropy(self, w: Tensor, wt: Tensor) -> Tensor:
        n = w.shape[-1]
        if n < 2:
            return torch.zeros(w.shape[0], device=w.device)
        # 16-bin histogram entropy
        nbins = 16
        result = torch.zeros(w.shape[0], device=w.device)
        for b in range(w.shape[0]):
            hist = torch.histc(w[b], bins=nbins, min=0.0, max=1.0)
            prob = hist / hist.sum().clamp(min=1e-8)
            prob = prob[prob > 0]
            result[b] = -(prob * prob.log()).sum() / torch.log(torch.tensor(float(nbins), device=w.device))
        return result.clamp(0.0, 1.0)

    def _m21_zero_crossings(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device)
        mean = w.mean(dim=-1, keepdim=True)
        centered = w - mean
        zc = (centered[:, 1:] * centered[:, :-1] < 0).float().sum(dim=-1)
        return zc / (w.shape[-1] - 1)

    def _m22_peaks(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device)
        is_peak = (w[:, 1:-1] > w[:, :-2]) & (w[:, 1:-1] > w[:, 2:])
        return is_peak.float().sum(dim=-1) / (w.shape[-1] - 2)

    def _m23_symmetry(self, w: Tensor, wt: Tensor) -> Tensor:
        if w.shape[-1] < 2:
            return torch.ones(w.shape[0], device=w.device)
        forward = w
        backward = w.flip(dims=[-1])
        diff_sq = ((forward - backward) ** 2).mean(dim=-1)
        var = w.var(dim=-1).clamp(min=1e-8) if w.shape[-1] > 1 else torch.ones(w.shape[0], device=w.device)
        return 1.0 / (1.0 + diff_sq / var)


_MORPH_METHODS = (
    "value", "mean", "std", "median", "max", "range",
    "skewness", "kurtosis",
    "velocity", "velocity_mean", "velocity_std",
    "acceleration", "acceleration_mean", "acceleration_std",
    "periodicity", "smoothness", "curvature", "shape_period",
    "trend", "stability", "entropy", "zero_crossings", "peaks", "symmetry",
)
