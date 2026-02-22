"""MMP F-Layer -- Cognitive Present (3D).

Three forward predictions for recognition, emotion, and scaffolding trajectories:

  F0: recognition_fc   -- Recognition accuracy prediction (1-5s) [0, 1]
  F1: emotional_fc     -- Emotional response prediction (2-10s) [0, 1]
  F2: scaffold_fc      -- Cognitive scaffolding prediction [0, 1]

H3 consumed:
    (4, 24, 1, 0)   sensory_pleasantness mean H24 L0    -- long-term pleasantness
    (22, 24, 1, 0)  entropy mean H24 L0                 -- long-term predictability
    (16, 20, 1, 0)  spectral_smoothness mean H20 L0     -- timbral quality

F-layer primarily reuses R+P outputs rather than reading new H3 tuples directly.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mmp/MMP-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PLEASANT_MEAN_36S = (4, 24, 1, 0)
_ENTROPY_MEAN_36S = (22, 24, 1, 0)
_SMOOTH_MEAN_5S = (16, 20, 1, 0)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D cognitive present (predictions) from R/P outputs + H3.

    Computes recognition trajectory, emotional response prediction, and
    cognitive scaffolding forecast for therapeutic planning.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r_outputs: ``(R0, R1, R2)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    r0, r1, r2 = r_outputs
    p0, p1, p2 = p_outputs

    # H3 features
    pleasant_mean = h3_features[_PLEASANT_MEAN_36S]
    entropy_mean = h3_features[_ENTROPY_MEAN_36S]
    smooth_mean = h3_features[_SMOOTH_MEAN_5S]

    # F0: Recognition prediction -- trajectory over H20 (5s)
    # Scarratt 2025: familiar music engages distributed memory network
    f0 = torch.sigmoid(
        0.35 * p0 + 0.30 * r1 + 0.20 * smooth_mean
        + 0.15 * p1
    )

    # F1: Emotional response prediction -- trajectory over H24 (36s)
    # Fang 2017: MT reduces cognitive decline in autobiographical memory
    f1 = torch.sigmoid(
        0.35 * p2 + 0.30 * pleasant_mean + 0.20 * r0
        + 0.15 * p0
    )

    # F2: Scaffold prediction -- session-level therapeutic benefit
    # Luxton 2025: Level 1 evidence for cognitive stimulation therapy
    # f09_scaffold * hippocampal_independence
    hippocampal_indep = torch.sigmoid(
        r0 - entropy_mean * 0.5
    )
    f2 = torch.sigmoid(
        0.50 * r2 * hippocampal_indep
        + 0.30 * p0
        + 0.20 * smooth_mean
    )

    return f0, f1, f2
