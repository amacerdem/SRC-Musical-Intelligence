"""resolution_expectation — Anticipation belief (SRP, F6).

"Tension is expected to resolve — predicted resolution trajectory."

Observe: F2:resolution_expect (1.0) — SRP forecast output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/resolution-expectation.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- SRP output index -------------------------------------------------------
_F2_RESOLUTION_EXPECT = 18


class ResolutionExpectation(AnticipationBelief):
    """Anticipation belief: expected tension resolution trajectory."""

    NAME = "resolution_expectation"
    FULL_NAME = "Resolution Expectation"
    FUNCTION = "F6"
    MECHANISM = "SRP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F2:resolution_expect", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe resolution expectation from SRP F2:resolution_expect.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` resolution expectation value.
        """
        return mechanism_output[:, :, _F2_RESOLUTION_EXPECT]
