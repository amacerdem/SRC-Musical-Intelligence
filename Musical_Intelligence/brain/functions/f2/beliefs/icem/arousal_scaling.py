"""arousal_scaling — Appraisal belief (ICEM, F2).

"The current IC level is producing arousal scaling."

Observe: 0.40*E1:arousal_response + 0.30*M1:arousal_pred
         + 0.30*P0:surprise_signal
No predict/update cycle.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/icem/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- ICEM output indices (13D) ------------------------------------------------
_E1_AROUSAL_RESPONSE = 1    # E1:arousal_response
_M1_AROUSAL_PRED = 5        # M1:arousal_pred
_P0_SURPRISE_SIGNAL = 9    # P0:surprise_signal


class ArousalScaling(AppraisalBelief):
    """Appraisal belief: arousal scaling from IC.

    Measures how IC translates to physiological arousal. Combines
    the raw arousal response, mathematical arousal prediction, and
    present-moment surprise signal. High values indicate strong
    IC-to-arousal mapping.

    Egermann et al. 2013: IC peaks → arousal↑ (p<0.001).
    Arousal = α·IC + β (linear mapping).
    """

    NAME = "arousal_scaling"
    FULL_NAME = "Arousal Scaling"
    FUNCTION = "F2"
    MECHANISM = "ICEM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E1:arousal_response", 0.40),
        ("M1:arousal_pred", 0.30),
        ("P0:surprise_signal", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe arousal scaling from ICEM outputs.

        Args:
            mechanism_output: ``(B, T, 13)`` ICEM output tensor.

        Returns:
            ``(B, T)`` observed arousal scaling value.
        """
        return (
            0.40 * mechanism_output[:, :, _E1_AROUSAL_RESPONSE]
            + 0.30 * mechanism_output[:, :, _M1_AROUSAL_PRED]
            + 0.30 * mechanism_output[:, :, _P0_SURPRISE_SIGNAL]
        )
