"""melodic_recognition — Appraisal belief (MMP, F4).

"I can still recognize this melody."

Observe: 0.60*P1:melodic_identification + 0.40*R1:melodic_recognition
No predict/update cycle. Feeds familiarity computation.
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- MMP output indices (12D: R3+P3+F3+C3) ------------------------------------
_R1_MELODIC_RECOGNITION = 1   # R1:melodic_recognition
_P1_MELODIC_ID = 4            # P1:melodic_identification


class MelodicRecognition(AppraisalBelief):
    """Appraisal belief: melodic recognition.

    Measures cortically-mediated melody recognition through
    STG + angular gyrus pathway. Preserved in Alzheimer's disease
    due to SMA/ACC storage independence from hippocampus.

    Jacobsen 2015: musical memory regions show least cortical atrophy
    in AD (fMRI+VBM, N=32).
    Dependency: Requires MMP mechanism (Relay, Depth 0).
    """

    NAME = "melodic_recognition"
    FULL_NAME = "Melodic Recognition"
    FUNCTION = "F4"
    MECHANISM = "MMP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:melodic_identification", 0.60),
        ("R1:melodic_recognition", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe melodic recognition from MMP outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` MMP output tensor.

        Returns:
            ``(B, T)`` melodic recognition value.
        """
        return (
            0.60 * mechanism_output[:, :, _P1_MELODIC_ID]
            + 0.40 * mechanism_output[:, :, _R1_MELODIC_RECOGNITION]
        )
