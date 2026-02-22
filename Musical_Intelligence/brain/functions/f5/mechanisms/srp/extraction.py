"""SRP N+C-Layer -- Extraction (6D).

Six neurochemical features modeling striatal reward prediction:

  N0: da_caudate          -- Caudate anticipatory DA ramp [0, 1]
  N1: da_nacc             -- NAcc consummatory DA burst [0, 1]
  N2: opioid_proxy        -- Mu-opioid hedonic signal [0, 1]
  C0: vta_drive           -- VTA dopaminergic drive [0, 1]
  C1: stg_nacc_coupling   -- STG-NAcc structural coupling [0, 1]
  C2: prediction_error    -- Reward prediction error (RPE) [0, 1]

H3 consumed (tuples 1-13):
    (7, 24, 8, 0)   amplitude velocity H24 L0          -- caudate ramp
    (0, 24, 18, 0)  roughness trend H24 L0             -- section tension
    (7, 20, 4, 1)   amplitude max H20 L1               -- anticipation gap
    (7, 16, 0, 2)   amplitude value H16 L2             -- current energy
    (0, 18, 0, 2)   roughness value H18 L2             -- current dissonance
    (0, 18, 1, 2)   roughness mean H18 L2              -- baseline dissonance
    (4, 18, 0, 2)   sensory_pleasantness value H18 L2  -- consonance phrase
    (16, 18, 15, 2) spectral_smoothness smooth H18 L2  -- opioid warmth
    (21, 16, 8, 0)  spectral_flux velocity H16 L0      -- RPE trigger
    (22, 16, 8, 0)  distribution_entropy vel H16 L0    -- surprise
    (4, 16, 8, 0)   sensory_pleasantness vel H16 L0    -- consonance surprise
    (25, 18, 0, 2)  x_l0l5[0] value H18 L2            -- coupling signal
    (11, 16, 22, 2) onset_strength peaks H16 L2        -- rhythmic coupling

R3 consumed:
    [0]      roughness               -- N2: inverse consonance
    [4]      sensory_pleasantness    -- N2: opioid correlate
    [7]      amplitude               -- N0: energy dynamics
    [11]     onset_strength          -- C1: event density
    [16]     spectral_smoothness     -- N2: hedonic warmth
    [21]     spectral_flux           -- C2: spectral change
    [22]     distribution_entropy    -- C2: uncertainty
    [25:33]  x_l0l5                  -- C1: STG-NAcc coupling

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 1-13 from demand spec) ---------------------------------
_AMP_VEL_36S = (7, 24, 8, 0)            # #1: caudate ramp
_ROUGH_TREND_36S = (0, 24, 18, 0)       # #2: section tension
_AMP_MAX_5S_FWD = (7, 20, 4, 1)         # #3: anticipation gap (L1 forward)
_AMP_VAL_1S = (7, 16, 0, 2)             # #4: current energy
_ROUGH_VAL_2S = (0, 18, 0, 2)           # #5: current dissonance phrase
_ROUGH_MEAN_2S = (0, 18, 1, 2)          # #6: baseline dissonance phrase
_PLEAS_VAL_2S = (4, 18, 0, 2)           # #7: consonance phrase
_SMOOTH_SMOOTH_2S = (16, 18, 15, 2)     # #8: smoothness phrase
_SFLUX_VEL_1S = (21, 16, 8, 0)          # #9: spectral change rate
_ENTROPY_VEL_1S = (22, 16, 8, 0)        # #10: entropy change rate
_PLEAS_VEL_1S = (4, 16, 8, 0)           # #11: consonance surprise
_X_COUPLING_2S = (25, 18, 0, 2)         # #12: energy-consonance coupling
_ONSET_PEAKS_1S = (11, 16, 22, 2)       # #13: onset event density

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_ONSET_STRENGTH = 11
_SPECTRAL_SMOOTHNESS = 16
_SPECTRAL_FLUX = 21
_DISTRIBUTION_ENTROPY = 22
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor]:
    """N+C-layer: 6D extraction from H3/R3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(N0, N1, N2, C0, C1, C2)`` each ``(B, T)``.
    """
    # -- H3 features --
    amp_vel_36s = h3_features[_AMP_VEL_36S]
    rough_trend_36s = h3_features[_ROUGH_TREND_36S]
    amp_max_5s_fwd = h3_features[_AMP_MAX_5S_FWD]
    amp_val_1s = h3_features[_AMP_VAL_1S]
    rough_val_2s = h3_features[_ROUGH_VAL_2S]
    rough_mean_2s = h3_features[_ROUGH_MEAN_2S]
    pleas_val_2s = h3_features[_PLEAS_VAL_2S]
    smooth_smooth_2s = h3_features[_SMOOTH_SMOOTH_2S]
    sflux_vel_1s = h3_features[_SFLUX_VEL_1S]
    entropy_vel_1s = h3_features[_ENTROPY_VEL_1S]
    pleas_vel_1s = h3_features[_PLEAS_VEL_1S]
    x_coupling_2s = h3_features[_X_COUPLING_2S]
    onset_peaks_1s = h3_features[_ONSET_PEAKS_1S]

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]              # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    amplitude = r3_features[..., _AMPLITUDE]              # (B, T)
    onset_str = r3_features[..., _ONSET_STRENGTH]         # (B, T)
    smoothness = r3_features[..., _SPECTRAL_SMOOTHNESS]   # (B, T)
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]      # (B, T)
    entropy = r3_features[..., _DISTRIBUTION_ENTROPY]     # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)

    # -- Derived signals --
    consonance = 1.0 - roughness  # inverse roughness = consonance proxy

    # N0: Caudate anticipatory DA ramp
    # Salimpoor 2011: caudate DA ramps 9-15s before peak (r=0.71)
    # Quasi-hyperbolic ramp = energy velocity * anticipation gap
    anticipation_gap = torch.sigmoid(amp_max_5s_fwd - amp_val_1s)
    n0 = torch.sigmoid(
        0.35 * amp_vel_36s * anticipation_gap
        + 0.30 * amplitude * amp_val_1s
        + 0.35 * rough_trend_36s * consonance
    )

    # N1: NAcc consummatory DA burst
    # Salimpoor 2011: NAcc DA bursts at peak moments (r=0.84)
    # Peak = high energy * high consonance * surprise
    surprise = torch.sigmoid(sflux_vel_1s + entropy_vel_1s)
    n1 = torch.sigmoid(
        0.35 * amp_val_1s * consonance
        + 0.30 * surprise * pleasantness
        + 0.35 * pleas_vel_1s * onset_peaks_1s
    )

    # N2: Opioid hedonic proxy
    # Mallik 2017: naltrexone blocks music-evoked pleasure (mu-opioid)
    # Opioid = consonance * smoothness * pleasantness
    n2 = torch.sigmoid(
        0.35 * pleas_val_2s * consonance
        + 0.35 * smooth_smooth_2s * pleasantness
        + 0.30 * (1.0 - rough_val_2s) * smoothness
    )

    # C0: VTA dopaminergic drive
    # Menon & Levitin 2005: VTA activates during pleasant music
    # VTA drive = energy dynamics + consonance dynamics
    c0 = torch.sigmoid(
        0.40 * amp_vel_36s * amplitude
        + 0.30 * rough_mean_2s * consonance
        + 0.30 * pleas_val_2s * amp_val_1s
    )

    # C1: STG-NAcc structural coupling
    # Salimpoor 2013: STG-NAcc connectivity predicts reward
    # Coupling = x_l0l5 * onset density * consonance
    x_coupling = x_l0l5.mean(dim=-1)  # (B, T)
    c1 = torch.sigmoid(
        0.35 * x_coupling * x_coupling_2s
        + 0.35 * onset_str * onset_peaks_1s
        + 0.30 * consonance * pleasantness
    )

    # C2: Reward prediction error (RPE)
    # Cheung 2019: surprise + uncertainty drive musical pleasure
    # RPE = spectral change * entropy change * consonance surprise
    c2 = torch.sigmoid(
        0.35 * sflux_vel_1s * spectral_flux
        + 0.35 * entropy_vel_1s * entropy
        + 0.30 * pleas_vel_1s * pleasantness
    )

    return n0, n1, n2, c0, c1, c2
