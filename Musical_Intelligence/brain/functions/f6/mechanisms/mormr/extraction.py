"""MORMR E-Layer -- Extraction (4D).

Four neurochemical features modeling mu-opioid receptor activation:

  f01: opioid_release       -- Endogenous opioid release proxy [0, 1]
  f02: chills_count         -- Chills frequency proxy [0, 1]
  f03: nacc_binding         -- NAcc opioid activity proxy [0, 1]
  f04: reward_sensitivity   -- Individual music reward sensitivity [0, 1]

H3 consumed (tuples 0-6):
    (4, 16, 1, 2)   sensory_pleasantness mean H16 L2     -- mean pleasantness 1s
    (0, 16, 1, 2)   roughness mean H16 L2                -- mean roughness 1s
    (12, 8, 1, 2)   warmth mean H8 L2                    -- mean warmth 500ms
    (7, 8, 0, 2)    amplitude value H8 L2                -- amplitude 500ms
    (41, 8, 0, 2)   beauty_coupling value H8 L2           -- beauty coupling 500ms
    (4, 16, 8, 0)   sensory_pleasantness velocity H16 L0  -- pleasantness velocity 1s
    (41, 16, 20, 2) beauty_coupling entropy H16 L2        -- beauty entropy 1s

R3 consumed:
    [0]      roughness               -- consonance quality (inverse)
    [4]      sensory_pleasantness    -- direct hedonic signal
    [7]      amplitude               -- peak magnitude for chills
    [8]      loudness                -- pleasure intensity level
    [12]     warmth                  -- timbral richness
    [13]     brightness              -- spectral character
    [22]     energy_change           -- dynamic modulation
    [33:41]  x_l4l5                  -- sustained pleasure coupling
    [41:49]  x_l5l7                  -- pleasure-structure beauty

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/mormr/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 0-6 from demand spec) ----------------------------------
_PLEAS_MEAN_1S = (4, 16, 1, 2)          # #0: mean pleasantness over 1s
_ROUGH_MEAN_1S = (0, 16, 1, 2)          # #1: mean roughness over 1s
_WARMTH_MEAN_500MS = (12, 8, 1, 2)      # #2: mean warmth at 500ms
_AMP_VAL_500MS = (7, 8, 0, 2)           # #3: amplitude at 500ms
_BEAUTY_VAL_500MS = (41, 8, 0, 2)       # #4: beauty coupling at 500ms
_PLEAS_VEL_1S = (4, 16, 8, 0)           # #5: pleasantness velocity over 1s
_BEAUTY_ENTROPY_1S = (41, 16, 20, 2)    # #6: beauty entropy at 1s

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_LOUDNESS = 8
_WARMTH = 12
_BRIGHTNESS = 13
_ENERGY_CHANGE = 22
_X_L4L5_START = 33
_X_L4L5_END = 41
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """E-layer: 4D extraction from H3/R3 features.

    Models mu-opioid receptor activation during musical pleasure,
    based on Putkinen et al. (2025) PET evidence.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``.
    """
    # -- H3 features --
    pleas_mean_1s = h3_features[_PLEAS_MEAN_1S]
    rough_mean_1s = h3_features[_ROUGH_MEAN_1S]
    warmth_mean_500ms = h3_features[_WARMTH_MEAN_500MS]
    amp_val_500ms = h3_features[_AMP_VAL_500MS]
    beauty_val_500ms = h3_features[_BEAUTY_VAL_500MS]
    pleas_vel_1s = h3_features[_PLEAS_VEL_1S]
    beauty_entropy_1s = h3_features[_BEAUTY_ENTROPY_1S]

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]                # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    amplitude = r3_features[..., _AMPLITUDE]                # (B, T)
    loudness = r3_features[..., _LOUDNESS]                  # (B, T)
    warmth = r3_features[..., _WARMTH]                      # (B, T)
    brightness = r3_features[..., _BRIGHTNESS]              # (B, T)
    energy_change = r3_features[..., _ENERGY_CHANGE]        # (B, T)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # -- Derived signals --
    beauty_coupling = x_l5l7.mean(dim=-1)  # (B, T) -- beauty proxy

    # f01: Opioid Release
    # Putkinen 2025: [11C]carfentanil binding increases in VS, OFC, amygdala
    # during music (d = 4.8). Opioid release driven by sustained hedonic quality.
    # sigma(0.35 * mean_pleasantness_1s + 0.20 * (1 - mean_roughness_1s)
    #       + 0.15 * mean_warmth_500ms)
    # Remaining weight from R3 pleasantness for instantaneous hedonic signal.
    f01 = torch.sigmoid(
        0.35 * pleas_mean_1s
        + 0.20 * (1.0 - rough_mean_1s)
        + 0.15 * warmth_mean_500ms
        + 0.30 * pleasantness
    )

    # f02: Chills Count
    # Putkinen 2025: chills count correlates with NAcc BPND (r = -0.52).
    # Chills triggered by peak emotional moments with high aesthetic value.
    # sigma(... + 0.20 * amplitude_500ms + 0.15 * beauty_coupling_500ms)
    f02 = torch.sigmoid(
        0.30 * loudness * amplitude
        + 0.20 * amp_val_500ms
        + 0.15 * beauty_val_500ms
        + 0.20 * beauty_coupling
        + 0.15 * energy_change
    )

    # f03: NAcc Binding
    # Putkinen 2025: NAcc shows strongest music-induced MOR activation.
    # sigma(0.40 * f01 + 0.30 * pleasantness_velocity_1s)
    # Remaining weight from brightness for timbral context.
    f03 = torch.sigmoid(
        0.40 * f01
        + 0.30 * pleas_vel_1s
        + 0.30 * pleasantness * brightness
    )

    # f04: Reward Sensitivity
    # Putkinen 2025: baseline MOR tone modulates pleasure-BOLD coupling (d = 1.16).
    # Mas-Herrero 2014: musical anhedonia dissociates from monetary reward.
    # sigma(0.40 * f01 * f02 + 0.30 * beauty_entropy_1s)
    f04 = torch.sigmoid(
        0.40 * f01 * f02
        + 0.30 * beauty_entropy_1s
        + 0.30 * warmth * pleasantness
    )

    return f01, f02, f03, f04
