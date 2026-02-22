"""MCCN F-Layer -- Forecast (1D).

Forward prediction of chills onset:
  chills_onset_pred  -- Predicted chills onset probability [0, 1]

Forecasts likelihood of a chill event in the upcoming 1-3s based on acoustic
buildup patterns and current network activation. Salimpoor 2011:
anticipatory dopamine release in caudate precedes chills, implying the brain
actively predicts peak pleasure moments. High values indicate acoustic
conditions (crescendo, tension buildup, harmonic trajectory) are converging
toward a chills trigger. tau_decay = 3.0s (Chabin 2020).

The prediction integrates:
  1. Energy buildup: amplitude velocity and RMS energy velocity capture
     crescendo patterns that typically precede chills.
  2. Surprise trajectory: spectral deviation at 500ms and energy change
     acceleration capture musical surprise buildup.
  3. Context: mean loudness over 1s provides the baseline against which
     crescendos are evaluated.

H3 demands consumed (6 tuples -- all shared with E-layer):
  (7,  8,  8,  2)  amplitude velocity H8 L2      -- crescendo detection
  (7,  16, 2,  2)  amplitude std H16 L2           -- dynamic range
  (9,  8,  8,  2)  rms_energy velocity H8 L2      -- energy buildup
  (22, 8,  8,  2)  energy_change velocity H8 L2   -- dynamic shift
  (8,  16, 1,  2)  loudness mean H16 L2            -- background loudness
  (21, 8,  0,  2)  spectral_change value H8 L2    -- surprise buildup

E-layer features:
  f01 (theta_prefrontal), f02 (theta_central),
  f03 (arousal_index), f04 (chills_magnitude)

Salimpoor et al. 2011: anticipatory caudate DA before chills (r = 0.71;
PET, N = 8).
Chabin et al. 2020: chills sustain ~3s, theta buildup (HD-EEG, N = 18).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/mccn/f_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples consumed (all shared with E-layer) ----------------------------
_AMP_VEL_500MS = (7, 8, 8, 2)            # amplitude velocity H8 L2
_AMP_STD_1S = (7, 16, 2, 2)              # amplitude std H16 L2
_RMS_VEL_500MS = (9, 8, 8, 2)            # rms_energy velocity H8 L2
_ENERGY_CHG_VEL_500MS = (22, 8, 8, 2)    # energy_change velocity H8 L2
_LOUD_MEAN_1S = (8, 16, 1, 2)            # loudness mean H16 L2
_SPEC_DEV_500MS = (21, 8, 0, 2)          # spectral_change value H8 L2


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor]:
    """F-layer: predict probability of imminent chills onset.

    Integrates acoustic buildup dynamics with current network activation
    to forecast chills 1-3s ahead. Salimpoor 2011 demonstrated anticipatory
    dopamine release in caudate preceding chills by several seconds.

    Energy buildup (amplitude velocity + RMS energy velocity) captures
    crescendo patterns. Surprise trajectory (spectral deviation + energy
    change acceleration) captures musical surprise buildup. Mean loudness
    provides baseline context for crescendo evaluation.

    The E-layer chills magnitude (f04) and network state (P0) gate the
    prediction: acoustic buildup only predicts chills when the cortical
    network is already partially engaged.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(f01, f02, f03, f04)`` from extraction layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0,)`` -- single-element tuple, ``(B, T)``.
    """
    _f01, _f02, _f03, f04 = e
    p0, _p1 = p

    # -- H3 features --
    amp_vel = h3_features[_AMP_VEL_500MS]           # (B, T)
    amp_std = h3_features[_AMP_STD_1S]              # (B, T)
    rms_vel = h3_features[_RMS_VEL_500MS]           # (B, T)
    energy_chg_vel = h3_features[_ENERGY_CHG_VEL_500MS]  # (B, T)
    loud_mean = h3_features[_LOUD_MEAN_1S]          # (B, T)
    spec_dev = h3_features[_SPEC_DEV_500MS]         # (B, T)

    # -- Derived signals --
    # Energy buildup: crescendo detection from amplitude + RMS dynamics
    energy_buildup = 0.50 * amp_vel + 0.50 * rms_vel

    # Surprise trajectory: spectral deviation + energy change acceleration
    surprise_traj = 0.50 * spec_dev + 0.50 * energy_chg_vel

    # -- F0: Chills Onset Prediction --
    # sigma(0.30 * energy_buildup * amp_std
    #      + 0.35 * surprise_traj * (1 - loud_mean.abs())
    #      + 0.35 * f04 * p0)
    # Buildup predicts chills only when network is partially engaged (f04*p0).
    # Salimpoor 2011: caudate DA precedes chills (r = 0.71).
    # tau_decay = 3.0s (Chabin 2020 chills sustain window).
    f0 = torch.sigmoid(
        0.30 * energy_buildup * amp_std.clamp(min=0.1)
        + 0.35 * surprise_traj * (1.0 - loud_mean.abs()).clamp(min=0.1)
        + 0.35 * f04 * p0.clamp(min=0.1)
    )

    return (f0,)
