"""collective_pleasure_pred -- Anticipation belief (SSRI, F9).

"The predicted collective pleasure from sustained group flow
and shared musical experience."

Observe: 0.50*F1:flow_sustain_pred + 0.50*f05:collective_pleasure
No predict/update cycle.

See Building/C3-Brain/F9-Social/beliefs/collective-pleasure-pred.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- SSRI output indices ---------------------------------------------------
_F05_COLLECTIVE_PLEASURE = 4         # f05:collective_pleasure
_F1_FLOW_SUSTAIN_PRED = 10           # F1:flow_sustain_pred


class CollectivePleasurePred(AnticipationBelief):
    """Anticipation belief: predicted collective pleasure trajectory."""

    NAME = "collective_pleasure_pred"
    FULL_NAME = "Collective Pleasure Prediction"
    FUNCTION = "F9"
    MECHANISM = "SSRI"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:flow_sustain_pred", 0.50),
        ("f05:collective_pleasure", 0.50),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe collective pleasure prediction from SSRI output.

        Args:
            mechanism_output: ``(B, T, 11)`` SSRI output tensor.

        Returns:
            ``(B, T)`` predicted collective pleasure.
        """
        return (
            0.50 * mechanism_output[:, :, _F1_FLOW_SUSTAIN_PRED]
            + 0.50 * mechanism_output[:, :, _F05_COLLECTIVE_PLEASURE]
        )
