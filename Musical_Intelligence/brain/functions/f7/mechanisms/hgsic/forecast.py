"""HGSIC F-Layer -- Forecast (3D).

Three forward predictions for groove state:

  F0: groove_prediction    -- Predicted future groove strength
  F1: beat_expectation     -- Expected next beat alignment
  F2: motor_anticipation   -- Motor system preparation for next groove event

H3 consumed:
    (9, 16, 14, 2)   roughness_total periodicity H16 bidi -- roughness cycling
    (7, 16, 15, 0)   amplitude skewness H16              -- dynamic asymmetry
    (7, 16, 18, 0)   amplitude trend H16                 -- dynamic trajectory
    (23, 16, 14, 2)  flatness periodicity H16 bidi       -- spectral cycling
    (24, 16, 1, 0)   timbre_change mean H16              -- timbral dynamics

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hgsic/HGSIC-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_PERIOD_H16 = (9, 16, 14, 2)
_AMPLITUDE_SKEW_H16 = (7, 16, 15, 0)
_AMPLITUDE_TREND_H16 = (7, 16, 18, 0)
_FLATNESS_PERIOD_H16 = (23, 16, 14, 2)
_TIMBRE_CHANGE_MEAN_H16 = (24, 16, 1, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from H3 + E/M/P outputs.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    f01, f02, f03 = e_outputs
    m0, m1 = m_outputs
    p0, p1, p2 = p_outputs

    B = f01.shape[0]
    T = f01.shape[1] if f01.dim() > 1 else 1
    device = f01.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    roughness_period = h3_features.get(_ROUGHNESS_PERIOD_H16, zero)
    amplitude_skew = h3_features.get(_AMPLITUDE_SKEW_H16, zero)
    amplitude_trend = h3_features.get(_AMPLITUDE_TREND_H16, zero)
    flatness_period = h3_features.get(_FLATNESS_PERIOD_H16, zero)
    timbre_change_mean = h3_features.get(_TIMBRE_CHANGE_MEAN_H16, zero)

    # F0: Groove Prediction -- predicted future groove strength
    # Madison 2011: groove depends on dynamic range and complexity
    f0 = torch.sigmoid(
        0.25 * m0
        + 0.20 * roughness_period
        + 0.20 * amplitude_skew
        + 0.20 * flatness_period
        + 0.15 * p0
    )

    # F1: Beat Expectation -- expected next beat alignment
    # Janata 2012: beat expectation from entrainment + dynamic trajectory
    f1 = torch.sigmoid(
        0.30 * p2
        + 0.25 * amplitude_trend
        + 0.25 * f01
        + 0.20 * m1
    )

    # F2: Motor Anticipation -- motor system preparation
    # Witek 2014: groove drives anticipatory motor response
    f2 = torch.sigmoid(
        0.30 * p1
        + 0.25 * f03
        + 0.25 * timbre_change_mean
        + 0.20 * m0
    )

    return f0, f1, f2
