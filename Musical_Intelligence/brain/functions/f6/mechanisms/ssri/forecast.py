"""SSRI F-Layer -- Forecast (2D).

Social Synchrony Reward Integration forward predictions:
  bonding_trajectory_pred   -- Predicted social bonding direction [0, 1]
  flow_sustain_pred         -- Predicted group flow sustainability [0, 1]

bonding_trajectory_pred forecasts whether social bonding is strengthening
or weakening. The current social_bonding_index (f02, weight 0.50) is the
strongest predictor, supplemented by coupling_trend_1s (weight 0.30) for
whether interpersonal coordination is strengthening, and loudness_trend_5s
(weight 0.20) for shared dynamic trajectory. tau_bonding = 120.0s,
reflecting that social bonds accumulate over minutes of shared experience.

flow_sustain_pred forecasts whether group flow can be maintained. The
current group_flow_state (f03, weight 0.40) combines with entrainment
quality (f04, weight 0.30) as coordination precision, and an arousal
signal (weight 0.30) approximated from R3 features (mechanisms lack
direct belief state access). Flow requires both coordination and
appropriate activation level -- too little arousal leads to disengagement,
while excessive arousal disrupts relaxed focus (Gold et al. 2019: optimal
complexity maximizes musical pleasure via inverted-U).

H3 demands consumed (2 tuples):
  (25, 16, 18, 2) coupling trend 1s L2      -- consonance-energy direction
  (8, 20, 18, 0)  loudness trend 5s LTI L0  -- long-range dynamic trajectory

Dependencies:
  E-layer f02 (social_bonding_index)
  E-layer f03 (group_flow_state)
  E-layer f04 (entrainment_quality)
  R3[8] loudness (arousal approximation)

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ssri/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_COUPLING_TREND_H16 = (25, 16, 18, 2)   # coupling trend 1s L2
_LOUDNESS_TREND_H20 = (8, 20, 18, 0)    # loudness trend 5s LTI L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_LOUDNESS = 8   # velocity_D -- used as arousal approximation


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: bonding trajectory and flow sustainability predictions.

    bonding_trajectory_pred forecasts social bonding direction. Current
    bonding state (f02) is the strongest predictor, coupling trend
    indicates coordination direction, loudness trend captures shared
    dynamic trajectory. tau_bonding = 120.0s.

    flow_sustain_pred forecasts whether group flow is sustainable.
    Current flow state (f03), entrainment precision (f04), and arousal
    (approximated from loudness at R3[8]) determine sustainability.
    Gold et al. 2019: optimal complexity maximizes pleasure (inverted-U).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e_outputs: ``(f01, f02, f03, f04, f05)`` from extraction layer.
        m_outputs: ``(spe, sa)`` from temporal integration layer.
        p_outputs: ``(prefrontal_coupling, endorphin_proxy)`` from P-layer.

    Returns:
        ``(bonding_trajectory_pred, flow_sustain_pred)`` each ``(B, T)``
    """
    _f01, f02, f03, f04, _f05 = e_outputs

    # -- H3 features --
    coupling_trend_1s = h3_features[_COUPLING_TREND_H16]   # (B, T)
    loudness_trend_5s = h3_features[_LOUDNESS_TREND_H20]   # (B, T)

    # -- Arousal approximation from loudness trend --
    # Since mechanism layers lack direct belief state access, we approximate
    # arousal from the long-range loudness trend. Positive trend = rising
    # arousal; we pass through sigmoid for [0, 1] range.
    arousal_approx = torch.sigmoid(loudness_trend_5s)  # (B, T)

    # -- bonding_trajectory_pred --
    # Forecasts social bonding direction. f02 (0.50) is best predictor,
    # coupling trend (0.30) indicates coordination trajectory, loudness
    # trend (0.20) captures shared dynamic direction. tau_bonding = 120.0s.
    bonding_trajectory_pred = torch.sigmoid(
        0.50 * f02
        + 0.30 * coupling_trend_1s
        + 0.20 * loudness_trend_5s
    )

    # -- flow_sustain_pred --
    # Forecasts group flow sustainability. Current flow (f03, 0.40),
    # entrainment precision (f04, 0.30) sustains flow, arousal (0.30) is
    # the energetic resource. Flow requires both coordination and
    # appropriate activation -- inverted-U relationship.
    # Gold et al. 2019: optimal complexity maximizes pleasure.
    flow_sustain_pred = torch.sigmoid(
        0.40 * f03
        + 0.30 * f04
        + 0.30 * arousal_approx
    )

    return bonding_trajectory_pred, flow_sustain_pred
