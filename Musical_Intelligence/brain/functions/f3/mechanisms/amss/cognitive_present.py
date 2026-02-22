"""AMSS P-Layer -- Cognitive Present (2D).

Two present-processing dimensions for stream selection and competition:

  P0: attended_stream      -- Currently attended stream identity [0, 1]
  P1: competition_state    -- Inter-stream competition intensity [0, 1]

H3 consumed: none (pure E/M integration).

P0 combines stream coherence (M0) with the attention gate (E4) to determine
which stream is currently foregrounded. High P0 = strong attentional lock.

P1 captures competition: high segregation depth (M1) combined with low
attended stream (1-P0) indicates strong rivalry between streams.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/amss/
Alain 2007: attended vs ignored streams show different ERP signatures.
Elhilali 2009: bistability arises from competition between stream percepts.
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from E/M outputs.

    Args:
        e_outputs: ``(E0, E1, E2, E3, E4)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    _e0, _e1, _e2, _e3, e4 = e_outputs
    m0, m1 = m_outputs

    # P0: Attended stream -- attentional selection of foregrounded stream
    # Alain 2007: attention modulates ORN, confirming top-down stream selection
    p0 = torch.sigmoid(
        0.50 * m0 + 0.50 * e4
    )

    # P1: Competition state -- rivalry between concurrent streams
    # Elhilali 2009: competition drives bistability in stream perception
    p1 = torch.sigmoid(
        0.50 * m1 + 0.50 * (1.0 - p0)
    )

    return p0, p1
