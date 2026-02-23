"""dissociation_index — Appraisal belief (DAED, F6).

"Degree of dissociation between wanting and liking — indicates when
anticipatory and consummatory reward systems diverge."

Observe: dissociation_index (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/dissociation-index.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- DAED output index -------------------------------------------------------
_DISSOCIATION_INDEX = 4


class DissociationIndex(AppraisalBelief):
    """Appraisal belief: wanting-liking dissociation degree."""

    NAME = "dissociation_index"
    FULL_NAME = "Dissociation Index"
    FUNCTION = "F6"
    MECHANISM = "DAED"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("dissociation_index", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe dissociation index from DAED dissociation_index.

        Args:
            mechanism_output: ``(B, T, 8)`` DAED output tensor.

        Returns:
            ``(B, T)`` wanting-liking dissociation value.
        """
        return mechanism_output[:, :, _DISSOCIATION_INDEX]
