"""imagery_recognition — Anticipation belief (MIAA, F1).

"Recognition probability when real sound arrives."

Dependency chain:
    MIAA (Depth 0, Relay) → imagery_recognition
    Without MIAA mechanism output, this belief cannot be computed.

Observe: F2:recognition_pred (1.0) — MIAA forecast output.
No predict/update cycle. Feeds Core beliefs' predict() methods as context.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/miaa/imagery_recognition.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# ── MIAA output index ────────────────────────────────────────────────
_F2_RECOGNITION_PRED = 10     # F2:recognition_pred


class ImageryRecognition(AnticipationBelief):
    """Anticipation belief: recognition probability at gap resolution.

    Predicts how likely the listener will recognize the upcoming sound
    as matching the imagined template. High values indicate strong
    familiarity and vivid imagery → high recognition confidence.
    Feeds into timbral_character.predict() as forward-looking context.

    Dependency: Requires MIAA mechanism (Relay, Depth 0, no upstream).
    """

    NAME = "imagery_recognition"
    FULL_NAME = "Imagery Recognition"
    FUNCTION = "F1"
    MECHANISM = "MIAA"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F2:recognition_pred", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe imagery recognition from MIAA F2:recognition_pred.

        Args:
            mechanism_output: ``(B, T, 11)`` MIAA output tensor.

        Returns:
            ``(B, T)`` recognition prediction strength.
        """
        return mechanism_output[:, :, _F2_RECOGNITION_PRED]
