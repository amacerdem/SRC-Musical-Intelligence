"""phrase_boundary_pred — Anticipation belief (HMCE, F7).

"A phrase boundary is approaching."

Observe: phrase_boundary_pred (1.0) — HMCE forecast.
No predict/update cycle. Feeds salience and segmentation.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/phrase-boundary-pred.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- HMCE output index ---------------------------------------------------------
_PHRASE_BOUNDARY_PRED = 9      # phrase_boundary_pred


class PhraseBoundaryPred(AnticipationBelief):
    """Anticipation belief: phrase boundary prediction.

    Forward prediction for approaching phrase boundaries.
    High values indicate a boundary is imminent.
    Feeds salience engine and segmentation processes.

    Dependency: Requires HMCE mechanism (Relay, Depth 0).
    """

    NAME = "phrase_boundary_pred"
    FULL_NAME = "Phrase Boundary Prediction"
    FUNCTION = "F7"
    MECHANISM = "HMCE"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("phrase_boundary_pred", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe phrase boundary prediction from HMCE forecast.

        Args:
            mechanism_output: ``(B, T, 11)`` HMCE output tensor.

        Returns:
            ``(B, T)`` phrase boundary prediction value.
        """
        return mechanism_output[:, :, _PHRASE_BOUNDARY_PRED]
