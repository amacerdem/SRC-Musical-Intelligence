"""attention_shift_pred — Anticipation belief (IACM, F3).

"Frontal attention shift within ~400ms."

Observe: F1:attention_shift_pred (1.0) — IACM forecast.
No predict/update cycle. Feeds F5 Emotion (arousal preparation).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- IACM output index --------------------------------------------------------
_F1_ATTENTION_SHIFT_PRED = 9   # F1:attention_shift_pred


class AttentionShiftPred(AnticipationBelief):
    """Anticipation belief: frontal attention shift prediction.

    Forward prediction for attention reorienting ~400ms ahead.
    Feeds attention_capture's predict() and emotion preparation.

    Dependency: Requires IACM mechanism (Relay, Depth 0).
    """

    NAME = "attention_shift_pred"
    FULL_NAME = "Attention Shift Prediction"
    FUNCTION = "F3"
    MECHANISM = "IACM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:attention_shift_pred", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe attention shift prediction from IACM F1.

        Args:
            mechanism_output: ``(B, T, 11)`` IACM output tensor.

        Returns:
            ``(B, T)`` attention shift prediction value.
        """
        return mechanism_output[:, :, _F1_ATTENTION_SHIFT_PRED]
