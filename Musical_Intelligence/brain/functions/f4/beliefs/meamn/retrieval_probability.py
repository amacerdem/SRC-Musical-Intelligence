"""retrieval_probability — Appraisal belief (MEAMN, F4).

"My probability of accessing this memory is X."

Observe: P0:memory_state (1.0)
No predict/update cycle. Feeds familiarity computation.
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- MEAMN output indices (12D) ------------------------------------------------
_P0_MEMORY_STATE = 5          # P0:memory_state


class RetrievalProbability(AppraisalBelief):
    """Appraisal belief: memory retrieval probability.

    Direct read of MEAMN P0:memory_state. Indicates the current
    probability of accessing an autobiographical memory.

    Janata 2009: 30-80% MEAM trigger rate.
    Dependency: Requires MEAMN mechanism (Relay, Depth 0).
    """

    NAME = "retrieval_probability"
    FULL_NAME = "Retrieval Probability"
    FUNCTION = "F4"
    MECHANISM = "MEAMN"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:memory_state", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe retrieval probability from MEAMN outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` MEAMN output tensor.

        Returns:
            ``(B, T)`` retrieval probability value.
        """
        return mechanism_output[:, :, _P0_MEMORY_STATE]
