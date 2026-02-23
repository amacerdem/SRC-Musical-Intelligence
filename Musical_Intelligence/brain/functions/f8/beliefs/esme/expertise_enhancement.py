"""expertise_enhancement -- Core belief (ESME, F8).

"Musical expertise has enhanced auditory mismatch detection and
cross-domain transfer."

Observe: 0.50*f04:expertise_enhancement + 0.30*M0:mmn_expertise_function
         + 0.20*F2:developmental_trajectory
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.92 (very high -- expertise builds slowly).

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/expertise-enhancement.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- ESME output indices ---------------------------------------------------
_F04_EXPERTISE_ENHANCEMENT = 3       # f04:expertise_enhancement
_M0_MMN_EXPERTISE_FUNCTION = 4       # M0:mmn_expertise_function
_F2_DEVELOPMENTAL_TRAJECTORY = 10    # F2:developmental_trajectory

# -- H3 tuples for predict -------------------------------------------------
_EXPERTISE_TREND = (0, 8, 18, 0)     # expertise M18 trend at 200ms, L0
_EXPERTISE_PERIOD = (0, 12, 14, 0)   # expertise M14 period 525ms, L0

# -- Predict weights --------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class ExpertiseEnhancement(CoreBelief):
    """Core belief: expertise-driven enhancement of auditory processing."""

    NAME = "expertise_enhancement"
    FULL_NAME = "Expertise Enhancement"
    FUNCTION = "F8"
    MECHANISM = "ESME"
    TAU = 0.92
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f04:expertise_enhancement", 0.50),
        ("M0:mmn_expertise_function", 0.30),
        ("F2:developmental_trajectory", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe expertise enhancement from ESME output.

        Args:
            mechanism_output: ``(B, T, 11)`` ESME output tensor.

        Returns:
            ``(B, T)`` observed expertise enhancement value.
        """
        return (
            0.50 * mechanism_output[:, :, _F04_EXPERTISE_ENHANCEMENT]
            + 0.30 * mechanism_output[:, :, _M0_MMN_EXPERTISE_FUNCTION]
            + 0.20 * mechanism_output[:, :, _F2_DEVELOPMENTAL_TRAJECTORY]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next expertise enhancement value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``trained_timbre_recognition``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_EXPERTISE_TREND, zero)
        period = h3_features.get(_EXPERTISE_PERIOD, zero)
        ctx = context.get("trained_timbre_recognition", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
