"""AMSS M-Layer -- Temporal Integration (2D).

Two composite signals integrating E-layer stream features:

  M0: stream_coherence     -- Overall coherence of the attended stream [0, 1]
  M1: segregation_depth    -- Depth of segregation between competing streams [0, 1]

H3 consumed: none (pure E-layer integration).

M0 combines harmonic (E1), spectral (E2), and temporal (E3) stream cues
into a single coherence index. High coherence = strong, well-defined stream.

M1 captures the depth of segregation: attention gate (E4) modulates the
average of spectral and temporal streams, combined with onset tracking (E0)
for boundary-driven segregation.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/amss/
Elhilali 2009: stream coherence predicts perceptual segregation.
Bregman 1994: multiple cues combine for stream formation.
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_temporal_integration(
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from E-layer outputs.

    Args:
        e_outputs: ``(E0, E1, E2, E3, E4)`` each ``(B, T)``.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    e0, e1, e2, e3, e4 = e_outputs

    # M0: Stream coherence -- harmonic + spectral + temporal cues
    # Elhilali 2009: coherence across frequency channels predicts streaming
    m0 = torch.sigmoid(
        0.40 * e1 + 0.35 * e2 + 0.25 * e3
    )

    # M1: Segregation depth -- attention-gated stream separation
    # Elhilali 2009: attention modulates competition between streams
    # Bregman 1994: onset boundaries reinforce segregation
    m1 = torch.sigmoid(
        0.60 * e4 * (e2 + e3) / 2.0 + 0.40 * e0
    )

    return m0, m1
