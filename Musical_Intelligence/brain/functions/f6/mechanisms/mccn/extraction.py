"""MCCN E-Layer -- Extraction (4D).

Musical Chills Cortical Network extraction signals:
  f01: theta_prefrontal    -- Right prefrontal theta power increase [0, 1]
  f02: theta_central       -- Central theta power decrease (inverse) [0, 1]
  f03: arousal_index       -- Physiological arousal from beta/alpha ratio [0, 1]
  f04: chills_magnitude    -- Peak chills magnitude [0, 1]

Two parallel pathways compute theta oscillation signatures and physiological
arousal, which are then integrated into a chills magnitude signal.

Theta pathway (f01, f02): Captures the theta oscillation contrast of chills --
right prefrontal theta increase (f01) simultaneous with central/temporal theta
decrease (f02). Theta is proxied through x_l0l5 periodicity at 100ms (theta
timescale ~5 Hz). Source localization: OFC (p < 1e-05), insula (p < 1e-06),
SMA (p < 1e-07) co-activate with this theta pattern.

Arousal pathway (f03): Tracks physiological arousal via energy dynamics.
Beta/alpha ratio increase during chills (F(2,15) = 4.77, p = 0.014) is
proxied by RMS energy velocity and instantaneous energy level.

Integration (f04): Chills magnitude combines peak loudness (acoustic trigger
at resolution) with the f01 * f03 product, ensuring chills require
co-activation of reward (theta prefrontal) and arousal.

H3 demands consumed (16 tuples):
  (25, 3,  0,  2)  x_l0l5 value H3 L2              -- theta proxy 100ms
  (25, 3,  14, 2)  x_l0l5 periodicity H3 L2         -- theta periodicity 100ms
  (25, 16, 14, 2)  x_l0l5 periodicity H16 L2        -- sustained theta 1s
  (25, 16, 1,  2)  x_l0l5 mean H16 L2               -- mean coupling 1s
  (8,  3,  0,  2)  loudness value H3 L2              -- instantaneous intensity
  (8,  8,  4,  2)  loudness max H8 L2                -- peak loudness 500ms
  (8,  16, 1,  2)  loudness mean H16 L2              -- loudness baseline 1s
  (7,  8,  8,  2)  amplitude velocity H8 L2          -- crescendo rate
  (7,  16, 2,  2)  amplitude std H16 L2              -- dynamic range 1s
  (9,  3,  0,  2)  rms_energy value H3 L2            -- arousal 100ms
  (9,  8,  8,  2)  rms_energy velocity H8 L2         -- arousal buildup
  (9,  16, 1,  2)  rms_energy mean H16 L2            -- sustained activation
  (0,  8,  1,  2)  roughness mean H8 L2              -- tension tracking
  (0,  16, 2,  2)  roughness std H16 L2              -- tension dynamics
  (21, 8,  0,  2)  spectral_change value H8 L2       -- surprise event
  (22, 8,  8,  2)  energy_change velocity H8 L2      -- dynamic shift

R3 features:
  [0]  roughness, [7] amplitude, [8] loudness, [9] rms_energy,
  [21] spectral_change, [22] energy_change, [25:33] x_l0l5

Upstream reads:
  DAED relay (via relay_outputs) -- wanting_index, liking_index for gating
  MORMR relay (via relay_outputs) -- opioid context

Chabin et al. 2020: RPF theta F(2,15) = 3.28, p = 0.049; RC theta
F(2,15) = 4.09, p = 0.025; beta/alpha F(2,15) = 4.77, p = 0.014
(HD-EEG, N = 18).
Putkinen et al. 2025: OFC + amygdala MOR during chills (PET, N = 15).
Salimpoor et al. 2011: Caudate -> NAcc DA during chills (PET, N = 8).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/mccn/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples consumed -------------------------------------------------------
_COUPLING_VAL_100MS = (25, 3, 0, 2)      # x_l0l5 value H3 L2 -- theta proxy
_THETA_PERIOD_100MS = (25, 3, 14, 2)     # x_l0l5 periodicity H3 L2
_THETA_PERIOD_1S = (25, 16, 14, 2)       # x_l0l5 periodicity H16 L2
_COUPLING_MEAN_1S = (25, 16, 1, 2)       # x_l0l5 mean H16 L2
_LOUD_VAL_100MS = (8, 3, 0, 2)           # loudness value H3 L2
_LOUD_MAX_500MS = (8, 8, 4, 2)           # loudness max H8 L2
_LOUD_MEAN_1S = (8, 16, 1, 2)            # loudness mean H16 L2
_AMP_VEL_500MS = (7, 8, 8, 2)            # amplitude velocity H8 L2
_AMP_STD_1S = (7, 16, 2, 2)              # amplitude std H16 L2
_RMS_VAL_100MS = (9, 3, 0, 2)            # rms_energy value H3 L2
_RMS_VEL_500MS = (9, 8, 8, 2)            # rms_energy velocity H8 L2
_RMS_MEAN_1S = (9, 16, 1, 2)             # rms_energy mean H16 L2
_ROUGH_MEAN_500MS = (0, 8, 1, 2)         # roughness mean H8 L2
_ROUGH_STD_1S = (0, 16, 2, 2)            # roughness std H16 L2
_SPEC_DEV_500MS = (21, 8, 0, 2)          # spectral_change value H8 L2
_ENERGY_CHG_VEL_500MS = (22, 8, 8, 2)    # energy_change velocity H8 L2

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_AMPLITUDE = 7
_LOUDNESS = 8
_RMS_ENERGY = 9
_SPECTRAL_CHANGE = 21
_ENERGY_CHANGE = 22
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """E-layer: 4D extraction of theta + arousal + chills signals.

    Implements the cortical chills network from Chabin et al. (2020).
    Two parallel pathways:
        Theta (f01, f02): prefrontal theta increase vs central decrease.
            Proxied through x_l0l5 periodicity at 100ms timescale.
        Arousal (f03): RMS energy velocity + instantaneous energy level.
    Integration (f04): peak loudness * f01 * f03 co-activation gate.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        relay_outputs: ``{"DAED": (B, T, D), "MORMR": (B, T, D)}``.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``.
    """
    # -- H3 features --
    coupling_val = h3_features[_COUPLING_VAL_100MS]       # (B, T)
    theta_period_100 = h3_features[_THETA_PERIOD_100MS]   # (B, T)
    theta_period_1s = h3_features[_THETA_PERIOD_1S]       # (B, T)
    coupling_mean_1s = h3_features[_COUPLING_MEAN_1S]     # (B, T)
    loud_val_100 = h3_features[_LOUD_VAL_100MS]           # (B, T)
    loud_max_500 = h3_features[_LOUD_MAX_500MS]           # (B, T)
    rms_val_100 = h3_features[_RMS_VAL_100MS]             # (B, T)
    rms_vel_500 = h3_features[_RMS_VEL_500MS]             # (B, T)
    rough_std_1s = h3_features[_ROUGH_STD_1S]             # (B, T)

    # -- R3 features (context) --
    roughness = r3_features[..., _ROUGHNESS]              # (B, T)
    loudness = r3_features[..., _LOUDNESS]                # (B, T)
    rms_energy = r3_features[..., _RMS_ENERGY]            # (B, T)

    # -- f01: Theta Prefrontal (excitatory) --
    # Chabin 2020: RPF theta F(2,15) = 3.28, p = 0.049.
    # sigma(0.35 * theta_periodicity_100ms + 0.30 * mean_coupling_1s)
    # Prefrontal theta increase is the excitatory signature of chills.
    f01 = torch.sigmoid(
        0.35 * theta_period_100
        + 0.30 * coupling_mean_1s
    )

    # -- f02: Theta Central (inverse -- decrease during chills) --
    # Chabin 2020: RC theta F(2,15) = 4.09, p = 0.025;
    #              RT theta F(2,15) = 5.88, p = 0.006.
    # sigma(0.40 * (1 - theta_periodicity_100ms) + 0.30 * roughness_std_1s)
    # Central/temporal theta decrease contrasts with prefrontal increase.
    f02 = torch.sigmoid(
        0.40 * (1.0 - theta_period_100)
        + 0.30 * rough_std_1s
    )

    # -- f03: Arousal Index --
    # Chabin 2020: beta/alpha ratio F(2,15) = 4.77, p = 0.014.
    # sigma(0.35 * |energy_velocity_500ms| + 0.30 * rms_energy_100ms)
    # Physiological arousal from sympathetic activation.
    # abs(): both energy increase (crescendo) and decrease (dramatic silence)
    # trigger physiological arousal
    f03 = torch.sigmoid(
        0.35 * torch.abs(rms_vel_500)
        + 0.30 * rms_val_100
    )

    # -- f04: Chills Magnitude --
    # sigma(0.35 * peak_loudness_500ms + 0.30 * f01 * f03)
    # High only when both prefrontal reward (f01) and arousal (f03)
    # are co-active. Peak loudness captures crescendo trigger.
    f04 = torch.sigmoid(
        0.35 * loud_max_500
        + 0.30 * f01 * f03
    )

    return f01, f02, f03, f04
