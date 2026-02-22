"""valence_shift_pred — Anticipation belief (ICEM, F2).

"Valence will shift in the near future (~2.5s)."

Observe: F1:valence_shift_2_5s (1.0) — ICEM valence forecast.
No predict/update cycle. Feeds F5 Emotion and F6 Reward as context.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/icem/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- ICEM output index ---------------------------------------------------------
_F1_VALENCE_SHIFT = 12     # F1:valence_shift_2_5s


class ValenceShiftPred(AnticipationBelief):
    """Anticipation belief: valence shift prediction ~2.5s ahead.

    Forward prediction for subjective feeling change. Based on current
    valence state, tonal stability context, and key clarity.

    Feeds into emotion regulation (F5) — anticipating valence shifts
    prepares emotional appraisal, and reward (F6) — expected pleasure
    contributes to wanting/liking.

    Gold et al. 2019: pleasure depends on joint uncertainty and surprise.
    """

    NAME = "valence_shift_pred"
    FULL_NAME = "Valence Shift Prediction"
    FUNCTION = "F2"
    MECHANISM = "ICEM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:valence_shift_2_5s", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe valence shift prediction from ICEM F1.

        Args:
            mechanism_output: ``(B, T, 13)`` ICEM output tensor.

        Returns:
            ``(B, T)`` forward valence shift prediction.
        """
        return mechanism_output[:, :, _F1_VALENCE_SHIFT]
