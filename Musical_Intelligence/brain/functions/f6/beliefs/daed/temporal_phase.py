"""temporal_phase — Appraisal belief (DAED, F6).

"Current temporal phase of the dopaminergic reward cycle —
anticipatory vs consummatory."

Observe: temporal_phase (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/temporal-phase.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- DAED output index -------------------------------------------------------
_TEMPORAL_PHASE = 5


class TemporalPhase(AppraisalBelief):
    """Appraisal belief: dopaminergic reward cycle temporal phase."""

    NAME = "temporal_phase"
    FULL_NAME = "Temporal Phase"
    FUNCTION = "F6"
    MECHANISM = "DAED"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("temporal_phase", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe temporal phase from DAED temporal_phase.

        Args:
            mechanism_output: ``(B, T, 8)`` DAED output tensor.

        Returns:
            ``(B, T)`` temporal phase value.
        """
        return mechanism_output[:, :, _TEMPORAL_PHASE]
