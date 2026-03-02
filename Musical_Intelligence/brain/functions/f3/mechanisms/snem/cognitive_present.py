"""SNEM P-Layer — Cognitive Present (3D).

Three present-processing dimensions for entrainment and selective gain:

  P0: beat_locked_activity   — Beat-locked cortical activity [0, 1]
  P1: entrainment_strength   — Overall entrainment quality [0, 1]
  P2: selective_gain         — Attention gain from entrainment x coupling [0, 1]

H3 consumed (reuses E-layer demands):
    (8, 20, 14, 0)   loudness periodicity H20 L0 — beat periodicity at 5s
    (11, 20, 14, 0)  onset periodicity H20 L0    — onset periodicity at 5s

R3 consumed:
    [7]  amplitude — instant amplitude for beat-locked modulation
    [10] spectral_flux — instant flux for onset gating

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/snem/SNEM-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (reused from extraction) ---------------------------------------
_LOUD_PERIOD_H20 = (8, 20, 14, 0)       # beat periodicity at 5s
_ONSET_PERIOD_H20 = (11, 20, 14, 0)     # onset periodicity at 5s

# -- R3 indices ----------------------------------------------------------------
_AMPLITUDE = 7
_SPECTRAL_FLUX = 10


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3/R3 + E/M outputs.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    e0, e1, _e2 = e_outputs
    (m0, _m1, _m2) = m_outputs

    loud_period_h20 = h3_features[_LOUD_PERIOD_H20]
    onset_period_h20 = h3_features[_ONSET_PERIOD_H20]

    # P0: Beat-locked activity — cortical tracking of beat
    # Nozaradan 2011: SS-EP at beat frequency in auditory cortex.
    # Loudness periodicity at 5s provides multi-cycle beat context.
    p0 = torch.sigmoid(
        0.40 * e0 + 0.30 * m0 + 0.30 * loud_period_h20
    )

    # P1: Entrainment strength — quality of oscillatory lock
    # Large 2008: dynamic attending theory — stronger lock = better attending.
    # Onset periodicity at 5s reflects sustained regularity of attack timing.
    p1 = torch.sigmoid(
        0.40 * m0 + 0.30 * e0 + 0.30 * onset_period_h20
    )

    # P2: Selective gain — attention enhancement at expected positions
    # Nozaradan 2018: selective enhancement at beat frequency.
    # Entrainment x coupling interaction gated by periodicity context.
    p2 = torch.sigmoid(
        0.35 * e0 * e1 + 0.35 * loud_period_h20
        + 0.30 * onset_period_h20
    )

    return p0, p1, p2
