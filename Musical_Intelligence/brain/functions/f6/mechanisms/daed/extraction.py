"""DAED E-Layer -- Extraction (4D).

Four dopaminergic features modeling anticipation-experience dissociation:

  f01: anticipatory_da      -- Caudate DA proxy (anticipatory ramp) [0, 1]
  f02: consummatory_da      -- NAcc DA proxy (consummatory burst) [0, 1]
  f03: wanting_index        -- Berridge incentive salience [0, 1]
  f04: liking_index         -- Berridge hedonic "liking" [0, 1]

H3 consumed (tuples 0-6 from demand spec):
    (8, 16, 8, 0)   loudness velocity H16 L0           -- anticipatory DA ramp
    (21, 4, 20, 0)   spectral_flux entropy H4 L0       -- prediction uncertainty
    (0, 8, 8, 0)    roughness velocity H8 L0           -- tension dynamics
    (4, 16, 1, 2)   sensory_pleasantness mean H16 L2   -- consummatory pleasure
    (8, 16, 1, 2)   loudness mean H16 L2               -- intensity baseline
    (25, 16, 20, 2) x_l0l5 entropy H16 L2              -- wanting uncertainty
    (4, 3, 0, 2)    sensory_pleasantness value H3 L2   -- immediate hedonic

R3 consumed:
    [0]      roughness               -- tension (inverse consonance)
    [4]      sensory_pleasantness    -- direct hedonic signal
    [7]      amplitude               -- energy build-up
    [8]      loudness                -- perceptual loudness
    [10]     spectral_flux           -- onset detection
    [21]     spectral_change         -- spectral dynamics
    [22]     energy_change           -- crescendo dynamics
    [25:33]  x_l0l5                  -- coupling for peak timing

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/daed/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 0-6 from demand spec) ----------------------------------
_LOUD_VEL_1S = (8, 16, 8, 0)           # #0: loudness velocity 1s -- anticipatory DA ramp
_SPEC_ENTROPY_125MS = (21, 4, 20, 0)   # #1: spectral uncertainty 125ms
_ROUGH_VEL_500MS = (0, 8, 8, 0)        # #2: roughness velocity 500ms -- tension
_PLEAS_MEAN_1S = (4, 16, 1, 2)         # #3: mean pleasantness 1s -- consummatory
_LOUD_MEAN_1S = (8, 16, 1, 2)          # #4: mean loudness 1s -- intensity baseline
_COUPLING_ENTROPY_1S = (25, 16, 20, 2) # #5: coupling entropy 1s -- wanting uncertainty
_PLEAS_VAL_100MS = (4, 3, 0, 2)        # #6: pleasantness 100ms -- immediate hedonic

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_LOUDNESS = 8
_ONSET_STRENGTH = 10
_SPECTRAL_CHANGE = 21
_ENERGY_CHANGE = 22
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """E-layer: 4D extraction from H3/R3 features.

    Implements the core dopaminergic dissociation from Salimpoor et al. (2011).
    Two parallel pathways:
        Anticipatory (f01, f03): loudness velocity, spectral uncertainty,
            roughness velocity -> caudate DA ramp 15-30s before peak.
        Consummatory (f02, f04): mean pleasantness, mean loudness -> NAcc DA
            burst at peak emotion moment.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``.
    """
    # -- H3 features --
    loud_vel_1s = h3_features[_LOUD_VEL_1S]
    spec_entropy_125ms = h3_features[_SPEC_ENTROPY_125MS]
    rough_vel_500ms = h3_features[_ROUGH_VEL_500MS]
    pleas_mean_1s = h3_features[_PLEAS_MEAN_1S]
    loud_mean_1s = h3_features[_LOUD_MEAN_1S]
    coupling_entropy_1s = h3_features[_COUPLING_ENTROPY_1S]
    pleas_val_100ms = h3_features[_PLEAS_VAL_100MS]

    # -- R3 features (unused directly in sigmoid formulas but available) --
    # The E-layer formulas reference H3 multi-scale features.
    # R3 provides context; H3 provides the multi-scale dynamics.

    # f01: Anticipatory DA -- caudate DA proxy
    # Salimpoor 2011: caudate BP correlates with chills count (r = 0.71)
    # sigma(0.35 * loudness_velocity_1s + 0.20 * spectral_uncertainty_125ms
    #        + 0.15 * roughness_velocity_500ms)
    f01 = torch.sigmoid(
        0.35 * loud_vel_1s
        + 0.20 * spec_entropy_125ms
        + 0.15 * rough_vel_500ms
    )

    # f02: Consummatory DA -- NAcc DA proxy
    # Salimpoor 2011: NAcc BP correlates with pleasure rating (r = 0.84)
    # sigma(0.35 * mean_pleasantness_1s + 0.15 * mean_loudness_1s)
    f02 = torch.sigmoid(
        0.35 * pleas_mean_1s
        + 0.15 * loud_mean_1s
    )

    # f03: Wanting index -- anticipatory motivation (Berridge incentive salience)
    # sigma(0.40 * f01 + 0.30 * coupling_entropy_1s)
    f03 = torch.sigmoid(
        0.40 * f01
        + 0.30 * coupling_entropy_1s
    )

    # f04: Liking index -- consummatory pleasure (Berridge hedonic "liking")
    # sigma(0.50 * f02 + 0.20 * pleasantness_100ms)
    f04 = torch.sigmoid(
        0.50 * f02
        + 0.20 * pleas_val_100ms
    )

    return f01, f02, f03, f04
