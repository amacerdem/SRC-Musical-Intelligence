"""LDAC F-Layer -- Forecast (1D).

Forward prediction for sensory gating state:
  F0: sensory_gating_pred -- Predicted sensory gating state [0, 1]

Sensory gating prediction (F0) forecasts the near-future state of
pleasure-dependent sensory gating by combining the STG-liking coupling
(f01 / E0) with the IC x liking interaction (f03 / E2). When liking is
high and IC is low, gating is predicted to remain open (enhanced
processing); when IC is high and liking is low, gating is predicted to
suppress (reduced processing).

Prediction horizon is short (~0.5-1s), consistent with LDAC's rapid
tau_decay = 0.5s. Enables downstream systems (notably F3 Attention via
ASU.sensory_gain) to anticipate changes in auditory cortex responsiveness,
supporting proactive allocation of attentional resources.

H3 demands consumed: None. Operates entirely on E-layer outputs (f01, f03).
Prediction is based on current pleasure state and IC-liking interaction as
indicators of the near-future gating trajectory.

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ldac/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_forecast(
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """Compute F-layer: 1D sensory gating prediction.

    F0 (sensory_gating_pred): Combines STG-liking coupling (f01, w=0.50)
    with IC x liking interaction (f03, w=0.50). The rationale:

    1. Current liking level (f01): If pleasure is high, sensory processing
       is predicted to remain enhanced (liking is temporally autocorrelated
       during naturalistic listening).

    2. IC x liking interaction (f03): If current moment shows high IC in
       disliked music (high f03 = suppression active), prediction is that
       gating will tighten further. If IC is low or music is liked,
       suppression is minimal and prediction favors open gating.

    Args:
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``
            from extraction layer.

    Returns:
        ``(F0,)`` each ``(B, T)``.
    """
    f01, _f02, f03, _f04 = e_outputs

    # -- F0: Sensory Gating Prediction -----------------------------------------
    # sigma(0.5 * f01 + 0.5 * f03)
    # Gold et al. 2023a: liking state predicts near-future gating
    # Cheung et al. 2019: IC-based prediction in harmonic domain
    f0 = torch.sigmoid(
        0.50 * f01
        + 0.50 * f03
    )

    return (f0,)
