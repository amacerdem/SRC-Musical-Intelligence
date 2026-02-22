"""GSSM F-Layer -- Forecast (2D).

Two therapeutic outcome predictions:

  cv_pred_30min  -- CV prediction with 30-minute persistence [0, 1]
  balance_pred   -- Balance score prediction [0, 1]

H3 consumed: 0 unique tuples. Reuses coupling_periodicity_1s (25, 16, 14, 2)
from the M-layer demand set.

Yamashita 2025: stimulation effects persist post-session; 15-session protocol
showed cumulative benefit with walking speed increase at session 15 vs 1
(p = 0.002). Sansare 2025: cerebellar iTBS reduced postural sway for >= 30 min.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/gssm/f_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (shared with M-layer, no unique demands) -----------------------
_COUPLING_PERIOD_1S = (25, 16, 14, 2)     # shared #9: coupling periodicity 1s


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D forecast from E/M/P outputs + shared H3.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f07, f08, f09)`` each ``(B, T)``.
        m_outputs: ``(stride_cv, sma_m1_coupling, balance_score,
                      gait_stability)`` each ``(B, T)``.
        p_outputs: ``(phase_lock_strength, variability_level)``
                   each ``(B, T)``.

    Returns:
        ``(cv_pred_30min, balance_pred)`` each ``(B, T)``.
    """
    f07, f08, f09 = e_outputs
    stride_cv, sma_m1_coupling, balance_score, gait_stability = m_outputs
    phase_lock_strength, variability_level = p_outputs

    # Reuse coupling periodicity from shared M-layer demand
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]

    # cv_pred_30min (idx 9): CV prediction with 30-minute persistence
    # Yamashita 2025: stimulation effects persist post-session
    # Sansare 2025: cerebellar iTBS effects sustained >= 30 min
    # sigma(0.5 * f08 + 0.5 * coupling_periodicity_1s)
    cv_pred_30min = torch.sigmoid(
        0.50 * f08
        + 0.50 * coupling_period_1s * sma_m1_coupling
    )

    # balance_pred (idx 10): Balance score prediction
    # Yamashita 2025: Mini-BESTest d=1.05; CV-balance r=0.62
    # sigma(0.5 * f09 + 0.5 * gait_stability)
    # Longer-horizon: current gait quality predicts future balance
    balance_pred = torch.sigmoid(
        0.50 * f09
        + 0.50 * gait_stability
    )

    return cv_pred_30min, balance_pred
