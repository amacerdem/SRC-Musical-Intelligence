"""SDED M-Layer — Temporal Integration (1D).

Single composite detection function combining early detection
with MMN deviation signal:

  M0: detection_function — Combined roughness detection strength

No H3/R3 dependencies — uses only E-layer outputs.

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/sded/SDED-temporal-integration.md
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def _wsig(x: Tensor) -> Tensor:
    """Wide sigmoid — full [0, 1] dynamic range (gain=5, center=0.35)."""
    return (1.0 + torch.exp(-5.0 * (x - 0.35))).reciprocal()


def compute_temporal_integration(
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """M-layer: 1D temporal integration from E-layer.

    Args:
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.

    Returns:
        ``(M0,)`` single-element tuple, ``(B, T)``.
    """
    e0, e1, _e2 = e_outputs

    # M0: Combined detection function
    # Integrates early detection (0.60) with MMN deviation (0.40).
    # Conservative sigmoid: max input ~1.0, output ~[0.50, 0.73].
    # Bidelman 2013: brainstem encodes consonance hierarchy innately
    m0 = _wsig(0.60 * e0 + 0.40 * e1)

    return (m0,)
