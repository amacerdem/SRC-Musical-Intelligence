"""ASAP F-Layer -- Forecast (2D).

Action Simulation for Auditory Prediction forward predictions:
  beat_when_pred_0_5s   -- Next beat "when" prediction (~0.5s ahead) [0, 1]
  simulation_pred       -- Motor simulation continuation prediction [0, 1]

beat_when_pred_0_5s predicts the likelihood that a beat will occur at the
motor-predicted time point ~0.5s ahead. Combines current beat prediction
state (f10) with sustained beat periodicity signal (H3). Higher values
indicate confident temporal prediction. Large et al. 2023: dynamic
oscillator models predict optimal beat perception near 2 Hz (~500ms).
beat_when_pred = sigma(0.5 * f10 + 0.5 * beat_periodicity_1s)

simulation_pred predicts whether the motor simulation will maintain or
strengthen in the near future. Combines current simulation strength (f11)
with sustained motor-auditory coupling periodicity. Thaut et al. 2015:
period entrainment drives motor optimization -- simulation persists when
coupling is periodic.
simulation_pred = sigma(0.5 * f11 + 0.5 * coupling_period_1s)

H3 demands: 0 new tuples -- reuses from E-layer and M-layer:
  beat_periodicity_1s:  (10, 16, 14, 0) from E-layer
  coupling_period_1s:   (25, 16, 14, 0) from M-layer

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/asap/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys reused from E-layer and M-layer --------------------------------
_BEAT_PERIOD_H16 = (10, 16, 14, 0)      # spectral_flux periodicity H16 L0 (1s)
_COUPLING_PERIOD_H16 = (25, 16, 14, 0)  # x_l0l5[0] periodicity H16 L0 (1s)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: beat timing and simulation continuation predictions.

    beat_when_pred_0_5s predicts next beat event timing. Averages current
    beat prediction (f10) with sustained beat periodicity (H3). Highly
    periodic rhythms with strong current prediction yield confident
    forecasts. Large et al. 2023: optimal beat perception ~2 Hz.

    simulation_pred predicts motor simulation continuation. Averages
    current simulation strength (f11) with coupling periodicity at 1s.
    Periodic coupling + strong simulation -> sustained prediction.
    Thaut et al. 2015: period entrainment optimizes motor simulation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(f10, f11, f12)`` from extraction layer.
        m: ``(prediction_accuracy, simulation_strength, coupling_index)``
           from temporal integration layer.
        p: ``(motor_to_auditory, auditory_to_motor, dorsal_activity)``
           from cognitive present layer.

    Returns:
        ``(beat_when_pred_0_5s, simulation_pred)`` each ``(B, T)``
    """
    f10, f11, _f12 = e
    _pred_acc, _sim_str, coupling_index = m
    motor_to_aud, _aud_to_motor, _dorsal = p

    # -- H3 features (reused) --
    beat_period = h3_features[_BEAT_PERIOD_H16]        # (B, T)
    coupling_period = h3_features[_COUPLING_PERIOD_H16]  # (B, T)

    # -- beat_when_pred_0_5s --
    # Next beat "when" prediction. Combines current beat prediction (f10)
    # with sustained beat periodicity. Confident temporal prediction when
    # both current state and underlying regularity are strong.
    # Large et al. 2023: dynamic oscillators predict optimal ~2 Hz.
    # beat_when_pred = sigma(0.5 * f10 + 0.5 * beat_periodicity_1s)
    beat_when_pred = torch.sigmoid(
        0.50 * f10 + 0.50 * beat_period
    )

    # -- simulation_pred --
    # Motor simulation continuation prediction. Combines current
    # simulation strength (f11) with coupling periodicity at 1s. If
    # coupling is periodic and simulation is strong, prediction sustains.
    # Thaut et al. 2015: period entrainment drives motor optimization.
    # simulation_pred = sigma(0.5 * f11 + 0.5 * coupling_period_1s)
    simulation_pred = torch.sigmoid(
        0.50 * f11 + 0.50 * coupling_period
    )

    return beat_when_pred, simulation_pred
