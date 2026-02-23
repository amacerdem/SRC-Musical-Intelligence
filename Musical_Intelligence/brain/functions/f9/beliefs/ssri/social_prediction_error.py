"""social_prediction_error -- Appraisal belief (SSRI, F9).

"The current social prediction error magnitude for interpersonal
musical synchrony."

Observe: M0:social_prediction_error (1.0) -- direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F9-Social/beliefs/social-prediction-error.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SSRI output index -----------------------------------------------------
_M0_SOCIAL_PREDICTION_ERROR = 5      # M0:social_prediction_error


class SocialPredictionError(AppraisalBelief):
    """Appraisal belief: social prediction error in musical interaction."""

    NAME = "social_prediction_error"
    FULL_NAME = "Social Prediction Error"
    FUNCTION = "F9"
    MECHANISM = "SSRI"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("M0:social_prediction_error", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe social prediction error from SSRI output.

        Args:
            mechanism_output: ``(B, T, 11)`` SSRI output tensor.

        Returns:
            ``(B, T)`` observed social prediction error.
        """
        return mechanism_output[:, :, _M0_SOCIAL_PREDICTION_ERROR]
