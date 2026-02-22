"""MAA F-Layer — Forecast (3D).

Forward predictions for appreciation development:
  F0: appreciation_growth     (predicted growth in appreciation over exposure)
  F1: pattern_recognition     (predicted pattern discovery in atonal material)
  F2: aesthetic_development   (predicted aesthetic trajectory)

H3 demands consumed:
  H_coupling:           (41,16,18,0) — trend for appreciation trajectory
  tonalness:            (14,16,1,0) reused
  sensory_pleasantness: (4,16,1,0) reused
  spectral_change:      (21,16,20,0) reused

See Hargreaves 1984: familiarity shifts inverted-U peak rightward over time.
See Greenberg 2015: openness predicts growth in complex music preference.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_H_COUPLING_H16_TREND = (41, 16, 18, 0)
_TONALNESS_H16_MEAN = (14, 16, 1, 0)
_SENSORY_PLEAS_H16_MEAN = (4, 16, 1, 0)
_SPECTRAL_CHANGE_H16_ENT = (21, 16, 20, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for appreciation development.

    Projects how atonal appreciation will develop based on current
    complexity tolerance, familiarity, aesthetic evaluation, and
    temporal trends in cross-band coupling.

    Hargreaves 1984: familiarity shifts preference peak rightward —
    appreciation grows with exposure. Greenberg 2015: openness predicts
    sustained engagement with complex music.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    e0, e1 = e
    p0, p1, p2 = p

    h_coupling_trend_1s = h3_features[_H_COUPLING_H16_TREND]
    tonal_mean_1s = h3_features[_TONALNESS_H16_MEAN]
    pleas_mean_1s = h3_features[_SENSORY_PLEAS_H16_MEAN]
    spec_change_ent_1s = h3_features[_SPECTRAL_CHANGE_H16_ENT]

    # -- F0: Appreciation Growth --
    # Predicted growth in appreciation: driven by familiarity index (E1,
    # exposure builds appreciation) and positive coupling trend. The
    # aesthetic evaluation (P2) provides current appreciation baseline.
    # Hargreaves 1984: repeated exposure → increased preference.
    f0 = torch.sigmoid(
        0.30 * e1
        + 0.30 * h_coupling_trend_1s
        + 0.20 * p2
        + 0.20 * pleas_mean_1s
    )

    # -- F1: Pattern Recognition --
    # Predicted pattern discovery: pattern search (P0) and complexity
    # tolerance (E0) drive expectation that structure will be found.
    # Tonal context (inverted) indicates how much discovery remains.
    # Berlyne 1971: exploration drive for novel/complex stimuli.
    f1 = torch.sigmoid(
        0.35 * p0
        + 0.25 * e0
        + 0.20 * (1.0 - tonal_mean_1s)
        + 0.20 * spec_change_ent_1s
    )

    # -- F2: Aesthetic Development --
    # Predicted aesthetic trajectory: overall forward projection combining
    # context assessment (P1), coupling trend, and appreciation composite.
    # Greenberg 2015: openness enables sustained aesthetic development.
    f2 = torch.sigmoid(
        0.30 * p1
        + 0.25 * h_coupling_trend_1s
        + 0.25 * p2
        + 0.20 * pleas_mean_1s
    )

    return f0, f1, f2
