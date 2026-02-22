"""MSR F-Layer -- Forecast (2D).

Two forward predictions for sensorimotor processing:

  performance_efficiency  -- Trial-level efficiency prediction [0, 1]
  processing_automaticity -- Session-level automaticity [0, 1]

H3 consumed (tuples 19-21 from demand spec):
    (7, 3, 0, 2)    amplitude value H3 L2     -- motor drive 100ms
    (7, 16, 1, 2)   amplitude mean H16 L2     -- sustained motor state 1s
    (21, 4, 8, 2)   spectral_change vel H4 L2 -- tempo velocity 125ms

M-layer consumed:
    efficiency_index  -- Current efficiency feeds performance prediction

P-layer consumed:
    training_level    -- Training estimate feeds automaticity prediction

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/msr/f_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 19-21 from demand spec) --------------------------------
_AMP_VAL_100MS = (7, 3, 0, 2)       # #19: amplitude at 100ms -- motor drive
_AMP_MEAN_1S = (7, 16, 1, 2)        # #20: mean amplitude 1s -- sustained motor
_TEMPO_VEL_125MS = (21, 4, 8, 2)    # #21: tempo velocity 125ms -- rate dynamics


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D forecast from E/M/P outputs + H3.

    Generates predictions about future sensorimotor processing efficiency:
        performance_efficiency: Trial-level performance from PLV/P2 balance +
            motor dynamics. Grahn & Brett 2007. Alpheis 2025.
        processing_automaticity: Session-level automaticity from training level
            + long-term amplitude stability. Blasi 2025. Fujioka 2012.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f04, f05, f06)`` each ``(B, T)``.
        m_outputs: ``(plv_high_freq, p2_amplitude, efficiency_index)`` each ``(B, T)``.
        p_outputs: ``(bottom_up_precision, top_down_modulation, training_level)`` each ``(B, T)``.

    Returns:
        ``(performance_efficiency, processing_automaticity)`` each ``(B, T)``.
    """
    _f04, _f05, f06 = e_outputs
    _plv_high_freq, _p2_amplitude, efficiency_index = m_outputs
    _bottom_up_precision, _top_down_modulation, training_level = p_outputs

    # -- H3 features --
    amp_val_100ms = h3_features[_AMP_VAL_100MS]
    amp_mean_1s = h3_features[_AMP_MEAN_1S]
    tempo_vel_125ms = h3_features[_TEMPO_VEL_125MS]

    # performance_efficiency (idx 9): Trial-level efficiency prediction
    # Grahn & Brett 2007: musicians show consistent motor-area activation
    # Alpheis 2025: stable FC patterns in trained musicians
    # Combines efficiency index (M-layer) with motor dynamics signals
    performance_efficiency = torch.sigmoid(
        0.35 * efficiency_index
        + 0.25 * f06
        + 0.25 * amp_val_100ms
        + 0.15 * tempo_vel_125ms
    )

    # processing_automaticity (idx 10): Session-level automaticity
    # Blasi 2025: structural neuroplasticity (GMV increases in IFG, cerebellum)
    # Fujioka 2012: internalized timing in beta oscillations
    # Combines training level (P-layer) with long-term amplitude stability
    processing_automaticity = torch.sigmoid(
        0.40 * training_level
        + 0.30 * amp_mean_1s
        + 0.15 * efficiency_index
        + 0.15 * amp_val_100ms
    )

    return performance_efficiency, processing_automaticity
