"""CSG E-Layer — Extraction (3D).

Three explicit features modeling the consonance-salience gradient:

  E0: salience_activation   — ACC/AI activation from dissonance [0, 1]
  E1: sensory_evidence      — Heschl's gyrus processing load [0, 1]
  E2: consonance_valence    — Consonance-valence mapping [-1, 1] (tanh)

H3 consumed:
    (0, 0, 0, 2)    roughness value H0 L2       — instant roughness
    (4, 3, 0, 2)    sensory_pleas value H3 L2   — consonance proxy 100ms
    (10, 3, 13, 2)  loudness entropy H3 L2      — loudness entropy
    (1, 3, 0, 2)    sethares value H3 L2        — dissonance confirmation
    (0, 3, 2, 2)    roughness std H3 L2         — roughness variability
    (4, 3, 8, 2)    sensory_pleas velocity H3 L2 — pleasantness change rate
    (4, 16, 1, 2)   sensory_pleas mean H16 L2   — sustained pleasantness

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/csg/CSG-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_H0 = (0, 0, 0, 2)
_PLEAS_H3 = (4, 3, 0, 2)
_LOUD_ENTROPY = (10, 3, 13, 2)
_SETHARES_H3 = (1, 3, 0, 2)
_ROUGHNESS_STD = (0, 3, 2, 2)
_PLEAS_VEL = (4, 3, 8, 2)
_PLEAS_MEAN_1S = (4, 16, 1, 2)


def _wsig(x: Tensor) -> Tensor:
    """Wide sigmoid — full [0, 1] dynamic range (gain=5, center=0.35)."""
    return (1.0 + torch.exp(-5.0 * (x - 0.35))).reciprocal()


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``. E2 is tanh-valued ``[-1, 1]``.
    """
    roughness_h0 = h3_features[_ROUGHNESS_H0]
    pleas_h3 = h3_features[_PLEAS_H3]
    loud_entropy = h3_features[_LOUD_ENTROPY]
    sethares_h3 = h3_features[_SETHARES_H3]
    roughness_std = h3_features[_ROUGHNESS_STD]
    pleas_vel = h3_features[_PLEAS_VEL]
    pleas_mean_1s = h3_features[_PLEAS_MEAN_1S]

    # Consonance/dissonance/ambiguity from H3 pleasantness
    dissonance = 1.0 - pleas_h3
    ambiguity = 1.0 - torch.abs(pleas_h3 - 0.5) * 2

    # E0: Salience activation — ACC/AI driven by dissonance
    # Bravo 2017: strong dissonance -> ACC/AI, d=5.16
    e0 = _wsig(
        0.40 * dissonance + 0.35 * roughness_h0 + 0.25 * loud_entropy
    )

    # E1: Sensory evidence — Heschl's gyrus intermediate processing
    # Bravo 2017: intermediate dissonance -> HG load, d=1.9
    e1 = _wsig(
        0.40 * ambiguity + 0.35 * sethares_h3 + 0.25 * roughness_std
    )

    # E2: Consonance-valence mapping [-1, 1]
    # Bravo 2017: linear consonance-valence trend, d=3.31
    # Center pleasantness around 0.5 → dissonant=negative, consonant=positive
    centered_pleas = (pleas_mean_1s - 0.5) * 2.0
    e2 = torch.tanh(
        0.35 * pleas_vel + 0.65 * centered_pleas
    )

    return e0, e1, e2
