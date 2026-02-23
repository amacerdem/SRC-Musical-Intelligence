"""TPIO F-Layer -- Forecast (3D).

Three forward predictions for timbre perception-imagery processing:

  F0: imagery_stability_pred  -- Predicted stability of timbral imagery
  F1: timbre_expectation      -- Expected next timbral state
  F2: overlap_pred            -- Predicted perception-imagery overlap

Uses E/M/P outputs -- no additional H3 dependencies.

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/tpio/TPIO-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/M/P outputs.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        m_outputs: ``(M0,)`` each ``(B, T)``.
        p_outputs: ``(P0, P1)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    f01, f02, f03, f04 = e_outputs
    (m0,) = m_outputs
    p0, p1 = p_outputs

    # F0: Imagery Stability Prediction
    # Sustained imagery depends on overlap strength and SMA engagement
    # Halpern 2004: imagery fidelity correlates with overlap
    f0 = torch.sigmoid(
        0.40 * m0
        + 0.30 * f02
        + 0.30 * p1
    )

    # F1: Timbre Expectation
    # Predicted next timbral state from current perception + cortical state
    # McAdams 1999: spectral continuity drives timbre expectation
    f1 = torch.sigmoid(
        0.35 * p0
        + 0.30 * f01
        + 0.20 * f04
        + 0.15 * m0
    )

    # F2: Overlap Prediction
    # Predicted future overlap between perception and imagery
    # Zatorre 2005: right hemisphere maintains overlap over time
    f2 = torch.sigmoid(
        0.40 * f03
        + 0.30 * m0
        + 0.30 * p0
    )

    return f0, f1, f2
