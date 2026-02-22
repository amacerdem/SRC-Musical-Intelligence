"""mode_detection — Appraisal belief (VMM, F5).

"Major/minor mode (0.5 = ambiguous)."

Observe: C0:mode_detection_state (1.0)
No predict/update cycle. Feeds F2 Prediction (mode confidence).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- VMM output indices (12D) -------------------------------------------------
_C0_MODE_DETECTION_STATE = 10  # C0:mode_detection_state


class ModeDetection(AppraisalBelief):
    """Appraisal belief: major/minor mode detection.

    Near 1.0 = major, near 0.0 = minor, 0.5 = ambiguous.
    Requires phrase-level context (2-3 chords minimum).

    Dalla Bella 2001: mode is primary cue for perceived emotion.
    Dependency: Requires VMM mechanism (Relay, Depth 0).
    """

    NAME = "mode_detection"
    FULL_NAME = "Mode Detection"
    FUNCTION = "F5"
    MECHANISM = "VMM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("C0:mode_detection_state", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe mode detection from VMM outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` VMM output tensor.

        Returns:
            ``(B, T)`` mode detection state.
        """
        return mechanism_output[:, :, _C0_MODE_DETECTION_STATE]
