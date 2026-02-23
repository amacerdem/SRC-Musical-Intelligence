"""resource_allocation -- Appraisal belief (DDSMI, F9).

"The current allocation of attentional resources between social
and musical processing, modulated by visual input."

Observe: 0.60*E2:f15_visual_modulation + 0.40*M2:mTRF_balance
No predict/update cycle.

See Building/C3-Brain/F9-Social/beliefs/resource-allocation.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- DDSMI output indices --------------------------------------------------
_E2_VISUAL_MODULATION = 2            # E2:f15_visual_modulation
_M2_MTRF_BALANCE = 5                 # M2:mTRF_balance


class ResourceAllocation(AppraisalBelief):
    """Appraisal belief: social-musical resource allocation balance."""

    NAME = "resource_allocation"
    FULL_NAME = "Resource Allocation"
    FUNCTION = "F9"
    MECHANISM = "DDSMI"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E2:f15_visual_modulation", 0.60),
        ("M2:mTRF_balance", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe resource allocation from DDSMI output.

        Args:
            mechanism_output: ``(B, T, 11)`` DDSMI output tensor.

        Returns:
            ``(B, T)`` observed resource allocation balance.
        """
        return (
            0.60 * mechanism_output[:, :, _E2_VISUAL_MODULATION]
            + 0.40 * mechanism_output[:, :, _M2_MTRF_BALANCE]
        )
