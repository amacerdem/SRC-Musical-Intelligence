"""MorphComputer -- dispatch table for all 24 temporal morphologies.

Stateless dispatcher that maps morph indices (0-23) to pure computation
functions.  Raw output is NOT normalized (scaling is downstream).
"""
from __future__ import annotations

from typing import Callable, Dict

import torch
from torch import Tensor

# -- Distribution morphs (M0-M7) --
from .distribution.central import (
    m0_weighted_mean,
    m1_mean,
    m3_median,
)
from .distribution.spread import m2_std, m5_range
from .distribution.shape import (
    m4_max,
    m6_skewness,
    m7_kurtosis,
)

# -- Dynamics morphs (M8-M13, M15, M18, M21) --
from .dynamics.derivatives import (
    m8_velocity,
    m9_velocity_mean,
    m10_velocity_std,
    m11_acceleration,
    m12_acceleration_mean,
    m13_acceleration_std,
)
from .dynamics.smoothness import m15_smoothness
from .dynamics.trend import m18_trend, m21_zero_crossings

# -- Rhythm morphs (M14, M17, M22) --
from .rhythm.periodicity import (
    m14_periodicity,
    m17_shape_period,
    m22_peaks,
)

# -- Information morph (M20) --
from .information.entropy import m20_entropy

# -- Symmetry morphs (M16, M19, M23) --
from .symmetry.features import (
    m16_curvature,
    m19_stability,
    m23_symmetry,
)

# Type alias for morph function signature
MorphFn = Callable[[Tensor, Tensor], Tensor]


class MorphComputer:
    """Stateless dispatch table for the 24 H3 temporal morphologies.

    Each morph function receives ``(window, weights)`` and returns ``(B,)``.
    Raw morph values are returned without normalization; use
    :func:`~ear.h3.morphology.scaling.normalize_morph` downstream.

    Raises:
        ValueError: If ``morph_idx`` is outside ``[0, 23]``.
    """

    def __init__(self) -> None:
        self._dispatch: Dict[int, MorphFn] = {
            0:  m0_weighted_mean,
            1:  m1_mean,
            2:  m2_std,
            3:  m3_median,
            4:  m4_max,
            5:  m5_range,
            6:  m6_skewness,
            7:  m7_kurtosis,
            8:  m8_velocity,
            9:  m9_velocity_mean,
            10: m10_velocity_std,
            11: m11_acceleration,
            12: m12_acceleration_mean,
            13: m13_acceleration_std,
            14: m14_periodicity,
            15: m15_smoothness,
            16: m16_curvature,
            17: m17_shape_period,
            18: m18_trend,
            19: m19_stability,
            20: m20_entropy,
            21: m21_zero_crossings,
            22: m22_peaks,
            23: m23_symmetry,
        }

    def compute(
        self,
        window: Tensor,
        weights: Tensor,
        morph_idx: int,
    ) -> Tensor:
        """Compute a single morph for a batched window.

        Args:
            window: ``(B, win_len)`` -- R3 scalar values in the time window.
            weights: ``(win_len,)`` -- Pre-normalized attention weights
                (sum to 1.0).
            morph_idx: Integer in ``[0, 23]`` selecting the morph.

        Returns:
            ``(B,)`` -- One raw (un-normalized) scalar per batch item.

        Raises:
            ValueError: If *morph_idx* is not in ``[0, 23]``.
        """
        if morph_idx not in self._dispatch:
            raise ValueError(
                f"Invalid morph_idx={morph_idx}; must be in [0, 23]."
            )
        return self._dispatch[morph_idx](window, weights)
