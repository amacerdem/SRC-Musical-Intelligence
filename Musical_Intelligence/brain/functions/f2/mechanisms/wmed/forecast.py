"""WMED F-Layer -- Forecast (4D).

Forward predictions for rhythm processing and paradox dynamics:
  F0: next_beat_pred           (predicted timing of next beat event)
  F1: tapping_accuracy_pred    (predicted tapping accuracy given current state)
  F2: wm_interference_pred     (predicted WM interference with motor timing)
  F3: paradox_strength_pred    (predicted paradox magnitude going forward)

H3 demands consumed:
  H_coupling:  (41,16,20,0) -- entropy at 1s memory (rhythmic uncertainty)

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/wmed/
Noboa 2025: paradox prediction, beta=-0.418.
Grahn 2007: beat prediction in BG-SMA loop.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_H_COUPLING_H16_ENT = (41, 16, 20, 0)  # H_coupling entropy at 1s memory


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for rhythm and paradox.

    F0 predicts next beat timing from phase locking (P0) and
    rhythmic engagement (P2) — when phase-locked and engaged,
    the next beat is strongly predicted.

    F1 predicts tapping accuracy from current engagement (P2)
    and entrainment (E0), modulated by rhythmic uncertainty.

    F2 predicts WM interference from pattern segmentation (P1)
    and WM contribution (E1) — high WM demand + complex patterns
    = predicted interference.

    F3 predicts paradox strength going forward from P0 (phase lock)
    and inverted P1 (segmentation) — strong phase lock + poor
    segmentation = predicted paradox intensification.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2, F3)`` each ``(B, T)``
    """
    e0, e1 = e
    p0, p1, p2 = p

    h_coupling_ent_1s = h3_features[_H_COUPLING_H16_ENT]  # (B, T)

    # -- F0: Next Beat Prediction --
    # Predicted beat timing: phase locking + engagement + low uncertainty.
    # Grahn 2007: BG predicts upcoming beats via motor preparation.
    f0 = torch.sigmoid(
        0.40 * p0
        + 0.35 * p2
        + 0.25 * (1.0 - h_coupling_ent_1s)
    )

    # -- F1: Tapping Accuracy Prediction --
    # Predicted tapping performance: engagement + entrainment,
    # penalized by rhythmic uncertainty (entropy).
    f1 = torch.sigmoid(
        0.35 * p2
        + 0.30 * e0
        + 0.20 * p0
        + 0.15 * (1.0 - h_coupling_ent_1s)
    )

    # -- F2: WM Interference Prediction --
    # Predicted WM interference with motor timing: pattern segmentation
    # demand + WM contribution + rhythmic uncertainty.
    # High values = WM load will interfere with tapping.
    f2 = torch.sigmoid(
        0.35 * p1
        + 0.30 * e1
        + 0.20 * h_coupling_ent_1s
        + 0.15 * (1.0 - p0)
    )

    # -- F3: Paradox Strength Prediction --
    # Predicted paradox magnitude: strong phase lock (P0) + weak pattern
    # segmentation (1-P1) = entrainment without WM support.
    # Noboa 2025: this dissociation pattern predicts degraded performance.
    f3 = torch.sigmoid(
        0.40 * p0
        + 0.30 * (1.0 - p1)
        + 0.20 * e0
        + 0.10 * (1.0 - e1)
    )

    return f0, f1, f2, f3
