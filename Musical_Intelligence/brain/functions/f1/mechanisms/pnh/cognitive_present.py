"""PNH P-Layer — Cognitive Present (3D).

Three present-processing dimensions for ratio hierarchy encoding:

  P0: ratio_enc       — Current ratio encoding state
  P1: conflict_mon    — Current conflict monitoring activation (IFG/ACC)
  P2: consonance_pref — Consonance-preference binding

H3 consumed:
    (4, 10, 0, 2)   pleasantness value H10 L2  — current consonance
    (14, 10, 0, 2)  tonalness value H10 L2     — ratio purity
    (17, 10, 14, 2) spectral_auto period H10 L2 — harmonic regularity
    (8, 10, 0, 2)   velocity_D value H10 L2    — attention weight (loudness)

R3 consumed:
    [0] roughness — for consonance-preference binding

See Docs/C³/Models/IMU-α2-PNH/PNH.md §6.1
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PLEASANT_H10 = (4, 10, 0, 2)
_TONALNESS_H10 = (14, 10, 0, 2)
_AUTOCORR_PERIOD_H10 = (17, 10, 14, 2)
_VELOCITY_D_H10 = (8, 10, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(H0, H1, H2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    _h0, h1, h2 = e_outputs
    m0, m1 = m_outputs

    # H3 features
    pleasant_h10 = h3_features[_PLEASANT_H10]
    tonalness_h10 = h3_features[_TONALNESS_H10]
    autocorr_period = h3_features[_AUTOCORR_PERIOD_H10]
    velocity_d_h10 = h3_features[_VELOCITY_D_H10]

    roughness = r3_features[:, :, _ROUGHNESS]

    # P0: Ratio Encoding — current harmonic context state
    # Tonalness × harmonic periodicity × loudness attention
    p0 = torch.sigmoid(
        0.40 * tonalness_h10
        + 0.30 * autocorr_period
        + 0.30 * velocity_d_h10
    )

    # P1: Conflict Monitoring — IFG/ACC activation
    # Neural activation (M1) weighted by expertise modulation (H2)
    p1 = torch.sigmoid(0.60 * m1 + 0.40 * h1)

    # P2: Consonance Preference — pleasantness × (1 - roughness)
    # Sarasso 2019: consonance → aesthetic appreciation (η²p=0.685)
    p2 = torch.sigmoid(
        0.50 * pleasant_h10 * (1.0 - roughness)
        + 0.30 * h2
        + 0.20 * m0
    )

    return p0, p1, p2
