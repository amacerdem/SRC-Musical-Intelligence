"""IACM F-Layer — Forecast (3D).

Three forward predictions for inharmonicity-attention dynamics:

  F0: object_segreg_pred       — Predicted object segregation state [0, 1]
  F1: attention_shift_pred     — Predicted attention shift magnitude [0, 1]
  F2: multiple_objects_pred    — Predicted multi-object parsing load [0, 1]

H3 consumed: (none — relies on E/M/P layer outputs)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/iacm/IACM-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/M/P outputs.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)``.
        p_outputs: ``(P0, P1)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    e0, e1, _e2 = e_outputs
    (_m0, m1, m2) = m_outputs
    (p0, _p1) = p_outputs

    # F0: Object segregation prediction — future scene parsing
    # Herrmann 2015: sustained segregation from regularity + entropy
    f0 = torch.sigmoid(0.50 * e1 + 0.50 * m1)

    # F1: Attention shift prediction — upcoming capture events
    # Albouy 2017: inharmonic capture predicts attention reorienting
    f1 = torch.sigmoid(0.50 * e0 + 0.50 * p0)

    # F2: Multiple objects prediction — multi-stream parsing load
    # Zatorre 2007: scene complexity from segregation + perception
    f2 = torch.sigmoid(0.50 * e1 + 0.50 * m2)

    return f0, f1, f2
