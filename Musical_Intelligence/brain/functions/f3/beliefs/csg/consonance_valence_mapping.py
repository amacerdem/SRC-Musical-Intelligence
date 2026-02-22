"""consonance_valence_mapping — Appraisal belief (CSG cross-function, F3).

"Consonance directly predicts emotional valence."

Observe: P1:affective_evaluation (1.0) — tanh-valued [-1, 1].
No predict/update cycle. Feeds F5 Emotion (valence bridge).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- CSG output index ---------------------------------------------------------
_P1_AFFECTIVE_EVALUATION = 7   # P1:affective_evaluation (tanh, [-1,1])


class ConsonanceValenceMapping(AppraisalBelief):
    """Appraisal belief: consonance-to-valence mapping.

    Direct bridge from consonance level to emotional valence.
    Positive = consonant/pleasant, negative = dissonant/unpleasant.
    Range: [-1, 1] (tanh-valued from CSG P1).

    CSG is F1-primary; this belief is cross-function to F3.
    Dependency: Requires CSG mechanism (Relay, Depth 0, F1).
    """

    NAME = "consonance_valence_mapping"
    FULL_NAME = "Consonance-Valence Mapping"
    FUNCTION = "F3"
    MECHANISM = "CSG"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:affective_evaluation", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe consonance-valence mapping from CSG P1.

        Args:
            mechanism_output: ``(B, T, 12)`` CSG output tensor.

        Returns:
            ``(B, T)`` consonance-valence mapping value [-1, 1].
        """
        return mechanism_output[:, :, _P1_AFFECTIVE_EVALUATION]
