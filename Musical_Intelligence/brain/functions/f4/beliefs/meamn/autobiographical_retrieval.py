"""autobiographical_retrieval — Core belief (MEAMN, F4).

"I remember this." Music uniquely activates autobiographical memory.

Observe: 0.40*P0:memory_state + 0.30*E0:f01_retrieval + 0.30*P1:emotional_color
Predict: τ×prev + w_trend×M18 + w_period×M14 + w_ctx×beliefs_{t-1}
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.85 (highest in system — memory retrieval is maximally persistent).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- MEAMN output indices (12D) ------------------------------------------------
_E0_F01_RETRIEVAL = 0         # E0:f01_retrieval
_P0_MEMORY_STATE = 5          # P0:memory_state
_P1_EMOTIONAL_COLOR = 6       # P1:emotional_color

# -- H3 tuples for predict ----------------------------------------------------
_WARMTH_TREND = (12, 20, 18, 0)        # warmth M18 trend 5s L0
_TONALNESS_PERIOD = (14, 16, 14, 2)    # tonalness M14 periodicity 1s L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.03
_W_PERIOD = 0.04
_W_CTX = 0.03


class AutobiographicalRetrieval(CoreBelief):
    """Core belief: autobiographical memory retrieval.

    Measures strength of music-evoked autobiographical memory (MEAM).
    High values = strong memory retrieval (hippocampus-mPFC-PCC hub).
    τ=0.85 reflects maximal persistence — memories don't vanish between frames.

    Janata 2009: mPFC tracks autobiographically salient tonal space
    (fMRI 3T, N=13, t(9)=5.784, p<0.0003).
    Dependency: Requires MEAMN mechanism (Relay, Depth 0).
    """

    NAME = "autobiographical_retrieval"
    FULL_NAME = "Autobiographical Retrieval"
    FUNCTION = "F4"
    MECHANISM = "MEAMN"
    TAU = 0.85
    BASELINE = 0.3

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:memory_state", 0.40),
        ("E0:f01_retrieval", 0.30),
        ("P1:emotional_color", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe autobiographical retrieval from MEAMN outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` MEAMN output tensor.

        Returns:
            ``(B, T)`` observed retrieval value.
        """
        return (
            0.40 * mechanism_output[:, :, _P0_MEMORY_STATE]
            + 0.30 * mechanism_output[:, :, _E0_F01_RETRIEVAL]
            + 0.30 * mechanism_output[:, :, _P1_EMOTIONAL_COLOR]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next retrieval value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``nostalgia_intensity``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_WARMTH_TREND, zero)
        period = h3_features.get(_TONALNESS_PERIOD, zero)
        ctx = context.get("nostalgia_intensity", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
