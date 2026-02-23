"""da_caudate — Appraisal belief (DAED, F6).

"Caudate nucleus dopaminergic activation level — anticipatory reward
processing."

Observe: caudate_activation (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/da-caudate.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- DAED output index -------------------------------------------------------
_CAUDATE_ACTIVATION = 6


class DaCaudate(AppraisalBelief):
    """Appraisal belief: caudate nucleus dopaminergic activation."""

    NAME = "da_caudate"
    FULL_NAME = "DA Caudate"
    FUNCTION = "F6"
    MECHANISM = "DAED"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("caudate_activation", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe caudate activation from DAED caudate_activation.

        Args:
            mechanism_output: ``(B, T, 8)`` DAED output tensor.

        Returns:
            ``(B, T)`` caudate activation value.
        """
        return mechanism_output[:, :, _CAUDATE_ACTIVATION]
