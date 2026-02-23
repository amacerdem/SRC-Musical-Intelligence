"""meter_structure — Appraisal belief (HGSIC, F7).

"The rhythmic pattern organizes into a clear metric structure."

Observe: f02:meter_integration (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/meter-structure.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HGSIC output index -------------------------------------------------------
_F02_METER_INTEGRATION = 1     # f02:meter_integration


class MeterStructure(AppraisalBelief):
    """Appraisal belief: metric structure clarity.

    Direct readout of metric integration from HGSIC.
    High values indicate clear hierarchical meter.
    Low values indicate ambiguous or absent meter.

    Dependency: Requires HGSIC mechanism (Relay, Depth 0).
    """

    NAME = "meter_structure"
    FULL_NAME = "Meter Structure"
    FUNCTION = "F7"
    MECHANISM = "HGSIC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f02:meter_integration", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe meter structure from HGSIC f02:meter_integration.

        Args:
            mechanism_output: ``(B, T, 11)`` HGSIC output tensor.

        Returns:
            ``(B, T)`` metric structure value.
        """
        return mechanism_output[:, :, _F02_METER_INTEGRATION]
