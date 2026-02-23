"""HMCE E-Layer -- Extraction (3D).

Three features modeling hierarchical context at different timescales:

  f01: short_context   -- Local event-level context (100ms)
  f02: medium_context  -- Phrase-level context (250ms)
  f03: long_context    -- Formal structure context (1s)

H3 consumed:
    (17, 3, 14, 0)  spectral_autocorr periodicity H3  -- local pitch regularity
    (17, 3, 2, 0)   spectral_autocorr std H3           -- local pitch variability
    (11, 8, 14, 0)  onset_strength periodicity H8      -- rhythmic regularity
    (7, 3, 2, 0)    amplitude std H3                   -- dynamic variability
    (60, 8, 1, 0)   x_l0l2l5 mean H8                  -- medium-range integration
    (21, 16, 18, 0) spectral_change trend H16          -- long-range trajectory
    (60, 16, 1, 0)  x_l0l2l5 mean H16                 -- long-range structure
    (51, 16, 13, 0) x_l5l7 kurtosis H16               -- structural surprise

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hmce/HMCE-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_SPECTRAL_AUTO_PERIOD_H3 = (17, 3, 14, 0)
_SPECTRAL_AUTO_STD_H3 = (17, 3, 2, 0)
_ONSET_PERIOD_H8 = (11, 8, 14, 0)
_AMPLITUDE_STD_H3 = (7, 3, 2, 0)
_HIER_MEAN_H8 = (60, 8, 1, 0)
_SPECTRAL_CHANGE_TREND_H16 = (21, 16, 18, 0)
_HIER_MEAN_H16 = (60, 16, 1, 0)
_CONTEXT_KURT_H16 = (51, 16, 13, 0)

# -- R3 indices ----------------------------------------------------------------
_SPECTRAL_AUTO = 17
_ONSET_STRENGTH = 11


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from R3/H3.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(f01, f02, f03)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    spectral_auto_period = h3_features.get(_SPECTRAL_AUTO_PERIOD_H3, zero)
    spectral_auto_std = h3_features.get(_SPECTRAL_AUTO_STD_H3, zero)
    onset_period_h8 = h3_features.get(_ONSET_PERIOD_H8, zero)
    amplitude_std = h3_features.get(_AMPLITUDE_STD_H3, zero)
    hier_mean_h8 = h3_features.get(_HIER_MEAN_H8, zero)
    spectral_change_trend = h3_features.get(_SPECTRAL_CHANGE_TREND_H16, zero)
    hier_mean_h16 = h3_features.get(_HIER_MEAN_H16, zero)
    context_kurt = h3_features.get(_CONTEXT_KURT_H16, zero)

    # f01: Short Context -- local event-level encoding (100ms)
    # Koelsch 2009: A1 processes local pitch/onset at gamma-alpha timescale
    f01 = torch.sigmoid(
        0.35 * spectral_auto_period
        + 0.30 * amplitude_std
        + 0.35 * spectral_auto_std
    )

    # f02: Medium Context -- phrase-level structure (250ms)
    # Pearce 2018: theta-timescale integration for phrase structure
    f02 = torch.sigmoid(
        0.40 * hier_mean_h8
        + 0.35 * onset_period_h8
        + 0.25 * spectral_auto_period
    )

    # f03: Long Context -- formal structure (1s)
    # Koelsch 2009: MTG encodes long-range tonal/formal organization
    f03 = torch.sigmoid(
        0.30 * hier_mean_h16
        + 0.30 * spectral_change_trend
        + 0.25 * context_kurt
        + 0.15 * hier_mean_h8
    )

    return f01, f02, f03
