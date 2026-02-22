"""precision_weighting — Appraisal belief (IACM, F3).

"Context stability determines prediction error weight."

Observe: E2:precision_weighting (1.0) — direct from IACM.
No predict/update cycle. Feeds F2 precision engine.
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- IACM output index --------------------------------------------------------
_E2_PRECISION_WEIGHTING = 2    # E2:precision_weighting


class PrecisionWeighting(AppraisalBelief):
    """Appraisal belief: context-dependent precision weighting.

    Measures how stable the current context is for weighting
    prediction errors. High values = stable context, high PE weight.

    Dependency: Requires IACM mechanism (Relay, Depth 0).
    """

    NAME = "precision_weighting"
    FULL_NAME = "Precision Weighting"
    FUNCTION = "F3"
    MECHANISM = "IACM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E2:precision_weighting", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe precision weighting from IACM E2.

        Args:
            mechanism_output: ``(B, T, 11)`` IACM output tensor.

        Returns:
            ``(B, T)`` precision weighting value.
        """
        return mechanism_output[:, :, _E2_PRECISION_WEIGHTING]
