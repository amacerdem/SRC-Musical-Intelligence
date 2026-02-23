"""da_nacc — Appraisal belief (DAED, F6).

"Nucleus accumbens dopaminergic activation level — consummatory reward
processing."

Observe: nacc_activation (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/da-nacc.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- DAED output index -------------------------------------------------------
_NACC_ACTIVATION = 7


class DaNacc(AppraisalBelief):
    """Appraisal belief: nucleus accumbens dopaminergic activation."""

    NAME = "da_nacc"
    FULL_NAME = "DA NAcc"
    FUNCTION = "F6"
    MECHANISM = "DAED"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("nacc_activation", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe NAcc activation from DAED nacc_activation.

        Args:
            mechanism_output: ``(B, T, 8)`` DAED output tensor.

        Returns:
            ``(B, T)`` NAcc activation value.
        """
        return mechanism_output[:, :, _NACC_ACTIVATION]
