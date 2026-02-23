"""social_coordination -- Core belief (DDSMI, F9).

"The listener is engaged in social coordination during musical
interaction, tracked via dual-brain neural coupling."

Observe: 0.50*E0:f13_social_coordination + 0.30*P0:partner_sync
         + 0.20*M0:mTRF_social
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.60 (moderate -- social coordination fluctuates).

See Building/C3-Brain/F9-Social/beliefs/social-coordination.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- DDSMI output indices --------------------------------------------------
_E0_SOCIAL_COORDINATION = 0          # E0:f13_social_coordination
_M0_MTRF_SOCIAL = 3                  # M0:mTRF_social
_P0_PARTNER_SYNC = 6                 # P0:partner_sync

# -- H3 tuples for predict -------------------------------------------------
_COORDINATION_TREND = (0, 8, 18, 0)  # coordination M18 trend at 200ms, L0
_COORDINATION_PERIOD = (0, 12, 14, 0) # coordination M14 period 525ms, L0

# -- Predict weights --------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class SocialCoordination(CoreBelief):
    """Core belief: dual-brain social coordination during music."""

    NAME = "social_coordination"
    FULL_NAME = "Social Coordination"
    FUNCTION = "F9"
    MECHANISM = "DDSMI"
    TAU = 0.60
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E0:f13_social_coordination", 0.50),
        ("P0:partner_sync", 0.30),
        ("M0:mTRF_social", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe social coordination from DDSMI output.

        Args:
            mechanism_output: ``(B, T, 11)`` DDSMI output tensor.

        Returns:
            ``(B, T)`` observed social coordination value.
        """
        return (
            0.50 * mechanism_output[:, :, _E0_SOCIAL_COORDINATION]
            + 0.30 * mechanism_output[:, :, _P0_PARTNER_SYNC]
            + 0.20 * mechanism_output[:, :, _M0_MTRF_SOCIAL]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next social coordination value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``neural_synchrony``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_COORDINATION_TREND, zero)
        period = h3_features.get(_COORDINATION_PERIOD, zero)
        ctx = context.get("neural_synchrony", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
