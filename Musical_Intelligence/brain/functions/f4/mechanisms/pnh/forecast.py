"""PNH F-Layer — Forecast (3D).

Three forward predictions for dissonance resolution, preference, and expertise:

  F0: dissonance_resolution_fc  — Dissonance resolution prediction (0.5-2s) [0, 1]
  F1: preference_judgment_fc    — Preference judgment prediction (1-3s) [0, 1]
  F2: expertise_modulation_fc   — Expertise modulation forecast [0, 1]

H3 consumed:
    (14, 14, 18, 0) tonalness trend H14 L0  — purity trajectory over progression (700ms)

F-layer primarily reuses H+M+P outputs rather than reading new H3 tuples directly.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pnh/PNH-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_TONALNESS_TREND_700MS = (14, 14, 18, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    h_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from H/M/P outputs + H3 context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        h_outputs: ``(H0, H1, H2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    h0, _h1, h2 = h_outputs
    m0, m1 = m_outputs
    p0, p1, p2 = p_outputs

    # -- H3 lookups ------------------------------------------------------------
    tonalness_trend = h3_features[_TONALNESS_TREND_700MS]  # (B, T)

    # -- F0: Dissonance resolution prediction ----------------------------------
    # Harrison & Pearce 2020: consonance = interference + harmonicity + familiarity
    # Uses structural expectation (P0) trajectory and ratio complexity (M0)
    # to predict whether current dissonance resolves to consonance
    f0 = torch.sigmoid(
        0.40 * p0 + 0.30 * (1.0 - m0) + 0.30 * tonalness_trend
    )

    # -- F1: Preference judgment prediction ------------------------------------
    # Sarasso et al. 2019: consonance-preference link; memorization d=0.474
    # Consonance preference (P2) drives aesthetic evaluation prediction
    f1 = torch.sigmoid(
        0.40 * p2 + 0.30 * p0 + 0.30 * (1.0 - h0)
    )

    # -- F2: Expertise modulation forecast -------------------------------------
    # Schon et al. 2005: musicians N1-P2 (100-200ms) vs non-musicians N2 (200-300ms)
    # Training-dependent sensitivity from H2 expertise and familiarity trajectory
    f2 = torch.sigmoid(
        0.40 * h2 + 0.30 * tonalness_trend + 0.30 * m1
    )

    return f0, f1, f2
