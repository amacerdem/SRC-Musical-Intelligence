"""groove_trajectory — Anticipation belief (HGSIC, F7).

"Groove will continue / intensify at this trajectory."

Observe: groove_prediction (1.0) — HGSIC forecast.
No predict/update cycle. Feeds groove_quality.predict() as context.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/groove-trajectory.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- HGSIC output index -------------------------------------------------------
_GROOVE_PREDICTION = 8         # groove_prediction


class GrooveTrajectory(AnticipationBelief):
    """Anticipation belief: groove trajectory prediction.

    Forward prediction for how groove quality will evolve.
    Feeds groove_quality's predict() and the precision engine.

    Dependency: Requires HGSIC mechanism (Relay, Depth 0).
    """

    NAME = "groove_trajectory"
    FULL_NAME = "Groove Trajectory"
    FUNCTION = "F7"
    MECHANISM = "HGSIC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("groove_prediction", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe groove trajectory from HGSIC forecast.

        Args:
            mechanism_output: ``(B, T, 11)`` HGSIC output tensor.

        Returns:
            ``(B, T)`` groove trajectory prediction value.
        """
        return mechanism_output[:, :, _GROOVE_PREDICTION]
