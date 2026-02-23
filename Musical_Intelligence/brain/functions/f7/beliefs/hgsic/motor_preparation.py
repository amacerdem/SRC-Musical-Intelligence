"""motor_preparation — Appraisal belief (HGSIC, F7).

"Motor system is prepared for upcoming beat execution."

Observe: motor_preparation (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/motor-preparation.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HGSIC output index -------------------------------------------------------
_MOTOR_PREPARATION = 6         # motor_preparation


class MotorPreparation(AppraisalBelief):
    """Appraisal belief: motor preparation state.

    Direct readout of motor preparation from HGSIC.
    High values indicate the motor system is ready for
    upcoming beat execution (preSMA activation).
    Low values indicate unprepared motor state.

    Dependency: Requires HGSIC mechanism (Relay, Depth 0).
    """

    NAME = "motor_preparation"
    FULL_NAME = "Motor Preparation"
    FUNCTION = "F7"
    MECHANISM = "HGSIC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("motor_preparation", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe motor preparation from HGSIC output.

        Args:
            mechanism_output: ``(B, T, 11)`` HGSIC output tensor.

        Returns:
            ``(B, T)`` motor preparation value.
        """
        return mechanism_output[:, :, _MOTOR_PREPARATION]
