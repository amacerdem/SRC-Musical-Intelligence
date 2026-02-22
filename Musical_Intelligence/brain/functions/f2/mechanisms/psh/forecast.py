"""PSH F-Layer — Forecast (3D).

Forward predictions for silencing and persistence dynamics:
  F0: post_stim_silencing   (predicted degree of post-stimulus silencing)
  F1: error_persistence     (predicted persistence of low-level PE)
  F2: next_prediction       (predicted accuracy of next top-down prediction)

F0 predicts how strongly high-level representations will be silenced
in the upcoming window. Based on current silencing efficiency (M-layer)
and long-range tonal stability context (H3).

F1 predicts how strongly low-level PE will persist. Based on current
sensory persistence (P1) and ongoing amplitude/onset dynamics (H3).

F2 predicts the accuracy of the next top-down prediction cycle. Based
on current prediction match (P0) and high-level coupling trends (H3).

H3 demands consumed:
  tonal_stability:  (41,8,0,0) reused, (41,16,1,0) reused
  amplitude:        (7,1,0,2) reused
  onset_strength:   (10,0,0,2) reused
  chroma_C:         (25,0,0,2), (25,3,0,2), (25,3,16,2)

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/psh/
de Vries & Wurm 2023: predictive hierarchy generates forward expectations.
Wacongne 2012: two PE systems with distinct forward dynamics.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
# High-level coupling context (reused from M-layer)
_TONAL_H8_VAL = (41, 8, 0, 0)       # tonal_stability at 500ms value memory
_TONAL_H16_MEAN = (41, 16, 1, 0)    # tonal_stability at 1s mean memory

# Low-level sensory dynamics (reused)
_AMP_H1_VAL = (7, 1, 0, 2)          # amplitude at 50ms value integration
_ONSET_H0_VAL = (11, 0, 0, 2)       # onset_strength at 25ms value integration

# Chroma coupling (low-level forward predictions)
_CHROMA_H0_VAL = (25, 0, 0, 2)      # chroma_C at 25ms value integration
_CHROMA_H3_VAL = (25, 3, 0, 2)      # chroma_C at 100ms value integration
_CHROMA_H3_CURV = (25, 3, 16, 2)    # chroma_C at 100ms curvature integration


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for silencing dynamics.

    F0 projects post-stimulus silencing based on high-level coupling
    strength and extraction. When tonal stability is high (strong
    predictions), silencing is predicted to be strong.

    F1 projects error persistence based on low-level sensory context.
    Amplitude and onset dynamics predict ongoing PE generation.

    F2 projects next prediction accuracy based on current prediction
    match (P0) and chroma coupling trends (forward extrapolation).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    e0, e1 = e
    p0, p1, _p2 = p

    # -- H3 features --
    tonal_h8 = h3_features[_TONAL_H8_VAL]
    tonal_h16_mean = h3_features[_TONAL_H16_MEAN]
    amp_h1 = h3_features[_AMP_H1_VAL]
    onset_h0 = h3_features[_ONSET_H0_VAL]
    chroma_h0 = h3_features[_CHROMA_H0_VAL]
    chroma_h3 = h3_features[_CHROMA_H3_VAL]
    chroma_h3_curv = h3_features[_CHROMA_H3_CURV]

    # -- F0: Post-Stimulus Silencing --
    # Predicted silencing of high-level representations.
    # Strong tonal context (long-range stability) + high E0 (high-level
    # features available for silencing) = strong predicted silencing.
    # de Vries & Wurm 2023: predictable stimuli produce stronger silencing.
    f0 = torch.sigmoid(
        0.35 * e0
        + 0.35 * tonal_h16_mean
        + 0.30 * tonal_h8
    )

    # -- F1: Error Persistence --
    # Predicted persistence of low-level PE signals.
    # Ongoing sensory dynamics (amplitude, onset) predict continued
    # PE generation regardless of prediction accuracy.
    # Wacongne 2012: local PE system in auditory cortex is persistent.
    f1 = torch.sigmoid(
        0.35 * e1
        + 0.25 * p1
        + 0.20 * amp_h1
        + 0.20 * onset_h0
    )

    # -- F2: Next Prediction --
    # Predicted accuracy of the upcoming top-down prediction cycle.
    # Current prediction match (P0) extrapolated with chroma coupling
    # dynamics (curvature = acceleration of tonal change).
    # Low curvature = stable trajectory = likely accurate next prediction.
    # High curvature = changing trajectory = less certain prediction.
    f2 = torch.sigmoid(
        0.35 * p0
        + 0.25 * chroma_h3
        + 0.20 * chroma_h0
        + 0.20 * (1.0 - chroma_h3_curv)
    )

    return f0, f1, f2
