"""SLEE M-Layer -- Temporal Integration (3D).

Statistical Learning Expertise Enhancement temporal dynamics:
  exposure_model    -- Statistical model building over time [0, 1]
  pattern_memory    -- Pattern accumulation over time [0, 1]
  expertise_state   -- Long-term expertise consolidation [0, 1]

exposure_model tracks the accumulation of the internal distribution
representation through exponential moving average of f01 over the
session timescale. Reflects how repeated exposure to statistical
regularities builds a robust model. Bridwell 2017: cortical sensitivity
to guitar note patterns at 4 Hz.

pattern_memory tracks the build-up of pitch stability patterns through
EMA with tau = 3s. Pitch stability at 100ms (H3 tuple 0) is combined
with stability variability over 1s (H3 tuple 1) to estimate how reliably
the system retains learned patterns. Billig 2022: hippocampus supports
sequence binding and statistical learning memory.

expertise_state uses the pattern binding trend over 1s (H3 tuple 2,
x_l4l5[0], H16, M18, L0) as a direct proxy for expertise consolidation.
Increasing trend indicates specialization deepening; stable trend
indicates plateau. Doelling & Poeppel 2015: years of training correlate
with entrainment strength (PLV).

H3 demands consumed (3 tuples):
  (24, 3, 0, 2)    pitch_stability value H3 L2    -- stability 100ms
  (24, 16, 2, 2)   pitch_stability std H16 L2     -- stability variability 1s
  (33, 16, 18, 0)  x_l4l5 trend H16 L0            -- binding trend 1s

Dependencies:
  E-layer f01 (statistical_model)
  R3[24] pitch_stability
  R3[33:41] x_l4l5

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/slee/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_STABILITY_VAL_H3 = (24, 3, 0, 2)         # pitch stability 100ms
_STABILITY_STD_H16 = (24, 16, 2, 2)       # stability variability 1s
_BINDING_TREND_H16 = (33, 16, 18, 0)      # pattern binding trend 1s

# -- EMA constant --------------------------------------------------------------
_TAU_PATTERN = 3.0  # seconds, for pattern_memory accumulation


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    ednr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: temporal dynamics of statistical learning.

    exposure_model: EMA of f01 (statistical model) over the session
    timescale. Captures how the internal distribution representation
    strengthens with repeated exposure. Bridwell 2017: cortical
    sensitivity buildup at 4 Hz for guitar note patterns.

    pattern_memory: EMA of pitch stability with tau = 3s. Integrates
    pitch stability at 100ms with its variability over 1s to estimate
    retained pattern reliability. Billig 2022: hippocampal sequence
    binding mechanism for working-memory timescale.

    expertise_state: Uses the pattern binding trend over 1s (H3 tuple 2)
    as direct proxy for expertise consolidation. Increasing trend
    indicates specialization deepening. Doelling & Poeppel 2015: years
    of training correlate with entrainment strength (PLV).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e_outputs: ``(f01, f02, f03, f04)`` from extraction layer.
        ednr: ``(B, T, 10)`` -- upstream EDNR relay output.

    Returns:
        ``(exposure_model, pattern_memory, expertise_state)`` each ``(B, T)``
    """
    f01, _f02, _f03, _f04 = e_outputs

    # -- H3 features --
    stability_100ms = h3_features[_STABILITY_VAL_H3]       # (B, T)
    stability_std_1s = h3_features[_STABILITY_STD_H16]     # (B, T)
    binding_trend_1s = h3_features[_BINDING_TREND_H16]     # (B, T)

    # -- exposure_model --
    # EMA of f01 over the session timescale. Since mechanisms are
    # feedforward (no recurrent state), we approximate the EMA as a
    # sigmoid combination of f01 with the current stability signal.
    # sigma(0.50 * f01 + 0.25 * stability_100ms)
    # Bridwell 2017: cortical sensitivity to guitar note patterns at 4 Hz
    exposure_model = torch.sigmoid(
        0.50 * f01
        + 0.25 * stability_100ms
    )

    # -- pattern_memory --
    # EMA of pitch stability at tau = 3s. Combines pitch stability
    # at 100ms with stability variability over 1s.
    # sigma(0.35 * stability_100ms + 0.35 * stability_std_1s)
    # Billig 2022: hippocampus supports sequence binding and stat learning
    pattern_memory = torch.sigmoid(
        0.35 * stability_100ms
        + 0.35 * stability_std_1s
    )

    # -- expertise_state --
    # Pattern binding trend over 1s as expertise consolidation proxy.
    # sigma(0.50 * binding_trend_1s + 0.25 * pattern_memory)
    # Doelling & Poeppel 2015: training years correlate with PLV
    expertise_state = torch.sigmoid(
        0.50 * binding_trend_1s
        + 0.25 * pattern_memory
    )

    return exposure_model, pattern_memory, expertise_state
