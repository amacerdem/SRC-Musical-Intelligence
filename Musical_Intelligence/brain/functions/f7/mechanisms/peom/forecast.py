"""PEOM F-Layer -- Forecast (2D).

Two forward predictions for beat timing and velocity profile:

  next_beat_pred_T       -- Next beat onset prediction (T ahead) [0, 1]
  velocity_profile_pred  -- Velocity profile prediction 0.5T ahead [0, 1]

H3 consumed: None (reuses E-layer tuples)
    beat_periodicity_1s from (10, 16, 14, 2) -- already in E-layer
    coupling_periodicity_1s from (25, 16, 14, 2) -- already in P-layer

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/peom/f_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (reused from E and P layers) -----------------------------------
_ONSET_PERIOD_1S = (10, 16, 14, 2)        # beat periodicity 1s (from E)
_COUPLING_PERIOD_1S = (25, 16, 14, 2)     # coupling periodicity 1s (from P)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D forecast from E/M/P outputs + shared H3 context.

    Generates predictions about upcoming motor states:
        next_beat_pred_T: beat onset timing prediction
        velocity_profile_pred: velocity trajectory prediction

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03)`` each ``(B, T)``.
        m_outputs: ``(motor_period, velocity, acceleration, cv_reduction)``
                   each ``(B, T)``.
        p_outputs: ``(period_lock_strength, kinematic_smoothness)``
                   each ``(B, T)``.

    Returns:
        ``(next_beat_pred_T, velocity_profile_pred)`` each ``(B, T)``.
    """
    f01, f02, _f03 = e_outputs
    _motor_period, _velocity, _acceleration, _cv_reduction = m_outputs
    _period_lock, _kinematic_smooth = p_outputs

    # -- H3 features (reused from E and P layers) --
    beat_periodicity_1s = h3_features[_ONSET_PERIOD_1S]      # beat period
    coupling_periodicity_1s = h3_features[_COUPLING_PERIOD_1S]  # coupling period

    # Next beat prediction: when the next beat will occur
    # Thaut 1998b: motor period entrains even during subliminal tempo changes
    # Repp 2005: period correction as distinct predictive mechanism
    # sigma(0.5 * f01 + 0.5 * beat_periodicity_1s)
    next_beat_pred = torch.sigmoid(
        0.50 * f01
        + 0.50 * beat_periodicity_1s
    )

    # Velocity profile prediction: upcoming velocity trajectory shape
    # Thaut 2015: CTR enables anticipatory velocity planning
    # Ross & Balasubramaniam 2022: motor simulation for prediction
    # sigma(0.5 * f02 + 0.5 * coupling_periodicity_1s)
    velocity_profile_pred = torch.sigmoid(
        0.50 * f02
        + 0.50 * coupling_periodicity_1s
    )

    return next_beat_pred, velocity_profile_pred
