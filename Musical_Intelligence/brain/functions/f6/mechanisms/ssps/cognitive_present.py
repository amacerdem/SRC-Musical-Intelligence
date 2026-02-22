"""SSPS P-Layer -- Cognitive Present (1D).

Present-moment position on the saddle-shaped preference surface:
  surface_position_state  -- Current surface position [0, 1]

Summarises where the listener currently sits on the saddle-shaped IC x entropy
preference surface as a single present-moment value.  Values near 1.0 indicate
proximity to an optimal zone peak; values near 0.5 indicate the saddle trough;
values near 0.0 indicate distance from both peaks.

Cheung et al. 2019: Bilateral amygdala/hippocampus and auditory cortex show
IC x entropy interaction reflecting surface position.

H3 demands consumed: None new (reuses E-layer outputs f03 and f04).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ssps/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    h3_features: dict,
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """Compute P-layer: surface position state (1D).

    surface_position_state: Equal blend of saddle position (f03, which zone)
    and peak proximity (f04, how optimal).  Sigmoid activation bounds output
    to [0, 1].

    Cheung 2019: bilateral amygdala/hippocampus show IC x entropy interaction.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}`` (unused).
        r3_features: ``(B, T, 97)`` R3 spectral features (unused).
        e_outputs: ``(f01, f02, f03, f04, saddle_value)`` from E-layer.

    Returns:
        ``(surface_position_state,)`` -- single ``(B, T)`` tensor.
    """
    _f01, _f02, f03, f04, _saddle_value = e_outputs

    # -- surface_position_state --
    # sigma(0.5 * f03_saddle_position + 0.5 * f04_peak_proximity)
    # Equal weighting: both the surface position (which zone) and peak
    # proximity (how optimal) contribute equally to the present-state summary.
    surface_position = torch.sigmoid(0.5 * f03 + 0.5 * f04)

    return (surface_position,)
