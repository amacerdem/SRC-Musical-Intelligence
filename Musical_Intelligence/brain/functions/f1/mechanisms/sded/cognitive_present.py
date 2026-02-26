"""SDED P-Layer — Cognitive Present (3D).

Three present-processing dimensions for roughness at the sensory level:

  P0: roughness_detection   — Current roughness quality at sensory level
  P1: deviation_detection   — Roughness deviation from contextual mean
  P2: behavioral_response   — Behavioral response strength

H3 consumed:
    (0, 0, 0, 2)   roughness value H0 L2       — instant roughness (reused)
    (0, 3, 1, 2)   roughness mean H3 L2        — context (reused)
    (5, 0, 0, 2)   inharmonicity value H0 L2   — spectral clarity component
    (14, 3, 1, 0)  tonalness mean H3 L0        — pitch clarity (reused)
    (18, 0, 0, 2)  tristimulus1 value H0 L2    — F0 energy for roughness quality
    (17, 3, 0, 2)  spectral_auto value H3 L2   — cross-band coupling
    (2, 3, 1, 2)   helmholtz mean H3 L2        — consonance context

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/sded/SDED-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_H0 = (0, 0, 0, 2)
_ROUGHNESS_MEAN = (0, 3, 1, 2)
_INHARM_H0 = (5, 0, 0, 2)
_TONALNESS_MEAN = (14, 3, 1, 0)
_TRIST1_H0 = (18, 0, 0, 2)
_SPECTRAL_AUTO_H3 = (17, 3, 0, 2)
_HELMHOLTZ_MEAN = (2, 3, 1, 2)


def _wsig(x: Tensor) -> Tensor:
    """Wide sigmoid — full [0, 1] dynamic range (gain=5, center=0.35)."""
    return (1.0 + torch.exp(-5.0 * (x - 0.35))).reciprocal()


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3 + E/M outputs.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0,)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    _e0, _e1, _e2 = e_outputs
    (m0,) = m_outputs

    # H3 features
    roughness_h0 = h3_features[_ROUGHNESS_H0]
    roughness_mean = h3_features[_ROUGHNESS_MEAN]
    inharm_h0 = h3_features[_INHARM_H0]
    tonalness_mean = h3_features[_TONALNESS_MEAN]
    trist1_h0 = h3_features[_TRIST1_H0]
    spectral_auto_h3 = h3_features[_SPECTRAL_AUTO_H3]
    helmholtz_mean = h3_features[_HELMHOLTZ_MEAN]

    # P0: Roughness detection — spectral clarity modulates roughness quality
    # Spectral Clarity Index: (1-inharmonicity)*tristimulus1 + tonalness
    # Fishman 2001: A1 phase-locked oscillatory activity for roughness
    p0 = _wsig(
        0.30 * roughness_h0
        + 0.25 * (1.0 - inharm_h0) * trist1_h0
        + 0.25 * tonalness_mean
        + 0.20 * spectral_auto_h3
    )

    # P1: Deviation detection — roughness change from contextual mean
    # |instant - mean| captures mismatch magnitude (MMN substrate)
    p1 = torch.abs(roughness_h0 - roughness_mean)

    # P2: Behavioral response — detection + roughness + consonance context
    # Crespo-Bojorque 2018: behavioral accuracy varies with expertise
    p2 = _wsig(
        0.40 * m0 + 0.30 * p0 + 0.30 * helmholtz_mean
    )

    return p0, p1, p2
