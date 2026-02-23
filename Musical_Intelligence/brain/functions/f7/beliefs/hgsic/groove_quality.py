"""groove_quality — Core belief (HGSIC, F7).

"This music has a strong groove / makes me want to move."

Observe: 0.50*groove_index + 0.30*f03:motor_groove + 0.20*coupling_strength
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.55 (moderate — groove fluctuates over phrases).

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/groove-quality.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- HGSIC output indices (11D) -----------------------------------------------
_F03_MOTOR_GROOVE = 2          # f03:motor_groove
_GROOVE_INDEX = 3              # groove_index
_COUPLING_STRENGTH = 4         # coupling_strength

# -- H3 tuples for predict ----------------------------------------------------
_AMPLITUDE_SMOOTHNESS = (7, 16, 15, 0)    # velocity_A M15 smoothness 1s L0
_ENERGY_PERIODICITY = (22, 11, 14, 2)     # energy M14 periodicity 525ms L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class GrooveQuality(CoreBelief):
    """Core belief: groove quality and motor engagement.

    Measures the degree to which musical rhythm induces motor
    engagement and groove sensation. High values indicate strong
    groove (Janata et al. 2012). Low values indicate weak or
    absent groove.

    Dependency: Requires HGSIC mechanism (Relay, Depth 0).
    """

    NAME = "groove_quality"
    FULL_NAME = "Groove Quality"
    FUNCTION = "F7"
    MECHANISM = "HGSIC"
    TAU = 0.55
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("groove_index", 0.50),
        ("f03:motor_groove", 0.30),
        ("coupling_strength", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe groove quality from HGSIC outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` HGSIC output tensor.

        Returns:
            ``(B, T)`` observed groove quality value.
        """
        return (
            0.50 * mechanism_output[:, :, _GROOVE_INDEX]
            + 0.30 * mechanism_output[:, :, _F03_MOTOR_GROOVE]
            + 0.20 * mechanism_output[:, :, _COUPLING_STRENGTH]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next groove quality value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``beat_prominence``,
                ``period_entrainment``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_AMPLITUDE_SMOOTHNESS, zero)
        period = h3_features.get(_ENERGY_PERIODICITY, zero)
        ctx = (
            context.get("beat_prominence", zero)
            + context.get("period_entrainment", zero)
        ) * 0.5

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
