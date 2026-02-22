"""MIAA M-Layer — Temporal Integration (2D).

Composite imagery dynamics from E-layer outputs.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/miaa/MIAA-temporal-integration.md

Simple weighted combinations — no R³/H³ needed at this layer.

Outputs:
    M0: activation_function   [0, 1]  Composite AC activation at time t
    M1: familiarity_effect    [0, 1]  Familiarity enhancement magnitude
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor


def compute_temporal_integration(
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: 2D composite dynamics from E-layer.

    Args:
        e_outputs: Tuple of (E0, E1, E2) from extraction.

    Returns:
        Tuple of (M0, M1), each ``(B, T)``.
    """
    e0, e1, e2 = e_outputs

    # M0: activation_function — composite AC activation
    #     Weighted sum of imagery activation (BA22+A1) and A1 modulation.
    #     0.60 weights general imagery higher than A1-specific modulation.
    m0 = 0.60 * e0 + 0.40 * e2

    # M1: familiarity_effect — enhancement scaled by base activation
    #     Familiarity enhancement only meaningful when base imagery is active.
    #     Product ensures both must be present for strong familiarity effect.
    m1 = e1 * e0

    return m0, m1
