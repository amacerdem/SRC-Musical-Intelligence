"""PEOM P-Layer -- Cognitive Present (2D).

Two present-processing dimensions for period entrainment state:

  period_lock_strength   -- Current period-locked neural activity strength [0, 1]
  kinematic_smoothness   -- Current jerk-reduction metric [0, 1]

H3 consumed (tuples 13-14):
    (25, 16, 14, 2) coupling periodicity H16 L2       -- lock stability 1s
    (25, 16, 21, 2) coupling zero_crossings H16 L2    -- lock disruptions 1s

R3 consumed:
    [25:33]  x_l0l5                   -- motor-auditory coupling

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/peom/p_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 13-14 from demand spec) --------------------------------
_COUPLING_PERIOD_1S = (25, 16, 14, 2)      # #13: coupling periodicity 1s
_COUPLING_ZC_1S = (25, 16, 21, 2)          # #14: coupling zero-crossings 1s

# -- R3 indices ----------------------------------------------------------------
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from H3/R3 + E/M outputs.

    P-layer outputs are the primary relay exports:
        period_lock_strength -> F3 Attention salience, cross-relay motor timing
        kinematic_smoothness -> F5 Emotion motor fluency contribution

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03)`` each ``(B, T)``.
        m_outputs: ``(motor_period, velocity, acceleration, cv_reduction)``
                   each ``(B, T)``.

    Returns:
        ``(period_lock_strength, kinematic_smoothness)`` each ``(B, T)``.
    """
    f01, f02, _f03 = e_outputs
    _motor_period, velocity, _acceleration, _cv_reduction = m_outputs

    # -- H3 features --
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]  # lock stability
    coupling_zc_1s = h3_features[_COUPLING_ZC_1S]          # lock disruptions

    # -- R3 features --
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    coupling = x_l0l5.mean(dim=-1)                          # (B, T)

    # Period lock strength: how firmly motor is locked to auditory period
    # Fujioka 2012: beta oscillations in SMA modulated by rhythmic stimulus
    # Nozaradan 2011: neural entrainment to beat frequencies
    # Combines f01 (entrainment) + coupling periodicity - zero-crossings
    period_lock_strength = torch.sigmoid(
        0.35 * f01 * coupling_period_1s
        + 0.35 * coupling * coupling_period_1s
        + 0.30 * (1.0 - coupling_zc_1s) * f01
    )

    # Kinematic smoothness: jerk-reduction under period entrainment
    # Thaut 2015: fixed period CTR reduces jerk
    # Thaut 2009b: distinct cortico-cerebellar activations
    # sigma(coupling_periodicity + 0.5 * velocity)
    kinematic_smoothness = torch.sigmoid(
        0.40 * coupling_period_1s
        + 0.30 * velocity
        + 0.30 * f02 * coupling
    )

    return period_lock_strength, kinematic_smoothness
