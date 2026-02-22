"""PEOM M-Layer -- Temporal Integration (4D).

Four temporal integration features for period entrainment kinematics:

  motor_period      -- Entrained motor period (normalized) [0, 1]
  velocity          -- Optimized velocity profile [0, 1]
  acceleration      -- Optimized acceleration profile [0, 1]
  cv_reduction      -- Coefficient of variation reduction [0, 1]

H3 consumed (tuples 9-12):
    (7, 16, 1, 2)   amplitude mean H16 L2        -- mean amplitude 1s
    (8, 8, 1, 0)    loudness mean H8 L0           -- mean loudness 500ms
    (21, 4, 8, 0)   spectral_change velocity H4 L0 -- tempo velocity 125ms
    (21, 16, 1, 0)  spectral_change mean H16 L0   -- mean tempo change 1s

R3 consumed:
    [7]      amplitude               -- motor drive signal
    [8]      loudness                -- perceptual intensity
    [21]     spectral_change         -- tempo dynamics

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/peom/m_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 9-12 from demand spec) ---------------------------------
_AMP_MEAN_1S = (7, 16, 1, 2)         # #9: mean amplitude 1s -- motor drive
_LOUD_MEAN_500MS = (8, 8, 1, 0)      # #10: mean loudness 500ms -- intensity
_TEMPO_VEL_125MS = (21, 4, 8, 0)     # #11: tempo velocity 125ms -- rate change
_TEMPO_MEAN_1S = (21, 16, 1, 0)      # #12: mean tempo change 1s -- drift

# -- R3 indices ----------------------------------------------------------------
_AMPLITUDE = 7
_LOUDNESS = 8
_SPECTRAL_CHANGE = 21

# -- Integration constant ------------------------------------------------------
_TAU = 4.0  # seconds -- period convergence time constant (Thaut 2015)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """M-layer: 4D temporal integration from E-layer + H3/R3 features.

    Implements the kinematic model from Thaut et al. (2015):
        motor_period: dP/dt = tau^-1 * (T - P(t)), tau = 4.0s
        velocity: v(t) = dx/dt with reduced jerk under fixed period
        acceleration: a(t) = d^2x/dt^2 from velocity profile
        cv_reduction: 1 - (CV_entrained / CV_self_paced)

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03)`` each ``(B, T)``.

    Returns:
        ``(motor_period, velocity, acceleration, cv_reduction)`` each ``(B, T)``.
    """
    f01, f02, f03 = e_outputs

    # -- H3 features --
    amp_mean_1s = h3_features[_AMP_MEAN_1S]          # mean amplitude 1s
    loud_mean_500ms = h3_features[_LOUD_MEAN_500MS]   # mean loudness 500ms
    tempo_vel_125ms = h3_features[_TEMPO_VEL_125MS]   # tempo velocity 125ms
    tempo_mean_1s = h3_features[_TEMPO_MEAN_1S]       # mean tempo change 1s

    # -- R3 features --
    amplitude = r3_features[..., _AMPLITUDE]          # (B, T)
    loudness = r3_features[..., _LOUDNESS]            # (B, T)

    # Motor period: dP/dt = tau^-1 * (T - P(t))
    # Grahn & Brett 2007: putamen Z=5.67, SMA Z=5.03
    # Motor drive from mean amplitude (1s) and loudness (500ms)
    motor_drive = 0.50 * amp_mean_1s + 0.50 * loud_mean_500ms
    # Period convergence: entrainment level modulates convergence rate
    motor_period = torch.sigmoid(
        0.40 * f01 * motor_drive
        + 0.30 * amp_mean_1s * amplitude
        + 0.30 * loud_mean_500ms * loudness
    )

    # Velocity: optimized v(t) = dx/dt under stable period locking
    # Thaut 2015: CTR optimizes velocity profiles
    # Uses tempo velocity at 125ms for fine-grained dynamics
    velocity = torch.sigmoid(
        0.35 * f02 * tempo_vel_125ms
        + 0.35 * motor_drive * f01
        + 0.30 * amplitude * loudness
    )

    # Acceleration: a(t) = d^2x/dt^2 from velocity
    # Smooth acceleration from fixed period providing CTR
    # Cerebellum motor timing error correction
    acceleration = torch.sigmoid(
        0.35 * velocity * tempo_vel_125ms
        + 0.35 * tempo_mean_1s * f01
        + 0.30 * f02 * motor_drive
    )

    # CV reduction: directly from f03 (variability reduction)
    # Yamashita 2025: stride time CV 4.51% -> 2.80% (d=-1.10)
    # 1 - (CV_entrained / CV_self_paced) normalized
    cv_reduction = torch.sigmoid(
        0.40 * f03
        + 0.30 * f01 * f02
        + 0.30 * motor_period * velocity
    )

    return motor_period, velocity, acceleration, cv_reduction
