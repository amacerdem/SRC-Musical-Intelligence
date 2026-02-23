"""reward_response_pred — Anticipation belief (STAI, F1).

"The current aesthetic state predicts this level of reward response."

Observe: 0.50*F1:reward_response_pred + 0.30*P2:aesthetic_response
         + 0.20*E2:aesthetic_integration
No predict/update cycle. Feeds downstream reward beliefs as context.

See Building/C3-Brain/F1-Sensory-Processing/beliefs/reward-response-pred.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- STAI output indices ---------------------------------------------------
_E2_AESTHETIC_INTEGRATION = 2     # E2:aesthetic_integration
_P2_AESTHETIC_RESPONSE = 8        # P2:aesthetic_response
_F1_REWARD_RESPONSE_PRED = 10     # F1:reward_response_pred


class RewardResponsePred(AnticipationBelief):
    """Anticipation belief: predicted reward response from aesthetic state."""

    NAME = "reward_response_pred"
    FULL_NAME = "Reward Response Prediction"
    FUNCTION = "F1"
    MECHANISM = "STAI"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:reward_response_pred", 0.50),
        ("P2:aesthetic_response", 0.30),
        ("E2:aesthetic_integration", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe reward response prediction from STAI output.

        Args:
            mechanism_output: ``(B, T, 12)`` STAI output tensor.

        Returns:
            ``(B, T)`` predicted reward response.
        """
        return (
            0.50 * mechanism_output[:, :, _F1_REWARD_RESPONSE_PRED]
            + 0.30 * mechanism_output[:, :, _P2_AESTHETIC_RESPONSE]
            + 0.20 * mechanism_output[:, :, _E2_AESTHETIC_INTEGRATION]
        )
