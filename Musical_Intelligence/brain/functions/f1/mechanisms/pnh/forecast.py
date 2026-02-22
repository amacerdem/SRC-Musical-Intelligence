"""PNH F-Layer — Forecast (3D).

Three forward predictions for ratio hierarchy processing:

  F0: dissonance_res_fc  — Dissonance resolution prediction (0.5-2s)
  F1: pref_judgment_fc   — Preference judgment prediction (1-3s)
  F2: expertise_mod_fc   — Expertise modulation forecast

H3 consumed:
    (0, 14, 1, 0)  roughness mean H14 L0       — avg dissonance over progression
    (0, 18, 18, 0) roughness trend H18 L0      — dissonance trajectory over phrase
    (4, 18, 19, 0) pleasantness stability H18 L0 — consonance stability
    (5, 14, 1, 0)  inharmonicity mean H14 L0   — avg complexity over progression
    (3, 14, 1, 2)  stumpf mean H14 L2          — fusion stability
    (14, 14, 3, 0) tonalness std H14 L0        — purity variation
    (2, 18, 1, 0)  helmholtz mean H18 L0       — harmonic template over phrase

See Docs/C³/Models/IMU-α2-PNH/PNH.md §6.1
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_MEAN_H14 = (0, 14, 1, 0)
_ROUGHNESS_TREND_H18 = (0, 18, 18, 0)
_PLEASANT_STAB_H18 = (4, 18, 19, 0)
_INHARM_MEAN_H14 = (5, 14, 1, 0)
_STUMPF_MEAN_H14 = (3, 14, 1, 2)
_TONALNESS_STD_H14 = (14, 14, 3, 0)
_HELMHOLTZ_MEAN_H18 = (2, 18, 1, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/M/P outputs + H3 trends.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(H0, H1, H2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    _h0, _h1, h2 = e_outputs
    m0, _m1 = m_outputs
    _p0, p1, p2 = p_outputs

    # H3 temporal features
    roughness_trend = h3_features[_ROUGHNESS_TREND_H18]
    pleasant_stab = h3_features[_PLEASANT_STAB_H18]
    stumpf_mean = h3_features[_STUMPF_MEAN_H14]
    helmholtz_mean = h3_features[_HELMHOLTZ_MEAN_H18]

    # F0: Dissonance Resolution Prediction (0.5-2s)
    # Based on roughness trend and consonance trajectory
    # Coefficient sum: 0.40 + 0.30 + 0.30 = 1.0
    f0 = torch.sigmoid(
        0.40 * (1.0 - roughness_trend)
        + 0.30 * helmholtz_mean
        + 0.30 * p1
    )

    # F1: Preference Judgment Prediction (1-3s)
    # Consonance stability → pleasure mapping
    # Coefficient sum: 0.40 + 0.30 + 0.30 = 1.0
    f1 = torch.sigmoid(
        0.40 * pleasant_stab
        + 0.30 * p2
        + 0.30 * stumpf_mean
    )

    # F2: Expertise Modulation Forecast
    # Training-dependent sensitivity prediction
    # Coefficient sum: 0.50 + 0.50 = 1.0
    f2 = torch.sigmoid(
        0.50 * h2
        + 0.50 * m0
    )

    return f0, f1, f2
