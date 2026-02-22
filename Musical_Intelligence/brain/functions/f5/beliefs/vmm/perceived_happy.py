"""perceived_happy — Core belief (VMM, F5).

"This music sounds happy (perceived, not felt)."

Observe: 0.40*P0:perceived_happy + 0.30*V1:mode_signal + 0.30*V2:consonance_valence
Predict: τ×prev + w_trend×M18 + w_period×M14 + w_ctx×beliefs_{t-1}
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.55 (moderate — tracks major/consonant character over phrases).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- VMM output indices (12D) -------------------------------------------------
_V1_MODE_SIGNAL = 1           # V1:mode_signal
_V2_CONSONANCE_VALENCE = 2    # V2:consonance_valence
_P0_PERCEIVED_HAPPY = 7       # P0:perceived_happy

# -- H3 tuples for predict ----------------------------------------------------
_CONSONANCE_TREND = (4, 20, 18, 0)     # sensory_pleasantness M18 trend 5s L0
_TONALNESS_PERIOD = (14, 22, 14, 2)    # tonalness M14 periodicity 15s L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.04
_W_PERIOD = 0.03
_W_CTX = 0.03


class PerceivedHappy(CoreBelief):
    """Core belief: perceived happiness in music.

    Measures the degree to which music is perceived as happy/joyful.
    This is perceived (what the music expresses), not felt emotion.
    Major mode + consonance + brightness = high perceived happiness.

    Dalla Bella 2001: perceived happy correlates with major mode,
    fast tempo, high pitch (behavioral, N=60).
    Dependency: Requires VMM mechanism (Relay, Depth 0).
    """

    NAME = "perceived_happy"
    FULL_NAME = "Perceived Happiness"
    FUNCTION = "F5"
    MECHANISM = "VMM"
    TAU = 0.55
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:perceived_happy", 0.40),
        ("V1:mode_signal", 0.30),
        ("V2:consonance_valence", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe perceived happiness from VMM outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` VMM output tensor.

        Returns:
            ``(B, T)`` observed perceived happiness value.
        """
        return (
            0.40 * mechanism_output[:, :, _P0_PERCEIVED_HAPPY]
            + 0.30 * mechanism_output[:, :, _V1_MODE_SIGNAL]
            + 0.30 * mechanism_output[:, :, _V2_CONSONANCE_VALENCE]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next perceived happiness value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``mode_detection``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_CONSONANCE_TREND, zero)
        period = h3_features.get(_TONALNESS_PERIOD, zero)
        ctx = context.get("mode_detection", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
