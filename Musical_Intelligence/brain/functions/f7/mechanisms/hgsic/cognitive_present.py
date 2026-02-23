"""HGSIC P-Layer -- Cognitive Present (3D).

Three present-processing dimensions for groove state:

  P0: pstg_activation    -- Posterior STG activation for groove processing
  P1: motor_preparation  -- Premotor cortex preparation for movement
  P2: onset_sync         -- Onset synchronization quality

Uses E/M outputs + PEOM relay -- no additional H3 dependencies for P-layer.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hgsic/HGSIC-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from E/M outputs + PEOM relay.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        relay_outputs: ``{"PEOM": (B, T, 11)}``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    f01, f02, f03 = e_outputs
    m0, m1 = m_outputs

    B, T = r3_features.shape[:2]
    device = r3_features.device
    zero = torch.zeros(B, T, device=device)

    # PEOM relay context for present processing
    peom = relay_outputs.get("PEOM")
    if peom is not None and peom.dim() >= 2:
        peom_period_lock = peom[:, :, 0]
        peom_next_beat = peom[:, :, 2] if peom.shape[-1] > 2 else zero
    else:
        peom_period_lock = zero
        peom_next_beat = zero

    # P0: pSTG Activation -- posterior STG groove processing
    # Janata 2012: STG involved in auditory analysis for groove
    p0 = torch.sigmoid(
        0.30 * m0
        + 0.25 * f01
        + 0.25 * f02
        + 0.20 * m1
    )

    # P1: Motor Preparation -- premotor cortex for movement urge
    # Janata 2012: PMC activation correlates with groove desire
    p1 = torch.sigmoid(
        0.30 * f03
        + 0.25 * m1
        + 0.25 * m0
        + 0.20 * peom_period_lock
    )

    # P2: Onset Sync -- onset synchronization quality
    # Witek 2014: groove requires beat-locked onset alignment
    p2 = torch.sigmoid(
        0.30 * f01
        + 0.25 * peom_period_lock
        + 0.25 * peom_next_beat
        + 0.20 * f02
    )

    return p0, p1, p2
