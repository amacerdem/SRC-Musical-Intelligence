"""medium_context — Appraisal belief (HMCE, F7).

"Medium-range temporal context is active (~4-8s window)."

Observe: f02:medium_context (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/medium-context.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HMCE output index ---------------------------------------------------------
_F02_MEDIUM_CONTEXT = 1        # f02:medium_context


class MediumContext(AppraisalBelief):
    """Appraisal belief: medium-range temporal context.

    Direct readout of medium-context encoding from HMCE.
    Represents ~4-8s temporal integration window (phrase level).
    High values indicate strong medium-range context.

    Dependency: Requires HMCE mechanism (Relay, Depth 0).
    """

    NAME = "medium_context"
    FULL_NAME = "Medium Context"
    FUNCTION = "F7"
    MECHANISM = "HMCE"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f02:medium_context", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe medium context from HMCE f02:medium_context.

        Args:
            mechanism_output: ``(B, T, 11)`` HMCE output tensor.

        Returns:
            ``(B, T)`` medium context value.
        """
        return mechanism_output[:, :, _F02_MEDIUM_CONTEXT]
