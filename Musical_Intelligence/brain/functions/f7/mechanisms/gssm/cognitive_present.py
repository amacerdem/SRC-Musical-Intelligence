"""GSSM P-Layer -- Cognitive Present (2D).

Two present-state assessments of gait-synchronized stimulation:

  phase_lock_strength  -- Current gait-phase lock activity [0, 1]
  variability_level    -- Current stride variability (INVERTED balance) [0, 1]

H3 consumed (tuples 10-11):
    (25, 16, 21, 2) x_l0l5 zero_crossings H16 L2  -- coupling phase resets 1s
    (22, 8, 8, 0)   energy_change velocity H8 L0   -- energy dynamics 500ms

R3 consumed:
    [22]     energy_change   -- gait energy fluctuation
    [25:33]  x_l0l5          -- coupling phase resets

SPECIAL: variability_level uses INVERTED formula:
    sigma(0.5 * f07 + 0.5 * (1 - balance_var))
    where balance_var proxies balance variability from M-layer balance_score.

Grahn & Brett 2007: putamen Z=5.67 for beat period locking; SMA Z=5.03.
Yamashita 2025: stride time CV as primary outcome; CV-balance r = 0.62.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/gssm/p_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 10-11 from demand spec) --------------------------------
_COUPLING_ZC_1S = (25, 16, 21, 2)         # #10: coupling phase resets 1s
_ENERGY_VEL_500MS = (22, 8, 8, 0)         # #11: energy dynamics 500ms

# -- R3 indices ----------------------------------------------------------------
_ENERGY_CHANGE = 22          # D group
_X_L0L5_START = 25           # F group (coupling)
_X_L0L5_END = 33


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from H3/R3 + E/M outputs.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f07, f08, f09)`` each ``(B, T)``.
        m_outputs: ``(stride_cv, sma_m1_coupling, balance_score,
                      gait_stability)`` each ``(B, T)``.

    Returns:
        ``(phase_lock_strength, variability_level)`` each ``(B, T)``.
    """
    f07, f08, f09 = e_outputs
    stride_cv, sma_m1_coupling, balance_score, gait_stability = m_outputs

    # -- H3 features --
    coupling_zc_1s = h3_features[_COUPLING_ZC_1S]
    energy_vel_500ms = h3_features[_ENERGY_VEL_500MS]

    # -- R3 features --
    energy_change = r3_features[..., _ENERGY_CHANGE]            # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]      # (B, T, 8)
    coupling_mean = x_l0l5.mean(dim=-1)                         # (B, T)

    # phase_lock_strength (idx 7): Instantaneous gait-stimulation phase lock
    # Grahn & Brett 2007: putamen Z=5.67, SMA Z=5.03 for beat period locking
    # More phase resets (zero_crossings) = weaker phase lock (negative indicator)
    # Yamashita 2025: continuous heel-strike phase-locked stimulation
    phase_lock_strength = torch.sigmoid(
        0.40 * f07
        + 0.30 * sma_m1_coupling * coupling_mean
        - 0.30 * coupling_zc_1s
    )

    # variability_level (idx 8): Instantaneous stride variability
    # SPECIAL INVERTED formula: sigma(0.5*f07 + 0.5*(1 - balance_var))
    # Uses balance_score as proxy for balance_var (higher balance = lower var)
    # Energy velocity at 500ms (half-stride) captures gait energy variability
    # Yamashita 2025: CV from 20 stride steps; continuous frame-by-frame version
    balance_var = balance_score  # proxy from M-layer
    variability_level = torch.sigmoid(
        0.35 * stride_cv
        + 0.35 * energy_vel_500ms * energy_change
        + 0.30 * (1.0 - balance_var)
    )

    return phase_lock_strength, variability_level
