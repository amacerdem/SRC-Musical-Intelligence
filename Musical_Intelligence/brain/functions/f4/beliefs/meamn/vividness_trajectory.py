"""vividness_trajectory — Anticipation belief (MEAMN, F4).

"Memory will become vivid within 2-5 seconds."

Observe: F0:mem_vividness_fc (1.0)
No predict/update cycle. Feeds precision engine (pi_pred).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- MEAMN output indices (12D) ------------------------------------------------
_F0_MEM_VIVIDNESS_FC = 8      # F0:mem_vividness_fc


class VividnessTrajectory(AnticipationBelief):
    """Anticipation belief: vividness trajectory.

    Forward prediction of memory vividness (2-5s ahead).
    Hippocampal retrieval trajectory over H20 (5s) consolidation.

    Janata 2009: hippocampal retrieval trajectory (t(9)=5.784).
    Dependency: Requires MEAMN mechanism (Relay, Depth 0).
    """

    NAME = "vividness_trajectory"
    FULL_NAME = "Vividness Trajectory"
    FUNCTION = "F4"
    MECHANISM = "MEAMN"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F0:mem_vividness_fc", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe vividness trajectory from MEAMN outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` MEAMN output tensor.

        Returns:
            ``(B, T)`` vividness trajectory prediction.
        """
        return mechanism_output[:, :, _F0_MEM_VIVIDNESS_FC]
