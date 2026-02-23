"""context_depth — Core belief (HMCE, F7).

"The listener has built a deep hierarchical context model."

Observe: 0.50*context_depth + 0.20*f01:short_context
         + 0.15*f02:medium_context + 0.15*f03:long_context
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.70 (high — context models build slowly and persist).

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/context-depth.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- HMCE output indices (11D) ------------------------------------------------
_F01_SHORT_CONTEXT = 0         # f01:short_context
_F02_MEDIUM_CONTEXT = 1        # f02:medium_context
_F03_LONG_CONTEXT = 2          # f03:long_context
_CONTEXT_DEPTH = 3             # context_depth

# -- H3 tuples for predict ----------------------------------------------------
_TONAL_STABILITY_TREND = (60, 16, 18, 0)  # tonal_stability M18 trend 1s L0
_TONAL_STABILITY_MEAN = (60, 16, 1, 0)    # tonal_stability M1 mean 1s L0

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class ContextDepth(CoreBelief):
    """Core belief: hierarchical context depth.

    Measures how deeply the listener has built a hierarchical
    context model spanning short, medium, and long time scales.
    High values indicate rich contextual understanding.
    Low values indicate shallow or fragmented context.

    Dependency: Requires HMCE mechanism (Relay, Depth 0).
    """

    NAME = "context_depth"
    FULL_NAME = "Context Depth"
    FUNCTION = "F7"
    MECHANISM = "HMCE"
    TAU = 0.70
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("context_depth", 0.50),
        ("f01:short_context", 0.20),
        ("f02:medium_context", 0.15),
        ("f03:long_context", 0.15),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe context depth from HMCE outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` HMCE output tensor.

        Returns:
            ``(B, T)`` observed context depth value.
        """
        return (
            0.50 * mechanism_output[:, :, _CONTEXT_DEPTH]
            + 0.20 * mechanism_output[:, :, _F01_SHORT_CONTEXT]
            + 0.15 * mechanism_output[:, :, _F02_MEDIUM_CONTEXT]
            + 0.15 * mechanism_output[:, :, _F03_LONG_CONTEXT]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next context depth value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``short_context``,
                ``medium_context``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_TONAL_STABILITY_TREND, zero)
        period = h3_features.get(_TONAL_STABILITY_MEAN, zero)
        ctx = (
            context.get("short_context", zero)
            + context.get("medium_context", zero)
        ) * 0.5

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
