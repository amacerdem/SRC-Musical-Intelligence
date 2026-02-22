"""memory_preservation — Appraisal belief (MMP, F4).

"Musical memories preserved despite disease."

Observe: C0:preservation_index (1.0)
No predict/update cycle. Feeds F10 Clinical meta-layer.
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- MMP output indices (12D: R3+P3+F3+C3) ------------------------------------
_C0_PRESERVATION_INDEX = 9    # C0:preservation_index


class MemoryPreservation(AppraisalBelief):
    """Appraisal belief: memory preservation.

    Clinical metric: cortical_strength / (cortical + episodic + epsilon).
    High values = strong cortically-mediated musical memory with
    minimal hippocampal dependency (preserved in AD).

    Jacobsen 2015: SMA/ACC show least cortical atrophy in AD.
    Dependency: Requires MMP mechanism (Relay, Depth 0).
    """

    NAME = "memory_preservation"
    FULL_NAME = "Memory Preservation"
    FUNCTION = "F4"
    MECHANISM = "MMP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("C0:preservation_index", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe memory preservation from MMP outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` MMP output tensor.

        Returns:
            ``(B, T)`` preservation index value.
        """
        return mechanism_output[:, :, _C0_PRESERVATION_INDEX]
