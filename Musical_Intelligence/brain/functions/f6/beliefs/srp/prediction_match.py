"""prediction_match — Appraisal belief (SRP, F6).

"The sensory input matches or violates the current prediction."

Observe: T1:prediction_match (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/prediction-match.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SRP output index -------------------------------------------------------
_T1_PREDICTION_MATCH = 7


class PredictionMatch(AppraisalBelief):
    """Appraisal belief: degree of prediction-outcome match."""

    NAME = "prediction_match"
    FULL_NAME = "Prediction Match"
    FUNCTION = "F6"
    MECHANISM = "SRP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("T1:prediction_match", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe prediction match from SRP T1:prediction_match.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` prediction-outcome match value.
        """
        return mechanism_output[:, :, _T1_PREDICTION_MATCH]
