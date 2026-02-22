"""CLAM F-Layer -- Forecast (2D).

Forward predictions for closed-loop affective modulation:
  F0: target_affect_pred    — Predicted target affect state (next loop cycle)
  F1: modulation_success    — Predicted success of current modulation attempt

F0 forecasts what the target affect state will be in the next loop cycle
(~1s ahead). Combines the current hedonic state (sensory pleasantness
at 525ms), the ongoing control trajectory, and affect error dynamics.
When the loop is converging (error decreasing), F0 approximates the
target. When diverging, F0 reflects the drifting decoded state.

F1 predicts whether the current modulation attempt will succeed. Combines
feedback trend (spectral flux trend at 1s), arousal modulation quality
(P0), and loop coherence. High F1 predicts that the loop will converge
to the target. This feeds the affective_control appraisal belief and
maps to NAcc reward-system coupling (loop success = reward).

H3 demands consumed (2 tuples):
  (4, 12, 0, 0)   sensory_pleasantness value H12 L0 -- hedonic state
  (21, 16, 18, 0) spectral_flux trend H16 L0        -- feedback trend
  Note: (4, 12, 0, 0) shared with P-layer.

Ehrlich et al. 2019: 3/5 participants converge to target (loop success).
Daly et al. 2019: music parameter trajectory predicts affect convergence.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PLEAS_VAL_H12 = (4, 12, 0, 0)          # sensory_pleasantness value H12 L0
_FLUX_TREND_H16 = (21, 16, 18, 0)       # spectral_flux trend H16 L0


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: forward predictions for affective modulation.

    F0 (target_affect_pred) forecasts the target affect state for the
    next loop cycle. Current hedonic state + control trajectory + error
    dynamics project where the affect will land. Convergent loops
    produce F0 close to B1 (target); divergent loops drift.

    F1 (modulation_success) predicts loop convergence. Feedback trend
    (spectral flux trend at 1s) + arousal modulation (P0) + loop
    coherence (E1) estimate whether the current attempt will succeed.
    Maps to NAcc reward coupling: successful modulation = reward.

    Ehrlich et al. 2019: 3/5 participants converge to target (N=5).
    Daly et al. 2019: music parameter trajectory affects convergence.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(B0, B1, B2, C0, C1)`` from temporal integration layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``
    """
    _e0, e1 = e
    _b0, b1, b2, c0, c1 = m
    p0, p1 = p

    # -- H3 features --
    pleas_val = h3_features[_PLEAS_VAL_H12]      # (B, T)
    flux_trend = h3_features[_FLUX_TREND_H16]     # (B, T)

    # -- Derived signals --
    # Error trajectory: decreasing error = converging loop
    error_reduction = (1.0 - b2.clamp(0.0, 1.0)) * e1

    # Feedback quality: positive trend in feedback signal = effective control
    feedback_quality = 0.50 * flux_trend + 0.50 * c1

    # -- F0: Target Affect Prediction --
    # Forecasts the next-cycle target affect state. When the loop is
    # converging (low error, strong control), F0 approaches B1 (target).
    # When diverging, F0 reflects the drifting hedonic state.
    # Ehrlich 2019: closed-loop BCI steers affect over ~1s latency.
    f0 = torch.sigmoid(
        0.35 * b1 * error_reduction.clamp(min=0.1)
        + 0.35 * pleas_val * c0
        + 0.30 * p1 * (1.0 - b2.clamp(0.0, 1.0))
    )

    # -- F1: Modulation Success --
    # Predicts whether the current modulation will succeed. Feedback
    # trend + arousal modulation + loop coherence estimate convergence.
    # Maps to NAcc reward coupling: loop success = reward signal.
    # Ehrlich 2019: 3/5 participant success rate for affect convergence.
    f1 = torch.sigmoid(
        0.35 * p0 * e1.clamp(min=0.1)
        + 0.35 * feedback_quality * error_reduction
        + 0.30 * p1 * pleas_val
    )

    return f0, f1
