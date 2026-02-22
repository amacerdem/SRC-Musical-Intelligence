"""arousal_change_pred — Anticipation belief (ICEM, F2).

"Arousal will change in the near future (~1.3s)."

Observe: F0:arousal_change_1_3s (1.0) — ICEM arousal forecast.
No predict/update cycle. Feeds F5 Emotion and F6 Reward as context.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/icem/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- ICEM output index ---------------------------------------------------------
_F0_AROUSAL_CHANGE = 11     # F0:arousal_change_1_3s


class ArousalChangePred(AnticipationBelief):
    """Anticipation belief: arousal change prediction ~1.3s ahead.

    Forward prediction for SCR/arousal response. Based on current arousal
    state, sustained onset context, and pitch salience context.

    Feeds into emotion regulation (F5) — anticipating arousal changes
    allows preparatory autonomic adjustment, and reward (F6) — expected
    arousal contributes to wanting/anticipation.

    Salimpoor et al. 2011: caudate dopamine release during anticipation.
    """

    NAME = "arousal_change_pred"
    FULL_NAME = "Arousal Change Prediction"
    FUNCTION = "F2"
    MECHANISM = "ICEM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F0:arousal_change_1_3s", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe arousal change prediction from ICEM F0.

        Args:
            mechanism_output: ``(B, T, 13)`` ICEM output tensor.

        Returns:
            ``(B, T)`` forward arousal change prediction.
        """
        return mechanism_output[:, :, _F0_AROUSAL_CHANGE]
