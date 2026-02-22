"""AMSS F-Layer -- Forecast (2D).

Two forward predictions for stream dynamics:

  F0: stream_stability_pred      -- Predicted stability of current stream [0, 1]
  F1: segregation_shift_pred     -- Predicted shift in segregation state [0, 1]

H3 consumed:
    (25, 16, 18, 0)  coupling trend 1s L0  -- integration trend for stability

F0 predicts whether the current stream will remain stable based on coherence
(M0), attended stream strength (P0), and long-range coupling trend.

F1 predicts whether a segregation shift (stream switch) is imminent based on
segregation depth (M1), competition state (P1), and onset tracking (E0).

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/amss/
Elhilali 2009: stream stability relates to spectral coherence persistence.
Bregman 1994: stream switches triggered by onset boundaries and grouping changes.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_COUPLING_TREND_1S = (25, 16, 18, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D forecast from E/M/P outputs + H3 context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2, E3, E4)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1)`` each ``(B, T)``.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    e0, _e1, _e2, _e3, _e4 = e_outputs
    m0, m1 = m_outputs
    p0, p1 = p_outputs

    coupling_trend = h3_features[_COUPLING_TREND_1S]

    # F0: Stream stability prediction -- will the current stream persist?
    # Elhilali 2009: spectral coherence persistence predicts stream stability
    f0 = torch.sigmoid(
        0.40 * m0 + 0.30 * p0 + 0.30 * coupling_trend
    )

    # F1: Segregation shift prediction -- is a stream switch imminent?
    # Bregman 1994: onset boundaries and grouping changes trigger switches
    f1 = torch.sigmoid(
        0.40 * m1 + 0.30 * p1 + 0.30 * e0
    )

    return f0, f1
