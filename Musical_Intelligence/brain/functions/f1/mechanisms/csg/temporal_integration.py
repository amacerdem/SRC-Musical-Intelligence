"""CSG M-Layer — Temporal Integration (3D).

Three composite signals integrating E-layer with temporal context:

  M0: salience_response       — Graded salience network response [0, 1]
  M1: rt_valence_judgment      — Inverted-U RT function [0, 1]
  M2: aesthetic_appreciation   — Consonance preference index [0, 1]

H3 consumed:
    (0, 16, 1, 2)  roughness mean H16 L2      — long-range roughness context
    (9, 3, 0, 2)   spectral_centroid H3 L2    — brightness for RT
    (4, 16, 1, 2)  sensory_pleas mean H16 L2  — sustained pleasantness (reused)
    (1, 3, 0, 2)   sethares value H3 L2       — psychoacoustic dissonance (reused)

R3 consumed:
    [4]  sensory_pleasantness — consonance proxy
    [12] warmth — spectral envelope quality

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/csg/CSG-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_MEAN_1S = (0, 16, 1, 2)
_CENTROID_H3 = (9, 3, 0, 2)
_PLEAS_MEAN_1S = (4, 16, 1, 2)
_SETHARES_H3 = (1, 3, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_PLEAS = 4
_WARMTH = 12


def compute_temporal_integration(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from E-layer + H3/R3.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``.
    """
    e0, e1, _e2 = e_outputs

    roughness_mean_1s = h3_features[_ROUGHNESS_MEAN_1S]
    centroid_h3 = h3_features[_CENTROID_H3]
    pleas_mean_1s = h3_features[_PLEAS_MEAN_1S]
    sethares_h3 = h3_features[_SETHARES_H3]

    consonance = r3_features[:, :, _PLEAS]
    warmth = r3_features[:, :, _WARMTH]
    ambiguity = 1.0 - torch.abs(consonance - 0.5) * 2

    # M0: Graded salience response
    # Bravo 2017: graded ACC/AI -> HG -> baseline across consonance levels
    # Diversified: reduced E0/E1 echo, added direct sethares dissonance
    m0 = torch.sigmoid(
        0.30 * e0 + 0.20 * e1
        + 0.25 * roughness_mean_1s + 0.25 * sethares_h3
    )

    # M1: RT valence judgment — inverted-U (intermediate = longest RT)
    # Bravo 2017: RT_intermediate=6792ms > RT_consonant=4333ms
    m1 = torch.sigmoid(
        0.40 * ambiguity + 0.30 * e1 + 0.30 * centroid_h3
    )

    # M2: Aesthetic appreciation — consonance preference
    # Sarasso 2019: consonant > dissonant, d=2.008
    m2 = torch.sigmoid(
        0.40 * consonance + 0.30 * pleas_mean_1s + 0.30 * warmth
    )

    return m0, m1, m2
