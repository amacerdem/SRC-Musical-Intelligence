"""IOTMS E-Layer -- Extraction (4D).

Individual opioid-reward sensitivity features:
  f01: mor_baseline_proxy    -- MOR availability proxy (trait) [0, 1]
  f02: pleasure_bold_slope   -- Pleasure-BOLD coupling slope [0, 1]
  f03: reward_propensity     -- Music reward propensity index [0, 1]
  f04: music_reward_index    -- Overall music reward sensitivity [0, 1]

MOR baseline proxy (f01) anchors the entire IOTMS cascaded chain by
estimating trait-level mu-opioid receptor availability from sustained
hedonic quality (mean pleasantness at 1s) and consonance quality
(inverse roughness skewness at 1s).

Pleasure-BOLD slope (f02) captures how steeply subjective pleasure
maps onto neural BOLD response, modulated by f01 and mean loudness.
Putkinen 2025: MOR BPND correlated with pleasure-BOLD slope (d=1.16).

Reward propensity (f03) combines pleasure-BOLD coupling with
sustained opioid-perceptual coupling interaction (x_l4l5 at 1s).
Mas-Herrero 2014: BMRQ predicted music pleasure (R^2=0.30).

Music reward index (f04) integrates reward propensity with coupling
trend and harmonic richness (tristimulus1).
Martinez-Molina 2016: BMRQ predicted pleasure ratings (R^2=0.40).

The computation is cascaded sequential: f01 -> f02 -> f03 -> f04.
Each feature feeds the next, forming a trait estimation chain.

H3 demands consumed (12):
  (4,  8,  0, 2) sensory_pleasantness mean H8  L2  -- hedonic at 500ms
  (4,  16, 0, 2) sensory_pleasantness mean H16 L2  -- hedonic at 1s
  (4,  16, 2, 2) sensory_pleasantness std  H16 L2  -- hedonic variability
  (0,  8,  0, 2) roughness mean H8  L2             -- roughness at 500ms
  (0,  16, 6, 2) roughness skew H16 L2             -- roughness skewness
  (8,  8,  0, 2) loudness mean H8  L2              -- loudness at 500ms
  (8,  16, 0, 2) loudness mean H16 L2              -- loudness at 1s
  (33, 8,  0, 2) x_l4l5[0] mean H8  L2            -- coupling at 500ms
  (33, 16, 0, 2) x_l4l5[0] mean H16 L2            -- coupling at 1s
  (33, 16, 18, 2) x_l4l5[0] trend H16 L2          -- coupling trend
  (14, 16, 0, 2) tristimulus1 mean H16 L2          -- harmonic richness
  (14, 16, 2, 2) tristimulus1 std  H16 L2          -- tristimulus variability

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/iotms/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (12 tuples) --------------------------------------
# f01: MOR baseline proxy
_PLEASANT_MEAN_H8 = (4, 8, 0, 2)       # mean sensory_pleasantness H8 L2
_PLEASANT_MEAN_H16 = (4, 16, 0, 2)     # mean sensory_pleasantness H16 L2
_PLEASANT_STD_H16 = (4, 16, 2, 2)      # std sensory_pleasantness H16 L2
_ROUGH_MEAN_H8 = (0, 8, 0, 2)          # mean roughness H8 L2
_ROUGH_SKEW_H16 = (0, 16, 6, 2)        # skew roughness H16 L2

# f02: pleasure-BOLD slope
_LOUD_MEAN_H8 = (8, 8, 0, 2)           # mean loudness H8 L2
_LOUD_MEAN_H16 = (8, 16, 0, 2)         # mean loudness H16 L2

# f03: reward propensity
_COUPLING_MEAN_H8 = (33, 8, 0, 2)      # mean x_l4l5[0] H8 L2
_COUPLING_MEAN_H16 = (33, 16, 0, 2)    # mean x_l4l5[0] H16 L2

# f04: music reward index
_COUPLING_TREND_H16 = (33, 16, 18, 2)  # trend x_l4l5[0] H16 L2
_TRISTIM_MEAN_H16 = (14, 16, 0, 2)     # mean tristimulus1 H16 L2
_TRISTIM_STD_H16 = (14, 16, 2, 2)      # std tristimulus1 H16 L2


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D cascaded opioid-reward trait features.

    Cascaded sequential computation:
      f01 (MOR baseline) -> f02 (pleasure-BOLD slope) ->
      f03 (reward propensity) -> f04 (music reward index)

    Each feature builds on the previous, forming a trait estimation
    chain from neurochemical baseline to composite reward sensitivity.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"MORMR": (B, T, D), "DAED": (B, T, D)}``.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``.
    """
    # -- H3 features for f01 --
    pleasant_mean_1s = h3_features[_PLEASANT_MEAN_H16]      # (B, T)
    rough_skew_1s = h3_features[_ROUGH_SKEW_H16]            # (B, T)

    # -- H3 features for f02 --
    loud_mean_1s = h3_features[_LOUD_MEAN_H16]              # (B, T)

    # -- H3 features for f03 --
    coupling_mean_1s = h3_features[_COUPLING_MEAN_H16]      # (B, T)

    # -- H3 features for f04 --
    coupling_trend_1s = h3_features[_COUPLING_TREND_H16]    # (B, T)
    tristim_mean_1s = h3_features[_TRISTIM_MEAN_H16]        # (B, T)

    # -- f01: MOR baseline proxy (anchor) --
    # sigma(0.35 * mean_pleasantness_1s + 0.30 * (1 - roughness_skew_1s))
    # Remaining 0.35 goes to implicit bias (sigmoid center).
    # Putkinen 2025: baseline MOR predicted pleasure-BOLD in insula,
    # ACC, SMA, STG, NAcc, thalamus.
    f01 = torch.sigmoid(
        0.35 * pleasant_mean_1s
        + 0.30 * (1.0 - rough_skew_1s)
    )

    # -- f02: Pleasure-BOLD coupling slope (depends on f01) --
    # sigma(0.40 * f01 + 0.30 * mean_loudness_1s)
    # Putkinen 2025: MOR BPND correlated with pleasure-BOLD slope (d=1.16).
    f02 = torch.sigmoid(
        0.40 * f01
        + 0.30 * loud_mean_1s
    )

    # -- f03: Reward propensity (depends on f02) --
    # sigma(0.35 * f02 + 0.35 * sustained_coupling_1s)
    # Mas-Herrero 2014: BMRQ predicted music pleasure (R^2=0.30).
    f03 = torch.sigmoid(
        0.35 * f02
        + 0.35 * coupling_mean_1s
    )

    # -- f04: Music reward index (depends on f03) --
    # sigma(0.40 * f03 + 0.30 * coupling_trend_1s + 0.30 * mean_tristimulus_1s)
    # Martinez-Molina 2016: BMRQ predicted pleasure ratings (R^2=0.40).
    f04 = torch.sigmoid(
        0.40 * f03
        + 0.30 * coupling_trend_1s
        + 0.30 * tristim_mean_1s
    )

    return f01, f02, f03, f04
