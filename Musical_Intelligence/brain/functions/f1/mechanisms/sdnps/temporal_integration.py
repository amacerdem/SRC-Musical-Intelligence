"""SDNPS M-Layer — Temporal Integration (1D).

Single composite function: NPS validity as a function of spectral complexity.

  M0: nps_stimulus_function — NPS × stimulus_dependency product

No H3/R3 dependencies — uses only E-layer outputs.

See Docs/C³/Models/SPU-γ1-SDNPS/SDNPS.md §7.2
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor


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

    # M0: NPS Stimulus Function
    # Maps the r=0.34→0.24→-0.10 degradation curve
    # f01 (NPS value) × f02 (stimulus dependency) = validity
    m0 = e0 * e1

    return (m0,)
