"""episodic_boundary — Appraisal belief (HCMC, F4).

"Phrase ended, new one began." Event boundary detection.

Observe: P1:segmentation_state (1.0)
No predict/update cycle. Feeds salience mixer + familiarity segmentation.
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HCMC output indices (11D) ------------------------------------------------
_P1_SEGMENTATION_STATE = 7    # P1:segmentation_state


class EpisodicBoundary(AppraisalBelief):
    """Appraisal belief: episodic boundary.

    Detects moments where hippocampus closes one episodic segment
    and opens another. High values = major structural boundary.

    Zacks 2007: event segmentation theory — boundaries trigger encoding.
    Dependency: Requires HCMC mechanism (Encoder, Depth 1).
    """

    NAME = "episodic_boundary"
    FULL_NAME = "Episodic Boundary"
    FUNCTION = "F4"
    MECHANISM = "HCMC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:segmentation_state", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe episodic boundary from HCMC outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` HCMC output tensor.

        Returns:
            ``(B, T)`` episodic boundary value.
        """
        return mechanism_output[:, :, _P1_SEGMENTATION_STATE]
