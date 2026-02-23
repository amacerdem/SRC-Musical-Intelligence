"""wanting_ramp — Anticipation belief (DAED, F6).

"Anticipatory wanting is ramping up — predicted wanting trajectory
from dopaminergic dynamics."

Observe: f03:wanting_index (1.0) — DAED wanting index output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/wanting-ramp.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- DAED output index -------------------------------------------------------
_F03_WANTING_INDEX = 2


class WantingRamp(AnticipationBelief):
    """Anticipation belief: wanting trajectory ramp from DA dynamics."""

    NAME = "wanting_ramp"
    FULL_NAME = "Wanting Ramp"
    FUNCTION = "F6"
    MECHANISM = "DAED"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f03:wanting_index", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe wanting ramp from DAED f03:wanting_index.

        Args:
            mechanism_output: ``(B, T, 8)`` DAED output tensor.

        Returns:
            ``(B, T)`` wanting ramp value.
        """
        return mechanism_output[:, :, _F03_WANTING_INDEX]
