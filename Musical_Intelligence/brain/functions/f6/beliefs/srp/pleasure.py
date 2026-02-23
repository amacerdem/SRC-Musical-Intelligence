"""pleasure — Core belief (SRP, F6).

"I am experiencing hedonic pleasure from this musical stimulus."

Observe: 1.0*P2:pleasure
Predict: t*prev + (1-t)*baseline + trend + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

t = 0.7

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/pleasure.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- SRP output index -------------------------------------------------------
_P2_PLEASURE = 15                 # P2:pleasure

# -- H3 tuples for predict --------------------------------------------------
_GENERIC_TREND = (7, 8, 18, 0)   # amplitude M18 trend, L0

# -- Predict weights ---------------------------------------------------------
_W_TREND = 0.05
_W_CTX = 0.02


class Pleasure(CoreBelief):
    """Core belief: hedonic pleasure from the musical stimulus."""

    NAME = "pleasure"
    FULL_NAME = "Pleasure"
    FUNCTION = "F6"
    MECHANISM = "SRP"
    TAU = 0.7
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P2:pleasure", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe pleasure from SRP P2:pleasure.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` observed pleasure value.
        """
        return mechanism_output[:, :, _P2_PLEASURE]

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next pleasure value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``wanting``, ``liking``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_GENERIC_TREND, zero)
        ctx_wanting = context.get("wanting", zero)
        ctx_liking = context.get("liking", zero)

        return base + _W_TREND * trend + _W_CTX * ctx_wanting + _W_CTX * ctx_liking
