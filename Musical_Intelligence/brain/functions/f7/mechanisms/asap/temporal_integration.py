"""ASAP M-Layer -- Temporal Integration (3D).

Action Simulation for Auditory Prediction temporal integration signals:
  prediction_accuracy   -- Temporal prediction error (inverse) [0, 1]
  simulation_strength   -- Motor simulation amplitude [0, 1]
  coupling_index        -- Bidirectional motor-auditory coupling strength [0, 1]

prediction_accuracy directly inherits from f10 (beat_prediction). Beat
prediction strength IS prediction accuracy -- when the motor system
successfully predicts upcoming beats, the periodicity signals are strong.
Grahn & Brett 2007: beat-inducing rhythms activate putamen + SMA
(F(2,38)=20.67, p<.001).

simulation_strength directly inherits from f11 (motor_simulation). The
ongoing simulation amplitude at fast timescales reflects how vigorously
the motor system generates temporal predictions. Barchet et al. 2024:
finger-tapping optimal at ~2 Hz (beta=0.31 for perception prediction).

coupling_index combines f11 and f12 through sigmoid with equal weights.
Both simulation strength (f11) and dorsal pathway activity (f12) must be
high for strong coupling. Equal weighting reflects the bidirectional
nature -- motor-to-auditory and auditory-to-motor contribute equally.

H3 demands consumed (3 tuples):
  (21, 4, 8, 0)   spectral_flux velocity H4 L0     -- Tempo velocity 125ms
  (21, 16, 1, 0)  spectral_flux mean H16 L0        -- Mean tempo change 1s
  (25, 16, 14, 0) x_l0l5[0] periodicity H16 L0     -- Coupling periodicity 1s

R3 features:
  [21] spectral_change (tempo dynamics)

E-layer dependencies:
  f10 (beat_prediction), f11 (motor_simulation), f12 (dorsal_stream)

Grahn & Brett 2007: putamen Z=5.67 for beat-inducing rhythms.
Barchet et al. 2024: tapping optimal at ~2 Hz (beta=0.31).

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/asap/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_TEMPO_VEL_H4 = (21, 4, 8, 0)           # spectral_flux velocity H4 L0 (125ms)
_TEMPO_MEAN_H16 = (21, 16, 1, 0)        # spectral_flux mean H16 L0 (1s)
_COUPLING_PERIOD_H16 = (25, 16, 14, 0)  # x_l0l5[0] periodicity H16 L0 (1s)

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_SPECTRAL_CHANGE = 21


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: prediction accuracy, simulation strength, coupling.

    prediction_accuracy directly inherits from f10 (beat_prediction).
    Beat prediction strength IS prediction accuracy. Grahn & Brett 2007:
    putamen + SMA activation for beat-inducing rhythms (F(2,38)=20.67).

    simulation_strength directly inherits from f11 (motor_simulation).
    Ongoing simulation amplitude reflects motor prediction vigor.
    Barchet et al. 2024: tapping optimal ~2 Hz (beta=0.31).

    coupling_index = sigma(0.5 * f11 + 0.5 * f12). Joint measure of
    motor-auditory coupling tightness. Both simulation (f11) and dorsal
    pathway (f12) must be active for strong coupling. Equal weighting
    reflects bidirectionality.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(f10, f11, f12)`` from extraction layer.
        relay_outputs: ``{"PEOM": (B, T, 11), "MSR": (B, T, 11)}``

    Returns:
        ``(prediction_accuracy, simulation_strength, coupling_index)``
        each ``(B, T)``
    """
    f10, f11, f12 = e

    # -- prediction_accuracy = f10 --
    # Beat prediction strength IS prediction accuracy. When the motor
    # system successfully predicts beats, periodicity signals are strong.
    # Grahn & Brett 2007: putamen (Z=5.67) + SMA (Z=5.03).
    prediction_accuracy = f10

    # -- simulation_strength = f11 --
    # Ongoing simulation amplitude at fast timescales directly reflects
    # motor prediction vigor. Barchet et al. 2024: beta=0.31.
    simulation_strength = f11

    # -- coupling_index = sigma(0.5 * f11 + 0.5 * f12) --
    # Bidirectional motor-auditory coupling measure. Both simulation
    # and dorsal pathway must be active for strong coupling.
    coupling_index = torch.sigmoid(
        0.50 * f11 + 0.50 * f12
    )

    return prediction_accuracy, simulation_strength, coupling_index
