"""CHPI M-Layer -- Temporal Integration (2D).

Cross-modal temporal features for harmonic context:
  M0: visual_motor_lead      (anticipatory signal from cross-modal timing)
  M1: harmonic_surprise_mod  (surprise modulation from harmonic context)

H3 demands consumed:
  roughness:                (0,8,1,0)
  sensory_pleasantness:     (4,16,1,0)
  onset_strength:           (10,3,14,2)
  tonalness:                (14,8,1,0)
  chroma_C:                 (25,8,1,0)
  distribution_concentration: (23,3,8,2)

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/chpi/
Musacchia 2007: cross-modal training enhances temporal encoding in brainstem.
Vuust 2022: predictive processing integrates timing across modalities.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ROUGHNESS_H8_MEAN = (0, 8, 1, 0)
_CONSONANCE_H16_MEAN = (4, 16, 1, 0)
_ONSET_H3_PERIOD = (10, 3, 14, 2)
_TONALNESS_H8_MEAN = (14, 8, 1, 0)
_CHROMA_C_H8_MEAN = (25, 8, 1, 0)
_DIST_CONC_H3_VEL = (23, 3, 8, 2)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: cross-modal temporal features for harmonic context.

    M0 models anticipatory signals: cross-modal timing provides advance
    cues for harmonic events via periodic onset structure and tonal context.
    M1 models surprise modulation: sustained harmonic context modulates
    the magnitude of harmonic surprise responses.

    Musacchia et al. 2007: musicians show enhanced cross-modal brainstem
    encoding with earlier ABR latencies (p<0.05).
    Vuust et al. 2022: predictive processing framework for cross-modal
    temporal integration.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1 = e

    roughness_mean_500ms = h3_features[_ROUGHNESS_H8_MEAN]
    consonance_mean_1s = h3_features[_CONSONANCE_H16_MEAN]
    onset_period_100ms = h3_features[_ONSET_H3_PERIOD]
    tonalness_mean_500ms = h3_features[_TONALNESS_H8_MEAN]
    chroma_mean_500ms = h3_features[_CHROMA_C_H8_MEAN]
    dist_conc_vel = h3_features[_DIST_CONC_H3_VEL]

    # -- M0: Visual-Motor Lead --
    # Anticipatory signal from cross-modal temporal cues. Periodic onsets
    # provide motor-auditory timing predictions, tonal context gives
    # harmonic expectation, chroma provides tonal identity.
    # Musacchia 2007: cross-modal training enhances temporal encoding.
    m0 = torch.sigmoid(
        0.30 * e0
        + 0.25 * onset_period_100ms
        + 0.25 * tonalness_mean_500ms
        + 0.20 * chroma_mean_500ms
    )

    # -- M1: Harmonic Surprise Modulation --
    # Sustained harmonic context modulates surprise magnitude. High
    # consonance context + low roughness = strong harmonic expectation,
    # so deviations produce larger surprise. Voice-leading parsimony
    # and spectral concentration velocity contribute.
    # Koelsch 2005: harmonic context modulates ERAN amplitude.
    m1 = torch.sigmoid(
        0.30 * e1
        + 0.25 * consonance_mean_1s
        + 0.25 * (1.0 - roughness_mean_500ms)
        + 0.20 * dist_conc_vel
    )

    return m0, m1
