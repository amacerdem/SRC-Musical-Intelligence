"""catchiness_pred -- Anticipation belief (NSCP, F9).

"The current musical stimulus will be perceived as catchy /
commercially appealing."

Observe: F2:catchiness_pred (1.0) -- NSCP catchiness extrapolation.
No predict/update cycle.

See Building/C3-Brain/F9-Social/beliefs/catchiness-pred.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- NSCP output index -----------------------------------------------------
_F2_CATCHINESS_PRED = 10             # F2:catchiness_pred


class CatchinessPred(AnticipationBelief):
    """Anticipation belief: predicted catchiness / commercial appeal."""

    NAME = "catchiness_pred"
    FULL_NAME = "Catchiness Prediction"
    FUNCTION = "F9"
    MECHANISM = "NSCP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F2:catchiness_pred", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe catchiness prediction from NSCP F2:catchiness_pred.

        Args:
            mechanism_output: ``(B, T, 11)`` NSCP output tensor.

        Returns:
            ``(B, T)`` forward catchiness prediction.
        """
        return mechanism_output[:, :, _F2_CATCHINESS_PRED]
