"""SDED E-Layer — Extraction (3D).

Three explicit features modeling the neural-behavioral dissociation
of roughness detection (Crespo-Bojorque 2018):

  E0: early_detection      — Pre-attentive roughness detection (universal)
  E1: mmn_dissonance        — MMN amplitude for dissonant deviants
  E2: behavioral_accuracy   — Baseline behavioral discrimination (= E1)

H3 consumed:
    (0, 0, 0, 2)   roughness value H0 L2   — instant roughness at brainstem
    (0, 3, 1, 2)   roughness mean H3 L2    — sustained context for deviance
    (1, 0, 0, 2)   sethares value H0 L2    — psychoacoustic dissonance
    (2, 0, 0, 2)   helmholtz value H0 L2   — consonance (inverted)
    (14, 3, 1, 0)  tonalness mean H3 L0    — pitch clarity modulation

R3 consumed:
    [3] stumpf — tonal fusion (pitch salience proxy for MMN gating)

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/sded/SDED-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_H0 = (0, 0, 0, 2)
_ROUGHNESS_MEAN = (0, 3, 1, 2)
_SETHARES_H0 = (1, 0, 0, 2)
_HELMHOLTZ_H0 = (2, 0, 0, 2)
_TONALNESS_MEAN = (14, 3, 1, 0)

# -- R3 indices ----------------------------------------------------------------
_STUMPF = 3


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from R3/H3.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    # H3 features
    roughness_h0 = h3_features[_ROUGHNESS_H0]
    roughness_mean = h3_features[_ROUGHNESS_MEAN]
    sethares_h0 = h3_features[_SETHARES_H0]
    helmholtz_h0 = h3_features[_HELMHOLTZ_H0]
    tonalness_mean = h3_features[_TONALNESS_MEAN]

    # R3 direct
    stumpf = r3_features[:, :, _STUMPF]

    # E0: Early Detection (pre-attentive, universal)
    # Roughness * pitch clarity + psychoacoustic dissonance + (1 - consonance)
    # Crespo-Bojorque 2018: early MMN 152-258ms universal across expertise
    e0 = torch.sigmoid(
        0.40 * roughness_h0 * tonalness_mean
        + 0.30 * sethares_h0
        + 0.30 * (1.0 - helmholtz_h0)
    )

    # E1: MMN Dissonance (deviance-based, expertise-independent)
    # Detection * pitch salience + roughness deviation from context
    # Fishman 2001: A1 oscillatory activity correlates with dissonance
    roughness_dev = torch.abs(roughness_h0 - roughness_mean)
    e1 = torch.sigmoid(
        0.50 * e0 * stumpf
        + 0.50 * roughness_dev
    )

    # E2: Behavioral Accuracy (baseline = neural signal)
    # Neural-behavioral dissociation: without expertise modulation,
    # behavioral accuracy equals neural MMN signal
    e2 = e1

    return e0, e1, e2
