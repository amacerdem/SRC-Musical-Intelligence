"""AAC F-Layer -- Forecast (2D).

Two forward predictions for autonomic-arousal trajectory:

  F0: scr_pred_1s     -- SCR prediction 1s ahead [0, 1]
  F1: hr_pred_2s      -- HR prediction 2s ahead [0, 1]

H3 consumed:
    (7, 20, 4, 1)   amplitude max H20 L1     -- future energy 5s (SCR pred)
    (7, 22, 4, 1)   amplitude max H22 L1     -- future energy 15s (HR pred)

F-layer primarily reuses E+A/I/P outputs rather than reading new R3 directly.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/aac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_AMP_MAX_5S = (7, 20, 4, 1)
_AMP_MAX_15S = (7, 22, 4, 1)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ea_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
    i_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D forecast from E+A/I/P outputs + H3 context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        ea_outputs: ``(E0, E1, A0, A1, A2, A3, A4)`` each ``(B, T)``.
        i_outputs: ``(I0, I1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    _e0, _e1, a0, a1, _a2, _a3, _a4 = ea_outputs
    i0, i1 = i_outputs
    p0, _p1, p2 = p_outputs

    amp_max_5s = h3_features[_AMP_MAX_5S]
    amp_max_15s = h3_features[_AMP_MAX_15S]

    # F0: SCR prediction 1s ahead -- anticipatory sympathetic activation
    # Salimpoor 2009: anticipatory DA release in caudate precedes chills;
    # future energy peaks predict SCR onset
    f0 = torch.sigmoid(
        0.35 * amp_max_5s + 0.25 * a0 + 0.20 * p0
        + 0.20 * i0
    )

    # F1: HR prediction 2s ahead -- parasympathetic trajectory
    # Bernardi 2006: tempo modulates HR with ~2s lag; long-horizon
    # energy predicts sustained HR modulation
    f1 = torch.sigmoid(
        0.30 * amp_max_15s + 0.25 * a1 + 0.25 * p2
        + 0.20 * i1
    )

    return f0, f1
