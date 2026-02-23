"""structure_pred — Anticipation belief (HMCE, F7).

"Musical structure will continue / change in this manner."

Observe: structure_pred (1.0) — HMCE forecast.
No predict/update cycle. Feeds context_depth and long-range expectations.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/structure-pred.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- HMCE output index ---------------------------------------------------------
_STRUCTURE_PRED = 10           # structure_pred


class StructurePred(AnticipationBelief):
    """Anticipation belief: structural continuation prediction.

    Forward prediction for how musical structure will evolve.
    Feeds context_depth and long-range structural expectations.

    Dependency: Requires HMCE mechanism (Relay, Depth 0).
    """

    NAME = "structure_pred"
    FULL_NAME = "Structure Prediction"
    FUNCTION = "F7"
    MECHANISM = "HMCE"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("structure_pred", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe structure prediction from HMCE forecast.

        Args:
            mechanism_output: ``(B, T, 11)`` HMCE output tensor.

        Returns:
            ``(B, T)`` structure prediction value.
        """
        return mechanism_output[:, :, _STRUCTURE_PRED]
