"""RPEM M-Layer -- Temporal Integration (2D).

Two derived signals from E-layer RPE components:

  rpe_magnitude       -- Unsigned RPE strength: max(f03, f04) [0, 1]
  vs_response         -- Signed RPE (VS BOLD proxy): clamp(f03 - f04 + 0.5) [0, 1]

SPECIAL: This layer uses torch.max and torch.clamp instead of sigmoid.
  - rpe_magnitude captures unsigned prediction error strength regardless of valence.
  - vs_response models the ventral striatum BOLD crossover interaction (Gold 2023).
    Values > 0.5 = positive RPE (VS activation), < 0.5 = negative RPE (VS deactivation).

H3 consumed (tuples 8-12):
    (21, 8, 8, 0)   spectral_flux velocity H8 L0     -- spectral velocity 500ms
    (10, 3, 0, 2)   onset_strength value H3 L2        -- onset 100ms
    (10, 4, 0, 2)   onset_strength value H4 L2        -- onset 125ms (theta)
    (10, 8, 2, 2)   onset_strength std H8 L2          -- onset variability 500ms
    (8, 3, 0, 2)    loudness value H3 L2              -- loudness 100ms

Gold 2023: VS BOLD scales with RPE magnitude; crossover d = 1.07.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 8-12 from demand spec) ---------------------------------
_SPEC_VEL_500MS = (21, 8, 8, 0)       # #8: spectral velocity 500ms
_ONSET_100MS = (10, 3, 0, 2)          # #9: onset 100ms
_ONSET_125MS = (10, 4, 0, 2)          # #10: onset 125ms (theta band)
_ONSET_STD_500MS = (10, 8, 2, 2)      # #11: onset variability 500ms
_LOUD_100MS = (8, 3, 0, 2)            # #12: loudness 100ms


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from E-layer RPE signals.

    SPECIAL: Uses torch.max and torch.clamp, NOT sigmoid.
      - rpe_magnitude = max(f03_positive_rpe, f04_negative_rpe)
      - vs_response = clamp(f03 - f04 + 0.5, 0.0, 1.0)

    The H3 demands provide event detection and salience context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.

    Returns:
        ``(rpe_magnitude, vs_response)`` each ``(B, T)``.
    """
    _f01, _f02, f03, f04 = e_outputs

    # H3 features are consumed but not directly used in the M-layer math;
    # they feed into the E-layer computations that produce f03/f04.
    # We reference them here for demand registration completeness.
    _ = h3_features[_SPEC_VEL_500MS]     # spectral velocity 500ms
    _ = h3_features[_ONSET_100MS]         # onset 100ms
    _ = h3_features[_ONSET_125MS]         # onset 125ms
    _ = h3_features[_ONSET_STD_500MS]     # onset variability 500ms
    _ = h3_features[_LOUD_100MS]          # loudness 100ms

    # rpe_magnitude: Absolute RPE magnitude
    # max(f03, f04) -- unsigned strength regardless of valence.
    # Gold 2023: VS BOLD scales with RPE magnitude.
    rpe_magnitude = torch.max(f03, f04)

    # vs_response: Ventral striatum BOLD response proxy
    # clamp(f03 - f04 + 0.5, 0, 1) -- signed RPE centered at 0.5.
    # > 0.5 = positive RPE (VS activation), < 0.5 = negative RPE (VS deactivation).
    # Gold 2023: surprise x liked = VS up, surprise x disliked = VS down (d = 1.07).
    vs_response = torch.clamp(f03 - f04 + 0.5, 0.0, 1.0)

    return rpe_magnitude, vs_response
