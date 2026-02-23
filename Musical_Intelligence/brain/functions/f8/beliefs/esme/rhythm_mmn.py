"""rhythm_mmn -- Appraisal belief (ESME, F8).

"The current rhythm mismatch negativity response magnitude and
temporal deviance detection."

Observe: 0.60*f02:rhythm_mmn + 0.40*P1:rhythm_deviance_detection
No predict/update cycle.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/rhythm-mmn.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- ESME output indices ---------------------------------------------------
_F02_RHYTHM_MMN = 1                  # f02:rhythm_mmn
_P1_RHYTHM_DEVIANCE_DETECTION = 6    # P1:rhythm_deviance_detection


class RhythmMmn(AppraisalBelief):
    """Appraisal belief: rhythm mismatch negativity response."""

    NAME = "rhythm_mmn"
    FULL_NAME = "Rhythm MMN"
    FUNCTION = "F8"
    MECHANISM = "ESME"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f02:rhythm_mmn", 0.60),
        ("P1:rhythm_deviance_detection", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe rhythm MMN from ESME output.

        Args:
            mechanism_output: ``(B, T, 11)`` ESME output tensor.

        Returns:
            ``(B, T)`` observed rhythm mismatch negativity.
        """
        return (
            0.60 * mechanism_output[:, :, _F02_RHYTHM_MMN]
            + 0.40 * mechanism_output[:, :, _P1_RHYTHM_DEVIANCE_DETECTION]
        )
