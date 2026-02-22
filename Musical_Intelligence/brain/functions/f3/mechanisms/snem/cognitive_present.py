"""SNEM P-Layer — Cognitive Present (3D).

Three present-processing dimensions for entrainment and selective gain:

  P0: beat_locked_activity   — Beat-locked cortical activity [0, 1]
  P1: entrainment_strength   — Overall entrainment quality [0, 1]
  P2: selective_gain         — Attention gain from entrainment x coupling [0, 1]

H3 consumed:
    (10, 16, 14, 2)  flux periodicity H16 L2   — beat periodicity 1s (reused)
    (7, 16, 1, 2)    amplitude mean H16 L2     — beat salience context (reused)

R3 consumed:
    [7]  amplitude — instant amplitude for beat-locked modulation
    [10] spectral_flux — instant flux for onset gating

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/snem/SNEM-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_FLUX_PERIOD_1S = (10, 16, 14, 2)
_AMP_MEAN_1S = (7, 16, 1, 2)

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

    flux_period_1s = h3_features[_FLUX_PERIOD_1S]
    amp_mean_1s = h3_features[_AMP_MEAN_1S]

    # P0: Beat-locked activity — cortical tracking of beat
    # Nozaradan 2011: SS-EP at beat frequency in auditory cortex
    p0 = torch.sigmoid(
        0.40 * e0 + 0.30 * m0 + 0.30 * flux_period_1s
    )

    # P1: Entrainment strength — quality of oscillatory lock
    # Large 2008: dynamic attending theory — stronger lock = better attending
    p1 = torch.sigmoid(
        0.40 * m0 + 0.30 * e0 + 0.30 * amp_mean_1s
    )

    # P2: Selective gain — attention enhancement at expected positions
    # Nozaradan 2018: selective enhancement at beat frequency
    # Reuses E2 pattern: entrainment x coupling interaction
    p2 = torch.sigmoid(
        0.35 * e0 * e1 + 0.35 * flux_period_1s
        + 0.30 * amp_mean_1s
    )

    return p0, p1, p2
