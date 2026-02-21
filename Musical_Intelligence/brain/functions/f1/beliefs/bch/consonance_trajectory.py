"""consonance_trajectory — Anticipation belief (BCH, F1).

"Harmonic stability will continue at this level / is trending toward
more/less consonance."

Observe: F0:consonance_forecast (1.0) — BCH trend extrapolation.
No predict/update cycle. Feeds harmonic_stability.predict() as context.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/consonance-trajectory.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# ── BCH output index ────────────────────────────────────────────────
_F0_CONSONANCE_FORECAST = 12


class ConsonanceTrajectory(AnticipationBelief):
    """Anticipation belief: consonance trend extrapolation."""

    NAME = "consonance_trajectory"
    FULL_NAME = "Consonance Trajectory"
    FUNCTION = "F1"
    MECHANISM = "BCH"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F0:consonance_forecast", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe consonance trajectory from BCH F0:consonance_forecast.

        Args:
            mechanism_output: ``(B, T, 16)`` BCH output tensor.

        Returns:
            ``(B, T)`` forward consonance trend.
        """
        return mechanism_output[:, :, _F0_CONSONANCE_FORECAST]
