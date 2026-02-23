"""chills_proximity — Anticipation belief (SRP, F6).

"A chills / frisson event is approaching — proximity estimate."

Observe: F1:chills_proximity (1.0) — SRP forecast output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/chills-proximity.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- SRP output index -------------------------------------------------------
_F1_CHILLS_PROXIMITY = 17


class ChillsProximity(AnticipationBelief):
    """Anticipation belief: proximity to a chills / frisson event."""

    NAME = "chills_proximity"
    FULL_NAME = "Chills Proximity"
    FUNCTION = "F6"
    MECHANISM = "SRP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:chills_proximity", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe chills proximity from SRP F1:chills_proximity.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` chills proximity value.
        """
        return mechanism_output[:, :, _F1_CHILLS_PROXIMITY]
