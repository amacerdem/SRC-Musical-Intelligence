"""MAA E-Layer — Extraction (2D).

Immediate perceptual features relevant to atonal appreciation:
  E0: complexity_tolerance  (dissonance × atonality → subjective complexity)
  E1: familiarity_index     (periodicity-driven tonal familiarity proxy)

R3 direct reads:
  roughness:            [0]  — dissonance level
  sensory_pleasantness: [4]  — consonance proxy
  periodicity:          [5]  — tonal certainty
  tonalness:            [14] — key clarity / atonality index
  tristimulus1-3:       [18:21] — harmonic structure richness
  spectral_change:      [21] — structural complexity

No H3 demands consumed at this layer (pure R3 extraction).

See Brattico 2013: aesthetic judgments engage STG for complexity processing.
See McDermott 2010: consonance/roughness perception as learned preference.
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEAS = 4
_PERIODICITY = 5
_TONALNESS = 14
_TRISTIMULUS_START = 18
_TRISTIMULUS_END = 21
_SPECTRAL_CHANGE = 21


def compute_extraction(
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: immediate perceptual features for atonal appreciation.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    roughness = r3_features[..., _ROUGHNESS]
    sensory_pleas = r3_features[..., _SENSORY_PLEAS]
    periodicity = r3_features[..., _PERIODICITY]
    tonalness = r3_features[..., _TONALNESS]
    trist_mean = r3_features[..., _TRISTIMULUS_START:_TRISTIMULUS_END].mean(
        dim=-1,
    )  # (B, T) — harmonic structure richness
    spectral_change = r3_features[..., _SPECTRAL_CHANGE]

    # -- E0: Complexity Tolerance --
    # Subjective complexity is driven by dissonance (roughness), lack of
    # tonal anchoring (1 - tonalness), and spectral change rate.
    # Berlyne 1971: collative variables (complexity, novelty) determine
    # arousal potential. Hargreaves 1984: inverted-U for complexity.
    # Tristimulus richness adds harmonic variety to complexity estimate.
    e0 = torch.sigmoid(
        0.30 * roughness
        + 0.25 * (1.0 - tonalness)
        + 0.25 * spectral_change
        + 0.20 * trist_mean
    )

    # -- E1: Familiarity Index --
    # Tonal familiarity proxy: periodicity (tonal certainty) and consonance
    # provide an immediate estimate of how "familiar" the harmonic language
    # sounds. Low values indicate atonal/unfamiliar territory.
    # McDermott 2010: consonance preference is partially learned.
    # Hargreaves 1984: familiarity shifts inverted-U peak rightward.
    e1 = torch.sigmoid(
        0.40 * periodicity
        + 0.35 * sensory_pleas
        + 0.25 * tonalness
    )

    return e0, e1
