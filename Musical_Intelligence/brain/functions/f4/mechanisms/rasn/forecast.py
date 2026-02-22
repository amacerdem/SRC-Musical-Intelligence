"""RASN F-Layer -- Forecast (3D).

Forward predictions for rhythmic auditory stimulation neuroplasticity:
  F0: movement_timing_pred      — Movement timing prediction (0.5-1s ahead)
  F1: neuroplastic_change_pred  — Neuroplastic change prediction (long-term)
  F2: gait_improvement_pred     — Gait improvement prediction (sessions ahead)

F0 forecasts upcoming beat positions based on current entrainment state and
motor cortex prediction signals. Uses short-horizon beat induction to
project movement timing 0.5-1s ahead. Captures the SMA's role in beat
prediction -- anticipating the next beat before it arrives.

F1 projects long-term neuroplastic trajectory based on current plasticity
indicators. Uses long-horizon (H24, 36s) dynamics to estimate cumulative
effect of ongoing rhythmic stimulation on neural reorganization.

F2 forecasts motor recovery potential based on sensorimotor integration
trajectory. Uses medium-horizon (H16-H20) motor entrainment signals to
project expected gait parameter improvements.

H3 demands consumed (8 tuples -- F-layer specific):
  (4, 16, 0, 2)   sensory_pleasantness value H16 L2   -- engagement
  (4, 20, 18, 0)  sensory_pleasantness trend H20 L0   -- engagement trajectory
  (0, 16, 0, 2)   roughness value H16 L2              -- dissonance level
  (0, 20, 18, 0)  roughness trend H20 L0              -- dissonance trajectory
  (10, 20, 1, 0)  spectral_flux mean H20 L0           -- average onset 5s
  (10, 24, 19, 0) spectral_flux stability H24 L0      -- onset stability 36s
  (7, 20, 4, 0)   amplitude max H20 L0                -- peak energy 5s
  (7, 24, 3, 0)   amplitude std H24 L0                -- energy variability 36s

R3 features:
  [0] roughness, [4] sensory_pleasantness, [10] spectral_flux, [7] amplitude

Grahn & Brett 2007: SMA predicts beat positions (fMRI N=27, Z=5.03).
Blasi et al. 2025: structural neuroplasticity from rhythm (20 RCTs, N=718).
Wang 2022: RAS improves gait velocity and stride (22 studies).
Thaut et al. 2015: reticulospinal pathways; beta oscillations in SMA.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/rasn/RASN-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PLEAS_VAL_H16 = (4, 16, 0, 2)        # sensory_pleasantness value H16 L2
_PLEAS_TREND_H20 = (4, 20, 18, 0)     # sensory_pleasantness trend H20 L0
_ROUGH_VAL_H16 = (0, 16, 0, 2)        # roughness value H16 L2
_ROUGH_TREND_H20 = (0, 20, 18, 0)     # roughness trend H20 L0
_FLUX_MEAN_H20 = (10, 20, 1, 0)       # spectral_flux mean H20 L0
_FLUX_STAB_H24 = (10, 24, 19, 0)      # spectral_flux stability H24 L0
_AMP_MAX_H20 = (7, 20, 4, 0)          # amplitude max H20 L0
_AMP_STD_H24 = (7, 24, 3, 0)          # amplitude std H24 L0


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for RAS neuroplasticity.

    F0 (movement_timing_pred) forecasts upcoming beat positions. Current
    entrainment state (P0) + temporal precision (P1) + onset trajectory
    provide the prediction scaffold. SMA beat prediction extrapolates
    0.5-1s ahead.

    F1 (neuroplastic_change_pred) projects long-term neural reorganization.
    Current plasticity (M0) + engagement trajectory (pleasantness trend) +
    onset stability (flux stability at 36s) estimate cumulative plasticity.

    F2 (gait_improvement_pred) forecasts motor recovery potential. Motor
    facilitation level (P2) + motor recovery (M1) + energy trajectory
    project expected gait improvements.

    Grahn & Brett 2007: SMA predicts beat positions (Z=5.03, FDR p<.05).
    Blasi et al. 2025: structural neuroplasticity after >= 4 weeks
    (20 RCTs, N=718, hippocampal volume + WM integrity).
    Wang 2022: RAS improves gait velocity and stride (22 studies).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    _e0, _e1, e2 = e
    m0, m1 = m
    p0, p1, p2 = p

    # -- H3 features --
    pleas_val = h3_features[_PLEAS_VAL_H16]       # (B, T)
    pleas_trend = h3_features[_PLEAS_TREND_H20]   # (B, T)
    rough_val = h3_features[_ROUGH_VAL_H16]        # (B, T)
    rough_trend = h3_features[_ROUGH_TREND_H20]    # (B, T)
    flux_mean_5s = h3_features[_FLUX_MEAN_H20]     # (B, T)
    flux_stab_36s = h3_features[_FLUX_STAB_H24]    # (B, T)
    amp_max_5s = h3_features[_AMP_MAX_H20]          # (B, T)
    amp_std_36s = h3_features[_AMP_STD_H24]         # (B, T)

    # -- Derived signals --
    # Engagement trajectory: pleasantness trend indicates whether the
    # listener is becoming more or less engaged over time
    engagement_trajectory = 0.50 * pleas_val + 0.50 * pleas_trend

    # Challenge level: roughness provides complexity/dissonance information
    # for plasticity demand (moderate challenge = optimal)
    challenge_level = 0.50 * rough_val + 0.50 * (1.0 - rough_trend.abs())

    # -- F0: Movement Timing Prediction --
    # Forecasts upcoming beat positions 0.5-1s ahead. Current entrainment
    # state (P0) + temporal precision (P1) + onset trajectory.
    # Grahn & Brett 2007: SMA predicts beat positions (Z=5.03).
    f0 = torch.sigmoid(
        0.35 * p0 * p1.clamp(min=0.1)
        + 0.35 * flux_mean_5s
        + 0.30 * amp_max_5s
    )

    # -- F1: Neuroplastic Change Prediction --
    # Projects long-term neural reorganization. Plasticity composite (M0)
    # + engagement trajectory + onset stability at 36s consolidation window.
    # Blasi et al. 2025: structural changes >= 4 weeks (hippocampal volume).
    # Zhao 2025: duration >= 4 weeks shows measurable changes (n=968+).
    f1 = torch.sigmoid(
        0.35 * m0 * engagement_trajectory.clamp(min=0.1)
        + 0.35 * flux_stab_36s * challenge_level
        + 0.30 * e2 * pleas_val
    )

    # -- F2: Gait Improvement Prediction --
    # Forecasts motor recovery potential. Motor facilitation level (P2)
    # + motor recovery (M1) + energy variability (consistency indicator).
    # Wang 2022: RAS improves gait velocity and stride (22 studies).
    # Thaut et al. 2015: reticulospinal pathways modulated by beat.
    f2 = torch.sigmoid(
        0.40 * p2 * m1.clamp(min=0.1)
        + 0.30 * amp_max_5s * (1.0 - amp_std_36s)
        + 0.30 * engagement_trajectory
    )

    return f0, f1, f2
