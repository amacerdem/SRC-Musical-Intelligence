"""IGFE E-Layer -- Extraction (4D).

Four explicit features modeling gamma-frequency match and cognitive enhancement:

  E0: igf_match               -- Individual gamma frequency match [0, 1]
  E1: memory_enhancement      -- Gamma-mediated memory boost [0, 1]
  E2: executive_enhancement   -- Gamma-mediated executive boost [0, 1]
  E3: dose_response           -- Dose-dependent accumulation signal [0, 1]

H3 consumed:
    (5, 0, 0, 2)   periodicity value 25ms L2       -- gamma-range match
    (5, 1, 0, 2)   periodicity value 50ms L2       -- gamma tracking
    (10, 0, 0, 2)  spectral flux 25ms L2           -- gamma-range onset
    (41, 16, 1, 0) cognitive coupling mean 1s L0    -- dose accumulation
    (41, 8, 0, 0)  cognitive coupling value 500ms L0 -- integration
    (41, 16, 18, 0) cognitive coupling trend 1s L0  -- trajectory
    (7, 16, 1, 2)  amplitude mean 1s L2            -- intensity context

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/igfe/IGFE-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PERIOD_25MS = (5, 0, 0, 2)          # periodicity value 25ms L2
_PERIOD_50MS = (5, 1, 0, 2)          # periodicity value 50ms L2
_FLUX_25MS = (10, 0, 0, 2)           # spectral flux 25ms L2
_COG_COUPLING_MEAN_1S = (41, 16, 1, 0)   # cognitive coupling mean 1s L0
_COG_COUPLING_500MS = (41, 8, 0, 0)      # cognitive coupling value 500ms L0
_COG_COUPLING_TREND_1S = (41, 16, 18, 0) # cognitive coupling trend 1s L0
_AMP_MEAN_1S = (7, 16, 1, 2)         # amplitude mean 1s L2


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """E-layer: 4D extraction from H3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``.
    """
    period_25ms = h3_features[_PERIOD_25MS]
    period_50ms = h3_features[_PERIOD_50MS]
    flux_25ms = h3_features[_FLUX_25MS]
    cog_coupling_mean_1s = h3_features[_COG_COUPLING_MEAN_1S]
    cog_coupling_500ms = h3_features[_COG_COUPLING_500MS]
    cog_coupling_trend_1s = h3_features[_COG_COUPLING_TREND_1S]
    amp_mean_1s = h3_features[_AMP_MEAN_1S]

    # E0: IGF match -- gamma-range periodicity at 25ms and 50ms + onset
    # Baltus 2018: tACS at IGF enhances temporal resolution via phase-locking
    e0 = torch.sigmoid(
        0.35 * period_25ms + 0.35 * period_50ms
        + 0.30 * flux_25ms
    )

    # E1: Memory enhancement -- IGF match drives hippocampal gamma boost
    # Rufener 2016: gamma tACS improves phoneme categorization via memory
    e1 = torch.sigmoid(
        0.40 * e0 + 0.30 * cog_coupling_mean_1s
        + 0.30 * cog_coupling_500ms
    )

    # E2: Executive enhancement -- IGF match drives DLPFC gamma boost
    # Rufener 2016: cognitive improvement via executive-gamma pathway
    e2 = torch.sigmoid(
        0.40 * e0 + 0.30 * cog_coupling_500ms
        + 0.30 * amp_mean_1s
    )

    # E3: Dose response -- accumulated stimulation effect over time
    # Rufener 2016: dose-dependent accumulation over 20-minute sessions
    e3 = torch.sigmoid(
        0.50 * cog_coupling_trend_1s + 0.50 * amp_mean_1s
    )

    return e0, e1, e2, e3
