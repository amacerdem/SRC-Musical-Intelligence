"""detection_accuracy -- Appraisal belief (SLEE, F8).

"The current accuracy of pattern detection based on statistical
learning and expectation formation."

Observe: 0.60*f02:detection_accuracy + 0.40*P0:expectation_formation
No predict/update cycle.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/detection-accuracy.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SLEE output indices ---------------------------------------------------
_F02_DETECTION_ACCURACY = 1          # f02:detection_accuracy
_P0_EXPECTATION_FORMATION = 7        # P0:expectation_formation


class DetectionAccuracy(AppraisalBelief):
    """Appraisal belief: statistical learning detection accuracy."""

    NAME = "detection_accuracy"
    FULL_NAME = "Detection Accuracy"
    FUNCTION = "F8"
    MECHANISM = "SLEE"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f02:detection_accuracy", 0.60),
        ("P0:expectation_formation", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe detection accuracy from SLEE output.

        Args:
            mechanism_output: ``(B, T, 13)`` SLEE output tensor.

        Returns:
            ``(B, T)`` observed detection accuracy.
        """
        return (
            0.60 * mechanism_output[:, :, _F02_DETECTION_ACCURACY]
            + 0.40 * mechanism_output[:, :, _P0_EXPECTATION_FORMATION]
        )
