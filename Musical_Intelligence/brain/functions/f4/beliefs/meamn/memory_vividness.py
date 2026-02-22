"""memory_vividness — Appraisal belief (MEAMN, F4).

"Memory vividness high/low." Retrieval × emotional intensity product.

Observe: E0:f01_retrieval × P1:emotional_color (product)
No predict/update cycle. Feeds F6 Reward (vivid memories amplify reward).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- MEAMN output indices (12D) ------------------------------------------------
_E0_F01_RETRIEVAL = 0         # E0:f01_retrieval
_P1_EMOTIONAL_COLOR = 6       # P1:emotional_color


class MemoryVividness(AppraisalBelief):
    """Appraisal belief: memory vividness.

    Product of retrieval activation and emotional intensity.
    High values = vivid, emotionally charged memory experience.

    Belfi 2016: music-evoked memories more vivid than word-cued.
    Dependency: Requires MEAMN mechanism (Relay, Depth 0).
    """

    NAME = "memory_vividness"
    FULL_NAME = "Memory Vividness"
    FUNCTION = "F4"
    MECHANISM = "MEAMN"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E0:f01_retrieval", 0.50),
        ("P1:emotional_color", 0.50),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe memory vividness from MEAMN outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` MEAMN output tensor.

        Returns:
            ``(B, T)`` vividness value (retrieval × emotion product).
        """
        return (
            mechanism_output[:, :, _E0_F01_RETRIEVAL]
            * mechanism_output[:, :, _P1_EMOTIONAL_COLOR]
        )
