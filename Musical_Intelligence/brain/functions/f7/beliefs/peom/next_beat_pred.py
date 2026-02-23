"""next_beat_pred — Anticipation belief (PEOM, F7).

"Next beat will occur at predicted time T."

Observe: next_beat_pred_T (1.0) — PEOM forecast.
No predict/update cycle. Feeds period_entrainment.predict() as context.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/next-beat-pred.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- PEOM output index ---------------------------------------------------------
_NEXT_BEAT_PRED_T = 9  # next_beat_pred_T


class NextBeatPred(AnticipationBelief):
    """Anticipation belief: next beat prediction.

    Forward prediction for when the next beat will occur,
    based on motor-period entrainment. Feeds period_entrainment's
    predict() and the precision engine.

    Dependency: Requires PEOM mechanism (Relay, Depth 0).
    """

    NAME = "next_beat_pred"
    FULL_NAME = "Next Beat Prediction"
    FUNCTION = "F7"
    MECHANISM = "PEOM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("next_beat_pred_T", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe next beat prediction from PEOM forecast.

        Args:
            mechanism_output: ``(B, T, 11)`` PEOM output tensor.

        Returns:
            ``(B, T)`` next beat prediction value.
        """
        return mechanism_output[:, :, _NEXT_BEAT_PRED_T]
