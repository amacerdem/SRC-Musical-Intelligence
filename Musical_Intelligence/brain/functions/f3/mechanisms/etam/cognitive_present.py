"""ETAM P-Layer -- Cognitive Present (2D).

Present-processing envelope tracking and stream separation:
  P0: envelope_tracking   (current tempo envelope following accuracy)
  P1: stream_separation   (current ability to segregate auditory streams)

H3 demands consumed:
  x_l4l5:  (33,16,0,2)   -- cross-stream value 1s (tracking)

Dependencies on E-layer and M-layer:
  E0: early_window        -- transient detection for tracking
  E2: late_window         -- cognitive coupling for separation
  E3: instrument_asymmetry -- timbral cues for stream segregation
  M0: attention_gain      -- entrainment-modulated attention

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/etam/
London 2012: metric hierarchy creates graded attentional weights.
Grahn & Rowe 2012: STG tracks tempo envelope in real time.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CROSS_STREAM_VAL_1S = (33, 16, 0, 2)  # cross-stream value 1s (integration)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: envelope tracking and stream separation.

    P0 models real-time envelope tracking: attention gain (M0) focuses
    processing on the tempo envelope, early window (E0) provides transient
    cues, and cross-stream coupling indexes multi-stream coherence.

    P1 models stream separation: instrument asymmetry (E3) provides
    timbral cues for segregation, late window (E2) provides cognitive
    grouping context, and cross-stream coupling provides inter-stream
    structure information.

    London 2012: metric attention is hierarchically organized.
    Grahn & Rowe 2012: STG tracks tempo envelope parametrically.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, _e1, e2, e3 = e
    m0, _m1 = m

    cross_stream_val_1s = h3_features[_CROSS_STREAM_VAL_1S]

    # -- P0: Envelope Tracking --
    # Current accuracy of tempo envelope following. Attention gain (M0)
    # modulates tracking quality, early window (E0) provides onset/transient
    # alignment cues, and cross-stream coupling indexes how well multiple
    # streams maintain coherent tempo.
    # Grahn 2012: STG parametrically tracks beat strength.
    p0 = torch.sigmoid(
        0.40 * m0
        + 0.30 * e0
        + 0.30 * cross_stream_val_1s
    )

    # -- P1: Stream Separation --
    # Current ability to segregate concurrent auditory streams. Instrument
    # asymmetry (E3) provides timbral distinctiveness cues, late window (E2)
    # captures cognitive grouping at bar timescale, and cross-stream coupling
    # reflects structural relationships between streams.
    # London 2012: metric hierarchy supports perceptual grouping.
    p1 = torch.sigmoid(
        0.40 * e3
        + 0.30 * e2
        + 0.30 * cross_stream_val_1s
    )

    return p0, p1
