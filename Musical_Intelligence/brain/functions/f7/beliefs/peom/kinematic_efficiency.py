"""kinematic_efficiency — Core belief (PEOM, F7).

"Motor execution is kinematically smooth and velocity-optimized."

Observe: 0.40*f02:velocity_optimization + 0.30*velocity
         + 0.30*kinematic_smoothness
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.60 (moderate-high — tracks velocity optimization over phrases).

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/kinematic-efficiency.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- PEOM output indices (11D) ------------------------------------------------
_F02_VELOCITY_OPTIMIZATION = 1  # f02:velocity_optimization
_VELOCITY = 4                   # velocity
_KINEMATIC_SMOOTHNESS = 8       # kinematic_smoothness

# -- H3 tuples for predict ----------------------------------------------------
_MOTOR_COUPLING_PERIODICITY = (25, 16, 14, 2)  # x_l0l5 M14 periodicity 1s L2
_FAST_COUPLING = (25, 3, 14, 2)                # x_l0l5 M14 periodicity fast L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class KinematicEfficiency(CoreBelief):
    """Core belief: kinematic smoothness and velocity optimization.

    Measures the degree to which motor execution achieves smooth,
    velocity-optimized trajectories. High values indicate efficient
    motor planning (Todorov & Jordan 2002). Low values indicate
    jerky or suboptimal movement profiles.

    Dependency: Requires PEOM mechanism (Relay, Depth 0).
    """

    NAME = "kinematic_efficiency"
    FULL_NAME = "Kinematic Efficiency"
    FUNCTION = "F7"
    MECHANISM = "PEOM"
    TAU = 0.60
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f02:velocity_optimization", 0.40),
        ("velocity", 0.30),
        ("kinematic_smoothness", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe kinematic efficiency from PEOM outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` PEOM output tensor.

        Returns:
            ``(B, T)`` observed kinematic efficiency value.
        """
        return (
            0.40 * mechanism_output[:, :, _F02_VELOCITY_OPTIMIZATION]
            + 0.30 * mechanism_output[:, :, _VELOCITY]
            + 0.30 * mechanism_output[:, :, _KINEMATIC_SMOOTHNESS]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next kinematic efficiency value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``period_entrainment``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_MOTOR_COUPLING_PERIODICITY, zero)
        period = h3_features.get(_FAST_COUPLING, zero)
        ctx = context.get("period_entrainment", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
