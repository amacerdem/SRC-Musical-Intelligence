"""RPEM E-Layer -- Extraction (4D).

Four reward prediction error features:

  f01: surprise_signal    -- Information content / surprise magnitude [0, 1]
  f02: liking_signal      -- Real-time hedonic valence [0, 1]
  f03: positive_rpe       -- Positive RPE (surprise x liked) [0, 1]
  f04: negative_rpe       -- Negative RPE (surprise x disliked) [0, 1]

H3 consumed (tuples 0-7):
    (21, 4, 20, 0)  spectral_flux entropy H4 L0     -- spectral entropy 125ms
    (21, 3, 0, 2)   spectral_flux value H3 L2       -- spectral change 100ms
    (24, 3, 0, 2)   concentration value H3 L2       -- concentration change 100ms
    (4, 16, 1, 2)   sensory_pleasantness mean H16 L2 -- mean pleasantness 1s
    (0, 3, 0, 2)    roughness value H3 L2           -- roughness 100ms
    (0, 3, 8, 0)    roughness velocity H3 L0        -- roughness velocity 100ms
    (33, 3, 0, 2)   x_l4l5[0] value H3 L2          -- RPE coupling 100ms
    (25, 16, 20, 2) x_l0l5[0] entropy H16 L2       -- prediction entropy 1s

R3 consumed:
    [0]      roughness                  -- f02: inverse consonance
    [4]      sensory_pleasantness       -- f02: hedonic valence
    [8]      loudness (velocity_D)      -- salience encoding
    [10]     spectral_flux (onset_str)  -- musical deviation
    [21]     spectral_change            -- surprise proxy
    [24]     concentration_change       -- uncertainty signal
    [25:33]  x_l0l5                     -- prediction coupling
    [33:41]  x_l4l5                     -- RPE coupling

Gold 2023: VS shows surprise x liking crossover (d = 1.07).
Cheung 2019: uncertainty x surprise jointly predict pleasure.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 0-7 from demand spec) ----------------------------------
_SPEC_ENTROPY_125MS = (21, 4, 20, 0)     # #0: spectral entropy 125ms
_SPEC_CHANGE_100MS = (21, 3, 0, 2)       # #1: spectral change 100ms
_CONC_CHANGE_100MS = (24, 3, 0, 2)       # #2: concentration change 100ms
_PLEAS_MEAN_1S = (4, 16, 1, 2)           # #3: mean pleasantness 1s
_ROUGH_VAL_100MS = (0, 3, 0, 2)          # #4: roughness 100ms
_ROUGH_VEL_100MS = (0, 3, 8, 0)          # #5: roughness velocity 100ms
_RPE_COUPLING_100MS = (33, 3, 0, 2)      # #6: RPE coupling 100ms
_PRED_ENTROPY_1S = (25, 16, 20, 2)       # #7: prediction entropy 1s

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 8                # velocity_D
_ONSET_STRENGTH = 10         # spectral_flux -> onset_strength
_SPECTRAL_CHANGE = 21        # spectral_flux -> spectral_change
_CONCENTRATION_CHANGE = 24
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """E-layer: 4D extraction from H3/R3 features.

    Implements the reward prediction error crossover pattern (Gold 2023).
    Two primary signals (surprise, liking) are combined multiplicatively
    to produce signed positive/negative RPE.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``.
    """
    # -- H3 features --
    spec_entropy_125ms = h3_features[_SPEC_ENTROPY_125MS]
    spec_change_100ms = h3_features[_SPEC_CHANGE_100MS]
    conc_change_100ms = h3_features[_CONC_CHANGE_100MS]
    pleas_mean_1s = h3_features[_PLEAS_MEAN_1S]
    rough_val_100ms = h3_features[_ROUGH_VAL_100MS]
    rough_vel_100ms = h3_features[_ROUGH_VEL_100MS]
    rpe_coupling_100ms = h3_features[_RPE_COUPLING_100MS]
    pred_entropy_1s = h3_features[_PRED_ENTROPY_1S]

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]                     # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]       # (B, T)

    # -- f01: Surprise signal --
    # Information content: how unexpected the current musical event is.
    # Gold 2023: R STG reflects surprise magnitude (d = 1.22).
    # sigma(0.35 * spectral_entropy_125ms + 0.20 * spectral_change_100ms
    #        + 0.15 * concentration_100ms)
    # Remaining weight goes to R3 instantaneous features for completeness.
    f01 = torch.sigmoid(
        0.35 * spec_entropy_125ms
        + 0.20 * spec_change_100ms
        + 0.15 * conc_change_100ms
        + 0.30 * r3_features[..., _SPECTRAL_CHANGE]
    )

    # -- f02: Liking signal --
    # Real-time reward valence / hedonic value.
    # sigma(0.35 * mean_pleasantness_1s + 0.25 * (1 - roughness_100ms)
    #        + remaining R3 hedonic)
    # Gold 2023: liking interacts with surprise to produce RPE crossover in VS.
    f02 = torch.sigmoid(
        0.35 * pleas_mean_1s
        + 0.25 * (1.0 - rough_val_100ms)
        + 0.40 * pleasantness
    )

    # -- f03: Positive RPE --
    # Surprise x Liked: better-than-expected musical events.
    # sigma(0.50 * f01 * f02 + 0.20 * rpe_coupling_100ms + remaining)
    # Gold 2023: VS shows increased BOLD for surprising liked stimuli (d = 1.07).
    f03 = torch.sigmoid(
        0.50 * f01 * f02
        + 0.20 * rpe_coupling_100ms
        + 0.30 * pleasantness * spec_change_100ms
    )

    # -- f04: Negative RPE --
    # Surprise x Disliked: worse-than-expected events.
    # sigma(0.50 * f01 * (1 - f02) + 0.30 * roughness_velocity_100ms
    #        + 0.20 * prediction_entropy_1s)
    # Gold 2023: VS shows decreased BOLD for surprising disliked stimuli.
    f04 = torch.sigmoid(
        0.50 * f01 * (1.0 - f02)
        + 0.30 * rough_vel_100ms
        + 0.20 * pred_entropy_1s
    )

    return f01, f02, f03, f04
