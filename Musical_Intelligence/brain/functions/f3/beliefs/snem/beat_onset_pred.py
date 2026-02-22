"""beat_onset_pred — Anticipation belief (SNEM, F3).

"Next beat will come at time X (~0.5s ahead)."

Observe: F0:beat_onset_pred (1.0) — SNEM forecast.
No predict/update cycle. Feeds F6 Reward (beat PE) and F7 Motor (timing).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- SNEM output index --------------------------------------------------------
_F0_BEAT_ONSET_PRED = 9        # F0:beat_onset_pred


class BeatOnsetPred(AnticipationBelief):
    """Anticipation belief: next beat onset prediction.

    Forward prediction for when the next beat will occur.
    Feeds beat_entrainment's predict() and the precision engine.

    Dependency: Requires SNEM mechanism (Relay, Depth 0).
    """

    NAME = "beat_onset_pred"
    FULL_NAME = "Beat Onset Prediction"
    FUNCTION = "F3"
    MECHANISM = "SNEM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F0:beat_onset_pred", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe beat onset prediction from SNEM F0.

        Args:
            mechanism_output: ``(B, T, 12)`` SNEM output tensor.

        Returns:
            ``(B, T)`` beat onset prediction value.
        """
        return mechanism_output[:, :, _F0_BEAT_ONSET_PRED]
