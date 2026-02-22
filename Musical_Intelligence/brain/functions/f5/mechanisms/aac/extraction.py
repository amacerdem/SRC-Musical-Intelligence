"""AAC E+A-Layer -- Extraction (7D).

Seven explicit features modeling autonomic-arousal extraction:

  E0: emotional_arousal        -- Overall emotional arousal level [0, 1]
  E1: ans_response             -- Aggregate ANS response magnitude [0, 1]
  A0: scr                     -- Skin conductance response proxy [0, 1]
  A1: hr                      -- Heart rate modulation proxy [0, 1]
  A2: respr                   -- Respiratory rate modulation proxy [0, 1]
  A3: bvp                     -- Blood volume pulse modulation proxy [0, 1]
  A4: temp                    -- Peripheral temperature modulation proxy [0, 1]

H3 consumed:
    (7, 9, 4, 2)    amplitude max H9 L2             -- energy level 350ms
    (7, 9, 8, 2)    amplitude velocity H9 L2        -- energy change rate 350ms
    (7, 9, 11, 2)   amplitude acceleration H9 L2    -- onset acceleration 350ms
    (10, 9, 14, 2)  spectral_flux periodicity H9 L2 -- beat clarity 350ms
    (10, 16, 14, 2) spectral_flux periodicity H16 L2 -- bar-level tempo 1s
    (7, 16, 8, 2)   amplitude velocity H16 L2       -- bar-level dynamics 1s
    (7, 19, 19, 2)  amplitude stability H19 L2      -- baseline ANS reference 3s
    (7, 19, 1, 2)   amplitude mean H19 L2           -- homeostatic reference 3s
    (11, 9, 22, 2)  onset_strength peaks H9 L2      -- event density 350ms
    (21, 9, 8, 2)   spectral_flux velocity H9 L2    -- timbral change density

R3 consumed:
    [7]   amplitude        -- E0: energy driver
    [10]  spectral_flux    -- E1: beat periodicity
    [11]  onset_strength   -- A0: SCR onset
    [21]  spectral_flux    -- A3: timbral change for BVP

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/aac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_AMP_MAX_350MS = (7, 9, 4, 2)
_AMP_VEL_350MS = (7, 9, 8, 2)
_AMP_ACCEL_350MS = (7, 9, 11, 2)
_FLUX_PERIOD_350MS = (10, 9, 14, 2)
_FLUX_PERIOD_1S = (10, 16, 14, 2)
_AMP_VEL_1S = (7, 16, 8, 2)
_AMP_STAB_3S = (7, 19, 19, 2)
_AMP_MEAN_3S = (7, 19, 1, 2)
_ONSET_PEAKS_350MS = (11, 9, 22, 2)
_TIMBRE_VEL_350MS = (21, 9, 8, 2)

# -- R3 indices ----------------------------------------------------------------
_AMPLITUDE = 7
_SPECTRAL_FLUX_B = 10
_ONSET_STRENGTH = 11
_SPECTRAL_FLUX_D = 21


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor]:
    """E+A-layer: 7D extraction from H3/R3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(E0, E1, A0, A1, A2, A3, A4)`` each ``(B, T)``.
    """
    # -- H3 features --
    amp_max_350ms = h3_features[_AMP_MAX_350MS]
    amp_vel_350ms = h3_features[_AMP_VEL_350MS]
    amp_accel_350ms = h3_features[_AMP_ACCEL_350MS]
    flux_period_350ms = h3_features[_FLUX_PERIOD_350MS]
    flux_period_1s = h3_features[_FLUX_PERIOD_1S]
    amp_vel_1s = h3_features[_AMP_VEL_1S]
    amp_stab_3s = h3_features[_AMP_STAB_3S]
    amp_mean_3s = h3_features[_AMP_MEAN_3S]
    onset_peaks_350ms = h3_features[_ONSET_PEAKS_350MS]
    timbre_vel_350ms = h3_features[_TIMBRE_VEL_350MS]

    # -- R3 features --
    amplitude = r3_features[..., _AMPLITUDE]       # (B, T)
    flux_b = r3_features[..., _SPECTRAL_FLUX_B]    # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]      # (B, T)
    flux_d = r3_features[..., _SPECTRAL_FLUX_D]    # (B, T)

    # -- Derived signals --
    # Deviation from homeostatic baseline
    deviation = torch.abs(amplitude - amp_mean_3s)

    # E0: Emotional arousal -- amygdala activation proxy
    # Trost 2017: arousal maps to distinct ANS profiles; energy level +
    # change rate drive overall arousal (r=0.74 arousal tracking)
    e0 = torch.sigmoid(
        0.40 * amp_max_350ms + 0.30 * amp_vel_350ms
        + 0.20 * flux_period_1s + 0.10 * amplitude
    )

    # E1: ANS response magnitude -- aggregate sympathetic activation
    # Berntson 1991: autonomic space model, SNS/PNS co-activation
    # Acceleration + onset density signal SNS activation
    e1 = torch.sigmoid(
        0.35 * amp_accel_350ms + 0.30 * onset_peaks_350ms
        + 0.20 * amp_vel_1s + 0.15 * deviation
    )

    # A0: SCR -- skin conductance response proxy
    # Grewe 2007: SCR peaks at chill onset (77% participants, N=38)
    # Energy peaks + onset acceleration drive SCR
    a0 = torch.sigmoid(
        0.40 * amp_max_350ms * onset + 0.30 * amp_accel_350ms
        + 0.30 * onset_peaks_350ms
    )

    # A1: HR -- heart rate modulation proxy
    # Bernardi 2006: tempo/loudness modulate HR (N=24); crescendos
    # increase HR, pauses activate PNS (co-activation paradox)
    # Bar-level dynamics drive HR changes, stability anchors baseline
    a1 = torch.sigmoid(
        0.35 * amp_vel_1s + 0.30 * flux_period_1s
        + 0.20 * amp_stab_3s + 0.15 * flux_b
    )

    # A2: RespR -- respiratory rate modulation proxy
    # Bernardi 2006: tempo modulates RespR synchronously
    # Beat clarity drives respiratory entrainment
    a2 = torch.sigmoid(
        0.40 * flux_period_350ms + 0.30 * flux_period_1s
        + 0.20 * amp_vel_350ms + 0.10 * amplitude
    )

    # A3: BVP -- blood volume pulse modulation proxy
    # Trost 2017: timbral change modulates peripheral vasomotor tone
    a3 = torch.sigmoid(
        0.40 * timbre_vel_350ms + 0.30 * amp_vel_350ms
        + 0.20 * flux_d + 0.10 * deviation
    )

    # A4: Temp -- peripheral temperature modulation proxy
    # Blood-Zatorre 2001: chills recruit insular-brainstem circuitry
    # Slow stability-dependent temperature shift
    a4 = torch.sigmoid(
        0.35 * amp_stab_3s + 0.30 * amp_mean_3s
        + 0.20 * (1.0 - deviation) + 0.15 * flux_period_1s
    )

    return e0, e1, a0, a1, a2, a3, a4
