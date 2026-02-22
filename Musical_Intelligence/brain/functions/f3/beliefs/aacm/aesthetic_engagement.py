"""aesthetic_engagement — Appraisal belief (AACM, F3).

"Preferred intervals are increasing attention and inhibiting motor response."

Observe: 0.60*P0:n1p2_engagement + 0.40*M0:aesthetic_engagement
No predict/update cycle. Feeds F6 Reward (aesthetic contribution).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- AACM output indices (10D) ------------------------------------------------
_M0_AESTHETIC_ENGAGEMENT = 3   # M0:aesthetic_engagement
_P0_N1P2_ENGAGEMENT = 5       # P0:n1p2_engagement


class AestheticEngagement(AppraisalBelief):
    """Appraisal belief: aesthetic-attention engagement.

    Measures how strongly preferred intervals are capturing and
    sustaining attention. High values = strong aesthetic engagement.

    Sarasso 2019: consonant intervals enhance N1/P2 attention markers.
    Dependency: Requires AACM mechanism (Encoder, Depth 1).
    """

    NAME = "aesthetic_engagement"
    FULL_NAME = "Aesthetic Engagement"
    FUNCTION = "F3"
    MECHANISM = "AACM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:n1p2_engagement", 0.60),
        ("M0:aesthetic_engagement", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe aesthetic engagement from AACM outputs.

        Args:
            mechanism_output: ``(B, T, 10)`` AACM output tensor.

        Returns:
            ``(B, T)`` observed aesthetic engagement value.
        """
        return (
            0.60 * mechanism_output[:, :, _P0_N1P2_ENGAGEMENT]
            + 0.40 * mechanism_output[:, :, _M0_AESTHETIC_ENGAGEMENT]
        )
