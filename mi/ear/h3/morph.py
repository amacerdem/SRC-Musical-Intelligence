"""
MorphComputer — 24 morphological features.

Each morph reduces a windowed time series to a single scalar.
Morphs capture different statistical properties of the temporal evolution.
"""

from __future__ import annotations

import torch
from torch import Tensor

from ...core.constants import MORPH_NAMES


class MorphComputer:
    """Computes morphological features from windowed time series."""

    def compute(
        self,
        window: Tensor,
        weights: Tensor,
        morph_idx: int,
    ) -> Tensor:
        """Compute a single morph from a weighted window.

        Args:
            window: (B, win_len) time series segment
            weights: (win_len,) attention weights (normalized)
            morph_idx: which morph to compute (0-23)

        Returns:
            (B,) scalar morph value
        """
        dispatch = {
            0: self._m0_value,
            1: self._m1_mean,
            2: self._m2_std,
            3: self._m3_median,
            4: self._m4_max,
            5: self._m5_range,
            6: self._m6_skewness,
            7: self._m7_kurtosis,
            8: self._m8_velocity,
            9: self._m9_velocity_mean,
            10: self._m10_velocity_std,
            11: self._m11_acceleration,
            12: self._m12_acceleration_mean,
            13: self._m13_acceleration_std,
            14: self._m14_periodicity,
            15: self._m15_smoothness,
            16: self._m16_curvature,
            17: self._m17_shape_period,
            18: self._m18_trend,
            19: self._m19_stability,
            20: self._m20_entropy,
            21: self._m21_zero_crossings,
            22: self._m22_peaks,
            23: self._m23_symmetry,
        }
        fn = dispatch.get(morph_idx)
        if fn is None:
            raise ValueError(f"Unknown morph index: {morph_idx}")
        return fn(window, weights)

    # ═══════════════════════════════════════════════════════════════════
    # MORPH IMPLEMENTATIONS
    # ═══════════════════════════════════════════════════════════════════

    def _m0_value(self, w: Tensor, a: Tensor) -> Tensor:
        """Attention-weighted mean."""
        return (w * w).sum(dim=-1) if w.shape[-1] == 0 else (w * a).sum(dim=-1)

    def _m1_mean(self, w: Tensor, a: Tensor) -> Tensor:
        """Unweighted mean."""
        return w.mean(dim=-1)

    def _m2_std(self, w: Tensor, a: Tensor) -> Tensor:
        """Standard deviation."""
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        return w.std(dim=-1)

    def _m3_median(self, w: Tensor, a: Tensor) -> Tensor:
        """Median."""
        return w.median(dim=-1).values

    def _m4_max(self, w: Tensor, a: Tensor) -> Tensor:
        """Maximum."""
        return w.max(dim=-1).values

    def _m5_range(self, w: Tensor, a: Tensor) -> Tensor:
        """Max - Min."""
        return w.max(dim=-1).values - w.min(dim=-1).values

    def _m6_skewness(self, w: Tensor, a: Tensor) -> Tensor:
        """Distribution skew."""
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        mean = w.mean(dim=-1, keepdim=True)
        std = w.std(dim=-1, keepdim=True).clamp(min=1e-8)
        return ((w - mean) / std).pow(3).mean(dim=-1)

    def _m7_kurtosis(self, w: Tensor, a: Tensor) -> Tensor:
        """Distribution peakedness."""
        if w.shape[-1] < 4:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        mean = w.mean(dim=-1, keepdim=True)
        std = w.std(dim=-1, keepdim=True).clamp(min=1e-8)
        return ((w - mean) / std).pow(4).mean(dim=-1) - 3.0

    def _m8_velocity(self, w: Tensor, a: Tensor) -> Tensor:
        """First derivative (latest)."""
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        return w[:, -1] - w[:, -2]

    def _m9_velocity_mean(self, w: Tensor, a: Tensor) -> Tensor:
        """Mean of first derivative."""
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        vel = w[:, 1:] - w[:, :-1]
        return vel.mean(dim=-1)

    def _m10_velocity_std(self, w: Tensor, a: Tensor) -> Tensor:
        """Velocity variance (jerk proxy)."""
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        vel = w[:, 1:] - w[:, :-1]
        return vel.std(dim=-1)

    def _m11_acceleration(self, w: Tensor, a: Tensor) -> Tensor:
        """Second derivative (latest)."""
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        vel = w[:, 1:] - w[:, :-1]
        return vel[:, -1] - vel[:, -2]

    def _m12_acceleration_mean(self, w: Tensor, a: Tensor) -> Tensor:
        """Mean acceleration."""
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        vel = w[:, 1:] - w[:, :-1]
        acc = vel[:, 1:] - vel[:, :-1]
        return acc.mean(dim=-1)

    def _m13_acceleration_std(self, w: Tensor, a: Tensor) -> Tensor:
        """Acceleration variance."""
        if w.shape[-1] < 4:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        vel = w[:, 1:] - w[:, :-1]
        acc = vel[:, 1:] - vel[:, :-1]
        return acc.std(dim=-1)

    def _m14_periodicity(self, w: Tensor, a: Tensor) -> Tensor:
        """Autocorrelation peak strength."""
        if w.shape[-1] < 4:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        centered = w - w.mean(dim=-1, keepdim=True)
        norm = centered.norm(dim=-1, keepdim=True).clamp(min=1e-8)
        normalized = centered / norm
        # Lag-1 autocorrelation
        autocorr = (normalized[:, :-1] * normalized[:, 1:]).sum(dim=-1)
        return autocorr.clamp(0, 1)

    def _m15_smoothness(self, w: Tensor, a: Tensor) -> Tensor:
        """1/(1+|jerk|/σ) — scale-invariant smoothness."""
        if w.shape[-1] < 4:
            return torch.ones(w.shape[0], device=w.device, dtype=w.dtype)
        vel = w[:, 1:] - w[:, :-1]
        acc = vel[:, 1:] - vel[:, :-1]
        jerk = acc[:, 1:] - acc[:, :-1]
        sigma = w.std(dim=-1).clamp(min=1e-8)
        return 1.0 / (1.0 + jerk.abs().mean(dim=-1) / sigma)

    def _m16_curvature(self, w: Tensor, a: Tensor) -> Tensor:
        """Spectral curvature (mean absolute acceleration)."""
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        vel = w[:, 1:] - w[:, :-1]
        acc = vel[:, 1:] - vel[:, :-1]
        return acc.abs().mean(dim=-1)

    def _m17_shape_period(self, w: Tensor, a: Tensor) -> Tensor:
        """Oscillation period (zero-crossing based)."""
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        centered = w - w.mean(dim=-1, keepdim=True)
        signs = centered.sign()
        crossings = (signs[:, 1:] != signs[:, :-1]).float().sum(dim=-1)
        # Period = 2 * length / crossings
        period = 2.0 * w.shape[-1] / crossings.clamp(min=1.0)
        # Normalize to [0, 1] (larger period → higher value)
        return torch.sigmoid(period / w.shape[-1] - 0.5)

    def _m18_trend(self, w: Tensor, a: Tensor) -> Tensor:
        """Linear regression slope."""
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        n = w.shape[-1]
        x = torch.arange(n, device=w.device, dtype=w.dtype)
        x_mean = x.mean()
        y_mean = w.mean(dim=-1, keepdim=True)
        slope = ((x - x_mean) * (w - y_mean)).sum(dim=-1) / (
            (x - x_mean).pow(2).sum().clamp(min=1e-8)
        )
        return slope

    def _m19_stability(self, w: Tensor, a: Tensor) -> Tensor:
        """1/(1+var/σ²) — resistance to change."""
        if w.shape[-1] < 2:
            return torch.ones(w.shape[0], device=w.device, dtype=w.dtype)
        var = w.var(dim=-1)
        sigma_sq = w.mean(dim=-1).pow(2).clamp(min=1e-8)
        return 1.0 / (1.0 + var / sigma_sq)

    def _m20_entropy(self, w: Tensor, a: Tensor) -> Tensor:
        """Shannon entropy of histogram."""
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        # Soft histogram: bin values into 16 bins
        n_bins = 16
        w_min = w.min(dim=-1, keepdim=True).values
        w_max = w.max(dim=-1, keepdim=True).values
        w_range = (w_max - w_min).clamp(min=1e-8)
        normalized = (w - w_min) / w_range  # [0, 1]
        # Count per bin
        bin_idx = (normalized * (n_bins - 1)).long().clamp(0, n_bins - 1)
        counts = torch.zeros(w.shape[0], n_bins, device=w.device, dtype=w.dtype)
        counts.scatter_add_(1, bin_idx, torch.ones_like(w))
        prob = counts / counts.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        prob = prob.clamp(min=1e-10)
        entropy = -(prob * prob.log()).sum(dim=-1)
        max_entropy = torch.log(torch.tensor(n_bins, dtype=w.dtype, device=w.device))
        return (entropy / max_entropy).clamp(0, 1)

    def _m21_zero_crossings(self, w: Tensor, a: Tensor) -> Tensor:
        """Sign change count (normalized)."""
        if w.shape[-1] < 2:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        centered = w - w.mean(dim=-1, keepdim=True)
        signs = centered.sign()
        crossings = (signs[:, 1:] != signs[:, :-1]).float().sum(dim=-1)
        return crossings / (w.shape[-1] - 1)

    def _m22_peaks(self, w: Tensor, a: Tensor) -> Tensor:
        """Local maxima count (normalized)."""
        if w.shape[-1] < 3:
            return torch.zeros(w.shape[0], device=w.device, dtype=w.dtype)
        left = w[:, :-2]
        center = w[:, 1:-1]
        right = w[:, 2:]
        is_peak = (center > left) & (center > right)
        count = is_peak.float().sum(dim=-1)
        return count / (w.shape[-1] - 2)

    def _m23_symmetry(self, w: Tensor, a: Tensor) -> Tensor:
        """Forward/backward symmetry."""
        if w.shape[-1] < 2:
            return torch.ones(w.shape[0], device=w.device, dtype=w.dtype)
        n = w.shape[-1]
        half = n // 2
        forward = w[:, :half]
        backward = w[:, -half:].flip(dims=[-1])
        diff = (forward - backward).pow(2).mean(dim=-1)
        scale = w.var(dim=-1).clamp(min=1e-8)
        return 1.0 / (1.0 + diff / scale)
