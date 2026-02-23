"""auditory_motor_coupling — Appraisal belief (HGSIC, F7).

"Auditory and motor systems are strongly coupled."

Observe: coupling_strength (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/auditory-motor-coupling.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HGSIC output index -------------------------------------------------------
_COUPLING_STRENGTH = 4         # coupling_strength


class AuditoryMotorCoupling(AppraisalBelief):
    """Appraisal belief: auditory-motor coupling strength.

    Direct readout of the coupling strength between auditory and
    motor systems from HGSIC. High values indicate tight coupling
    (Grahn & Brett 2007). Low values indicate decoupled systems.

    Dependency: Requires HGSIC mechanism (Relay, Depth 0).
    """

    NAME = "auditory_motor_coupling"
    FULL_NAME = "Auditory-Motor Coupling"
    FUNCTION = "F7"
    MECHANISM = "HGSIC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("coupling_strength", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe auditory-motor coupling from HGSIC output.

        Args:
            mechanism_output: ``(B, T, 11)`` HGSIC output tensor.

        Returns:
            ``(B, T)`` coupling strength value.
        """
        return mechanism_output[:, :, _COUPLING_STRENGTH]
