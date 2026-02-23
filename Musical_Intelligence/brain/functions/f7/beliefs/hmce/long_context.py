"""long_context — Appraisal belief (HMCE, F7).

"Long-range temporal context is active (~15-30s window)."

Observe: f03:long_context (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/long-context.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HMCE output index ---------------------------------------------------------
_F03_LONG_CONTEXT = 2          # f03:long_context


class LongContext(AppraisalBelief):
    """Appraisal belief: long-range temporal context.

    Direct readout of long-context encoding from HMCE.
    Represents ~15-30s temporal integration window (section level).
    High values indicate strong long-range context.

    Dependency: Requires HMCE mechanism (Relay, Depth 0).
    """

    NAME = "long_context"
    FULL_NAME = "Long Context"
    FUNCTION = "F7"
    MECHANISM = "HMCE"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f03:long_context", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe long context from HMCE f03:long_context.

        Args:
            mechanism_output: ``(B, T, 11)`` HMCE output tensor.

        Returns:
            ``(B, T)`` long context value.
        """
        return mechanism_output[:, :, _F03_LONG_CONTEXT]
