"""TAR F-Layer -- Forecast (2D).

Forward predictions for therapeutic trajectory:
  F0: mood_improv_pred     -- Mood improvement prediction (2-5s ahead) [0, 1]
  F1: stress_reduc_pred    -- Stress reduction prediction (2-5s ahead) [0, 1]

Mood improvement forecast (F0) projects hedonic and valence trajectory
from current therapeutic state. Uses pleasantness trend (mood direction),
sustained arousal (energy context), and therapeutic product (E0*T3) to
estimate whether mood will improve over the next 2-5 seconds.

Stress reduction forecast (F1) projects the anxiolytic trajectory from
consonance improvement (roughness trend), tempo dynamics (velocity peak),
and therapeutic product (E0*T2) to estimate stress reduction over the
next 2-5 seconds.

Chanda & Levitin (2013): Sustained music exposure builds therapeutic
effects over time; cortisol reduction accumulates.

Bernardi et al. (2006): Cardiovascular relaxation builds over sustained
slow-tempo exposure; 30s+ exposure needed for reliable effects.

H3 demands consumed (4):
  (0, 15, 18, 0) roughness trend H15 L0        -- consonance trajectory stress
  (10, 16, 1, 0) loudness mean H16 L0          -- sustained arousal
  (8, 15, 8, 0)  velocity_A velocity H15 L0    -- tempo dynamics peak
  (7, 7, 8, 0)   amplitude velocity H7 L0      -- energy change breakthrough

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_ROUGH_TREND_H15 = (0, 15, 18, 0)     # roughness trend H15 L0
_LOUD_MEAN_H16 = (10, 16, 1, 0)       # loudness mean H16 L0
_VELOA_VEL_H15 = (8, 15, 8, 0)        # velocity_A velocity H15 L0
_AMP_VEL_H7 = (7, 7, 8, 0)            # amplitude velocity H7 L0


def _predict_future(
    trajectory: Tensor,
    context: Tensor,
    stability: Tensor,
) -> Tensor:
    """Generic future prediction from trajectory, context, and stability.

    Combines current trajectory direction with contextual support and
    stability anchor to estimate near-future therapeutic state.

    Args:
        trajectory: (B, T) direction signal (trend or current value).
        context: (B, T) contextual support (mean engagement, etc.).
        stability: (B, T) stability anchor (variability, pattern consistency).

    Returns:
        (B, T) predicted future state via sigmoid.
    """
    return torch.sigmoid(
        0.40 * trajectory
        + 0.35 * context
        + 0.25 * stability
    )


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: mood improvement and stress reduction forecasts.

    F0 (mood_improv_pred): Mood improvement trajectory from antidepressant
    state (E0*T3), sustained arousal context (loudness mean), and energy
    dynamics (amplitude velocity). Predicts valence/hedonic improvement
    over 2-5 seconds ahead.
    Chanda 2013: DA modulation accumulates over sustained exposure.

    F1 (stress_reduc_pred): Stress reduction trajectory from anxiolytic
    state (E0*T2), consonance trajectory (roughness trend improving),
    and tempo stability (velocity dynamics at peak scale). Predicts
    cortisol/anxiety reduction over 2-5 seconds ahead.
    Bernardi 2006: cardiovascular relaxation builds over 30s+ exposure.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0,)`` from extraction layer.
        m: ``(T0, T1, T2, T3, I0, I1)`` from temporal integration.
        p: ``(P0,)`` from cognitive present.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    (e0,) = e
    _t0, _t1, t2, t3, _i0, _i1 = m
    (p0,) = p

    # -- H3 features --
    rough_trend_h15 = h3_features[_ROUGH_TREND_H15]      # (B, T)
    loud_mean_h16 = h3_features[_LOUD_MEAN_H16]          # (B, T)
    veloa_vel_h15 = h3_features[_VELOA_VEL_H15]          # (B, T)
    amp_vel_h7 = h3_features[_AMP_VEL_H7]                # (B, T)

    # -- Antidepressant trajectory --
    # Mood improvement from therapeutic*depression_improv product,
    # weighted by sustained arousal and energy dynamics.
    # Chanda 2013: sustained DA release via music pleasure
    mood_trajectory = 0.50 * (e0 * t3) + 0.50 * p0

    # -- F0: Mood Improvement Prediction --
    f0 = _predict_future(
        trajectory=mood_trajectory,
        context=loud_mean_h16,
        stability=amp_vel_h7.abs().clamp(0.0, 1.0),
    )

    # -- Anxiolytic trajectory --
    # Stress reduction from therapeutic*anxiety_reduction product,
    # weighted by consonance improvement and slow tempo stability.
    # Bernardi 2006: slow tempo builds cardiovascular relaxation
    stress_trajectory = 0.50 * (e0 * t2) + 0.50 * p0

    # -- F1: Stress Reduction Prediction --
    f1 = _predict_future(
        trajectory=stress_trajectory,
        context=(1.0 - rough_trend_h15),       # improving consonance
        stability=(1.0 - veloa_vel_h15.abs().clamp(0.0, 1.0)),  # stable tempo
    )

    return f0, f1
