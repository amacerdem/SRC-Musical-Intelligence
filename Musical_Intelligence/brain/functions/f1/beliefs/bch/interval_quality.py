"""interval_quality — Appraisal belief (BCH, F1).

"The current interval sits at position X in the P1/P5/P4/M3/m6/TT
consonance hierarchy."

Observe: E2:hierarchy (1.0) — direct mechanism output, no weighted mix.
No predict/update cycle.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/interval-quality.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# ── BCH output index ────────────────────────────────────────────────
_E2_HIERARCHY = 2


class IntervalQuality(AppraisalBelief):
    """Appraisal belief: categorical consonance hierarchy position."""

    NAME = "interval_quality"
    FULL_NAME = "Interval Quality"
    FUNCTION = "F1"
    MECHANISM = "BCH"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E2:hierarchy", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe interval quality from BCH E2:hierarchy.

        Args:
            mechanism_output: ``(B, T, 16)`` BCH output tensor.

        Returns:
            ``(B, T)`` hierarchical consonance position.
        """
        return mechanism_output[:, :, _E2_HIERARCHY]
