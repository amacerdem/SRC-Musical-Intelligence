"""emotion_certainty — Appraisal belief (VMM, F5).

"Certain/uncertain about emotional character."

Observe: P2:emotion_certainty (1.0)
No predict/update cycle. Feeds precision engine (pi_pred for valence).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- VMM output indices (12D) -------------------------------------------------
_P2_EMOTION_CERTAINTY = 9     # P2:emotion_certainty


class EmotionCertainty(AppraisalBelief):
    """Appraisal belief: certainty about emotional character.

    High values = confident emotional classification.
    Low values = ambiguous (e.g. mixed-mode harmony).

    Dependency: Requires VMM mechanism (Relay, Depth 0).
    """

    NAME = "emotion_certainty"
    FULL_NAME = "Emotion Certainty"
    FUNCTION = "F5"
    MECHANISM = "VMM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P2:emotion_certainty", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe emotion certainty from VMM outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` VMM output tensor.

        Returns:
            ``(B, T)`` emotion certainty value.
        """
        return mechanism_output[:, :, _P2_EMOTION_CERTAINTY]
