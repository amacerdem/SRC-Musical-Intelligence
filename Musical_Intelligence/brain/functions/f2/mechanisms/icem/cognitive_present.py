"""ICEM P-Layer — Cognitive Present (2D).

Present-processing surprise and emotional evaluation:
  P0: surprise_signal       (IC computation result in present)
  P1: emotional_evaluation  (valence change assessment)

H3 demands consumed:
  spectral_flux:      (21,3,13,2) reused from E-layer
  loudness:           (10,3,0,2)
  key_clarity:        (51,3,0,2)
  tonal_stability:    (60,8,0,0)

See Docs/C3/Models/PCU-a3-ICEM/ICEM.md §6.1 Layer P.
Cheung 2019: amygdala/hippocampus uncertainty × surprise.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_SPECTRAL_FLUX_H3_ENTROPY = (21, 3, 13, 2)
_LOUDNESS_H3_VAL = (10, 3, 0, 2)
_KEY_CLARITY_H3_VAL = (51, 3, 0, 2)
_TONAL_STAB_H8_VAL = (60, 8, 0, 0)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: present surprise and emotional evaluation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.
        m: ``(M0, M1, M2, M3, M4)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, _e1, _e2, _e3 = e
    m0, m1, m2, _m3, _m4 = m

    spectral_flux_entropy = h3_features[_SPECTRAL_FLUX_H3_ENTROPY]
    loudness_100ms = h3_features[_LOUDNESS_H3_VAL]
    key_clarity_100ms = h3_features[_KEY_CLARITY_H3_VAL]
    tonal_stab_500ms = h3_features[_TONAL_STAB_H8_VAL]

    # -- P0: Surprise Signal --
    # Present-moment IC computation result. Integrates refined IC value +
    # raw IC proxy + spectral entropy + loudness (loud events are salient).
    # Cheung 2019: amygdala/hippocampus process uncertainty × surprise.
    p0 = torch.sigmoid(
        0.35 * m0
        + 0.25 * e0
        + 0.20 * spectral_flux_entropy
        + 0.20 * loudness_100ms
    )

    # -- P1: Emotional Evaluation --
    # Present-moment valence assessment. Valence prediction + arousal
    # context + tonal clarity + structural stability.
    # Gold 2019: inverted-U for IC on liking (p<0.001).
    p1 = torch.sigmoid(
        0.30 * m2
        + 0.25 * m1
        + 0.25 * key_clarity_100ms
        + 0.20 * tonal_stab_500ms
    )

    return p0, p1
