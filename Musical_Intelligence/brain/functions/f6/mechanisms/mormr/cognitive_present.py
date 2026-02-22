"""MORMR P-Layer -- Cognitive Present (1D).

One present-processing dimension for opioid state:

  current_opioid_state  -- Real-time mu-opioid receptor activity [0, 1]

H3 consumed (tuples 12-14):
    (22, 8, 8, 0)    energy_change velocity H8 L0          -- energy velocity 500ms
    (33, 8, 1, 2)    x_l4l5[0] mean H8 L2                 -- sustained pleasure 500ms
    (33, 16, 18, 0)  x_l4l5[0] trend H16 L0               -- pleasure trend 1s

P-layer output is the primary relay export for:
    - The reward computation (opioid contribution to overall reward signal)
    - Cross-relay interaction with DAED (dopamine + opioid convergence at NAcc)
    - Downstream ARU pleasure/arousal signals (opioid drives hedonic tone)

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/mormr/p_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 12-14 from demand spec) --------------------------------
_ENERGY_VEL_500MS = (22, 8, 8, 0)       # #12: energy velocity at 500ms
_PLEAS_MEAN_500MS = (33, 8, 1, 2)       # #13: sustained pleasure mean 500ms
_PLEAS_TREND_1S = (33, 16, 18, 0)       # #14: pleasure trend over 1s


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
) -> Tuple[Tensor]:
    """P-layer: 1D present processing from E/M outputs + H3 context.

    Produces the "present-moment" opioid state that is exported to the C3
    kernel scheduler. Combines opioid release (f01), opioid tone (M-layer),
    and sustained pleasure trajectory to produce a temporally smooth
    representation of the listener's opioid-mediated pleasure.

    The longer decay constant (tau = 5.0s vs DAED's tau = 3.0s) reflects the
    slower pharmacokinetics of the mu-opioid system compared to dopamine.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        m_outputs: ``(opioid_tone,)`` each ``(B, T)``.

    Returns:
        ``(current_opioid_state,)`` -- single tensor ``(B, T)`` wrapped in 1-tuple.
    """
    f01, f02, _f03, _f04 = e_outputs
    (opioid_tone,) = m_outputs

    energy_vel_500ms = h3_features[_ENERGY_VEL_500MS]
    pleas_mean_500ms = h3_features[_PLEAS_MEAN_500MS]
    pleas_trend_1s = h3_features[_PLEAS_TREND_1S]

    # current_opioid_state: Real-time mu-opioid receptor activity
    # Putkinen 2025: music-induced [11C]carfentanil binding changes in
    # VS, OFC, amygdala, thalamus, and temporal pole.
    # Integrates opioid release, opioid tone, and pleasure trajectory.
    current_opioid_state = torch.sigmoid(
        0.30 * f01
        + 0.25 * opioid_tone
        + 0.20 * pleas_mean_500ms
        + 0.15 * pleas_trend_1s
        + 0.10 * energy_vel_500ms
    )

    return (current_opioid_state,)
