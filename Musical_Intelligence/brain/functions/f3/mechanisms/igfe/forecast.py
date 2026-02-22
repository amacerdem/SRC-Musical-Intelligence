"""IGFE F-Layer -- Forecast (2D).

Two forward predictions for post-stimulation cognitive enhancement:

  F0: memory_enhancement_post     -- Predicted memory improvement post-tACS [0, 1]
  F1: executive_improve_post      -- Predicted executive improvement post-tACS [0, 1]

No H3 consumed -- forecast is derived entirely from E and P layer outputs.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/igfe/IGFE-forecast.md
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_forecast(
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D forecast from E and P outputs.

    Args:
        e: ``(E0, E1, E2, E3)`` each ``(B, T)``.
        p: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    _e0, e1, e2, e3 = e

    # F0: Memory enhancement post-stimulation
    # Rufener 2016: sustained memory benefits after gamma tACS
    f0 = torch.sigmoid(
        0.50 * e1 + 0.50 * e3
    )

    # F1: Executive improvement post-stimulation
    # Rufener 2016: sustained executive benefits after gamma tACS
    f1 = torch.sigmoid(
        0.50 * e2 + 0.50 * e3
    )

    return f0, f1
