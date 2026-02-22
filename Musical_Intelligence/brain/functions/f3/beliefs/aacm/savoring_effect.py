"""savoring_effect — Appraisal belief (AACM, F3).

"Liking leads to sustained attention and slower motor response (savoring)."

Observe: 0.60*P1:aesthetic_judgment + 0.40*E2:savoring_effect
No predict/update cycle. Feeds F6 Reward (sustained pleasure amplification).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- AACM output indices (10D) ------------------------------------------------
_E2_SAVORING_EFFECT = 2        # E2:savoring_effect
_P1_AESTHETIC_JUDGMENT = 6     # P1:aesthetic_judgment


class SavoringEffect(AppraisalBelief):
    """Appraisal belief: savoring effect (liking -> slow response).

    Measures how liking prolongs attention and slows motor response.
    High values = strong savoring (sustained engagement, slower RT).

    Brattico 2013: liked stimuli show slower RT + deeper processing.
    Dependency: Requires AACM mechanism (Encoder, Depth 1).
    """

    NAME = "savoring_effect"
    FULL_NAME = "Savoring Effect"
    FUNCTION = "F3"
    MECHANISM = "AACM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:aesthetic_judgment", 0.60),
        ("E2:savoring_effect", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe savoring effect from AACM outputs.

        Args:
            mechanism_output: ``(B, T, 10)`` AACM output tensor.

        Returns:
            ``(B, T)`` observed savoring effect value.
        """
        return (
            0.60 * mechanism_output[:, :, _P1_AESTHETIC_JUDGMENT]
            + 0.40 * mechanism_output[:, :, _E2_SAVORING_EFFECT]
        )
