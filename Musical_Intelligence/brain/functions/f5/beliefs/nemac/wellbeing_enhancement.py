"""wellbeing_enhancement — Appraisal belief (NEMAC, F5).

"Nostalgic music increasing my well-being."

Observe: W1:wellbeing_enhance (1.0)
No predict/update cycle. Feeds F10 Clinical (therapeutic monitoring).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- NEMAC output indices (11D) ------------------------------------------------
_W1_WELLBEING_ENHANCE = 6     # W1:wellbeing_enhance


class WellbeingEnhancement(AppraisalBelief):
    """Appraisal belief: nostalgia-driven wellbeing enhancement.

    Measures increase in subjective wellbeing from nostalgic music.

    Barrett 2010: music-evoked nostalgia enhances social bonding
    and meaning in life.
    Dependency: Requires NEMAC mechanism (Encoder, Depth 1).
    """

    NAME = "wellbeing_enhancement"
    FULL_NAME = "Wellbeing Enhancement"
    FUNCTION = "F5"
    MECHANISM = "NEMAC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("W1:wellbeing_enhance", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe wellbeing enhancement from NEMAC outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` NEMAC output tensor.

        Returns:
            ``(B, T)`` wellbeing enhancement value.
        """
        return mechanism_output[:, :, _W1_WELLBEING_ENHANCE]
