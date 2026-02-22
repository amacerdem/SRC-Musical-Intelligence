"""SPMC F-Layer -- Forecast (3D).

SMA-Premotor-M1 Motor Circuit forward predictions:

  sequence_pred  (dim 8)  -- Sequence planning prediction [0, 1]
  execution_pred (dim 9)  -- Motor execution prediction [0, 1]
  timing_pred    (dim 10) -- Timing precision prediction [0, 1]

The F-layer generates three forward-looking predictions for the motor
circuit.  Sequence prediction forecasts upcoming SMA encoding from
current planning + beat periodicity.  Execution prediction forecasts M1
output from current execution + tempo/stability context.  Timing
prediction forecasts cerebellar precision from current timing + tempo
variability.

All F-layer dimensions use forward-looking (L0) H3 features at the 1s
horizon and E-layer features as predictive context, consistent with the
motor system's anticipatory planning role.

H3 consumed (4 tuples -- F-layer):
    (10, 16, 14, 2)  onset_strength periodicity H16 L2  -- beat period 1s (sequence)
    (21, 16, 1, 0)   spectral_change mean H16 L0        -- mean tempo change 1s (exec)
    (21, 16, 2, 0)   spectral_change std H16 L0         -- tempo variability 1s (timing)
    (33, 16, 19, 0)  x_l4l5 stability H16 L0            -- sequence stability 1s (exec)

R3 consumed:
    [10]     spectral_flux    -- beat periodicity for sequence prediction
    [21]     spectral_change  -- tempo dynamics for execution and timing
    [33:41]  x_l4l5           -- sequence stability for execution/timing

Grahn & Brett 2007: SMA encodes beat expectation in metric rhythms.
Okada 2022: cerebellar dentate neurons encode timing of next movement
    (1/3 selectively active for synchronized vs reactive movements).
Harrison 2025: CTC pathway provides predictive motor timing.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/spmc/f_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (F-layer: 4 tuples) -------------------------------------------
_BEAT_PERIOD_H16 = (10, 16, 14, 2)   # beat periodicity 1s (sequence pred)
_TEMPO_MEAN_H16 = (21, 16, 1, 0)     # mean tempo change 1s (execution pred)
_TEMPO_STD_H16 = (21, 16, 2, 0)      # tempo variability 1s (timing pred)
_SEQ_STABILITY_H16 = (33, 16, 19, 0) # sequence stability 1s (execution pred)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forward predictions from E/M/P layers + H3.

    Computes three motor circuit predictions:
        sequence_pred (dim 8): Forecasts upcoming SMA sequence encoding.
            Combines current planning (f19) with 1s beat periodicity.
            Grahn & Brett 2007: SMA beat-strength patterns are predictive.
            Hoddinott & Grahn 2024: SMA RSA encodes beat expectation.
        execution_pred (dim 9): Forecasts upcoming M1 motor output.
            Uses current execution (f21) with forward-looking tempo mean
            and sequence stability at 1s horizon.
            Harrison 2025: CTC pathway predictive motor timing.
        timing_pred (dim 10): Forecasts cerebellar timing precision.
            Combines current timing (M-layer) with tempo variability and
            sequence stability.  Low tempo variability + high stability =
            maintained timing.
            Okada 2022: predictive timing neurons in dentate nucleus.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(f19, f20, f21)`` from E-layer.
        m: ``(circuit_flow, hierarchy_index, timing_precision)`` from M-layer.
        p: ``(sma_activity, m1_output)`` from P-layer.

    Returns:
        ``(sequence_pred, execution_pred, timing_pred)`` each ``(B, T)``.
    """
    f19, _f20, f21 = e
    _circuit_flow, _hierarchy_index, timing_precision = m
    sma_activity, m1_output = p

    # -- H3 features (1s forward-looking) --
    beat_period_1s = h3_features[_BEAT_PERIOD_H16]       # (B, T)
    tempo_mean_1s = h3_features[_TEMPO_MEAN_H16]         # (B, T)
    tempo_std_1s = h3_features[_TEMPO_STD_H16]           # (B, T)
    seq_stability_1s = h3_features[_SEQ_STABILITY_H16]   # (B, T)

    # -- sequence_pred (dim 8): SMA sequence prediction --
    # sequence_pred = sigma(0.5 * f19 + 0.5 * beat_period_1s)
    # Strong beat periodicity + active planning = high sequence prediction.
    # Grahn & Brett 2007: SMA beat expectation.
    sequence_pred = torch.sigmoid(
        0.50 * f19
        + 0.50 * beat_period_1s
    )

    # -- execution_pred (dim 9): M1 execution prediction --
    # Current execution + tempo mean + sequence stability.
    # Stable tempo + consistent sequences = continued motor execution.
    # Harrison 2025: CTC pathway predictive timing.
    execution_pred = torch.sigmoid(
        0.35 * f21
        + 0.25 * tempo_mean_1s
        + 0.25 * seq_stability_1s
        + 0.15 * m1_output
    )

    # -- timing_pred (dim 10): cerebellar timing prediction --
    # Current timing precision + inverted tempo variability + stability.
    # Low variability + high stability = maintained timing precision.
    # Okada 2022: 1/3 dentate neurons predict synchronized timing.
    inverted_tempo_var = 1.0 - tempo_std_1s.abs()
    timing_pred = torch.sigmoid(
        0.35 * timing_precision
        + 0.30 * inverted_tempo_var
        + 0.20 * seq_stability_1s
        + 0.15 * sma_activity
    )

    return sequence_pred, execution_pred, timing_pred
