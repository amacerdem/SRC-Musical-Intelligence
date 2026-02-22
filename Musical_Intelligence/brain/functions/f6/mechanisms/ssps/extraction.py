"""SSPS E-Layer -- Extraction (4D + saddle_value intermediate).

Saddle-shaped preference surface features:
  f01: ic_value            -- Current information content (surprise) level [0, 1]
  f02: entropy_value       -- Current entropy (uncertainty) level [0, 1]
  f03: saddle_position     -- Position on saddle-shaped preference surface [0, 1]
  f04: peak_proximity      -- Proximity to optimal preference zone peak [0, 1]

The E-layer extracts four explicit features that characterise the listener's
position on the saddle-shaped preference surface.  The key insight is that
musical preference is not a simple inverted-U of complexity -- it follows a
saddle-shaped surface in IC x entropy space with two distinct optimal zones
(Cheung et al. 2019).

Zone 1 (high entropy + low IC): Predictable events in uncertain contexts
produce pleasure because they resolve uncertainty (Mencke et al. 2019).

Zone 2 (low entropy + medium IC): Moderate surprise in stable contexts
triggers the classic inverted-U (Berlyne 1971).

The saddle value is max(zone1, zone2), combined with coupling entropy to
assess the interaction strength.

Cheung et al. 2019: IC x entropy interaction beta = -0.124, p = 0.000246.
Gold et al. 2023: R^2 = 0.496 for full saddle model.

H3 demands consumed (14):
  ( 0) (21,  2,  0,  0)  spectral_change value H2 L0     -- IC at 75ms
  ( 1) (21,  8,  8,  0)  spectral_change velocity H8 L0  -- IC velocity 500ms
  ( 2) (21, 16, 20,  2)  spectral_change entropy H16 L2  -- IC entropy 1s
  ( 3) (24,  8,  2,  2)  concentration_change std H8 L2  -- conc. std 500ms
  ( 4) (24, 16, 20,  2)  concentration_change entropy H16 L2 -- conc. entropy 1s
  ( 5) ( 0,  8,  1,  2)  roughness mean H8 L2            -- mean rough 500ms
  ( 6) ( 0, 16,  2,  2)  roughness std H16 L2            -- rough var 1s
  ( 7) ( 4,  8,  1,  2)  pleasantness mean H8 L2         -- mean pleas 500ms
  ( 8) ( 4, 16, 15,  0)  pleasantness smoothness H16 L0  -- pleas smooth 1s
  ( 9) ( 8, 16,  1,  2)  loudness mean H16 L2            -- mean loud 1s
  (10) (33,  8,  1,  2)  x_l4l5 coupling mean H8 L2      -- coupling 500ms
  (11) (33, 16, 20,  2)  x_l4l5 coupling entropy H16 L2  -- coupling ent 1s
  (12) (25,  8,  2,  2)  x_l0l5 context std H8 L2        -- ctx var 500ms
  (13) (25, 16,  1,  2)  x_l0l5 context mean H16 L2      -- mean ctx 1s

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ssps/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_IC_VAL_H2 = (21, 2, 0, 0)             # spectral_change value H2 L0
_IC_VEL_H8 = (21, 8, 8, 0)             # spectral_change velocity H8 L0
_IC_ENT_H16 = (21, 16, 20, 2)          # spectral_change entropy H16 L2
_CONC_STD_H8 = (24, 8, 2, 2)           # concentration_change std H8 L2
_CONC_ENT_H16 = (24, 16, 20, 2)        # concentration_change entropy H16 L2
_ROUGH_MEAN_H8 = (0, 8, 1, 2)          # roughness mean H8 L2
_ROUGH_STD_H16 = (0, 16, 2, 2)         # roughness std H16 L2
_PLEAS_MEAN_H8 = (4, 8, 1, 2)          # pleasantness mean H8 L2
_PLEAS_SMOOTH_H16 = (4, 16, 15, 0)     # pleasantness smoothness H16 L0
_LOUD_MEAN_H16 = (8, 16, 1, 2)         # loudness mean H16 L2
_COUPLING_MEAN_H8 = (33, 8, 1, 2)      # x_l4l5 coupling mean H8 L2
_COUPLING_ENT_H16 = (33, 16, 20, 2)    # x_l4l5 coupling entropy H16 L2
_CTX_STD_H8 = (25, 8, 2, 2)            # x_l0l5 context std H8 L2
_CTX_MEAN_H16 = (25, 16, 1, 2)         # x_l0l5 context mean H16 L2


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D saddle-surface features + saddle_value intermediate.

    f01 (ic_value): Current information content (surprise) from fast IC at
    75ms and IC velocity at 500ms.  Cheung 2019: IC forms one axis of the
    saddle-shaped preference surface.

    f02 (entropy_value): Current entropy (uncertainty) combining concentration
    entropy, roughness variability, and context variability.  Cheung 2019:
    entropy forms the second axis of the saddle surface.

    f03 (saddle_position): Position on the preference surface via IC x entropy
    interaction with two optimal zones.  Cheung 2019: interaction beta=-0.124.

    f04 (peak_proximity): Proximity to an optimal zone peak.  Gold 2023:
    R^2=0.496 for the full saddle model.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"IUCP": (B, T, D), "RPEM": (B, T, D)}``.

    Returns:
        ``(f01, f02, f03, f04, saddle_value)`` each ``(B, T)``.
        The first four are output dimensions; saddle_value is an intermediate
        needed by the F-layer.
    """
    # -- H3 features --
    ic_75ms = h3_features[_IC_VAL_H2]                    # (B, T)
    ic_velocity_500ms = h3_features[_IC_VEL_H8]          # (B, T)
    concentration_entropy_1s = h3_features[_CONC_ENT_H16]  # (B, T)
    roughness_std_1s = h3_features[_ROUGH_STD_H16]       # (B, T)
    context_variability_500ms = h3_features[_CTX_STD_H8]  # (B, T)
    coupling_entropy_1s = h3_features[_COUPLING_ENT_H16]  # (B, T)
    pleasantness_smoothness_1s = h3_features[_PLEAS_SMOOTH_H16]  # (B, T)

    # -- f01: IC Value --
    # sigma(0.35 * ic_75ms + 0.30 * ic_velocity_500ms)
    # Remaining 0.35 from implicit bias via sigmoid centering.
    # Cheung 2019: IC (information content) forms one axis of the saddle.
    f01 = torch.sigmoid(
        0.35 * ic_75ms
        + 0.30 * ic_velocity_500ms
        + 0.35 * h3_features[_IC_ENT_H16]
    )

    # -- f02: Entropy Value --
    # sigma(0.35 * concentration_entropy_1s + 0.35 * roughness_std_1s
    #       + 0.30 * context_variability_500ms)
    # Cheung 2019: entropy forms the second axis of the saddle surface.
    f02 = torch.sigmoid(
        0.35 * concentration_entropy_1s
        + 0.35 * roughness_std_1s
        + 0.30 * context_variability_500ms
    )

    # -- Saddle surface computation --
    # Zone 1: high entropy + low IC (predictable events in uncertain contexts)
    zone1 = f02 * (1.0 - f01)
    # Zone 2: low entropy + medium IC (inverted-U in stable contexts)
    zone2 = (1.0 - f02) * 4.0 * f01 * (1.0 - f01)
    # Saddle value: element-wise max of two optimal zones
    saddle_value = torch.max(zone1, zone2)

    # -- f03: Saddle Position --
    # sigma(0.35 * saddle_value + 0.30 * coupling_entropy_1s
    #       + 0.35 * concentration_entropy_1s)
    # Cheung 2019: IC x entropy interaction beta = -0.124, p = 0.000246
    f03 = torch.sigmoid(
        0.35 * saddle_value
        + 0.30 * coupling_entropy_1s
        + 0.35 * concentration_entropy_1s
    )

    # -- f04: Peak Proximity --
    # sigma(0.35 * f03 + 0.30 * pleasantness_smoothness_1s
    #       + 0.35 * saddle_value)
    # Gold 2023: R^2 = 0.496 for full saddle model; VS shows RPE-like pattern
    f04 = torch.sigmoid(
        0.35 * f03
        + 0.30 * pleasantness_smoothness_1s
        + 0.35 * saddle_value
    )

    return f01, f02, f03, f04, saddle_value
