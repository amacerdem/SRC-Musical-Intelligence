"""within_connectivity -- Appraisal belief (EDNR, F8).

"The current level of within-network functional connectivity
for specialized music processing regions."

Observe: 0.60*f01:within_connectivity + 0.40*current_compartm
No predict/update cycle.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/within-connectivity.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- EDNR output indices ---------------------------------------------------
_F01_WITHIN_CONNECTIVITY = 0         # f01:within_connectivity
_CURRENT_COMPARTM = 6                # current_compartm


class WithinConnectivity(AppraisalBelief):
    """Appraisal belief: within-network functional connectivity."""

    NAME = "within_connectivity"
    FULL_NAME = "Within Connectivity"
    FUNCTION = "F8"
    MECHANISM = "EDNR"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f01:within_connectivity", 0.60),
        ("current_compartm", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe within connectivity from EDNR output.

        Args:
            mechanism_output: ``(B, T, 10)`` EDNR output tensor.

        Returns:
            ``(B, T)`` observed within-network connectivity.
        """
        return (
            0.60 * mechanism_output[:, :, _F01_WITHIN_CONNECTIVITY]
            + 0.40 * mechanism_output[:, :, _CURRENT_COMPARTM]
        )
