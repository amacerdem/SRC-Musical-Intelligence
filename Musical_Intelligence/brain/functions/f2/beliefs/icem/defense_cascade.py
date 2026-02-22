"""defense_cascade — Appraisal belief (ICEM, F2).

"A defense cascade (orienting → threat appraisal) is active."

Observe: 0.50*E3:defense_cascade + 0.30*M3:scr_pred + 0.20*M4:hr_pred
No predict/update cycle.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/icem/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- ICEM output indices (13D) ------------------------------------------------
_E3_DEFENSE_CASCADE = 3    # E3:defense_cascade
_M3_SCR_PRED = 7           # M3:scr_pred
_M4_HR_PRED = 8            # M4:hr_pred


class DefenseCascade(AppraisalBelief):
    """Appraisal belief: defense cascade activation.

    Measures the degree to which the current auditory event triggers
    a defense cascade — orienting response followed by threat appraisal.
    Activated when high IC co-occurs with high arousal and loud events.

    Egermann et al. 2013: subjective unexpected → SCR↑, HR↓, RespR↑
    (p<0.001, defense cascade pattern).
    """

    NAME = "defense_cascade"
    FULL_NAME = "Defense Cascade"
    FUNCTION = "F2"
    MECHANISM = "ICEM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E3:defense_cascade", 0.50),
        ("M3:scr_pred", 0.30),
        ("M4:hr_pred", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe defense cascade from ICEM outputs.

        Args:
            mechanism_output: ``(B, T, 13)`` ICEM output tensor.

        Returns:
            ``(B, T)`` observed defense cascade value.
        """
        return (
            0.50 * mechanism_output[:, :, _E3_DEFENSE_CASCADE]
            + 0.30 * mechanism_output[:, :, _M3_SCR_PRED]
            + 0.20 * mechanism_output[:, :, _M4_HR_PRED]
        )
