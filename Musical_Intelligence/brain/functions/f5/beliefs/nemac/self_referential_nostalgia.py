"""self_referential_nostalgia — Appraisal belief (NEMAC, F5).

"Music holds personal meaning for me."

Observe: M0:mpfc_activation (1.0)
No predict/update cycle. Feeds F6 Reward (self-referential boost).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- NEMAC output indices (11D) ------------------------------------------------
_M0_MPFC_ACTIVATION = 2       # M0:mpfc_activation


class SelfReferentialNostalgia(AppraisalBelief):
    """Appraisal belief: self-referential nostalgia processing.

    Measures mPFC activation for self-referential processing.
    High = music has personal autobiographical significance.

    Janata 2009: dorsal mPFC tracks autobiographically salient music.
    Dependency: Requires NEMAC mechanism (Encoder, Depth 1).
    """

    NAME = "self_referential_nostalgia"
    FULL_NAME = "Self-Referential Nostalgia"
    FUNCTION = "F5"
    MECHANISM = "NEMAC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("M0:mpfc_activation", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe self-referential nostalgia from NEMAC outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` NEMAC output tensor.

        Returns:
            ``(B, T)`` self-referential nostalgia value.
        """
        return mechanism_output[:, :, _M0_MPFC_ACTIVATION]
