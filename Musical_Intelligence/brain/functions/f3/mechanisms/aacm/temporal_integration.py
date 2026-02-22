"""AACM M-Layer -- Temporal Integration (2D).

Aesthetic engagement and real-time appreciation integrated over time:
  M0: aesthetic_engagement   (sustained engagement from attention and consonance)
  M1: rt_appreciation        (real-time aesthetic appreciation from savoring)

H3 demands consumed:
  pleasant:    (3,3,0,2)   reused -- consonance value at 100ms
  loudness:    (8,3,2,2)   loudness std at 100ms -- intensity variability

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/aacm/
Sarasso 2019: sustained aesthetic engagement correlates with N1/P2 (N=22).
Brattico 2013: real-time appreciation reflected in vmPFC sustained BOLD (N=18).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PLEAS_H3 = (3, 3, 0, 2)           # pleasant value at 100ms (reused)
_LOUD_STD_H3 = (8, 3, 2, 2)        # loudness std at 100ms


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: temporal integration of aesthetic attention signals.

    M0 integrates attentional engagement (E0) with consonance context and
    intensity variability to produce sustained aesthetic engagement.
    M1 integrates savoring effect (E2) with consonance to produce a
    real-time appreciation signal.

    Sarasso 2019: N1/P2 enhancement persists across consonant trials.
    Brattico 2013: aesthetic appreciation builds over sustained exposure.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, _e1, e2 = e

    pleasant_100ms = h3_features[_PLEAS_H3]
    loudness_std_100ms = h3_features[_LOUD_STD_H3]

    # -- M0: Aesthetic Engagement --
    # Sustained engagement from attentional capture (E0) modulated by
    # consonance context and intensity variability. High consonance
    # sustains engagement; loudness variability adds dynamic interest.
    # Sarasso 2019: consonant trials show sustained N1/P2 enhancement.
    m0 = torch.sigmoid(
        0.50 * e0
        + 0.30 * pleasant_100ms
        + 0.20 * loudness_std_100ms
    )

    # -- M1: Real-Time Appreciation --
    # Immediate aesthetic appreciation built from savoring (E2) and
    # consonance level. The savoring effect provides temporal depth
    # while consonance anchors the hedonic quality.
    # Brattico 2013: real-time appreciation ratings correlate with vmPFC.
    m1 = torch.sigmoid(
        0.50 * e2
        + 0.50 * pleasant_100ms
    )

    return m0, m1
