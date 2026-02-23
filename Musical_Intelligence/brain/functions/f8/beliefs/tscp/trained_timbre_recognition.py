"""trained_timbre_recognition -- Core belief (TSCP, F8).

"Musical training has enhanced timbre recognition and cortical
specificity for trained instrument timbres."

Observe: 0.40*f01:trained_timbre_response + 0.30*P2:timbre_identity
         + 0.30*P0:recognition_quality
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.90 (very high -- plasticity changes slowly over training).

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/trained-timbre-recognition.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- TSCP output indices ---------------------------------------------------
_F01_TRAINED_TIMBRE_RESPONSE = 0     # f01:trained_timbre_response
_P0_RECOGNITION_QUALITY = 4          # P0:recognition_quality
_P2_TIMBRE_IDENTITY = 6              # P2:timbre_identity

# -- H3 tuples for predict -------------------------------------------------
_TIMBRE_TREND = (0, 8, 18, 0)       # timbre M18 trend at 200ms, L0
_TIMBRE_PERIOD = (0, 12, 14, 0)     # timbre M14 period 525ms, L0

# -- Predict weights --------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class TrainedTimbreRecognition(CoreBelief):
    """Core belief: expertise-driven timbre recognition quality."""

    NAME = "trained_timbre_recognition"
    FULL_NAME = "Trained Timbre Recognition"
    FUNCTION = "F8"
    MECHANISM = "TSCP"
    TAU = 0.90
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f01:trained_timbre_response", 0.40),
        ("P2:timbre_identity", 0.30),
        ("P0:recognition_quality", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe trained timbre recognition from TSCP output.

        Args:
            mechanism_output: ``(B, T, 10)`` TSCP output tensor.

        Returns:
            ``(B, T)`` observed timbre recognition value.
        """
        return (
            0.40 * mechanism_output[:, :, _F01_TRAINED_TIMBRE_RESPONSE]
            + 0.30 * mechanism_output[:, :, _P2_TIMBRE_IDENTITY]
            + 0.30 * mechanism_output[:, :, _P0_RECOGNITION_QUALITY]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next trained timbre recognition value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``expertise_enhancement``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_TIMBRE_TREND, zero)
        period = h3_features.get(_TIMBRE_PERIOD, zero)
        ctx = context.get("expertise_enhancement", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
