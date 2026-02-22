"""information_content — Core belief (ICEM, F2).

"The current event is unexpected (high information content)."

Observe: 0.40*E0:information_content + 0.30*M0:ic_value
         + 0.30*P0:surprise_signal
Predict: τ×prev + (1-τ)×baseline + trend + velocity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.35 (low-moderate — IC is event-driven, adapts quickly).
Multi-scale: 6 horizons (standard belief schedule).

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/icem/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- ICEM output indices (13D) ------------------------------------------------
_E0_INFORMATION_CONTENT = 0    # E0:information_content
_M0_IC_VALUE = 4               # M0:ic_value
_P0_SURPRISE_SIGNAL = 9       # P0:surprise_signal

# -- H3 tuples for predict ----------------------------------------------------
_SPECTRAL_FLUX_TREND = (21, 8, 18, 0)    # spectral_flux M18 trend 500ms L0
_ENTROPY_VEL = (22, 3, 8, 0)             # distribution_entropy velocity 100ms

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.05
_W_VEL = 0.03
_W_CTX = 0.02


class InformationContent(CoreBelief):
    """Core belief: event information content (surprise).

    Measures the unexpectedness of the current auditory event. High values
    indicate surprising/unexpected events (high IC); low values indicate
    expected/predicted events. IC = -log₂(P(event|context)).

    Egermann et al. 2013: IC peaks predict psychophysiological emotional
    responses (p<0.001). Cheung et al. 2019: uncertainty × surprise
    interaction (R²=0.654).
    """

    NAME = "information_content"
    FULL_NAME = "Information Content"
    FUNCTION = "F2"
    MECHANISM = "ICEM"
    TAU = 0.35
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E0:information_content", 0.40),
        ("M0:ic_value", 0.30),
        ("P0:surprise_signal", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe information content from ICEM outputs.

        Args:
            mechanism_output: ``(B, T, 13)`` ICEM output tensor.

        Returns:
            ``(B, T)`` observed information content value.
        """
        return (
            0.40 * mechanism_output[:, :, _E0_INFORMATION_CONTENT]
            + 0.30 * mechanism_output[:, :, _M0_IC_VALUE]
            + 0.30 * mechanism_output[:, :, _P0_SURPRISE_SIGNAL]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next information content value.

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

        trend = h3_features.get(_SPECTRAL_FLUX_TREND, zero)
        vel = h3_features.get(_ENTROPY_VEL, zero)
        ctx = context.get("prediction_hierarchy", zero)

        return base + _W_TREND * trend + _W_VEL * vel + _W_CTX * ctx
