"""CDEM M-Layer -- Temporal Integration (2D).

Temporal dynamics of music-mood congruency and context-dependent recall:

  M0: congruency_index         -- Music-mood congruency estimation [0, 1]
  M1: context_recall_prob      -- P(recall | context reinstated) [0, 1]

H3 consumed:
    (3, 20, 1, 0)   stumpf_fusion mean H20 L0             -- binding over 5s
    (4, 20, 18, 0)  sensory_pleasantness trend H20 L0     -- pleasantness traj.
    (0, 20, 18, 0)  roughness trend H20 L0                -- valence trajectory
    (12, 20, 1, 0)  warmth mean H20 L0                    -- sustained warmth
    (22, 20, 1, 0)  entropy mean H20 L0                   -- average complexity

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cdem/CDEM-temporal-integration.md
Sachs 2025: within-context emotion correlation > across-context (r=0.303 vs 0.265).
Godden & Baddeley 1975: ~40% better recall in same context (N=18).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from .extraction import ExtractionResult

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_5S = (3, 20, 1, 0)
_PLEAS_TREND_5S = (4, 20, 18, 0)
_ROUGH_TREND_5S = (0, 20, 18, 0)
_WARMTH_MEAN_5S = (12, 20, 1, 0)
_ENTROPY_MEAN_5S = (22, 20, 1, 0)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_WARMTH = 12
_ENTROPY = 22
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    c: ExtractionResult,
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from C-layer + H3/R3.

    M0 (congruency_index): how well the current music's emotional content
    matches the listening context. Consonance times familiarity (pleasant
    + recognized = congruent) and consonance-timbre interaction times
    warmth (familiar timbre warmth = matching context).
    Sachs 2025: within-context emotion correlation > across-context.
    Sakakibara 2025: nostalgia enhances memory vividness (Cohen's r=0.88).

    M1 (context_recall_prob): probability that a memory trace will be
    successfully retrieved when the context is reinstated. Based on
    encoding specificity (Tulving & Thomson 1973).
    Godden & Baddeley 1975: ~40% better recall in same context (N=18).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        c: :class:`ExtractionResult` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    # -- H3 features --
    _stumpf_mean_5s = h3_features[_STUMPF_MEAN_5S]       # (B, T)
    _pleas_trend_5s = h3_features[_PLEAS_TREND_5S]       # (B, T)
    _rough_trend_5s = h3_features[_ROUGH_TREND_5S]       # (B, T)
    warmth_mean_5s = h3_features[_WARMTH_MEAN_5S]        # (B, T)
    entropy_mean_5s = h3_features[_ENTROPY_MEAN_5S]      # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]              # (B, T)
    warmth = r3_features[..., _WARMTH]                    # (B, T)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # -- Derived signals from C-layer --
    familiar = c.familiar
    retrieval = c.retrieval

    # -- M0: Congruency Index --
    # sigma(0.50 * (1 - roughness) * familiar + 0.50 * x_l5l7.mean * warmth)
    # Sachs 2025: within-context emotion correlation (r=0.303) > across-context
    m0 = torch.sigmoid(
        0.50 * (1.0 - roughness) * familiar
        + 0.50 * x_l5l7.mean(dim=-1) * warmth
    )

    # -- M1: Context Recall Probability --
    # sigma(0.35 * retrieval + 0.35 * familiar + 0.30 * (1 - entropy))
    # Godden & Baddeley 1975: ~40% better recall in same context
    # Billig 2022: hippocampal architecture for auditory context binding
    m1 = torch.sigmoid(
        0.35 * retrieval
        + 0.35 * familiar
        + 0.30 * (1.0 - r3_features[..., _ENTROPY])
    )

    return m0, m1
