"""prediction_accuracy — Core belief (HTP, F2).

"My prediction was correct/wrong (post-stimulus silencing)."

Observe: 0.50*P0:sensory_match + 0.30*P1:pitch_prediction
         + 0.20*E3:hierarchy_gradient
Predict: τ×prev + (1-τ)×baseline + trend + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.5 (moderate-high — predictions build slowly, decay slowly).
Post-stimulus: high-level silenced when accurate (de Vries & Wurm 2023).

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/htp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- HTP output indices (12D) -------------------------------------------------
_E3_HIERARCHY_GRADIENT = 3   # E3:hierarchy_gradient
_P0_SENSORY_MATCH = 7        # P0:sensory_match
_P1_PITCH_PREDICTION = 8     # P1:pitch_prediction

# -- H3 tuples for predict ----------------------------------------------------
_SHARPNESS_TREND = (13, 8, 18, 0)    # sharpness M18 trend 500ms L0
_SPECTRAL_FLUX_VEL = (21, 3, 8, 0)   # spectral_flux M8 velocity 100ms L0

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.04
_W_PERIOD = 0.03
_W_CTX = 0.02


class PredictionAccuracy(CoreBelief):
    """Core belief: prediction accuracy / match.

    Measures how accurately current predictions match incoming input.
    High values indicate correct prediction (silencing expected).
    Low values indicate prediction error (learning signal).

    de Vries & Wurm 2023: high-level representations silenced post-stimulus
    when prediction is correct. Low-level persist as prediction errors.
    """

    NAME = "prediction_accuracy"
    FULL_NAME = "Prediction Accuracy"
    FUNCTION = "F2"
    MECHANISM = "HTP"
    TAU = 0.5
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:sensory_match", 0.50),
        ("P1:pitch_prediction", 0.30),
        ("E3:hierarchy_gradient", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe prediction accuracy from HTP outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` HTP output tensor.

        Returns:
            ``(B, T)`` observed prediction accuracy value.
        """
        return (
            0.50 * mechanism_output[:, :, _P0_SENSORY_MATCH]
            + 0.30 * mechanism_output[:, :, _P1_PITCH_PREDICTION]
            + 0.20 * mechanism_output[:, :, _E3_HIERARCHY_GRADIENT]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next prediction accuracy value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``prediction_hierarchy``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_SHARPNESS_TREND, zero)
        period = h3_features.get(_SPECTRAL_FLUX_VEL, zero)
        ctx = context.get("prediction_hierarchy", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
