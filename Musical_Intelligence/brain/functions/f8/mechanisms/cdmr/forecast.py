"""CDMR F-Layer -- Forecast (2D).

Context-Dependent Mismatch Response forward predictions:
  next_deviance         -- Attention allocation prediction [0, 1]
  context_continuation  -- Pattern expectation update [0, 1]

next_deviance predicts expected deviance at the next temporal step based on
current deviance history, context state, and binding curvature trends.
Drives pre-attentive resource allocation -- higher predicted deviance
increases vigilance for upcoming violations. Under the predictive coding
framework (Fong 2020), this represents the top-down prediction compared
against incoming sensory input.

context_continuation predicts whether the current melodic context will
continue, shift, or break. sigma(0.50 * f02 + 0.50 * melodic_expectation).
Combines current context modulation with accumulated melodic expectation.
Maps to ERAN-like syntactic prediction in IFG (Koelsch: long-term
music-syntactic regularities).

H3 demands consumed (1 tuple):
  (41, 16, 16, 2)  x_l5l6 curvature H16 L2  -- binding curvature over 1s

Dependencies:
  E-layer f02 (context_modulation)
  M-layer melodic_expectation
  M-layer deviance_history
  P-layer context_state
  EDNR relay (upstream)

Fong 2020: MMN as prediction error under predictive coding -- the prediction
itself.
Koelsch: ERAN reflects long-term music-syntactic regularities.

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/cdmr/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_BINDING_CURVATURE_H16 = (41, 16, 16, 2)  # binding curvature over 1s


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
    ednr: Tensor,
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: next deviance and context continuation predictions.

    next_deviance (idx 9) predicts expected deviance magnitude at upcoming
    time steps. Uses deviance history (M-layer), context state (P-layer),
    and binding curvature at 1s (H3) to extrapolate deviance trajectories.
    Curvature morph captures whether deviance patterns are accelerating,
    decelerating, or stable.
    Fong 2020: MMN as prediction error -- this is the prediction itself.

    context_continuation (idx 10) predicts whether the current melodic
    context will persist. Equal weighting of current context modulation
    (f02) and accumulated melodic expectation provides both immediate and
    historical context information. When both are high, the system predicts
    continued rich melodic context and maintains high sensitivity.
    Koelsch: ERAN reflects long-term music-syntactic regularities.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e_outputs: ``(f01, f02, f03, f04)`` from extraction layer.
        m_outputs: ``(melodic_expectation, deviance_history)`` from M-layer.
        p_outputs: ``(mismatch_signal, context_state, binding_state)``
            from P-layer.
        ednr: ``(B, T, 10)`` upstream EDNR relay output.

    Returns:
        ``(next_deviance, context_continuation)`` each ``(B, T)``
    """
    _f01, f02, _f03, _f04 = e_outputs
    melodic_expectation, deviance_history = m_outputs
    _mismatch_signal, context_state, _binding_state = p_outputs

    # -- H3 features --
    binding_curvature = h3_features[_BINDING_CURVATURE_H16]  # (B, T)

    # -- next_deviance --
    # Predicts expected deviance at upcoming time steps from deviance history,
    # context state, and binding curvature. Curvature captures acceleration
    # or deceleration of deviance patterns over 1s.
    # Fong 2020: top-down prediction compared against incoming sensory input.
    next_deviance = torch.sigmoid(
        0.35 * deviance_history
        + 0.30 * context_state
        + 0.25 * binding_curvature
    )

    # -- context_continuation --
    # Predicts whether melodic context will persist. Equal weighting of
    # current context modulation and accumulated melodic expectation.
    # Koelsch: ERAN reflects long-term music-syntactic regularities in IFG.
    context_continuation = torch.sigmoid(
        0.50 * f02
        + 0.50 * melodic_expectation
    )

    return next_deviance, context_continuation
