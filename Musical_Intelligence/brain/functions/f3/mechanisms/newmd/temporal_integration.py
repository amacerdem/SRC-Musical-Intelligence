"""NEWMD M-Layer -- Temporal Integration (2D).

Temporal dynamics of the entrainment-WM paradox:
  M0: paradox_magnitude   (strength of entrainment when flexibility is low)
  M1: dual_route_balance  (balanced engagement of both processing routes)

M0 captures the paradox: high entrainment (E0) combined with low flexibility
(1-E2) produces a strong paradox -- the system is entrained but inflexible.
Grahn 2009: putamen activation tracks beat strength even when WM is loaded.

M1 captures dual-route balance: equal weighting of entrainment (E0) and WM
capacity (E1). When balanced, both routes contribute; when imbalanced, one
route dominates (captured by E3 dissociation index).

No additional H3 demands consumed beyond E-layer inputs.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/newmd/
Grahn 2009: fMRI, N=18.
Tierney 2014: behavioral+EEG, N=30.
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_temporal_integration(
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: paradox magnitude and dual-route balance.

    M0 reflects the entrainment-rigidity paradox: strong entrainment (E0)
    combined with low flexibility cost (1-E2) means the system locks to
    the beat but cannot adaptively switch. This is the core of the
    Tierney 2014 dissociation -- strong beat-locking with poor flexibility.

    M1 reflects the overall balance between both processing routes:
    when E0 and E1 are both high, dual-route balance is maximal.

    Args:
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1, e2, _e3 = e

    # -- M0: Paradox Magnitude --
    # Entrainment strength when flexibility is low: high E0 + low E2 = paradox.
    # Grahn 2009: putamen activation persists under WM load, reflecting
    # automatic beat processing that is independent of cognitive control.
    m0 = torch.sigmoid(e0 * (1.0 - e2))

    # -- M1: Dual Route Balance --
    # Balanced engagement of entrainment and WM routes.
    # Tierney 2014: individual differences reflect relative reliance on routes.
    m1 = torch.sigmoid(0.50 * e0 + 0.50 * e1)

    return m0, m1
