"""RPEM P-Layer -- Cognitive Present (2D).

Two present-moment RPE state dimensions:

  current_rpe           -- Signed RPE: clamp(f03 - f04 + 0.5, 0, 1) [0, 1]
  vs_activation_state   -- VS engagement: sigma(0.5*current_rpe + 0.5*rpe_magnitude) [0, 1]

P-layer outputs are the primary relay exports:
    current_rpe          -> reward learning signal, precision engine
    vs_activation_state  -> salience, cross-relay DAED interaction

H3 consumed (tuples 13-14):
    (33, 8, 8, 0)   x_l4l5[0] velocity H8 L0   -- RPE coupling velocity 500ms
    (25, 8, 1, 2)   x_l0l5[0] mean H8 L2       -- prediction mean 500ms

Gold 2023: VS RPE crossover (d = 1.07).
Cheung 2019: uncertainty x surprise jointly predict pleasure.
Salimpoor 2011: DA release in VS at emotional peaks.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 13-14 from demand spec) --------------------------------
_RPE_COUPLING_VEL_500MS = (33, 8, 8, 0)   # #13: RPE coupling velocity 500ms
_PRED_MEAN_500MS = (25, 8, 1, 2)          # #14: prediction mean 500ms


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present-moment RPE state from E/M layers + H3.

    P-layer outputs are the primary relay exports:
        current_rpe         -> reward computation, precision engine
        vs_activation_state -> salience, cross-relay DAED interaction

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        m_outputs: ``(rpe_magnitude, vs_response)`` each ``(B, T)``.

    Returns:
        ``(current_rpe, vs_activation_state)`` each ``(B, T)``.
    """
    _f01, _f02, f03, f04 = e_outputs
    rpe_magnitude, _vs_response = m_outputs

    # H3 features for RPE dynamics context
    _ = h3_features[_RPE_COUPLING_VEL_500MS]  # RPE coupling velocity
    _ = h3_features[_PRED_MEAN_500MS]         # prediction mean baseline

    # current_rpe: Signed reward prediction error centered at 0.5.
    # clamp(f03 - f04 + 0.5, 0, 1)
    # > 0.5 = positive RPE (better than expected)
    # < 0.5 = negative RPE (worse than expected)
    # = 0.5 = matched expectations
    # Gold 2023: VS RPE crossover (d = 1.07).
    # Cheung 2019: uncertainty x surprise jointly determine pleasure.
    current_rpe = torch.clamp(f03 - f04 + 0.5, 0.0, 1.0)

    # vs_activation_state: Overall VS engagement regardless of RPE sign.
    # sigma(0.5 * current_rpe + 0.5 * rpe_magnitude)
    # Combines signed RPE + unsigned magnitude for total striatal processing.
    # Gold 2023: VS shows IC x liking interaction.
    # Salimpoor 2011: DA release in VS at emotional peaks.
    vs_activation_state = torch.sigmoid(
        0.5 * current_rpe + 0.5 * rpe_magnitude
    )

    return current_rpe, vs_activation_state
