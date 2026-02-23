"""entrainment_quality -- Appraisal belief (SSRI, F9).

"The quality of interpersonal entrainment during shared musical
experience."

Observe: f04:entrainment_quality (1.0) -- direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F9-Social/beliefs/entrainment-quality.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SSRI output index -----------------------------------------------------
_F04_ENTRAINMENT_QUALITY = 3         # f04:entrainment_quality


class EntrainmentQuality(AppraisalBelief):
    """Appraisal belief: interpersonal entrainment quality."""

    NAME = "entrainment_quality"
    FULL_NAME = "Entrainment Quality"
    FUNCTION = "F9"
    MECHANISM = "SSRI"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f04:entrainment_quality", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe entrainment quality from SSRI output.

        Args:
            mechanism_output: ``(B, T, 11)`` SSRI output tensor.

        Returns:
            ``(B, T)`` observed entrainment quality.
        """
        return mechanism_output[:, :, _F04_ENTRAINMENT_QUALITY]
