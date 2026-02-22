"""UDP F-Layer -- Forecast (3D).

Forward predictions for reward expectation, model improvement, and
pleasure anticipation:
  F0: reward_expectation       (expected reward from upcoming uncertainty resolution)
  F1: model_improvement        (expected gain in model accuracy)
  F2: pleasure_anticipation    (anticipated hedonic value)

H3 demands consumed:
  periodicity:           (5,16,18,0) trend -- tonal certainty trajectory
  tonalness:             (14,16,1,0) reused
  H_coupling:            (41,16,1,0) reused, (41,16,6,0) reused

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/udp/
Salimpoor et al. 2011: dopamine release during music anticipation (caudate).
Gold et al. 2019: inverted-U anticipatory pleasure under uncertainty.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PERIOD_H16_TREND = (5, 16, 18, 0)
_TONAL_H16_MEAN = (14, 16, 1, 0)
_H_COUPLING_H16_MEAN = (41, 16, 1, 0)
_H_COUPLING_H16_SKEW = (41, 16, 6, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for reward and pleasure.

    Extrapolates current uncertainty-reward dynamics into the future
    using long-horizon H3 trends and E/P layer context.

    Salimpoor et al. 2011: caudate dopamine release indexes anticipation
    of rewarding musical events.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    e0, e1 = e
    p0, p1, p2 = p

    # -- H3 features --
    period_trend_1s = h3_features[_PERIOD_H16_TREND]
    tonal_mean_1s = h3_features[_TONAL_H16_MEAN]
    h_coupling_mean_1s = h3_features[_H_COUPLING_H16_MEAN]
    h_coupling_skew_1s = h3_features[_H_COUPLING_H16_SKEW]

    # -- F0: Reward Expectation --
    # Expected reward from upcoming uncertainty resolution. Uses current
    # reward computation (P2) extrapolated by long-range tonal trend.
    # Salimpoor 2011: caudate encodes anticipatory reward.
    f0 = torch.sigmoid(
        0.35 * p2
        + 0.25 * e0
        + 0.20 * h_coupling_mean_1s
        + 0.20 * (1.0 - tonal_mean_1s)
    )

    # -- F1: Model Improvement --
    # Expected gain in predictive model accuracy. When uncertainty is
    # high (E0) but prediction accuracy is improving (P1), the model
    # is learning -- this is intrinsically rewarding.
    # Pearce 2005: IDyOM learning reduces entropy over exposure.
    f1 = torch.sigmoid(
        0.30 * p1
        + 0.25 * e0
        + 0.25 * period_trend_1s
        + 0.20 * h_coupling_skew_1s
    )

    # -- F2: Pleasure Anticipation --
    # Anticipated hedonic value combining reward expectation with
    # confirmation reward and long-range harmonic context.
    # Gold 2019: anticipatory pleasure peaks under moderate uncertainty.
    f2 = torch.sigmoid(
        0.30 * e1
        + 0.25 * p2
        + 0.25 * h_coupling_mean_1s
        + 0.20 * p0
    )

    return f0, f1, f2
