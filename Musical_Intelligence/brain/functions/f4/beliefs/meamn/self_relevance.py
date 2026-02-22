"""self_relevance — Appraisal belief (MEAMN, F4).

"This is MY music." vmPFC self-referential processing.

Observe: F2:self_ref_fc (1.0)
No predict/update cycle. Feeds F6 Reward (self-referential boosts hedonic value).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- MEAMN output indices (12D) ------------------------------------------------
_F2_SELF_REF_FC = 10          # F2:self_ref_fc


class SelfRelevance(AppraisalBelief):
    """Appraisal belief: self-relevance.

    Direct read of MEAMN F2:self_ref_fc. Measures vmPFC
    self-referential processing — "this music is about me."

    Janata 2009: mPFC self-referential processing
    (fMRI 3T, N=13, t(12)=2.96, p=0.012).
    Dependency: Requires MEAMN mechanism (Relay, Depth 0).
    """

    NAME = "self_relevance"
    FULL_NAME = "Self Relevance"
    FUNCTION = "F4"
    MECHANISM = "MEAMN"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F2:self_ref_fc", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe self-relevance from MEAMN outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` MEAMN output tensor.

        Returns:
            ``(B, T)`` self-relevance value.
        """
        return mechanism_output[:, :, _F2_SELF_REF_FC]
