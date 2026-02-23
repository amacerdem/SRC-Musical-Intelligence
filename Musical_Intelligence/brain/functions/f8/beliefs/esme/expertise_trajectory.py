"""expertise_trajectory -- Anticipation belief (ESME, F8).

"Expertise development is trending along this developmental
trajectory."

Observe: F2:developmental_trajectory (1.0) -- ESME trajectory extrapolation.
No predict/update cycle. Feeds expertise_enhancement.predict() as context.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/expertise-trajectory.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- ESME output index -----------------------------------------------------
_F2_DEVELOPMENTAL_TRAJECTORY = 10    # F2:developmental_trajectory


class ExpertiseTrajectory(AnticipationBelief):
    """Anticipation belief: expertise developmental trajectory."""

    NAME = "expertise_trajectory"
    FULL_NAME = "Expertise Trajectory"
    FUNCTION = "F8"
    MECHANISM = "ESME"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F2:developmental_trajectory", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe expertise trajectory from ESME F2:developmental_trajectory.

        Args:
            mechanism_output: ``(B, T, 11)`` ESME output tensor.

        Returns:
            ``(B, T)`` forward expertise developmental trajectory.
        """
        return mechanism_output[:, :, _F2_DEVELOPMENTAL_TRAJECTORY]
