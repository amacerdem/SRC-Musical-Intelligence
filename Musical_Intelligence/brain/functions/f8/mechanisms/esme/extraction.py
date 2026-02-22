"""ESME E-Layer -- Extraction (4D).

Expertise-specific mismatch negativity features:
  f01: pitch_mmn              -- Pitch MMN amplitude [0, 1]
  f02: rhythm_mmn             -- Rhythm MMN amplitude [0, 1]
  f03: timbre_mmn             -- Timbre MMN amplitude [0, 1]
  f04: expertise_enhancement  -- Domain-specific amplification [0, 1]

f01 captures pitch deviance detection strength weighted by consonance
reference and onset context. Enhanced in singers and violinists.
Koelsch et al. 1999: violinists show MMN to 0.75% pitch deviants in
major chord triads; MMN absent in non-musicians.

f02 captures onset timing deviation weighted by spectral change velocity
and temporal-spectral coupling. Enhanced in drummers and jazz musicians.
Vuust et al. 2012: genre-specific gradient jazz > rock > pop >
non-musicians for complex rhythmic deviants.

f03 captures spectral envelope change weighted by tristimulus deviation
across fundamental, mid, and high harmonics. Enhanced for trained
instrument timbre.
Tervaniemi 2022: "sound parameters most important in performance evoke
the largest MMN."

f04 modulates the maximum across all three domain-specific MMNs by a
trainable alpha parameter. Implements the gradient principle.
Criscuolo et al. 2022 ALE meta (k=84, N=3005): bilateral STG + L IFG
(BA44) in musicians.

H3 demands consumed (10 tuples):
  (2, 0, 0, 2)   helmholtz_kang value H0 L2        -- consonance baseline 25ms
  (2, 3, 1, 2)   helmholtz_kang mean H3 L2         -- consonance template 100ms
  (23, 3, 8, 0)  pitch_change velocity H3 L0       -- pitch deviant velocity 100ms
  (11, 3, 0, 0)  onset_strength value H3 L0        -- onset strength 100ms
  (21, 3, 8, 0)  spectral_flux velocity H3 L0      -- spectral deviance 100ms
  (33, 8, 0, 2)  x_l4l5 value H8 L2                -- temporal-spectral coupling 300ms
  (18, 2, 0, 2)  tristimulus1 value H2 L2           -- F0 energy 17ms
  (19, 2, 0, 2)  tristimulus2 value H2 L2           -- mid harmonics 17ms
  (20, 2, 0, 2)  tristimulus3 value H2 L2           -- high harmonics 17ms
  (24, 8, 2, 0)  timbre_change std H8 L0            -- timbre change 300ms

R3 inputs: helmholtz_kang[2], onset_strength[11], warmth[12],
           tonalness[14], tristimulus[18:21], spectral_flux[21],
           pitch_change[23], x_l4l5[33:41]

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/esme/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (10 tuples, all E-layer) --------------------------
# f01: Pitch MMN
_CONSONANCE_VAL_H0 = (2, 0, 0, 2)       # #0: consonance deviance baseline 25ms
_CONSONANCE_MEAN_H3 = (2, 3, 1, 2)      # #1: consonance template 100ms
_PITCH_VEL_H3 = (23, 3, 8, 0)           # #2: pitch deviant velocity 100ms

# f02: Rhythm MMN
_ONSET_VAL_H3 = (11, 3, 0, 0)           # #3: onset strength 100ms
_SPEC_CHANGE_VEL_H3 = (21, 3, 8, 0)     # #4: spectral deviance velocity 100ms
_TSC_VAL_H8 = (33, 8, 0, 2)             # #5: temporal-spectral coupling 300ms

# f03: Timbre MMN
_TRIST1_VAL_H2 = (18, 2, 0, 2)          # #6: tristimulus1 F0 energy 17ms
_TRIST2_VAL_H2 = (19, 2, 0, 2)          # #7: tristimulus2 mid harmonics 17ms
_TRIST3_VAL_H2 = (20, 2, 0, 2)          # #8: tristimulus3 high harmonics 17ms
_TIMBRE_STD_H8 = (24, 8, 2, 0)          # #9: timbre change std 300ms

# -- Upstream dimension defaults -----------------------------------------------
_EDNR_DIM = 10
_TSCP_DIM = 10
_CDMR_DIM = 11

# -- Trainable alpha for expertise enhancement ---------------------------------
_ALPHA = 1.5


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    ednr: Tensor,
    tscp: Tensor,
    cdmr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D expertise-specific MMN features.

    f01 (pitch_mmn): Pitch deviance detection from pitch change velocity
    at 100ms, helmholtz consonance difference (instantaneous minus
    template), and onset context.
    Koelsch et al. 1999: violinists detect 0.75% pitch deviants.

    f02 (rhythm_mmn): Onset timing deviation from onset strength at
    100ms, spectral change velocity, and temporal-spectral coupling
    at 300ms.
    Vuust et al. 2012: genre-specific gradient.

    f03 (timbre_mmn): Spectral envelope change from timbre change std
    at 300ms and tristimulus deviation (std across F0, mid, high
    harmonics at 17ms).
    Tervaniemi 2022: trained parameter evokes largest MMN.

    f04 (expertise_enhancement): Modulates max(f01, f02, f03) by
    alpha parameter for domain-specific amplification.
    Criscuolo et al. 2022: bilateral STG + L IFG in musicians.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        ednr: ``(B, T, 10)`` upstream EDNR output.
        tscp: ``(B, T, 10)`` upstream TSCP output.
        cdmr: ``(B, T, 11)`` upstream CDMR output.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``.
    """
    # -- H3 features -----------------------------------------------------------
    consonance_val = h3_features[_CONSONANCE_VAL_H0]     # (B, T) -- 25ms baseline
    consonance_mean = h3_features[_CONSONANCE_MEAN_H3]   # (B, T) -- 100ms template
    pitch_vel = h3_features[_PITCH_VEL_H3]               # (B, T) -- pitch velocity
    onset_val = h3_features[_ONSET_VAL_H3]               # (B, T) -- onset strength
    spec_change_vel = h3_features[_SPEC_CHANGE_VEL_H3]   # (B, T) -- spectral vel
    tsc_val = h3_features[_TSC_VAL_H8]                   # (B, T) -- temporal-spectral
    trist1 = h3_features[_TRIST1_VAL_H2]                 # (B, T) -- F0 energy
    trist2 = h3_features[_TRIST2_VAL_H2]                 # (B, T) -- mid harmonics
    trist3 = h3_features[_TRIST3_VAL_H2]                 # (B, T) -- high harmonics
    timbre_std = h3_features[_TIMBRE_STD_H8]             # (B, T) -- timbre change

    # -- Derived features ------------------------------------------------------
    # Helmholtz consonance difference: instantaneous - template
    helmholtz_diff = consonance_val - consonance_mean     # (B, T)

    # Tristimulus deviation: std across the three tristimulus components
    trist_stack = torch.stack([trist1, trist2, trist3], dim=-1)  # (B, T, 3)
    tristimulus_deviation = trist_stack.std(dim=-1)               # (B, T)

    # Upstream summary signals
    ednr_mean = ednr.mean(dim=-1)                         # (B, T)
    x_l4l5_mean = tsc_val                                 # (B, T) -- coupling proxy

    # -- f01: Pitch MMN --------------------------------------------------------
    # sigma(0.40 * abs(pitch_change_vel) + 0.30 * abs(helmholtz_diff)
    #       + 0.30 * onset_val)
    # Koelsch et al. 1999: violinists show MMN to 0.75% pitch deviants
    f01 = torch.sigmoid(
        0.40 * pitch_vel.abs()
        + 0.30 * helmholtz_diff.abs()
        + 0.30 * onset_val
    )

    # -- f02: Rhythm MMN -------------------------------------------------------
    # sigma(0.40 * abs(onset_deviation) + 0.30 * spec_change_vel
    #       + 0.30 * x_l4l5_mean)
    # Vuust et al. 2012: genre-specific gradient
    # Liao et al. 2024: percussionists recruit distinct NMR network
    f02 = torch.sigmoid(
        0.40 * onset_val.abs()
        + 0.30 * spec_change_vel
        + 0.30 * x_l4l5_mean
    )

    # -- f03: Timbre MMN -------------------------------------------------------
    # sigma(0.40 * timbre_change_std + 0.30 * tristimulus_deviation)
    # Tervaniemi 2022: trained parameter evokes largest MMN
    f03 = torch.sigmoid(
        0.40 * timbre_std
        + 0.30 * tristimulus_deviation
    )

    # -- f04: Expertise Enhancement --------------------------------------------
    # sigma(alpha * max(f01, f02, f03))
    # Criscuolo et al. 2022 ALE meta (k=84, N=3005)
    # Martins et al. 2022 constraint: gradient, not clean dissociation
    max_mmn = torch.max(torch.max(f01, f02), f03)
    f04 = torch.sigmoid(
        _ALPHA * max_mmn
    )

    return f01, f02, f03, f04
