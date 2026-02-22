"""SSPS F-Layer -- Forecast (1D).

Forward prediction for optimal zone trajectory:
  optimal_zone_pred  -- Predicted movement toward an optimal zone [0, 1]

Forecasts whether upcoming acoustic events will move the listener closer to
or further from a preference peak on the saddle surface.  High values indicate
predicted movement toward (or persistence at) an optimal zone peak.  Low
values indicate predicted movement toward the saddle trough.

The prediction leverages the temporal dynamics already encoded in the E-layer's
H3 features.  Because the E-layer reads IC velocity (H8, M8) and entropy
trends (H16, M20), the saddle_value already encodes directional information.
The F-layer surfaces this as an explicit prediction.

Gold et al. 2023: VS shows RPE-like surprise x liking interaction consistent
with predictive preference evaluation.

H3 demands consumed: None new (reuses E-layer saddle_value and f04).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ssps/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_forecast(
    h3_features: dict,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor],
) -> Tuple[Tensor]:
    """Compute F-layer: optimal zone prediction (1D).

    optimal_zone_pred: Combines peak proximity (f04) with raw saddle
    interaction value.  The saddle_value encodes directional preference
    topology independent of smoothness modulation.

    Gold 2023: VS shows RPE-like surprise x liking interaction.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}`` (unused).
        e_outputs: ``(f01, f02, f03, f04, saddle_value)`` from E-layer.
        p_outputs: ``(surface_position_state,)`` from P-layer (unused).

    Returns:
        ``(optimal_zone_pred,)`` -- single ``(B, T)`` tensor.
    """
    _f01, _f02, _f03, f04, saddle_value = e_outputs

    # -- optimal_zone_pred --
    # sigma(0.5 * f04_peak_proximity + 0.5 * saddle_value)
    # Peak proximity = current position baseline for prediction.
    # Saddle value = raw IC x entropy interaction topology signal.
    optimal_zone_pred = torch.sigmoid(0.5 * f04 + 0.5 * saddle_value)

    return (optimal_zone_pred,)
