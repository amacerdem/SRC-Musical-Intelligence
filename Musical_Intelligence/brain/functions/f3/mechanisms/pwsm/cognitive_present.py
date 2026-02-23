"""PWSM P-Layer -- Cognitive Present (2D).

Two present-processing dimensions for precision-weighted error state:

  P0: weighted_error     -- Current precision-weighted prediction error
  P1: precision_estimate -- Current precision estimate for context

H3 consumed:
    (37, 3, 17, 2)   pitch_height peaks H3 bidi   -- pitch event salience
    (11, 3, 0, 2)    onset_strength value H3 bidi  -- event strength

Upstream consumed:
    SNEM: entrainment_strength [1], beat_onset_pred [3]
    IACM: context dimensions for reliability

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/pwsm/PWSM-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PITCH_PEAKS_H3 = (37, 3, 17, 2)
_ONSET_H3 = (11, 3, 0, 2)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from H3 + E/M + upstream.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f19, f20, f21)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        upstream_outputs: ``{"SNEM": (B, T, 12), "IACM": (B, T, 11)}``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    f19, f20, f21 = e_outputs
    m0, m1 = m_outputs

    B = f19.shape[0]
    T = f19.shape[1] if f19.dim() > 1 else 1
    device = f19.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    pitch_peaks = h3_features.get(_PITCH_PEAKS_H3, zero)
    onset_h3 = h3_features.get(_ONSET_H3, zero)

    # Upstream context: SNEM entrainment and IACM reliability
    snem = upstream_outputs.get("SNEM")
    if snem is not None and snem.dim() >= 2 and snem.shape[-1] > 3:
        snem_entrainment = snem[:, :, 1]    # entrainment_strength
        snem_beat_pred = snem[:, :, 3]       # beat_onset_pred
    else:
        snem_entrainment = zero
        snem_beat_pred = zero

    iacm = upstream_outputs.get("IACM")
    if iacm is not None and iacm.dim() >= 2:
        iacm_context = iacm[:, :, 0]        # first dim as context proxy
    else:
        iacm_context = zero

    # P0: Weighted Error -- precision-weighted prediction error
    # Garrido 2009: MMN = precision * PE
    p0 = torch.sigmoid(
        0.25 * m0 * m1
        + 0.20 * pitch_peaks
        + 0.20 * onset_h3
        + 0.20 * snem_entrainment
        + 0.15 * (1.0 - f20)
    )

    # P1: Precision Estimate -- context-informed precision
    # Friston 2005: precision reflects context reliability
    p1 = torch.sigmoid(
        0.30 * m1
        + 0.25 * f21
        + 0.20 * iacm_context
        + 0.15 * snem_beat_pred
        + 0.10 * f19
    )

    return p0, p1
