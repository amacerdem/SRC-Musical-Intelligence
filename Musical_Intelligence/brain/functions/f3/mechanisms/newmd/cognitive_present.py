"""NEWMD P-Layer -- Cognitive Present (2D).

Present-processing integration for entrainment-WM dissociation:
  P0: current_entrain   (current entrainment state, fusing E/M with loudness)
  P1: current_wm_load   (current WM engagement, fusing E/M with pitch complexity)

P0 integrates entrainment strength (E0), paradox magnitude (M0), and
loudness sustained level (H3) to estimate the current neural entrainment
state. Grahn 2009: louder stimuli produce stronger SMA/putamen activation.

P1 integrates WM capacity (E1), dual-route balance (M1), and pitch
complexity (H3) to estimate the current working memory load.
Tierney 2014: melodic complexity increases WM demand.

H3 demands consumed:
  loudness:     (8,16,1,0)  -- loudness mean 1s (sustained level)
  pitch_change: (23,8,3,0)  -- pitch std 500ms (melodic complexity)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/newmd/
Grahn 2009: fMRI, N=18.
Tierney 2014: behavioral+EEG, N=30.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_LOUDNESS_MEAN_1S = (8, 16, 1, 0)    # loudness mean 1s -- sustained level
_PITCH_STD_500MS = (23, 8, 3, 0)     # pitch std 500ms -- melodic complexity


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: current entrainment state and WM load.

    P0 fuses entrainment strength (E0) with paradox magnitude (M0) and
    loudness at 1s scale. Louder, more regular stimuli produce stronger
    current entrainment (Grahn 2009: louder beats activate SMA more).

    P1 fuses WM capacity (E1) with dual-route balance (M1) and pitch
    complexity at 500ms scale. Higher melodic complexity drives greater
    WM demand (Tierney 2014: pitch complexity loads WM).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, e1, _e2, _e3 = e
    m0, m1 = m

    loudness_mean_1s = h3_features[_LOUDNESS_MEAN_1S]    # (B, T)
    pitch_std_500ms = h3_features[_PITCH_STD_500MS]       # (B, T)

    # -- P0: Current Entrainment --
    # Entrainment state: E0 (extraction) + M0 (paradox) + loudness (sustained).
    # Grahn 2009: SMA/putamen activation increases with beat salience.
    p0 = torch.sigmoid(
        0.40 * e0
        + 0.30 * m0
        + 0.30 * loudness_mean_1s
    )

    # -- P1: Current WM Load --
    # WM engagement: E1 (capacity) + M1 (balance) + pitch complexity.
    # Tierney 2014: melodic complexity loads working memory.
    p1 = torch.sigmoid(
        0.40 * e1
        + 0.30 * m1
        + 0.30 * pitch_std_500ms
    )

    return p0, p1
