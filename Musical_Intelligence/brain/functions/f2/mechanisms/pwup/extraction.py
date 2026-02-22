"""PWUP E-Layer -- Extraction (2D).

Precision signals from raw R3 spectral features:
  E0: tonal_precision     (tonal certainty from key clarity + tonalness)
  E1: rhythmic_precision  (rhythmic certainty from onset strength + periodicity)

High precision = high confidence in the current tonal/rhythmic context.
In atonal music, E0 drops (key clarity ~0.5 vs tonal ~0.8, Quiroga-Martinez 2019).
In metrically irregular passages, E1 drops (onset periodicity low).

R3 direct reads:
  [4]  sensory_pleasantness  (consonance proxy for tonal grounding)
  [5]  periodicity           (tonal certainty / pitch periodicity)
  [11] onset_strength        (event salience for rhythmic precision)
  [14] tonalness             (key clarity proxy)

H3 demands consumed: none (pure R3 extraction).

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/pwup/
Friston 2005: precision = inverse variance of prediction error.
Quiroga-Martinez 2019: precision modulates MMN amplitude in music.
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor

# -- R3 indices (post-freeze 97D) --------------------------------------------
_SENSORY_PLEAS = 4       # sensory_pleasantness (A group, consonance proxy)
_PERIODICITY = 5         # periodicity (A group, tonal certainty)
_ONSET_STRENGTH = 11     # onset_strength (B group, event salience)
_TONALNESS = 14          # tonalness (C group, key clarity proxy)


def compute_extraction(
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: instantaneous precision signals.

    Tonal precision combines tonalness (key clarity) and consonance
    (sensory pleasantness). Rhythmic precision combines onset strength
    (event salience) and periodicity (regularity). Both are sigmoid-
    activated to [0, 1] where 1 = maximum precision (certainty).

    Quiroga-Martinez et al. 2019: precision context (tonal vs atonal)
    modulates MMN amplitude (d = 3, p < 0.001, N = 40).

    Args:
        r3_features: ``(B, T, 97)`` raw R3.

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    # -- R3 direct reads --
    consonance = r3_features[..., _SENSORY_PLEAS]    # (B, T)
    periodicity = r3_features[..., _PERIODICITY]      # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]         # (B, T)
    tonalness = r3_features[..., _TONALNESS]          # (B, T)

    # -- E0: Tonal Precision --
    # Tonalness (key clarity) is the dominant cue for tonal precision.
    # Consonance provides harmonic grounding. High tonalness + consonance
    # = high confidence in the harmonic context (Friston 2005 precision).
    e0 = torch.sigmoid(
        0.50 * tonalness
        + 0.30 * consonance
        + 0.20 * periodicity
    )

    # -- E1: Rhythmic Precision --
    # Onset strength detects salient events; periodicity measures regularity
    # of those events. Strong, regular onsets = high rhythmic precision.
    # Sedley et al. 2016: auditory cortex encodes precision for timing.
    e1 = torch.sigmoid(
        0.55 * onset
        + 0.45 * periodicity
    )

    return e0, e1
