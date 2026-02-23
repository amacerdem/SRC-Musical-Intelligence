"""timbre_mmn -- Appraisal belief (ESME, F8).

"The current timbre mismatch negativity response magnitude and
spectral deviance detection."

Observe: 0.60*f03:timbre_mmn + 0.40*P2:timbre_deviance_detection
No predict/update cycle.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/timbre-mmn.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- ESME output indices ---------------------------------------------------
_F03_TIMBRE_MMN = 2                  # f03:timbre_mmn
_P2_TIMBRE_DEVIANCE_DETECTION = 7    # P2:timbre_deviance_detection


class TimbreMmn(AppraisalBelief):
    """Appraisal belief: timbre mismatch negativity response."""

    NAME = "timbre_mmn"
    FULL_NAME = "Timbre MMN"
    FUNCTION = "F8"
    MECHANISM = "ESME"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f03:timbre_mmn", 0.60),
        ("P2:timbre_deviance_detection", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe timbre MMN from ESME output.

        Args:
            mechanism_output: ``(B, T, 11)`` ESME output tensor.

        Returns:
            ``(B, T)`` observed timbre mismatch negativity.
        """
        return (
            0.60 * mechanism_output[:, :, _F03_TIMBRE_MMN]
            + 0.40 * mechanism_output[:, :, _P2_TIMBRE_DEVIANCE_DETECTION]
        )
