"""IACM E-Layer — Extraction (3D).

Three explicit features modeling inharmonicity-driven attention capture:

  E0: inharmonic_capture   — Inharmonicity-driven novelty detection [0, 1]
  E1: object_segregation   — Auditory scene object segregation [0, 1]
  E2: precision_weighting  — Temporal precision of tonal regularity [0, 1]

H3 consumed:
    (14, 3, 0, 2)   tonalness value H3 L2          — inharmonicity context 100ms
    (16, 0, 0, 2)   spectral_flatness value H0 L2  — noise proxy 25ms
    (0, 3, 20, 2)   roughness entropy H3 L2        — dissonance variability
    (14, 0, 0, 2)   tonalness value H0 L2          — instant tonal/noisy 25ms
    (5, 3, 0, 2)    periodicity value H3 L2        — scene coherence 100ms
    (5, 3, 2, 2)    periodicity std H3 L2          — scene variability 100ms
    (25, 3, 0, 2)   coupling value H3 L2           — scene binding 100ms
    (14, 4, 14, 2)  tonalness periodicity H4 L2    — tonal rhythm 125ms
    (14, 16, 14, 2) tonalness periodicity H16 L2   — long tonal pattern 1s
    (25, 16, 21, 2) coupling zero-crossings H16 L2 — phase resets 1s

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/iacm/IACM-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_TONALNESS_H3 = (14, 3, 0, 2)
_FLATNESS_H0 = (16, 0, 0, 2)
_ROUGHNESS_ENTROPY = (0, 3, 20, 2)
_TONALNESS_H0 = (14, 0, 0, 2)
_PERIODICITY_VAL = (5, 3, 0, 2)
_PERIODICITY_STD = (5, 3, 2, 2)
_COUPLING_VAL = (25, 3, 0, 2)
_TONALNESS_PERIOD_125 = (14, 4, 14, 2)
_TONALNESS_PERIOD_1S = (14, 16, 14, 2)
_COUPLING_ZC_1S = (25, 16, 21, 2)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    tonalness_100ms = h3_features[_TONALNESS_H3]
    flatness_25ms = h3_features[_FLATNESS_H0]
    roughness_entropy = h3_features[_ROUGHNESS_ENTROPY]
    tonalness_25ms = h3_features[_TONALNESS_H0]
    periodicity_val = h3_features[_PERIODICITY_VAL]
    periodicity_std = h3_features[_PERIODICITY_STD]
    coupling_val = h3_features[_COUPLING_VAL]
    tonalness_period_125 = h3_features[_TONALNESS_PERIOD_125]
    tonalness_period_1s = h3_features[_TONALNESS_PERIOD_1S]
    coupling_zc_1s = h3_features[_COUPLING_ZC_1S]

    # E0: Inharmonic capture — novelty detection from spectral irregularity
    # Albouy 2017: inharmonicity breaks regularity -> pre-attentive MMN
    e0 = torch.sigmoid(
        0.40 * (1.0 - tonalness_100ms) + 0.25 * flatness_25ms
        + 0.20 * roughness_entropy + 0.15 * (1.0 - tonalness_25ms)
    )

    # E1: Object segregation — auditory scene coherence
    # Herrmann 2015: ASSR modulated by spectral regularity
    e1 = torch.sigmoid(
        0.35 * periodicity_val + 0.25 * periodicity_std
        + 0.25 * coupling_val + 0.15 * tonalness_period_125
    )

    # E2: Precision weighting — temporal regularity of tonal patterns
    # Herrmann 2015 + Zatorre 2007: cross-scale tonal rhythm binding
    e2 = torch.sigmoid(
        0.40 * tonalness_period_125 + 0.30 * tonalness_period_1s
        + 0.30 * coupling_zc_1s
    )

    return e0, e1, e2
