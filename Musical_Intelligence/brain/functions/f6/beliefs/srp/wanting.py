"""wanting — Core belief (SRP, F6).

"I want more of this musical stimulus — anticipatory desire."

Observe: 1.0*P0:wanting
Predict: t*prev + (1-t)*baseline + trend + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

t = 0.6

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/wanting.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- SRP output index -------------------------------------------------------
_P0_WANTING = 13                  # P0:wanting

# -- H3 tuples for predict --------------------------------------------------
_GENERIC_TREND = (7, 8, 18, 0)   # amplitude M18 trend, L0

# -- Predict weights ---------------------------------------------------------
_W_TREND = 0.05
_W_CTX = 0.02


class Wanting(CoreBelief):
    """Core belief: anticipatory wanting / desire for the musical stimulus."""

    NAME = "wanting"
    FULL_NAME = "Wanting"
    FUNCTION = "F6"
    MECHANISM = "SRP"
    TAU = 0.6
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:wanting", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe wanting from SRP P0:wanting.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` observed wanting value.
        """
        return mechanism_output[:, :, _P0_WANTING]

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next wanting value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``tension``, ``wanting_ramp``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_GENERIC_TREND, zero)
        ctx_tension = context.get("tension", zero)
        ctx_ramp = context.get("wanting_ramp", zero)

        return base + _W_TREND * trend + _W_CTX * ctx_tension + _W_CTX * ctx_ramp
