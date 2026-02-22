"""ASAP P-Layer -- Cognitive Present (3D).

Action Simulation for Auditory Prediction present-time signals:
  motor_to_auditory   -- Motor-to-auditory prediction signal (forward model) [0, 1]
  auditory_to_motor   -- Auditory-to-motor update signal (inverse model) [0, 1]
  dorsal_activity     -- Dorsal pathway activation level [0, 1]

motor_to_auditory is the forward model signal -- the motor system's temporal
prediction flowing toward auditory cortex. Computed from the interaction of
prediction accuracy (M-layer) with simulation strength (M-layer), gated by
coupling index. The "when" prediction being broadcast. Patel & Iversen 2014:
motor system actively predicts upcoming onsets.

auditory_to_motor is the inverse model signal -- auditory onset information
flowing back to correct the motor simulation. Computed from the difference
between actual and predicted onset timing, modulated by coupling strength.
Low prediction error -> weak signal (accurate); high PE -> phase adjustment.
Ross & Balasubramaniam 2022: bidirectional coupling.

dorsal_activity directly inherits from f12 (dorsal_stream). The current
activation of posterior parietal cortex -- the hub for bidirectional
motor-auditory information flow. Ross et al. 2018: cTBS to parietal cortex
causally disrupts beat timing (double dissociation with cerebellum).

H3 demands: 0 new tuples -- all computation derives from upstream layers.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/asap/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: bidirectional motor-auditory coupling state.

    motor_to_auditory (forward model) -- the motor system's current
    temporal prediction flowing from SMA/premotor to auditory cortex via
    the dorsal pathway. Prediction accuracy gated by simulation strength
    and coupling produces the broadcast "when" signal.
    Patel & Iversen 2014: motor system generates forward prediction.

    auditory_to_motor (inverse model) -- temporal-context-driven error
    correction flowing from auditory cortex back to motor areas. Phase
    adjustment signal: when prediction error is low, signal is weak;
    when PE is high, signal drives correction.
    Ross & Balasubramaniam 2022: bidirectional coupling.

    dorsal_activity = f12 (dorsal_stream). Current activation of
    posterior parietal cortex, the dorsal pathway hub.
    Ross et al. 2018: cTBS double dissociation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(f10, f11, f12)`` from extraction layer.
        m: ``(prediction_accuracy, simulation_strength, coupling_index)``
           from temporal integration layer.

    Returns:
        ``(motor_to_auditory, auditory_to_motor, dorsal_activity)``
        each ``(B, T)``
    """
    f10, f11, f12 = e
    prediction_accuracy, simulation_strength, coupling_index = m

    # -- motor_to_auditory: Forward model --
    # Beat-entrainment-driven motor prediction flowing from SMA/premotor
    # to auditory cortex. Prediction accuracy (f10) gated by simulation
    # strength (f11), modulated by coupling index. This is the "when"
    # signal being broadcast.
    # Patel & Iversen 2014: motor forward temporal prediction.
    motor_to_auditory = torch.sigmoid(
        0.35 * prediction_accuracy * simulation_strength.clamp(min=0.1)
        + 0.35 * coupling_index * f10.clamp(min=0.1)
        + 0.30 * f11 * f12.clamp(min=0.1)
    )

    # -- auditory_to_motor: Inverse model --
    # Auditory onset information flowing back to correct motor simulation.
    # When prediction is accurate (high f10), the error correction signal
    # is weak. When prediction error is high (low f10), this signal drives
    # phase adjustment. Coupling strength modulates the feedback gain.
    # Ross & Balasubramaniam 2022: auditory input updates motor simulation.
    prediction_error = 1.0 - prediction_accuracy  # inverse of accuracy
    auditory_to_motor = torch.sigmoid(
        0.35 * prediction_error * coupling_index.clamp(min=0.1)
        + 0.35 * simulation_strength * (1.0 - f10).clamp(min=0.1)
        + 0.30 * f12 * prediction_error.clamp(min=0.1)
    )

    # -- dorsal_activity = f12 --
    # Current activation of posterior parietal cortex dorsal pathway hub.
    # Directly inherits from E-layer f12 (dorsal_stream).
    # Ross et al. 2018: cTBS to parietal cortex disrupts beat timing.
    dorsal_activity = f12

    return motor_to_auditory, auditory_to_motor, dorsal_activity
