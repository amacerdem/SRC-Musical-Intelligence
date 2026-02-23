"""compartmentalization_cost -- Appraisal belief (ECT, F8).

"The cost of between-network efficiency reduction due to
compartmentalized musical training."

Observe: 0.60*f02:between_reduction + 0.40*network_isolation
No predict/update cycle.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/compartmentalization-cost.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- ECT output indices ----------------------------------------------------
_F02_BETWEEN_REDUCTION = 1           # f02:between_reduction
_NETWORK_ISOLATION = 8               # network_isolation


class CompartmentalizationCost(AppraisalBelief):
    """Appraisal belief: between-network efficiency cost."""

    NAME = "compartmentalization_cost"
    FULL_NAME = "Compartmentalization Cost"
    FUNCTION = "F8"
    MECHANISM = "ECT"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f02:between_reduction", 0.60),
        ("network_isolation", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe compartmentalization cost from ECT output.

        Args:
            mechanism_output: ``(B, T, 12)`` ECT output tensor.

        Returns:
            ``(B, T)`` observed between-network cost.
        """
        return (
            0.60 * mechanism_output[:, :, _F02_BETWEEN_REDUCTION]
            + 0.40 * mechanism_output[:, :, _NETWORK_ISOLATION]
        )
