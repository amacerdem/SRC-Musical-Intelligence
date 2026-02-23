"""TPIO E-Layer -- Extraction (4D).

Four features modeling perception-imagery substrates for timbre:

  f01: perception_substrate  -- Real-time spectral encoding quality
  f02: imagery_substrate     -- Internally generated timbral representation
  f03: perc_imag_overlap     -- Degree of perception-imagery overlap
  f04: sma_imagery           -- SMA contribution to timbral motor imagery

H3 consumed:
    (12, 2, 0, 2)   warmth value H2 L2        -- instant warmth for timbral quality
    (13, 2, 0, 2)   sharpness value H2 L2     -- instant sharpness for spectral edge
    (14, 5, 1, 0)   tonalness mean H5 L0      -- pitch clarity context
    (15, 5, 0, 0)   clarity value H5 L0       -- spectral resolution
    (18, 2, 0, 2)   tristimulus1 H2 L2        -- fundamental energy
    (19, 2, 0, 2)   tristimulus2 H2 L2        -- mid-partial energy
    (20, 2, 0, 2)   tristimulus3 H2 L2        -- high-partial energy
    (12, 14, 1, 0)  warmth mean H14 L0        -- sustained warmth memory
    (14, 14, 1, 0)  tonalness mean H14 L0     -- sustained tonal clarity
    (18, 20, 1, 0)  tristimulus1 mean H20 L0  -- long-term fundamental
    (8, 20, 1, 0)   loudness mean H20 L0      -- sustained loudness baseline
    (7, 20, 18, 0)  amplitude trend H20 L0    -- dynamic envelope trajectory

R3 consumed:
    [12] warmth       -- timbral warmth
    [13] sharpness    -- spectral sharpness
    [14] tonalness    -- pitch clarity
    [18] tristimulus1 -- fundamental energy

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/tpio/TPIO-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_WARMTH_H2 = (12, 2, 0, 2)
_SHARPNESS_H2 = (13, 2, 0, 2)
_TONALNESS_MEAN_H5 = (14, 5, 1, 0)
_CLARITY_H5 = (15, 5, 0, 0)
_TRIST1_H2 = (18, 2, 0, 2)
_TRIST2_H2 = (19, 2, 0, 2)
_TRIST3_H2 = (20, 2, 0, 2)
_WARMTH_MEAN_H14 = (12, 14, 1, 0)
_TONALNESS_MEAN_H14 = (14, 14, 1, 0)
_TRIST1_MEAN_H20 = (18, 20, 1, 0)
_LOUDNESS_MEAN_H20 = (8, 20, 1, 0)
_AMPLITUDE_TREND_H20 = (7, 20, 18, 0)

# -- R3 indices ----------------------------------------------------------------
_WARMTH = 12
_SHARPNESS = 13
_TONALNESS = 14
_TRIST1 = 18


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """E-layer: 4D extraction from R3/H3.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    warmth_h2 = h3_features.get(_WARMTH_H2, zero)
    sharpness_h2 = h3_features.get(_SHARPNESS_H2, zero)
    tonalness_mean_h5 = h3_features.get(_TONALNESS_MEAN_H5, zero)
    clarity_h5 = h3_features.get(_CLARITY_H5, zero)
    trist1_h2 = h3_features.get(_TRIST1_H2, zero)
    trist2_h2 = h3_features.get(_TRIST2_H2, zero)
    trist3_h2 = h3_features.get(_TRIST3_H2, zero)
    warmth_mean_h14 = h3_features.get(_WARMTH_MEAN_H14, zero)
    tonalness_mean_h14 = h3_features.get(_TONALNESS_MEAN_H14, zero)
    trist1_mean_h20 = h3_features.get(_TRIST1_MEAN_H20, zero)
    loudness_mean_h20 = h3_features.get(_LOUDNESS_MEAN_H20, zero)
    amplitude_trend_h20 = h3_features.get(_AMPLITUDE_TREND_H20, zero)

    # R3 direct
    warmth_r3 = r3_features[:, :, _WARMTH]
    sharpness_r3 = r3_features[:, :, _SHARPNESS]
    tonalness_r3 = r3_features[:, :, _TONALNESS]
    trist1_r3 = r3_features[:, :, _TRIST1]

    # f01: Perception Substrate -- real-time spectral encoding
    # Halpern 2004: pSTG processes warmth + sharpness for timbral quality
    f01 = torch.sigmoid(
        0.25 * warmth_h2
        + 0.25 * sharpness_h2
        + 0.20 * trist1_h2
        + 0.15 * clarity_h5
        + 0.15 * tonalness_mean_h5
    )

    # f02: Imagery Substrate -- internally generated timbral representation
    # Crowder 1989: imagery preserves spectral detail from memory
    f02 = torch.sigmoid(
        0.30 * warmth_mean_h14
        + 0.25 * tonalness_mean_h14
        + 0.20 * trist1_mean_h20
        + 0.15 * loudness_mean_h20
        + 0.10 * amplitude_trend_h20
    )

    # f03: Perception-Imagery Overlap -- degree of shared substrate
    # Halpern 2004: overlap in pSTG between perceived and imagined timbre
    f03 = torch.sigmoid(
        0.40 * f01 * f02
        + 0.30 * warmth_r3 * warmth_mean_h14
        + 0.30 * trist1_r3 * trist1_mean_h20
    )

    # f04: SMA Imagery -- motor imagery contribution to timbral production
    # Zatorre 2005: SMA activation during timbral imagery
    trist_spectral = (trist1_h2 + trist2_h2 + trist3_h2) / 3.0
    f04 = torch.sigmoid(
        0.35 * trist_spectral
        + 0.25 * tonalness_r3
        + 0.20 * sharpness_r3
        + 0.20 * f02
    )

    return f01, f02, f03, f04
