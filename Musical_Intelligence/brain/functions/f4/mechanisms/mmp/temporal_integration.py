"""MMP P-Layer -- Temporal Integration (3D).

Three present-processing dimensions for preserved recognition in AD:

  P0: preserved_recognition   -- Current preserved recognition state [0, 1]
  P1: melodic_identification  -- Melody identification signal [0, 1]
  P2: familiarity             -- Familiarity response (warmth) [0, 1]

H3 consumed:
    (14, 20, 1, 0)   tonalness mean H20 L0             -- tonal stability (5s)
    (12, 24, 19, 0)  warmth stability H24 L0           -- long-term warmth (36s)
    (14, 24, 19, 0)  tonalness stability H24 L0        -- long-term tonal (36s)
    (10, 16, 0, 2)   loudness value H16 L2             -- current arousal (1s)
    (11, 16, 14, 2)  onset_strength periodicity H16 L2 -- rhythmic regularity (1s)

R3 consumed:
    [14] tonalness      -- melody tracking
    [41:49] x_l5l7      -- timbre warmth (nostalgia)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mmp/MMP-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_TONALNESS_MEAN_5S = (14, 20, 1, 0)
_WARMTH_STAB_36S = (12, 24, 19, 0)
_TONALNESS_STAB_36S = (14, 24, 19, 0)
_LOUDNESS_VAL_1S = (10, 16, 0, 2)
_ONSET_PERIOD_1S = (11, 16, 14, 2)

# -- R3 indices ----------------------------------------------------------------
_TONALNESS = 14
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    r_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D temporal integration from R-layer + H3/R3.

    Computes present-moment preserved recognition, melodic identification,
    and familiarity response.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        r_outputs: ``(R0, R1, R2)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    r0, r1, _r2 = r_outputs

    # H3 features
    tonalness_mean_5s = h3_features[_TONALNESS_MEAN_5S]
    warmth_stab_36s = h3_features[_WARMTH_STAB_36S]
    tonalness_stab_36s = h3_features[_TONALNESS_STAB_36S]
    loudness_val = h3_features[_LOUDNESS_VAL_1S]
    onset_period = h3_features[_ONSET_PERIOD_1S]

    # R3 features
    r3_tonalness = r3_features[..., _TONALNESS]
    r3_x_l5l7_mean = r3_features[..., _X_L5L7_START:_X_L5L7_END].mean(dim=-1)

    # Familiarity proxy: sustained warmth stability over 36s
    # No intermediate sigmoid — preserve dynamic range (BCH pattern)
    familiarity = warmth_stab_36s.clamp(0.0, 1.0)

    # Preservation factor from R-layer: reuse R0 as cortical pathway strength
    preservation_factor = r0

    # P0: Preserved recognition -- cortically-mediated recognition state
    # Scarratt 2025: familiar music activates auditory, motor, emotion, memory areas
    p0 = torch.sigmoid(
        0.40 * familiarity * preservation_factor
        + 0.30 * tonalness_stab_36s
        + 0.30 * onset_period
    )

    # P1: Melodic identification -- familiarity * tonalness
    # Sikka 2015: age-related shift to angular gyrus for recognition
    p1 = torch.sigmoid(
        0.40 * familiarity * r3_tonalness
        + 0.30 * tonalness_mean_5s
        + 0.30 * r1
    )

    # P2: Familiarity response -- warmth-familiarity interaction
    # El Haj 2012: music-evoked memories more specific in AD
    p2 = torch.sigmoid(
        0.40 * familiarity * r3_x_l5l7_mean
        + 0.30 * warmth_stab_36s
        + 0.30 * loudness_val
    )

    return p0, p1, p2
