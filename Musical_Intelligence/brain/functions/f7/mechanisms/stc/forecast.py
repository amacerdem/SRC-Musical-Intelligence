"""STC F-Layer -- Forecast (3D).

Forward predictions for interoceptive-motor connectivity:
  F0: connectivity_pred -- Connectivity change prediction [0, 1]
  F1: respiratory_pred  -- Respiratory control prediction [0, 1]
  F2: vocal_pred        -- Vocal production prediction [0, 1]

Connectivity prediction forecasts the expected insula-sensorimotor
connectivity state at the next time step by combining current
interoceptive coupling (f28) with interoceptive periodicity at 1s.
connectivity_pred = sigma(0.5 * f28 + 0.5 * interoceptive_period_1s).

Respiratory prediction forecasts the expected respiratory integration
state by combining f29 with respiratory periodicity at 1s.
respiratory_pred = sigma(0.5 * f29 + 0.5 * respiratory_period_1s).

Vocal prediction forecasts the expected speech sensorimotor state
by combining f30 with vocal warmth at 100ms (fast timescale).
vocal_pred = sigma(0.5 * f30 + 0.5 * vocal_warmth_100ms).
Zarate 2010: involuntary pitch correction implies automatic predictive
vocal control.

H3 demands consumed: None new (all shared with E-layer):
  (33, 16, 14, 2) Interoceptive period 1s
  (25, 16, 14, 2) Respiratory period 1s
  (12, 3, 0, 2)   Vocal warmth 100ms

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/stc/f_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (shared with E-layer) ----------------------------
_INTERO_PER_H16 = (33, 16, 14, 2)    # x_l4l5 periodicity H16 L2
_RESP_PER_H16 = (25, 16, 14, 2)      # x_l0l5 periodicity H16 L2
_WARMTH_VAL_H3 = (12, 3, 0, 2)       # warmth value H3 L2


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: connectivity, respiratory, vocal predictions.

    F0 (connectivity_pred): sigma(0.5 * f28 + 0.5 * interoceptive_period_1s).
    Zamorano 2023: resting-state connectivity patterns persist beyond active
    singing, supporting forward prediction of connectivity dynamics.

    F1 (respiratory_pred): sigma(0.5 * f29 + 0.5 * respiratory_period_1s).
    Tsunada 2024: tonic vocal suppression (predictive component) supports
    forward respiratory prediction mechanisms.

    F2 (vocal_pred): sigma(0.5 * f30 + 0.5 * vocal_warmth_100ms).
    Zarate 2010: automatic pitch correction implies predictive vocal control.
    Uses fast warmth signal (100ms) because vocal articulation operates at
    a faster timescale than breathing or interoceptive monitoring.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f28, f29, f30)`` from extraction layer.
        m_outputs: ``(connectivity_strength, respiratory_index,
                      voice_body_coupling)`` from temporal integration.
        p_outputs: ``(insula_activity, vocal_motor)`` from cognitive present.

    Returns:
        ``(connectivity_pred, respiratory_pred, vocal_pred)`` each ``(B, T)``.
    """
    f28, f29, f30 = e_outputs

    # -- H3 features (shared with E-layer) --
    intero_per_1s = h3_features[_INTERO_PER_H16]    # (B, T)
    resp_per_1s = h3_features[_RESP_PER_H16]          # (B, T)
    warmth_val = h3_features[_WARMTH_VAL_H3]           # (B, T)

    # -- F0: Connectivity Prediction --
    # sigma(0.5 * f28 + 0.5 * interoceptive_period_1s)
    # Zamorano 2023: lasting connectivity patterns support prediction
    connectivity_pred = torch.sigmoid(
        0.50 * f28
        + 0.50 * intero_per_1s
    )

    # -- F1: Respiratory Prediction --
    # sigma(0.5 * f29 + 0.5 * respiratory_period_1s)
    # Tsunada 2024: tonic vocal suppression = predictive component
    respiratory_pred = torch.sigmoid(
        0.50 * f29
        + 0.50 * resp_per_1s
    )

    # -- F2: Vocal Prediction --
    # sigma(0.5 * f30 + 0.5 * vocal_warmth_100ms)
    # Zarate 2010: automatic pitch correction = predictive vocal control
    vocal_pred = torch.sigmoid(
        0.50 * f30
        + 0.50 * warmth_val
    )

    return connectivity_pred, respiratory_pred, vocal_pred
