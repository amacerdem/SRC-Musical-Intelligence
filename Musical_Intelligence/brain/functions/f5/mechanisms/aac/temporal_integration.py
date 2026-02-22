"""AAC I-Layer -- Temporal Integration (2D).

Two composite signals integrating E+A-layer ANS markers into higher-level
autonomic composites:

  I0: chills_intensity    -- Music-evoked chills intensity [0, 1]
  I1: ans_composite       -- Aggregate ANS activation composite [0, 1]

H3 consumed:
    No new H3 tuples -- I-layer integrates E+A-layer outputs with
    co-activation logic from Berntson 1991 autonomic space model.

Mathematical formulation:
    Chills = co-activation paradox: SCR up + HR down (Berntson quadrant)
    ANS_composite = weighted combination of all 5 ANS markers

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/aac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ea_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """I-layer: 2D temporal integration from E+A-layer outputs.

    The chills signal implements Berntson's co-activation model:
    SCR increase (sympathetic) + HR deceleration (parasympathetic)
    = co-activation quadrant = peak musical emotion.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        ea_outputs: ``(E0, E1, A0, A1, A2, A3, A4)`` each ``(B, T)``.

    Returns:
        ``(I0, I1)`` each ``(B, T)``.
    """
    e0, e1, a0, a1, a2, a3, a4 = ea_outputs

    # I0: Chills intensity -- Berntson 1991 co-activation quadrant
    # Grewe 2007: 77% of participants report chills; SCR peaks at onset
    # Blood-Zatorre 2001: chills recruit paralimbic circuitry
    # Co-activation: high SCR (sympathetic up) * (1 - HR) (parasympathetic)
    # The co-activation paradox: simultaneous SNS and PNS activation
    coactivation = a0 * (1.0 - a1)  # SCR up, HR down
    i0 = torch.sigmoid(
        0.40 * coactivation + 0.25 * e0 + 0.20 * a4
        + 0.15 * e1
    )

    # I1: ANS composite -- weighted aggregate of 5 ANS markers
    # Hodges 2010: converging psychophysiological measures
    # SCR(0.30) + HR(0.25) + RespR(0.20) + BVP(0.15) + Temp(0.10)
    i1 = torch.sigmoid(
        0.30 * a0 + 0.25 * a1 + 0.20 * a2
        + 0.15 * a3 + 0.10 * a4
    )

    return i0, i1
