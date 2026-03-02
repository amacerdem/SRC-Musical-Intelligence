"""HCMC E-Layer -- Extraction (3D).

Hippocampal-cortical memory circuit feature extraction:

  E0: fast_binding          -- CA3 autoassociative binding of features [0, 1]
  E1: episodic_segmentation -- Event boundary detection at flux boundaries [0, 1]
  E2: cortical_storage      -- mPFC + PCC consolidation via replay [0, 1]

H3 consumed:
    (3, 16, 1, 2)   stumpf_fusion mean H16 L2       -- binding coherence at 1s
    (3, 16, 2, 2)   stumpf_fusion std H16 L2        -- binding variability at 1s
    (21, 16, 1, 2)  spectral_flux mean H16 L2       -- current segmentation rate
    (21, 16, 2, 2)  spectral_flux std H16 L2        -- flux variability at 1s
    (11, 16, 1, 2)  onset_strength mean H16 L2      -- event density at 1s
    (10, 16, 1, 2)  loudness mean H16 L2            -- encoding salience at 1s
    (7, 16, 1, 2)   amplitude mean H16 L2           -- energy level at 1s
    (5, 16, 1, 2)   harmonicity mean H16 L2         -- harmonic template at 1s
    (5, 20, 1, 0)   harmonicity mean H20 L0         -- harmonic stability over 5s
    (14, 16, 1, 2)  tonalness mean H16 L2           -- melodic content at 1s
    (14, 20, 22, 0) tonalness autocorrelation H20 L0 -- tonal repetition over 5s
    (22, 16, 1, 2)  entropy mean H16 L2             -- current pattern complexity

R3 consumed:
    [3]      stumpf_fusion  -- E0: binding coherence proxy
    [5]      harmonicity    -- E2: harmonic template match
    [7]      amplitude      -- E0: encoding salience
    [10]     loudness       -- E0: arousal correlate
    [11]     onset_strength -- E0+E1: event boundary marker
    [14]     tonalness      -- E2: melodic encoding quality
    [21]     spectral_flux  -- E1: segmentation trigger
    [22]     entropy        -- E1+E2: encoding difficulty
    [25:33]  x_l0l5         -- E0: fast hippocampal binding
    [41:49]  x_l5l7         -- E2: cortical long-term template

See Building/C3-Brain/F4-Memory-Systems/mechanisms/hcmc/HCMC-extraction.md
Rolls 2013: CA3 autoassociative network for fast pattern binding.
Zacks et al. 2007: Event segmentation theory -- boundaries trigger encoding.
Liu et al. 2024: Replay-triggered hippocampal-cortical transfer.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_1S = (3, 16, 1, 2)        # stumpf_fusion mean H16 L2
_STUMPF_STD_1S = (3, 16, 2, 2)         # stumpf_fusion std H16 L2
_FLUX_MEAN_1S = (21, 16, 1, 2)         # spectral_flux mean H16 L2
_FLUX_STD_1S = (21, 16, 2, 2)          # spectral_flux std H16 L2
_ONSET_MEAN_1S = (11, 16, 1, 2)        # onset_strength mean H16 L2
_LOUD_MEAN_1S = (10, 16, 1, 2)         # loudness mean H16 L2
_AMP_MEAN_1S = (7, 16, 1, 2)           # amplitude mean H16 L2
_HARM_MEAN_1S = (5, 16, 1, 2)          # harmonicity mean H16 L2
_HARM_MEAN_5S = (5, 20, 1, 0)          # harmonicity mean H20 L0
_TONAL_MEAN_1S = (14, 16, 1, 2)        # tonalness mean H16 L2
_TONAL_AUTOCORR_5S = (14, 20, 22, 0)   # tonalness autocorrelation H20 L0
_ENTROPY_MEAN_1S = (22, 16, 1, 2)      # entropy mean H16 L2

# -- R3 indices ----------------------------------------------------------------
_STUMPF_FUSION = 3
_HARMONICITY = 5
_AMPLITUDE = 7
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_TONALNESS = 14
_SPECTRAL_FLUX = 21
_ENTROPY = 22
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 features.

    E0 (fast_binding): Hippocampal CA3 autoassociative binding of incoming
    features into an episodic trace. Uses cross-domain interactions (x_l0l5)
    multiplied by tonal fusion (stumpf) at the 1s binding window.
    Rolls 2013: CA3 autoassociative binding.

    E1 (episodic_segmentation): Event boundary detection where musical
    structure changes, triggering new episodic segments. Spectral flux is
    the primary trigger; entropy and onset strength provide confirmation.
    Zacks et al. 2007: event segmentation theory.

    E2 (cortical_storage): Long-term cortical consolidation from hippocampal
    traces into mPFC/PCC. Uses consonance-timbre interactions (x_l5l7) and
    harmonic stability as templates for durable cortical storage.
    Liu et al. 2024: replay-triggered hippocampal-cortical transfer.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    # -- H3 features --
    stumpf_mean_1s = h3_features[_STUMPF_MEAN_1S]       # (B, T)
    flux_mean_1s = h3_features[_FLUX_MEAN_1S]            # (B, T)
    onset_mean_1s = h3_features[_ONSET_MEAN_1S]          # (B, T)
    loud_mean_1s = h3_features[_LOUD_MEAN_1S]            # (B, T)
    harm_mean_5s = h3_features[_HARM_MEAN_5S]            # (B, T)
    tonal_autocorr_5s = h3_features[_TONAL_AUTOCORR_5S]  # (B, T)
    entropy_mean_1s = h3_features[_ENTROPY_MEAN_1S]      # (B, T)

    # -- R3 features --
    stumpf = r3_features[..., _STUMPF_FUSION]            # (B, T)
    onset_str = r3_features[..., _ONSET_STRENGTH]        # (B, T)
    loudness = r3_features[..., _LOUDNESS]               # (B, T)
    flux = r3_features[..., _SPECTRAL_FLUX]              # (B, T)
    entropy = r3_features[..., _ENTROPY]                 # (B, T)
    harmonicity = r3_features[..., _HARMONICITY]         # (B, T)
    tonalness = r3_features[..., _TONALNESS]             # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # -- E0: Fast Binding --
    # CA3 autoassociative binding of features. Cross-domain interactions
    # (x_l0l5 = Energy x Consonance) multiplied by stumpf fusion at 1s.
    # Rolls 2013: CA3 autoassociative network for fast pattern binding.
    # Cheung et al. 2019: hippocampal uncertainty encoding.
    # f19 = sigma(0.35 * x_l0l5.mean * stumpf_mean_1s
    #           + 0.35 * stumpf * stumpf_mean_1s
    #           + 0.30 * onset_str * loudness)
    e0 = torch.sigmoid(
        0.35 * x_l0l5.mean(dim=-1) * stumpf_mean_1s
        + 0.35 * stumpf * stumpf_mean_1s
        + 0.30 * onset_str * loudness
    )

    # -- E1: Episodic Segmentation --
    # Event boundary detection via spectral flux boundaries.
    # Zacks et al. 2007: event boundaries trigger hippocampal encoding.
    # f20 = sigma(0.40 * flux * flux_mean_1s
    #           + 0.30 * entropy * flux
    #           + 0.30 * onset_str * flux)
    e1 = torch.sigmoid(
        0.40 * flux * flux_mean_1s
        + 0.30 * entropy * flux
        + 0.30 * onset_str * flux
    )

    # -- E2: Cortical Storage --
    # Long-term cortical pattern storage via mPFC + PCC consolidation.
    # Liu et al. 2024: hippocampal replay drives mPFC consolidation.
    # f21 = sigma(0.35 * x_l5l7.mean * harmonicity_mean_5s
    #           + 0.35 * harmonicity * tonalness_autocorr_5s
    #           + 0.30 * (1-entropy) * harmonicity * tonalness)
    # Harmonicity gate on Term 3: prevents inharmonic stimuli from
    # bypassing the harmonic quality requirement for cortical consolidation.
    # Liu et al. 2024: durable cortical storage requires harmonic templates.
    e2 = torch.sigmoid(
        0.35 * x_l5l7.mean(dim=-1) * harm_mean_5s
        + 0.35 * harmonicity * tonal_autocorr_5s
        + 0.30 * (1.0 - entropy) * harmonicity * tonalness
    )

    return e0, e1, e2
