"""valence_inversion — Appraisal belief (ICEM, F2).

"High IC is inverting valence (unexpected → negative feeling)."

Observe: 0.40*E2:valence_response + 0.30*M2:valence_pred
         + 0.30*P1:emotional_evaluation
No predict/update cycle.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/icem/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- ICEM output indices (13D) ------------------------------------------------
_E2_VALENCE_RESPONSE = 2       # E2:valence_response
_M2_VALENCE_PRED = 6           # M2:valence_pred
_P1_EMOTIONAL_EVALUATION = 10  # P1:emotional_evaluation


class ValenceInversion(AppraisalBelief):
    """Appraisal belief: valence inversion from IC.

    Measures the inverse relationship between IC and valence. High IC
    suppresses valence (unexpected events feel negative). The signal
    tracks the current state of this inversion process.

    Egermann et al. 2013: IC peaks → valence↓ (p<0.001).
    Valence = -γ·IC + δ (inverse linear mapping).
    Gold et al. 2019: inverted-U for IC on liking — moderate IC
    maximizes pleasure.
    """

    NAME = "valence_inversion"
    FULL_NAME = "Valence Inversion"
    FUNCTION = "F2"
    MECHANISM = "ICEM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E2:valence_response", 0.40),
        ("M2:valence_pred", 0.30),
        ("P1:emotional_evaluation", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe valence inversion from ICEM outputs.

        Args:
            mechanism_output: ``(B, T, 13)`` ICEM output tensor.

        Returns:
            ``(B, T)`` observed valence inversion value.
        """
        return (
            0.40 * mechanism_output[:, :, _E2_VALENCE_RESPONSE]
            + 0.30 * mechanism_output[:, :, _M2_VALENCE_PRED]
            + 0.30 * mechanism_output[:, :, _P1_EMOTIONAL_EVALUATION]
        )
