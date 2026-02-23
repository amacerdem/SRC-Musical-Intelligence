"""timing_precision — Appraisal belief (PEOM, F7).

"Motor timing variability is low (high precision)."

Observe: 0.50*f03:variability_reduction + 0.50*cv_reduction
No predict/update cycle.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/timing-precision.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- PEOM output indices (11D) ------------------------------------------------
_F03_VARIABILITY_REDUCTION = 2  # f03:variability_reduction
_CV_REDUCTION = 6               # cv_reduction


class TimingPrecision(AppraisalBelief):
    """Appraisal belief: motor timing precision.

    Measures how precisely motor timing aligns with the beat.
    High values indicate low variability (tight timing).
    Low values indicate sloppy or imprecise timing.

    Dependency: Requires PEOM mechanism (Relay, Depth 0).
    """

    NAME = "timing_precision"
    FULL_NAME = "Timing Precision"
    FUNCTION = "F7"
    MECHANISM = "PEOM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f03:variability_reduction", 0.50),
        ("cv_reduction", 0.50),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe timing precision from PEOM outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` PEOM output tensor.

        Returns:
            ``(B, T)`` observed timing precision value.
        """
        return (
            0.50 * mechanism_output[:, :, _F03_VARIABILITY_REDUCTION]
            + 0.50 * mechanism_output[:, :, _CV_REDUCTION]
        )
