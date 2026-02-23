"""prediction_error — Core belief (SRP, F6).

"The current sensory input deviates from expectation — reward prediction
error signal."

Observe: 1.0*C2:prediction_error
Predict: t*prev + (1-t)*baseline + trend + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

t = 0.5

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/prediction-error.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- SRP output index -------------------------------------------------------
_C2_PREDICTION_ERROR = 5          # C2:prediction_error

# -- H3 tuples for predict --------------------------------------------------
_SPEC_FLUX_TREND = (21, 8, 18, 0)  # spectral_flux M18 trend, L0

# -- Predict weights ---------------------------------------------------------
_W_TREND = 0.05
_W_CTX = 0.02


class PredictionError(CoreBelief):
    """Core belief: reward prediction error magnitude."""

    NAME = "prediction_error"
    FULL_NAME = "Prediction Error"
    FUNCTION = "F6"
    MECHANISM = "SRP"
    TAU = 0.5
    BASELINE = 0.0

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("C2:prediction_error", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe prediction error from SRP C2:prediction_error.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` observed prediction error value.
        """
        return mechanism_output[:, :, _C2_PREDICTION_ERROR]

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next prediction error value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``prediction_match``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_SPEC_FLUX_TREND, zero)
        ctx = context.get("prediction_match", zero)

        return base + _W_TREND * trend + _W_CTX * ctx
