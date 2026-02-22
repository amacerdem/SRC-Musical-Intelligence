"""perceived_sad — Core belief (VMM, F5).

"This music sounds sad (perceived, not felt)."

Observe: 0.40*P1:perceived_sad + 0.30*(1-V1:mode_signal) + 0.30*(1-V2:consonance_valence)
Predict: τ×prev + w_trend×M18 + w_period×M14 + w_ctx×beliefs_{t-1}
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.55 (symmetric with perceived_happy).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- VMM output indices (12D) -------------------------------------------------
_V1_MODE_SIGNAL = 1           # V1:mode_signal
_V2_CONSONANCE_VALENCE = 2    # V2:consonance_valence
_P1_PERCEIVED_SAD = 8         # P1:perceived_sad

# -- H3 tuples for predict ----------------------------------------------------
_ROUGHNESS_TREND = (0, 20, 18, 0)      # roughness M18 trend 5s L0
_TONALNESS_PERIOD = (14, 22, 14, 2)    # tonalness M14 periodicity 15s L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.04
_W_PERIOD = 0.03
_W_CTX = 0.03


class PerceivedSad(CoreBelief):
    """Core belief: perceived sadness in music.

    Measures the degree to which music is perceived as sad/melancholic.
    Symmetric inverse of perceived_happy. Minor mode + dissonance +
    low brightness = high perceived sadness.

    Dalla Bella 2001: perceived sad correlates with minor mode,
    slow tempo, low pitch (behavioral, N=60).
    Dependency: Requires VMM mechanism (Relay, Depth 0).
    """

    NAME = "perceived_sad"
    FULL_NAME = "Perceived Sadness"
    FUNCTION = "F5"
    MECHANISM = "VMM"
    TAU = 0.55
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:perceived_sad", 0.40),
        ("1-V1:mode_signal", 0.30),
        ("1-V2:consonance_valence", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe perceived sadness from VMM outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` VMM output tensor.

        Returns:
            ``(B, T)`` observed perceived sadness value.
        """
        return (
            0.40 * mechanism_output[:, :, _P1_PERCEIVED_SAD]
            + 0.30 * (1.0 - mechanism_output[:, :, _V1_MODE_SIGNAL])
            + 0.30 * (1.0 - mechanism_output[:, :, _V2_CONSONANCE_VALENCE])
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next perceived sadness value.

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

        trend = h3_features.get(_ROUGHNESS_TREND, zero)
        period = h3_features.get(_TONALNESS_PERIOD, zero)
        ctx = context.get("mode_detection", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
