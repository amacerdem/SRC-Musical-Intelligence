"""NEWMD E-Layer -- Extraction (4D).

Neural Entrainment-Working Memory Dissociation extraction layer.
Computes four dimensions that capture the fundamental tension between
neural entrainment strength and working memory capacity:

  E0: entrainment_strength   (rhythmic entrainment from onset/flux periodicity)
  E1: wm_capacity            (working memory load from energy/pitch/spectral complexity)
  E2: flexibility_cost       (cost of switching between entrainment and WM routes)
  E3: dissociation_index     (absolute divergence between entrainment and WM)

Core idea: Tierney 2014 showed that entrainment and WM are partially
dissociable -- strong entrainment does not guarantee strong WM engagement,
and vice versa. The E-layer captures this dual-route structure.

H3 demands consumed:
  onset_strength:   (11,6,0,0)    -- onset value 150ms (event detection)
  spectral_flux:    (10,6,4,0)    -- flux max 150ms (peak detection)
  onset_strength:   (11,11,14,0)  -- onset periodicity 750ms (beat regularity)
  amplitude:        (7,6,0,0)     -- amplitude value 150ms (beat amplitude)
  energy_change:    (22,8,1,0)    -- energy mean 500ms (dynamic level)
  pitch_change:     (23,8,3,0)    -- pitch std 500ms (melodic complexity)
  spectral_change:  (21,11,8,0)   -- spectral velocity 750ms (change rate)
  energy_change:    (22,14,13,0)  -- energy entropy ~900ms (complexity)
  pitch_change:     (23,14,1,0)   -- pitch mean ~900ms (melodic context)
  x_l0l5:           (25,20,13,0)  -- coupling entropy 5s (long-term load)
  spectral_centroid:(9,16,15,0)   -- centroid smoothness 1s (timbral stability)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/newmd/
Tierney 2014: behavioral+EEG, N=30.
Grahn 2009: fMRI, N=18.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ONSET_VAL_150MS = (11, 6, 0, 0)          # onset value 150ms -- event detection
_FLUX_MAX_150MS = (10, 6, 4, 0)           # flux max 150ms -- peak detection
_ONSET_PERIOD_750MS = (11, 11, 14, 0)     # onset periodicity 750ms -- beat regularity
_AMP_VAL_150MS = (7, 6, 0, 0)             # amplitude value 150ms -- beat amplitude
_ENERGY_MEAN_500MS = (22, 8, 1, 0)        # energy mean 500ms -- dynamic level
_PITCH_STD_500MS = (23, 8, 3, 0)          # pitch std 500ms -- melodic complexity
_SPECTRAL_VEL_750MS = (21, 11, 8, 0)      # spectral velocity 750ms -- change rate
_ENERGY_ENTROPY_900MS = (22, 14, 13, 0)   # energy entropy ~900ms -- complexity
_PITCH_MEAN_900MS = (23, 14, 1, 0)        # pitch mean ~900ms -- melodic context
_COUPLING_ENTROPY_5S = (25, 20, 13, 0)    # coupling entropy 5s -- long-term load
_CENTROID_SMOOTH_1S = (9, 16, 15, 0)      # centroid smoothness 1s -- timbral stability


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: entrainment, WM capacity, flexibility cost, dissociation.

    E0 captures neural entrainment strength from onset periodicity, flux
    peak detection, and beat amplitude -- the rhythmic route that locks
    neural oscillations to the stimulus (Tierney 2014).

    E1 captures working memory capacity from energy dynamics, pitch
    complexity, spectral velocity, and energy entropy -- the cognitive
    load route requiring sustained WM engagement (Grahn 2009).

    E2 captures flexibility cost: when entrainment is weak (1-E0) and
    long-term coupling entropy is high, switching between routes is
    costly. Pitch context and timbral stability modulate this cost.

    E3 captures dissociation: the absolute difference between E0 and
    E1 indicates how divergent the two routes are at any moment.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``
    """
    # -- H3 features --
    onset_val_150ms = h3_features[_ONSET_VAL_150MS]            # (B, T)
    flux_max_150ms = h3_features[_FLUX_MAX_150MS]              # (B, T)
    onset_period_750ms = h3_features[_ONSET_PERIOD_750MS]      # (B, T)
    amp_val_150ms = h3_features[_AMP_VAL_150MS]                # (B, T)
    energy_mean_500ms = h3_features[_ENERGY_MEAN_500MS]        # (B, T)
    pitch_std_500ms = h3_features[_PITCH_STD_500MS]            # (B, T)
    spectral_vel_750ms = h3_features[_SPECTRAL_VEL_750MS]      # (B, T)
    energy_entropy_900ms = h3_features[_ENERGY_ENTROPY_900MS]  # (B, T)
    pitch_mean_900ms = h3_features[_PITCH_MEAN_900MS]          # (B, T)
    coupling_entropy_5s = h3_features[_COUPLING_ENTROPY_5S]    # (B, T)
    centroid_smooth_1s = h3_features[_CENTROID_SMOOTH_1S]       # (B, T)

    # -- E0: Entrainment Strength --
    # Rhythmic entrainment from onset/flux periodicity and beat amplitude.
    # Tierney 2014: beat-locked neural responses in auditory cortex.
    e0 = torch.sigmoid(
        0.30 * onset_val_150ms
        + 0.30 * flux_max_150ms
        + 0.20 * onset_period_750ms
        + 0.20 * amp_val_150ms
    )

    # -- E1: WM Capacity --
    # Working memory load from energy, pitch, spectral, and entropy features.
    # Grahn 2009: SMA and putamen engaged during beat-based WM processing.
    e1 = torch.sigmoid(
        0.25 * energy_mean_500ms
        + 0.25 * pitch_std_500ms
        + 0.25 * spectral_vel_750ms
        + 0.25 * energy_entropy_900ms
    )

    # -- E2: Flexibility Cost --
    # Cost of switching routes: low entrainment + high long-term coupling
    # entropy + pitch context + timbral stability. High cost = rigid processing.
    # Tierney 2014: individual differences in flexibility predict performance.
    e2 = torch.sigmoid(
        0.30 * (1.0 - e0)
        + 0.30 * coupling_entropy_5s
        + 0.20 * pitch_mean_900ms
        + 0.20 * centroid_smooth_1s
    )

    # -- E3: Dissociation Index --
    # Absolute divergence between entrainment and WM routes.
    # Large dissociation = one route dominates; small = balanced processing.
    e3 = torch.abs(e0 - e1)

    return e0, e1, e2, e3
