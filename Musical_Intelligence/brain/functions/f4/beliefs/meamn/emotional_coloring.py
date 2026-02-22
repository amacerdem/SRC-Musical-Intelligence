"""emotional_coloring — Core belief (MEAMN, F4).

"This makes me feel..." Affective tag strength on retrieved memory.

Observe: 0.40*P1:emotional_color + 0.30*E2:f03_emotion + 0.30*M0:meam_retrieval
Predict: τ×prev + w_trend×M18 + w_period×M14 + w_ctx×beliefs_{t-1}

τ = 0.75 (high inertia — affective tags on memories are stable).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- MEAMN output indices (12D) ------------------------------------------------
_E2_F03_EMOTION = 2           # E2:f03_emotion
_M0_MEAM_RETRIEVAL = 3        # M0:meam_retrieval
_P1_EMOTIONAL_COLOR = 6       # P1:emotional_color

# -- H3 tuples for predict ----------------------------------------------------
_ROUGHNESS_TREND = (0, 20, 18, 0)      # roughness M18 trend 5s L0
_LOUDNESS_MEAN = (10, 20, 1, 0)        # loudness M1 mean 5s L0

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.03
_W_PERIOD = 0.04
_W_CTX = 0.03


class EmotionalColoring(CoreBelief):
    """Core belief: emotional coloring of memory.

    Measures affective tag strength on retrieved autobiographical memory.
    High values = strong emotional response to memory content.

    Janata 2009: mPFC emotional processing during MEAM retrieval
    (fMRI 3T, N=13, t(9)=3.442, p<0.008).
    Dependency: Requires MEAMN mechanism (Relay, Depth 0).
    """

    NAME = "emotional_coloring"
    FULL_NAME = "Emotional Coloring"
    FUNCTION = "F4"
    MECHANISM = "MEAMN"
    TAU = 0.75
    BASELINE = 0.3

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:emotional_color", 0.40),
        ("E2:f03_emotion", 0.30),
        ("M0:meam_retrieval", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe emotional coloring from MEAMN outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` MEAMN output tensor.

        Returns:
            ``(B, T)`` observed emotional coloring value.
        """
        return (
            0.40 * mechanism_output[:, :, _P1_EMOTIONAL_COLOR]
            + 0.30 * mechanism_output[:, :, _E2_F03_EMOTION]
            + 0.30 * mechanism_output[:, :, _M0_MEAM_RETRIEVAL]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next emotional coloring value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``autobiographical_retrieval``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_ROUGHNESS_TREND, zero)
        period = h3_features.get(_LOUDNESS_MEAN, zero)
        ctx = context.get("autobiographical_retrieval", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
