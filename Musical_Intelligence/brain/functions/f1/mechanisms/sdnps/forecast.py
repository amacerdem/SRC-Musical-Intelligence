"""SDNPS F-Layer — Forecast (3D).

Three forward predictions for stimulus-dependent pitch salience:

  F0: behavioral_consonance_pred  — Consonance prediction gated by dependency
  F1: roughness_response_pred     — Roughness response (stimulus-invariant)
  F2: generalization_limit        — NPS generalization to novel timbres

H3 consumed:
    (14, 3, 1, 0) tonalness mean H3 L0 — pitch clarity trend (for generalization)

See Docs/C³/Models/SPU-γ1-SDNPS/SDNPS.md §7.2 (Layer F)
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_TONALNESS_MEAN_FWD = (14, 3, 1, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/M/P outputs + H3 context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0,)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    _e0, e1, _e2 = e_outputs
    (m0,) = m_outputs
    p0, p1, p2 = p_outputs

    tonalness_mean = h3_features[_TONALNESS_MEAN_FWD]

    # F0: Behavioral Consonance Prediction
    # Gated by stimulus dependency — valid only when E1 is high
    # Coefficient sum: 0.60 + 0.40 = 1.0
    f0 = torch.sigmoid(0.60 * m0 + 0.40 * p1)

    # F1: Roughness Response Prediction
    # Stimulus-invariant (r=-0.57 holds for ALL timbres)
    # Coefficient sum: 0.57 + 0.43 = 1.0
    f1 = torch.sigmoid(0.57 * p2 + 0.43 * p0)

    # F2: Generalization Limit
    # How far NPS can generalize to novel timbres
    # Coefficient sum: 0.50 + 0.50 = 1.0
    f2 = torch.sigmoid(0.50 * e1 + 0.50 * tonalness_mean)

    return f0, f1, f2
