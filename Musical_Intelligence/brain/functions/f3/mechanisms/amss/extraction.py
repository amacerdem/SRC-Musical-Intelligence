"""AMSS E-Layer -- Extraction (5D).

Five explicit features modeling stream segregation cues and attention gating:

  E0: onset_tracking          -- Event boundary detection for stream parsing [0, 1]
  E1: harmonic_segregation    -- Harmonic content driving stream separation [0, 1]
  E2: spectral_stream         -- Spectral identity of current stream [0, 1]
  E3: temporal_stream          -- Temporal regularity of current stream [0, 1]
  E4: attention_gate           -- Top-down attention gain on stream selection [0, 1]

H3 consumed:
    (11, 8, 0, 2)   onset value 500ms L2            -- event boundary
    (11, 8, 14, 2)  onset periodicity 500ms L2       -- stream rhythm
    (7, 8, 0, 2)    amplitude value 500ms L2         -- stream energy
    (14, 8, 0, 2)   tonalness value 500ms L2         -- harmonic content
    (14, 14, 1, 0)  tonalness mean ~900ms L0         -- sustained tonal
    (15, 8, 0, 2)   centroid value 500ms L2          -- spectral identity
    (21, 8, 8, 0)   spectral velocity 500ms L0       -- change rate
    (15, 8, 2, 2)   centroid std 500ms L2            -- spectral spread
    (7, 8, 1, 2)    amplitude mean 500ms L2          -- stream level
    (8, 8, 0, 2)    loudness value 500ms L2          -- stream loudness
    (10, 8, 1, 2)   flux mean 500ms L2               -- spectral change
    (25, 8, 0, 2)   coupling value 500ms L2          -- binding
    (8, 8, 2, 2)    loudness std 500ms L2            -- dynamic range

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/amss/
Elhilali 2009: spectral coherence + temporal regularity drive stream formation.
Alain 2007: harmonic segregation indexed by ORN in EEG.
Bregman 1994: onset synchrony and frequency proximity as grouping cues.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ONSET_VAL_500MS = (11, 8, 0, 2)
_ONSET_PERIOD_500MS = (11, 8, 14, 2)
_AMP_VAL_500MS = (7, 8, 0, 2)
_TONALNESS_VAL_500MS = (14, 8, 0, 2)
_TONALNESS_MEAN_900MS = (14, 14, 1, 0)
_CENTROID_VAL_500MS = (15, 8, 0, 2)
_SPECTRAL_VEL_500MS = (21, 8, 8, 0)
_CENTROID_STD_500MS = (15, 8, 2, 2)
_AMP_MEAN_500MS = (7, 8, 1, 2)
_LOUDNESS_VAL_500MS = (8, 8, 0, 2)
_FLUX_MEAN_500MS = (10, 8, 1, 2)
_COUPLING_VAL_500MS = (25, 8, 0, 2)
_LOUDNESS_STD_500MS = (8, 8, 2, 2)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """E-layer: 5D extraction from H3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(E0, E1, E2, E3, E4)`` each ``(B, T)``.
    """
    onset_val = h3_features[_ONSET_VAL_500MS]
    onset_period = h3_features[_ONSET_PERIOD_500MS]
    amp_val = h3_features[_AMP_VAL_500MS]
    tonalness_val = h3_features[_TONALNESS_VAL_500MS]
    tonalness_mean = h3_features[_TONALNESS_MEAN_900MS]
    centroid_val = h3_features[_CENTROID_VAL_500MS]
    spectral_vel = h3_features[_SPECTRAL_VEL_500MS]
    centroid_std = h3_features[_CENTROID_STD_500MS]
    amp_mean = h3_features[_AMP_MEAN_500MS]
    loudness_val = h3_features[_LOUDNESS_VAL_500MS]
    flux_mean = h3_features[_FLUX_MEAN_500MS]
    coupling_val = h3_features[_COUPLING_VAL_500MS]
    loudness_std = h3_features[_LOUDNESS_STD_500MS]

    # E0: Onset tracking -- event boundary detection for stream parsing
    # Bregman 1994: onset synchrony is a primary grouping cue
    e0 = torch.sigmoid(
        0.40 * onset_val + 0.30 * onset_period
        + 0.30 * amp_val
    )

    # E1: Harmonic segregation -- tonal content drives stream separation
    # Alain 2007: mistuned harmonics produce ORN, indexing segregation
    e1 = torch.sigmoid(
        0.40 * tonalness_val + 0.30 * tonalness_mean
        + 0.30 * centroid_val
    )

    # E2: Spectral stream -- spectral identity of current stream
    # Elhilali 2009: spectral coherence drives stream formation
    e2 = torch.sigmoid(
        0.40 * centroid_val + 0.30 * spectral_vel
        + 0.30 * centroid_std
    )

    # E3: Temporal stream -- temporal regularity of current stream
    # Bregman 1994: temporal regularity promotes stream integration
    e3 = torch.sigmoid(
        0.40 * onset_period + 0.30 * amp_mean
        + 0.30 * loudness_val
    )

    # E4: Attention gate -- top-down gain on stream selection
    # Elhilali 2009: attention biases competition between streams
    e4 = torch.sigmoid(
        0.35 * flux_mean + 0.35 * coupling_val
        + 0.30 * loudness_std
    )

    return e0, e1, e2, e3, e4
