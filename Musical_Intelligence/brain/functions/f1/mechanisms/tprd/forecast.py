"""TPRD F-Layer — Forecast (3D).

Three forward predictions for tonotopy-pitch processing:

  F0: pitch_percept_fc    — Pitch percept prediction (50-200ms)
  F1: tonotopic_adpt_fc   — Tonotopic adaptation prediction (200-700ms)
  F2: dissociation_fc     — Dissociation evolution forecast (0.5-2s)

H3 consumed:
    (0, 14, 1, 0)   roughness mean H14 L0       — avg tonotopic load
    (5, 14, 1, 0)   inharmonicity mean H14 L0   — avg conflict over progression
    (3, 6, 1, 0)    stumpf mean H6 L0           — beat-level fusion stability
    (22, 14, 1, 0)  entropy mean H14 L0         — avg spectral complexity
    (4, 18, 19, 0)  pleasantness stability H18   — consonance stability
    (6, 10, 0, 2)   harmonic_dev value H10 L2   — template mismatch
    (7, 6, 8, 0)    amplitude velocity H6 L0    — energy change rate
    (8, 10, 0, 2)   velocity_D value H10 L2     — loudness at chord level

See Docs/C³/Models/IMU-β8-TPRD/TPRD.md §6.1
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_MEAN_H14 = (0, 14, 1, 0)
_INHARM_MEAN_H14 = (5, 14, 1, 0)
_STUMPF_MEAN_H6 = (3, 6, 1, 0)
_ENTROPY_MEAN_H14 = (22, 14, 1, 0)
_PLEASANT_STAB_H18 = (4, 18, 19, 0)
_HARM_DEV_H10 = (6, 10, 0, 2)
_AMP_VEL_H6 = (7, 6, 8, 0)
_VELOCITY_D_H10 = (8, 10, 0, 2)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/M/P outputs + H3 trends.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(T0, T1, T2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    _t0, _t1, t2 = e_outputs
    m0, m1 = m_outputs
    p0, p1 = p_outputs

    # H3 temporal features
    stumpf_mean_h6 = h3_features[_STUMPF_MEAN_H6]
    roughness_mean = h3_features[_ROUGHNESS_MEAN_H14]
    pleasant_stab = h3_features[_PLEASANT_STAB_H18]
    harm_dev = h3_features[_HARM_DEV_H10]

    # F0: Pitch Percept Prediction (50-200ms)
    # Pitch state + fusion stability → future pitch percept
    # Coefficient sum: 0.40 + 0.30 + 0.30 = 1.0
    f0 = torch.sigmoid(
        0.40 * p1
        + 0.30 * stumpf_mean_h6
        + 0.30 * m1
    )

    # F1: Tonotopic Adaptation Prediction (200-700ms)
    # Tonotopic state + roughness trend → adaptation forecast
    # Coefficient sum: 0.40 + 0.30 + 0.30 = 1.0
    f1 = torch.sigmoid(
        0.40 * p0
        + 0.30 * (1.0 - roughness_mean)
        + 0.30 * (1.0 - harm_dev)
    )

    # F2: Dissociation Evolution (0.5-2s)
    # Current dissociation + consonance stability → evolution
    # Coefficient sum: 0.35 + 0.35 + 0.30 = 1.0
    f2 = torch.sigmoid(
        0.35 * t2
        + 0.35 * m0
        + 0.30 * pleasant_stab
    )

    return f0, f1, f2
