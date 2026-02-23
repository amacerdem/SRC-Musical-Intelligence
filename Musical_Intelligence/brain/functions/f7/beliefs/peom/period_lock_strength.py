"""period_lock_strength — Appraisal belief (PEOM, F7).

"Motor period is strongly phase-locked to the auditory beat."

Observe: period_lock_strength (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/period-lock-strength.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- PEOM output index ---------------------------------------------------------
_PERIOD_LOCK_STRENGTH = 7  # period_lock_strength


class PeriodLockStrength(AppraisalBelief):
    """Appraisal belief: period lock strength.

    Direct readout of the motor-period phase-locking strength
    from PEOM. High values indicate strong period lock.

    Dependency: Requires PEOM mechanism (Relay, Depth 0).
    """

    NAME = "period_lock_strength"
    FULL_NAME = "Period Lock Strength"
    FUNCTION = "F7"
    MECHANISM = "PEOM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("period_lock_strength", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe period lock strength from PEOM output.

        Args:
            mechanism_output: ``(B, T, 11)`` PEOM output tensor.

        Returns:
            ``(B, T)`` period lock strength value.
        """
        return mechanism_output[:, :, _PERIOD_LOCK_STRENGTH]
