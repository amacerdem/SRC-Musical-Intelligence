"""HMCE F-Layer -- Forecast (2D).

Two forward predictions for hierarchical context processing:

  F0: phrase_boundary_pred -- Predicted phrase boundary likelihood
  F1: structure_pred       -- Predicted structural continuation

Uses E/M/P outputs -- no additional H3 dependencies.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hmce/HMCE-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D forecast from E/M/P outputs.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03)`` each ``(B, T)``.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    _f01, f02, f03 = e_outputs
    m0, m1, m2 = m_outputs
    p0, p1, p2 = p_outputs

    # F0: Phrase Boundary Prediction
    # High transition dynamics + low structure regularity -> boundary likely
    # Koelsch 2009: structural boundaries generate CPS-like ERP
    f0 = torch.sigmoid(
        0.35 * m2
        + 0.25 * (1.0 - m1)
        + 0.20 * p2
        + 0.20 * f03
    )

    # F1: Structure Prediction
    # Context depth + regularity + encoding strength predict continuation
    # Pearce 2018: IDyOM information content predicts structure
    f1 = torch.sigmoid(
        0.30 * m0
        + 0.25 * m1
        + 0.25 * p1
        + 0.20 * p0
    )

    return f0, f1
