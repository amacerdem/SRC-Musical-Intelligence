"""GSSM M-Layer -- Temporal Integration (4D).

Four integrated gait function estimates:

  stride_cv         -- Coefficient of variation of stride time [0, 1]
  sma_m1_coupling   -- SMA-M1 synchronization strength [0, 1]
  balance_score     -- Normalized Mini-BESTest score [0, 1]
  gait_stability    -- Overall gait pattern stability [0, 1]

H3 consumed (tuples 7-9):
    (7, 3, 0, 2)    amplitude value H3 L2          -- step amplitude 100ms
    (7, 16, 1, 2)   amplitude mean H16 L2          -- mean amplitude 1s
    (25, 16, 14, 2) x_l0l5 periodicity H16 L2      -- coupling periodicity 1s

R3 consumed:
    [7]      amplitude      -- step force for stride CV
    [25:33]  x_l0l5         -- SMA-M1 coupling

Yamashita 2025: CV = (SD/Mean)*100 from 20 stride time steps; tDCS (2mA) to
SMA (Fz) + gait-synchronized tACS to M1 (1cm lat/post from Cz).

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/gssm/m_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 7-9 from demand spec) ----------------------------------
_AMP_VAL_100MS = (7, 3, 0, 2)              # #7: step amplitude 100ms
_AMP_MEAN_1S = (7, 16, 1, 2)              # #8: mean amplitude 1s
_COUPLING_PERIOD_1S = (25, 16, 14, 2)     # #9: coupling periodicity 1s

# -- R3 indices ----------------------------------------------------------------
_AMPLITUDE = 7               # B group (velocity_A)
_X_L0L5_START = 25           # F group (coupling)
_X_L0L5_END = 33


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """M-layer: 4D temporal integration from E-layer + H3/R3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f07, f08, f09)`` each ``(B, T)``.

    Returns:
        ``(stride_cv, sma_m1_coupling, balance_score, gait_stability)``
        each ``(B, T)``.
    """
    f07, f08, f09 = e_outputs

    # -- H3 features --
    amp_val_100ms = h3_features[_AMP_VAL_100MS]
    amp_mean_1s = h3_features[_AMP_MEAN_1S]
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]

    # -- R3 features --
    amplitude = r3_features[..., _AMPLITUDE]                    # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]      # (B, T, 8)
    coupling_mean = x_l0l5.mean(dim=-1)                         # (B, T)

    # stride_cv (idx 3): Coefficient of variation of stride time
    # Yamashita 2025: CV from 20 stride time steps, real stim 4.51->2.80
    # Incorporates step amplitude at 100ms and mean amplitude at 1s
    stride_cv = torch.sigmoid(
        0.35 * amp_val_100ms * amplitude
        + 0.35 * amp_mean_1s
        + 0.30 * f08
    )

    # sma_m1_coupling (idx 4): SMA-M1 synchronization strength
    # Yamashita 2025: tDCS to SMA + tACS to M1, dual-site protocol
    # Coupling periodicity at 1s stride-level horizon
    sma_m1_coupling = torch.sigmoid(
        0.40 * coupling_period_1s * coupling_mean
        + 0.30 * amp_mean_1s * amplitude
        + 0.30 * f07
    )

    # balance_score (idx 5): Normalized Mini-BESTest score
    # Directly inherits from f09 (E-layer balance improvement)
    # Yamashita 2025: Mini-BESTest d = 1.05, eta_p^2 = 0.309
    balance_score = torch.sigmoid(
        0.50 * f09
        + 0.25 * coupling_mean * coupling_period_1s
        + 0.25 * amp_val_100ms * amplitude
    )

    # gait_stability (idx 6): Overall gait pattern stability
    # Combined index: sigma(0.5 * f07 + 0.5 * f08)
    # Higher stability = better gait under synchronized stimulation
    gait_stability = torch.sigmoid(
        0.50 * f07
        + 0.50 * f08
    )

    return stride_cv, sma_m1_coupling, balance_score, gait_stability
