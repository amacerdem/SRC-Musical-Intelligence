"""sad_pathway — Appraisal belief (VMM, F5).

"Limbic emotional circuit (minor/dissonant)."

Observe: R1:sad_pathway (1.0)
No predict/update cycle. Feeds F6 Reward (nostalgia/beauty pathway).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- VMM output indices (12D) -------------------------------------------------
_R1_SAD_PATHWAY = 4           # R1:sad_pathway


class SadPathway(AppraisalBelief):
    """Appraisal belief: limbic emotional pathway activation.

    Hippocampus/amygdala/PHG activation from minor/dissonant/dark music.

    Mitterschiffthaler 2007: sad music activates R hippocampus/amygdala.
    Dependency: Requires VMM mechanism (Relay, Depth 0).
    """

    NAME = "sad_pathway"
    FULL_NAME = "Sad Pathway"
    FUNCTION = "F5"
    MECHANISM = "VMM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("R1:sad_pathway", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe sad pathway from VMM outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` VMM output tensor.

        Returns:
            ``(B, T)`` sad pathway activation.
        """
        return mechanism_output[:, :, _R1_SAD_PATHWAY]
