"""pitch_mmn -- Appraisal belief (ESME, F8).

"The current pitch mismatch negativity response magnitude and
deviance detection sensitivity."

Observe: 0.60*f01:pitch_mmn + 0.40*P0:pitch_deviance_detection
No predict/update cycle.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/pitch-mmn.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- ESME output indices ---------------------------------------------------
_F01_PITCH_MMN = 0                   # f01:pitch_mmn
_P0_PITCH_DEVIANCE_DETECTION = 5     # P0:pitch_deviance_detection


class PitchMmn(AppraisalBelief):
    """Appraisal belief: pitch mismatch negativity response."""

    NAME = "pitch_mmn"
    FULL_NAME = "Pitch MMN"
    FUNCTION = "F8"
    MECHANISM = "ESME"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f01:pitch_mmn", 0.60),
        ("P0:pitch_deviance_detection", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe pitch MMN from ESME output.

        Args:
            mechanism_output: ``(B, T, 11)`` ESME output tensor.

        Returns:
            ``(B, T)`` observed pitch mismatch negativity.
        """
        return (
            0.60 * mechanism_output[:, :, _F01_PITCH_MMN]
            + 0.40 * mechanism_output[:, :, _P0_PITCH_DEVIANCE_DETECTION]
        )
