"""ETAM E-Layer -- Extraction (4D).

Tempo-entrained temporal windows and instrument asymmetry:
  E0: early_window          (150-220ms amplitude/loudness/onset integration)
  E1: middle_window         (320-360ms spectral flux/change/energy dynamics)
  E2: late_window           (410-450ms coupling and cognitive integration)
  E3: instrument_asymmetry  (timbral asymmetry across streams)

H3 demands consumed:
  amplitude:        (7,6,0,2), (7,6,4,2)
  loudness:         (8,6,0,0)
  onset_strength:   (11,6,0,0)
  spectral_flux:    (10,11,0,0)
  spectral_change:  (21,8,1,0)
  energy_change:    (22,11,8,0)
  x_l0l5:           (25,16,0,2)
  x_l5l7:           (41,14,1,0), (41,14,13,0)
  timbre_change:    (24,14,3,0), (24,8,0,0)

No R3 direct reads -- pure H3 extraction.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/etam/
Tierney & Kraus 2015: EEG entrainment -- temporal windows aligned to beat.
Grahn & Rowe 2012: fMRI -- STG encodes tempo envelope at multiple timescales.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_AMP_VAL_150MS = (7, 6, 0, 2)          # amplitude value 150ms (integration)
_AMP_MAX_150MS = (7, 6, 4, 2)          # amplitude max 150ms (integration)
_LOUD_VAL_150MS = (8, 6, 0, 0)         # loudness value 150ms (memory)
_ONSET_VAL_150MS = (11, 6, 0, 0)       # onset value 150ms (memory)
_FLUX_VAL_750MS = (10, 11, 0, 0)       # spectral flux value 750ms (memory)
_SPEC_CHG_MEAN_500MS = (21, 8, 1, 0)   # spectral change mean 500ms (memory)
_ENERGY_VEL_750MS = (22, 11, 8, 0)     # energy velocity 750ms (memory)
_COUPLING_VAL_1S = (25, 16, 0, 2)      # coupling value 1s (integration)
_COG_COUPLING_MEAN_900MS = (41, 14, 1, 0)   # cognitive coupling mean ~900ms
_COG_COUPLING_ENT_900MS = (41, 14, 13, 0)   # cognitive coupling entropy ~900ms
_TIMBRE_STD_900MS = (24, 14, 3, 0)     # timbre std ~900ms (memory)
_TIMBRE_VAL_500MS = (24, 8, 0, 0)      # timbre change value 500ms (memory)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: temporal windows and instrument asymmetry.

    Four extraction dimensions capture entrainment-relevant features at
    different temporal latencies, mirroring the cascade of auditory
    processing stages from brainstem through cortex.

    Tierney & Kraus 2015: beat-locked oscillations create temporal windows
    at ~150ms (brainstem), ~340ms (cortical), ~430ms (cognitive).
    Grahn & Rowe 2012: STG tempo envelope processing at multiple timescales.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``
    """
    # -- H3 features --
    amp_val_150ms = h3_features[_AMP_VAL_150MS]
    amp_max_150ms = h3_features[_AMP_MAX_150MS]
    loud_val_150ms = h3_features[_LOUD_VAL_150MS]
    onset_val_150ms = h3_features[_ONSET_VAL_150MS]
    flux_val_750ms = h3_features[_FLUX_VAL_750MS]
    spec_chg_mean_500ms = h3_features[_SPEC_CHG_MEAN_500MS]
    energy_vel_750ms = h3_features[_ENERGY_VEL_750MS]
    coupling_val_1s = h3_features[_COUPLING_VAL_1S]
    cog_coupling_mean_900ms = h3_features[_COG_COUPLING_MEAN_900MS]
    cog_coupling_ent_900ms = h3_features[_COG_COUPLING_ENT_900MS]
    timbre_std_900ms = h3_features[_TIMBRE_STD_900MS]
    timbre_val_500ms = h3_features[_TIMBRE_VAL_500MS]

    # -- E0: Early Window (150-220ms) --
    # Amplitude x loudness interaction captures energy envelope at brainstem
    # latency, plus onset event markers and peak amplitude for transient
    # detection. This is the first entrainment-relevant temporal window.
    # Tierney 2015: brainstem ABR at ~6ms phase-locks to beat.
    e0 = torch.sigmoid(
        0.35 * amp_val_150ms * loud_val_150ms
        + 0.35 * onset_val_150ms
        + 0.30 * amp_max_150ms
    )

    # -- E1: Middle Window (320-360ms) --
    # Spectral dynamics at medium timescales: flux (event density), spectral
    # change rate (timbral evolution), and energy dynamics (dynamics envelope).
    # Cortical N1/P2 latency range -- temporal attention modulates MMN.
    # Grahn 2012: STG parametrically encodes tempo envelope.
    e1 = torch.sigmoid(
        0.40 * flux_val_750ms
        + 0.30 * spec_chg_mean_500ms
        + 0.30 * energy_vel_750ms
    )

    # -- E2: Late Window (410-450ms) --
    # Coupling-based features at bar/cognitive timescale: sensorimotor
    # coupling strength, cognitive coupling mean and entropy. This window
    # captures higher-order metric structure processing.
    # London 2012: metric hierarchy creates attentional weights at bar level.
    e2 = torch.sigmoid(
        0.35 * coupling_val_1s
        + 0.35 * cog_coupling_mean_900ms
        + 0.30 * cog_coupling_ent_900ms
    )

    # -- E3: Instrument Asymmetry --
    # Timbral variability across streams: high timbre std indicates
    # multiple instruments with different timbral signatures, enabling
    # stream segregation. Value + variability combined.
    # Tierney 2015: timbral cues assist beat tracking in complex mixtures.
    e3 = torch.sigmoid(
        0.50 * timbre_std_900ms
        + 0.50 * timbre_val_500ms
    )

    return e0, e1, e2, e3
