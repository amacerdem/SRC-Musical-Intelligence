"""peak_detection — Appraisal belief (SRP, F6).

"A reward peak / climax moment is occurring in the musical stimulus."

Observe: M2:peak_detection (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/peak-detection.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SRP output index -------------------------------------------------------
_M2_PEAK_DETECTION = 12


class PeakDetection(AppraisalBelief):
    """Appraisal belief: reward peak / climax detection."""

    NAME = "peak_detection"
    FULL_NAME = "Peak Detection"
    FUNCTION = "F6"
    MECHANISM = "SRP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("M2:peak_detection", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe peak detection from SRP M2:peak_detection.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` peak detection value.
        """
        return mechanism_output[:, :, _M2_PEAK_DETECTION]
