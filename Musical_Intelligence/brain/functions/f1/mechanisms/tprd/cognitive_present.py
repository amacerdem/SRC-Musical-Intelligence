"""TPRD P-Layer — Cognitive Present (2D).

Two present-processing dimensions for tonotopy-pitch state:

  P0: tonotopic_state — Current tonotopic activation level
  P1: pitch_state     — Current pitch representation level

H3 consumed:
    (3, 0, 0, 2)   stumpf value H0 L2         — immediate pitch fusion
    (3, 3, 1, 2)   stumpf mean H3 L2          — brainstem pitch fusion
    (14, 6, 1, 0)  tonalness mean H6 L0       — beat-level pitch clarity
    (17, 6, 14, 0) spectral_auto period H6 L0 — beat-level harmonic periodicity

R3 consumed:
    [0] roughness  — tonotopic activation proxy
    [14] tonalness — pitch state proxy

See Docs/C³/Models/IMU-β8-TPRD/TPRD.md §6.1
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_H0 = (3, 0, 0, 2)
_STUMPF_MEAN_H3 = (3, 3, 1, 2)
_TONALNESS_MEAN_H6 = (14, 6, 1, 0)
_AUTOCORR_PERIOD_H6 = (17, 6, 14, 0)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_TONALNESS = 14


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(T0, T1, T2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    t0, _t1, _t2 = e_outputs
    _m0, m1 = m_outputs

    # H3 features
    stumpf_h0 = h3_features[_STUMPF_H0]
    stumpf_mean = h3_features[_STUMPF_MEAN_H3]
    tonalness_mean_h6 = h3_features[_TONALNESS_MEAN_H6]
    autocorr_period_h6 = h3_features[_AUTOCORR_PERIOD_H6]

    roughness = r3_features[:, :, _ROUGHNESS]
    tonalness = r3_features[:, :, _TONALNESS]

    # P0: Tonotopic State — current tonotopic activation
    # roughness × (1 - pitch fusion) → spectral processing dominance
    p0 = torch.sigmoid(
        0.40 * t0 * roughness
        + 0.30 * (1.0 - stumpf_h0)
        + 0.30 * (1.0 - stumpf_mean)
    )

    # P1: Pitch State — current pitch representation
    # tonalness × periodicity × fusion → F0 extraction quality
    p1 = torch.sigmoid(
        0.35 * tonalness_mean_h6 * autocorr_period_h6
        + 0.35 * tonalness * m1
        + 0.30 * stumpf_mean
    )

    return p0, p1
