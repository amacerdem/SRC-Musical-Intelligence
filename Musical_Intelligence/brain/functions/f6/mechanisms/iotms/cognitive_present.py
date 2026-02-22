"""IOTMS P-Layer -- Cognitive Present (1D).

Present-moment individual sensitivity state:
  P0: individual_sensitivity_state -- Current trait sensitivity [0, 1]

The P-layer produces a single present-moment summary of the individual's
music reward sensitivity. It combines two E-layer features with equal
weight:
  - f01 (MOR baseline proxy, 50%): neurochemical foundation
  - f03 (reward propensity, 50%): behavioral expression

individual_sensitivity = sigma(0.5 * f01 + 0.5 * f03)

This is a trait-level feature that changes slowly -- it represents a
stable individual difference in music reward sensitivity rather than a
time-varying event signal. Frame-to-frame variation reflects only the
slow temporal dynamics of the underlying H3 features at H8/H16 horizons.

Putkinen 2025: individual MOR tone modulates pleasure response magnitude.

H3 demands consumed: None new (reuses E-layer outputs f01, f03).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/iotms/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """Compute P-layer: 1D individual sensitivity state.

    Equal-weighted blend of MOR baseline (neurochemical trait) and
    reward propensity (behavioral trait). Sigmoid bounds the output
    to [0, 1].

    Putkinen 2025: individual MOR tone modulates pleasure response
    magnitude. Equal weighting reflects that both neurochemical
    availability and behavioral tendency contribute equally.

    Args:
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)`` from E-layer.

    Returns:
        ``(p0,)`` each ``(B, T)``.
    """
    f01, _f02, f03, _f04 = e_outputs

    # -- P0: Individual Sensitivity State --
    # sigma(0.5 * f01_mor_baseline_proxy + 0.5 * f03_reward_propensity)
    # Putkinen 2025: individual MOR tone modulates pleasure response
    p0 = torch.sigmoid(
        0.50 * f01
        + 0.50 * f03
    )

    return (p0,)
