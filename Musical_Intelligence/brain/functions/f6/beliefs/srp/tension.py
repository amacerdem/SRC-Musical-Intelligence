"""tension — Core belief (SRP, F6).

"Musical tension is building / releasing — driving reward anticipation."

Observe: 1.0*T0:tension
Predict: t*prev + (1-t)*baseline + trend + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

t = 0.55

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/tension.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- SRP output index -------------------------------------------------------
_T0_TENSION = 6                   # T0:tension

# -- H3 tuples for predict --------------------------------------------------
_AMPLITUDE_TREND = (7, 8, 18, 0)  # amplitude M18 trend, L0

# -- Predict weights ---------------------------------------------------------
_W_TREND = 0.05
_W_CTX = 0.02


class Tension(CoreBelief):
    """Core belief: musical tension level driving reward anticipation."""

    NAME = "tension"
    FULL_NAME = "Tension"
    FUNCTION = "F6"
    MECHANISM = "SRP"
    TAU = 0.55
    BASELINE = 0.0

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("T0:tension", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe tension from SRP T0:tension.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` observed tension value.
        """
        return mechanism_output[:, :, _T0_TENSION]

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next tension value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``harmonic_tension``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_AMPLITUDE_TREND, zero)
        ctx = context.get("harmonic_tension", zero)

        return base + _W_TREND * trend + _W_CTX * ctx
