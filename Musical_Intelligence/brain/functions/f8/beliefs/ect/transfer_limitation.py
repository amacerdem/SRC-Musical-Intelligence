"""transfer_limitation -- Anticipation belief (ECT, F8).

"The predicted limit of expertise transfer to non-trained domains."

Observe: transfer_limit (1.0) -- ECT transfer boundary prediction.
No predict/update cycle.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/transfer-limitation.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- ECT output index ------------------------------------------------------
_TRANSFER_LIMIT = 9                  # transfer_limit


class TransferLimitation(AnticipationBelief):
    """Anticipation belief: expertise transfer limitation."""

    NAME = "transfer_limitation"
    FULL_NAME = "Transfer Limitation"
    FUNCTION = "F8"
    MECHANISM = "ECT"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("transfer_limit", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe transfer limitation from ECT transfer_limit.

        Args:
            mechanism_output: ``(B, T, 12)`` ECT output tensor.

        Returns:
            ``(B, T)`` predicted transfer limitation.
        """
        return mechanism_output[:, :, _TRANSFER_LIMIT]
