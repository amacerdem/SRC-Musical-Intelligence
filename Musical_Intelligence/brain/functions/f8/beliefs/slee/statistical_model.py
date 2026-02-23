"""statistical_model -- Core belief (SLEE, F8).

"The listener has built this level of statistical model of the
musical environment through exposure-based learning."

Observe: 0.40*f01:statistical_model + 0.30*M0:exposure_model
         + 0.30*M1:pattern_memory
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.88 (high -- statistical models update gradually).

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/statistical-model.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- SLEE output indices ---------------------------------------------------
_F01_STATISTICAL_MODEL = 0           # f01:statistical_model
_M0_EXPOSURE_MODEL = 4               # M0:exposure_model
_M1_PATTERN_MEMORY = 5               # M1:pattern_memory

# -- H3 tuples for predict -------------------------------------------------
_STATISTICAL_TREND = (0, 8, 18, 0)   # statistical M18 trend at 200ms, L0
_STATISTICAL_PERIOD = (0, 12, 14, 0) # statistical M14 period 525ms, L0

# -- Predict weights --------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class StatisticalModel(CoreBelief):
    """Core belief: exposure-based statistical learning model."""

    NAME = "statistical_model"
    FULL_NAME = "Statistical Model"
    FUNCTION = "F8"
    MECHANISM = "SLEE"
    TAU = 0.88
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f01:statistical_model", 0.40),
        ("M0:exposure_model", 0.30),
        ("M1:pattern_memory", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe statistical model from SLEE output.

        Args:
            mechanism_output: ``(B, T, 13)`` SLEE output tensor.

        Returns:
            ``(B, T)`` observed statistical model strength.
        """
        return (
            0.40 * mechanism_output[:, :, _F01_STATISTICAL_MODEL]
            + 0.30 * mechanism_output[:, :, _M0_EXPOSURE_MODEL]
            + 0.30 * mechanism_output[:, :, _M1_PATTERN_MEMORY]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next statistical model value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``detection_accuracy``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_STATISTICAL_TREND, zero)
        period = h3_features.get(_STATISTICAL_PERIOD, zero)
        ctx = context.get("detection_accuracy", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
