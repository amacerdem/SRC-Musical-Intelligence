"""processing_load_pred — Anticipation belief (CSG cross-function, F3).

"Upcoming sensory load estimate."

Observe: F1:processing_pred (1.0) — CSG forecast.
No predict/update cycle. Feeds anticipatory resource allocation.
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- CSG output index ---------------------------------------------------------
_F1_PROCESSING_PRED = 10       # F1:processing_pred


class ProcessingLoadPred(AnticipationBelief):
    """Anticipation belief: upcoming processing load prediction.

    Forward prediction for sensory processing resource demand.
    Feeds anticipatory resource allocation in F3.

    CSG is F1-primary; this belief is cross-function to F3.
    Dependency: Requires CSG mechanism (Relay, Depth 0, F1).
    """

    NAME = "processing_load_pred"
    FULL_NAME = "Processing Load Prediction"
    FUNCTION = "F3"
    MECHANISM = "CSG"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:processing_pred", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe processing load prediction from CSG F1.

        Args:
            mechanism_output: ``(B, T, 12)`` CSG output tensor.

        Returns:
            ``(B, T)`` processing load prediction value.
        """
        return mechanism_output[:, :, _F1_PROCESSING_PRED]
