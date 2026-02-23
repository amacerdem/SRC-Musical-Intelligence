"""group_flow -- Appraisal belief (SSRI, F9).

"The current state of group flow during collective musical
experience, amplified by synchrony."

Observe: 0.60*f03:group_flow_state + 0.40*M1:synchrony_amplification
No predict/update cycle.

See Building/C3-Brain/F9-Social/beliefs/group-flow.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SSRI output indices ---------------------------------------------------
_F03_GROUP_FLOW_STATE = 2            # f03:group_flow_state
_M1_SYNCHRONY_AMPLIFICATION = 6     # M1:synchrony_amplification


class GroupFlow(AppraisalBelief):
    """Appraisal belief: collective group flow state."""

    NAME = "group_flow"
    FULL_NAME = "Group Flow"
    FUNCTION = "F9"
    MECHANISM = "SSRI"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f03:group_flow_state", 0.60),
        ("M1:synchrony_amplification", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe group flow from SSRI output.

        Args:
            mechanism_output: ``(B, T, 11)`` SSRI output tensor.

        Returns:
            ``(B, T)`` observed group flow state.
        """
        return (
            0.60 * mechanism_output[:, :, _F03_GROUP_FLOW_STATE]
            + 0.40 * mechanism_output[:, :, _M1_SYNCHRONY_AMPLIFICATION]
        )
