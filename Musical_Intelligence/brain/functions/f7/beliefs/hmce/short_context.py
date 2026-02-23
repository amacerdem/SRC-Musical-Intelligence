"""short_context — Appraisal belief (HMCE, F7).

"Short-range temporal context is active (~1-2s window)."

Observe: f01:short_context (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/short-context.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HMCE output index ---------------------------------------------------------
_F01_SHORT_CONTEXT = 0         # f01:short_context


class ShortContext(AppraisalBelief):
    """Appraisal belief: short-range temporal context.

    Direct readout of short-context encoding from HMCE.
    Represents ~1-2s temporal integration window.
    High values indicate strong short-range context.

    Dependency: Requires HMCE mechanism (Relay, Depth 0).
    """

    NAME = "short_context"
    FULL_NAME = "Short Context"
    FUNCTION = "F7"
    MECHANISM = "HMCE"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f01:short_context", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe short context from HMCE f01:short_context.

        Args:
            mechanism_output: ``(B, T, 11)`` HMCE output tensor.

        Returns:
            ``(B, T)`` short context value.
        """
        return mechanism_output[:, :, _F01_SHORT_CONTEXT]
