"""consolidation_strength — Appraisal belief (HCMC, F4).

"Hippocampal to cortical transfer strength."

Observe: P2:storage_state (1.0)
No predict/update cycle. Feeds learning rate adjustment.
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HCMC output indices (11D) ------------------------------------------------
_P2_STORAGE_STATE = 8         # P2:storage_state


class ConsolidationStrength(AppraisalBelief):
    """Appraisal belief: consolidation strength.

    Reflects cortical networks actively receiving consolidated traces
    from hippocampus. Uses consonance-timbre interactions and harmonic
    stability as templates for durable cortical storage.

    Sikka 2015: age-related hippocampal-to-cortical shift for musical
    semantic memory (fMRI, N=40).
    Dependency: Requires HCMC mechanism (Encoder, Depth 1).
    """

    NAME = "consolidation_strength"
    FULL_NAME = "Consolidation Strength"
    FUNCTION = "F4"
    MECHANISM = "HCMC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P2:storage_state", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe consolidation strength from HCMC outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` HCMC output tensor.

        Returns:
            ``(B, T)`` consolidation strength value.
        """
        return mechanism_output[:, :, _P2_STORAGE_STATE]
