"""IGFE F-Layer -- Forecast (2D).

Forward predictions for post-stimulation cognitive enhancement:
  F0: memory_enhancement_post    (predicted memory improvement after exposure)
  F1: executive_improve_post     (predicted executive function improvement)

H3 demands consumed:
  H_coupling:    (41,16,18,0) -- coupling trend for trajectory
  periodicity:   (5,16,1,0) reused -- stable gamma memory
  tonalness:     (14,16,1,0) reused -- sustained harmonic alignment
  amplitude:     (7,16,1,2) reused -- sustained intensity

Forecast layer extrapolates from present P-layer state and long-timescale
H3 features to predict post-stimulation cognitive benefits. Uses trend
morphology (M18) for coupling trajectory projection.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/igfe/
Bolland 2025: post-stimulation memory and executive effects persist 15-60 min.
Pastor 2002: gamma-memory binding predicts recall improvement.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_H_COUPLING_H16_TREND = (41, 16, 18, 0)  # H_coupling 1s trend memory
_PERIOD_H16_MEAN = (5, 16, 1, 0)         # periodicity 1s mean memory
_TONAL_H16_MEAN = (14, 16, 1, 0)         # tonalness 1s mean memory
_AMPL_H16_MEAN = (7, 16, 1, 2)           # amplitude 1s mean integration


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: post-stimulation enhancement predictions.

    Projects current gamma entrainment state into predicted cognitive
    benefits after stimulation ends. Memory enhancement depends on
    hippocampal coupling trajectory; executive improvement depends on
    sustained frontal entrainment.

    Bolland 2025: post-stimulation effects persist 15-60 min in meta-analysis.
    Pastor 2002: gamma phase-locking during encoding predicts later recall.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``
    """
    _e0, e1 = e
    p0, p1, p2 = p

    coupling_trend = h3_features[_H_COUPLING_H16_TREND]
    period_stable = h3_features[_PERIOD_H16_MEAN]
    tonal_stable = h3_features[_TONAL_H16_MEAN]
    ampl_stable = h3_features[_AMPL_H16_MEAN]

    # -- F0: Memory Enhancement Post-Stimulation --
    # Predicted memory improvement: current memory access (P2) state +
    # cognitive coupling trajectory (trend) + sustained gamma stability.
    # Pastor 2002: gamma-memory binding during exposure predicts recall.
    # Bolland 2025: memory benefits persist post-stimulation.
    f0 = torch.sigmoid(
        0.35 * p2
        + 0.25 * coupling_trend
        + 0.20 * period_stable
        + 0.20 * tonal_stable
    )

    # -- F1: Executive Improvement Post-Stimulation --
    # Predicted executive function improvement: gamma synchronization
    # (P0) + dose accumulation (P1) + sustained stimulus intensity.
    # Enhancement proxy (E1) carries modulation characteristics.
    # Polanía 2012: WM capacity enhanced by gamma-frequency tACS.
    f1 = torch.sigmoid(
        0.30 * p0
        + 0.25 * p1
        + 0.25 * ampl_stable
        + 0.20 * e1
    )

    return f0, f1
