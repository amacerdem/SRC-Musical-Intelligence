"""IUCP F-Layer -- Forecast (1D).

Forward prediction for complexity preference:
  F0: optimal_zone_pred -- Predicted preference zone [0, 1]

F0 forecasts whether the music will remain in the listener's preferred
complexity zone. It combines:

1. f04 (optimal complexity): The current estimate of where the listener's
   optimal zone lies, incorporating the interaction surface and hedonic
   variability.

2. f03 (IC x entropy interaction): The interaction dynamics that shift the
   optimal zone. If the interaction is strong and complexity is near optimal,
   the prediction is high.

tau_decay = 2.0s (Gold 2019) sets the relevant prediction horizon. This
enables anticipatory reward modulation: DAED can scale anticipation dopamine
based on predicted future preference.

H3 demands consumed: None new -- reuses E-layer outputs (f03, f04).

Gold et al. 2019: Inverted-U replicated across two studies (N=43+27).
Gold et al. 2023b: VS anticipatory coding of preference, F(1,22)=4.83.
Cheung et al. 2019: NAcc reflects uncertainty (not surprise); anticipatory
zone signal (fMRI, N=39+40).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/iucp/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_forecast(
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """Compute F-layer: predicted optimal complexity zone.

    F0 (optimal_zone_pred) projects the listener's optimal complexity zone
    forward based on current interaction surface (f03) and optimal complexity
    estimate (f04). High values predict music will remain in the preferred
    zone; low values predict drift away from optimal complexity.

    tau_decay = 2.0s (Gold 2019).
    Gold et al. 2023b: VS anticipatory coding of preference.
    Cheung et al. 2019: NAcc anticipatory zone signal.

    Args:
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(F0,)`` each ``(B, T)``
    """
    _e0, _e1, e2, e3 = e

    # -- F0: Optimal Zone Prediction --
    # sigma(0.5 * f04 + 0.5 * f03)
    # Projects the optimal complexity zone forward. f04 provides the
    # current optimal estimate; f03 provides the interaction dynamics
    # that shift the zone. Combined prediction enables anticipatory
    # reward modulation via DAED.
    # Gold 2019: tau_decay = 2.0s prediction horizon.
    # Cheung 2019: NAcc codes anticipatory uncertainty signal.
    f0 = torch.sigmoid(
        0.50 * e3
        + 0.50 * e2
    )

    return (f0,)
