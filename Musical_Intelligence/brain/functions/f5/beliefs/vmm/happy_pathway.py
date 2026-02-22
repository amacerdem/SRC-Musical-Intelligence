"""happy_pathway — Appraisal belief (VMM, F5).

"Striatal reward circuit (major/consonant)."

Observe: R0:happy_pathway (1.0)
No predict/update cycle. Feeds F6 Reward (wanting/liking).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- VMM output indices (12D) -------------------------------------------------
_R0_HAPPY_PATHWAY = 3         # R0:happy_pathway


class HappyPathway(AppraisalBelief):
    """Appraisal belief: striatal reward pathway activation.

    VS/DS/ACC activation from major/consonant/bright music.

    Mitterschiffthaler 2007: happy music activates ventral striatum + ACC.
    Dependency: Requires VMM mechanism (Relay, Depth 0).
    """

    NAME = "happy_pathway"
    FULL_NAME = "Happy Pathway"
    FUNCTION = "F5"
    MECHANISM = "VMM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("R0:happy_pathway", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe happy pathway from VMM outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` VMM output tensor.

        Returns:
            ``(B, T)`` happy pathway activation.
        """
        return mechanism_output[:, :, _R0_HAPPY_PATHWAY]
