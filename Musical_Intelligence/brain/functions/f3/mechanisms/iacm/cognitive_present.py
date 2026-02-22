"""IACM P-Layer — Cognitive Present (2D).

Two present-processing dimensions for inharmonicity attention:

  P0: p3a_capture        — Pre-attentive novelty response strength [0, 1]
  P1: spectral_encoding  — Current spectral scene encoding [0, 1]

H3 consumed:
    (16, 3, 20, 2)  flatness entropy H3 L2       — spectral unpredictability 100ms
    (5, 3, 0, 2)    periodicity value H3 L2      — scene coherence 100ms
    (5, 3, 2, 2)    periodicity std H3 L2        — scene variability 100ms
    (14, 3, 0, 2)   tonalness value H3 L2        — tonalness 100ms (reused)

R3 consumed: (none)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/iacm/IACM-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_FLATNESS_ENTROPY = (16, 3, 20, 2)
_PERIODICITY_VAL = (5, 3, 0, 2)
_PERIODICITY_STD = (5, 3, 2, 2)
_TONALNESS_H3 = (14, 3, 0, 2)


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from H3 + E/M outputs.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    e0, _e1, _e2 = e_outputs
    (m0, _m1, _m2) = m_outputs

    flatness_entropy = h3_features[_FLATNESS_ENTROPY]
    periodicity_val = h3_features[_PERIODICITY_VAL]
    periodicity_std = h3_features[_PERIODICITY_STD]
    tonalness_100ms = h3_features[_TONALNESS_H3]

    # P0: P3a capture — pre-attentive novelty response
    # Albouy 2017: MMN/P3a for pitch deviance; Koelsch 2019: entropy salience
    p0 = torch.sigmoid(
        0.40 * m0 + 0.30 * e0 + 0.30 * flatness_entropy
    )

    # P1: Spectral encoding — current scene spectral state
    # Herrmann 2015: ASSR coherence indexes scene regularity
    p1 = torch.sigmoid(
        0.40 * periodicity_val + 0.30 * periodicity_std
        + 0.30 * tonalness_100ms
    )

    return p0, p1
