"""LDAC P-Layer -- Cognitive Present (1D).

Present-moment STG modulation state:
  P0: stg_modulation_state -- Current STG modulation level [0, 1]

STG modulation state (P0) summarizes the present-moment state of
pleasure-dependent auditory cortex modulation. Equally weights the
continuous tracking signal (f04 / E3) and the pleasure gating signal
(f02 / E1). High values indicate strong reward-driven enhancement of
sensory processing; low values indicate suppressed or neutral auditory
cortex response.

tau_decay = 0.5s reflects rapid continuous tracking
(Gold 2023a continuous joystick data).

H3 demands consumed: None. Operates entirely on E-layer outputs (f02, f04).
All temporal dynamics are inherited from the E-layer's H3 demands.

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ldac/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """Compute P-layer: 1D STG modulation state.

    P0 (stg_modulation_state): Present-moment summary combining the
    moment-to-moment tracking signal (f04, w=0.50) with pleasure gating
    (f02, w=0.50). The equal weighting reflects that modulation state is
    determined both by the integrated tracking output and by the direct
    pleasure gating pathway.

    tau_decay = 0.5s, consistent with Gold et al. 2023a's continuous
    joystick paradigm showing rapid tracking of liking-dependent STG
    modulation.

    Args:
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``
            from extraction layer.

    Returns:
        ``(P0,)`` each ``(B, T)``.
    """
    _f01, f02, _f03, f04 = e_outputs

    # -- P0: STG Modulation State ----------------------------------------------
    # sigma(0.5 * f04 + 0.5 * f02)
    # Gold et al. 2023a: continuous tracking at sub-second timescale
    p0 = torch.sigmoid(
        0.50 * f04
        + 0.50 * f02
    )

    return (p0,)
