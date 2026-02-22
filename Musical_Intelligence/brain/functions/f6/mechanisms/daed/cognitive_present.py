"""DAED P-Layer -- Cognitive Present (2D).

Two present-moment dopamine system states exported to the C3 kernel:

  caudate_activation  -- Current caudate nucleus activation state [0, 1]
  nacc_activation     -- Current nucleus accumbens activation state [0, 1]

H3 consumed (tuples 14-15 from demand spec):
    (22, 8, 8, 0)   energy_change velocity H8 L0       -- dynamic build-up rate
    (25, 8, 0, 2)   x_l0l5 value H8 L2                -- present coupling state

P-layer outputs are the primary relay exports:
    caudate_activation  -> kernel scheduler, reward computation, salience
    nacc_activation     -> kernel scheduler, reward computation, salience

The temporal dissociation between these two signals (caudate leads, NAcc follows)
is the fundamental finding of Salimpoor (2011) and the core DAED model output.

Salimpoor 2011: caudate [11C]raclopride binding decreases (DA release) 15-30s
    before peak emotion (t = 3.2).
Salimpoor 2011: NAcc [11C]raclopride binding decreases at peak moment
    (t = 2.8, r = 0.84 vs pleasure rating).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/daed/p_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 14-15 from demand spec) --------------------------------
_ENERGY_VEL_500MS = (22, 8, 8, 0)       # #14: energy velocity 500ms -- build-up rate
_COUPLING_VAL_500MS = (25, 8, 0, 2)     # #15: coupling at 500ms -- present state


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from H3/R3 + E/M outputs.

    Produces the "present-moment" cognitive state of the mesolimbic dopamine
    system. These are the exported relay fields that the C3 kernel scheduler
    reads.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        m_outputs: ``(dissociation_index, temporal_phase)`` each ``(B, T)``.

    Returns:
        ``(caudate_activation, nacc_activation)`` each ``(B, T)``.
    """
    f01, f02, f03, f04 = e_outputs
    _dissociation_index, temporal_phase = m_outputs

    energy_vel_500ms = h3_features[_ENERGY_VEL_500MS]
    coupling_val_500ms = h3_features[_COUPLING_VAL_500MS]

    # caudate_activation: current anticipatory dopamine level
    # Salimpoor 2011: caudate [11C]raclopride BP decreases 15-30s before peak (t=3.2)
    # Combines f01 (anticipatory DA), f03 (wanting), and energy velocity
    # sigma(0.35 * f01 + 0.30 * f03 + 0.20 * energy_vel_500ms + 0.15 * temporal_phase)
    caudate_activation = torch.sigmoid(
        0.35 * f01
        + 0.30 * f03
        + 0.20 * energy_vel_500ms
        + 0.15 * temporal_phase
    )

    # nacc_activation: current consummatory dopamine level
    # Salimpoor 2011: NAcc [11C]raclopride BP decreases at peak (t=2.8, r=0.84)
    # Combines f02 (consummatory DA), f04 (liking), and coupling state
    # sigma(0.35 * f02 + 0.30 * f04 + 0.20 * coupling_val_500ms + 0.15 * (1 - temporal_phase))
    nacc_activation = torch.sigmoid(
        0.35 * f02
        + 0.30 * f04
        + 0.20 * coupling_val_500ms
        + 0.15 * (1.0 - temporal_phase)
    )

    return caudate_activation, nacc_activation
