"""emotional_arousal — Core belief (AAC, F5).

"I am emotionally activated."

Observe: 0.50*E0:emotional_arousal + 0.30*P0:current_intensity + 0.20*I1:ans_composite
Predict: τ×prev + w_trend×M18 + w_period×M14 + w_ctx×beliefs_{t-1}
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.5 (lowest F5 inertia — arousal responds faster than valence).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- AAC output indices (14D) -------------------------------------------------
_E0_EMOTIONAL_AROUSAL = 0     # E0:emotional_arousal
_I1_ANS_COMPOSITE = 8         # I1:ans_composite
_P0_CURRENT_INTENSITY = 9     # P0:current_intensity

# -- H3 tuples for predict ----------------------------------------------------
_AMPLITUDE_VELOCITY = (7, 16, 8, 0)      # amplitude M8 velocity 1s L0
_ONSET_PERIODICITY = (11, 16, 14, 2)     # onset_strength M14 periodicity 1s L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.04
_W_CTX = 0.03


class EmotionalArousal(CoreBelief):
    """Core belief: emotional arousal level.

    Measures the degree of emotional activation. High values indicate
    intense emotional engagement; low values indicate calm/relaxed state.

    Craig 2005: anterior insula as interoceptive awareness hub for
    arousal signals (review).
    Dependency: Requires AAC mechanism (Relay, Depth 0).
    """

    NAME = "emotional_arousal"
    FULL_NAME = "Emotional Arousal"
    FUNCTION = "F5"
    MECHANISM = "AAC"
    TAU = 0.5
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E0:emotional_arousal", 0.50),
        ("P0:current_intensity", 0.30),
        ("I1:ans_composite", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe emotional arousal from AAC outputs.

        Args:
            mechanism_output: ``(B, T, 14)`` AAC output tensor.

        Returns:
            ``(B, T)`` observed emotional arousal value.
        """
        return (
            0.50 * mechanism_output[:, :, _E0_EMOTIONAL_AROUSAL]
            + 0.30 * mechanism_output[:, :, _P0_CURRENT_INTENSITY]
            + 0.20 * mechanism_output[:, :, _I1_ANS_COMPOSITE]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next emotional arousal value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``chills_intensity``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_AMPLITUDE_VELOCITY, zero)
        period = h3_features.get(_ONSET_PERIODICITY, zero)
        ctx = context.get("chills_intensity", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
