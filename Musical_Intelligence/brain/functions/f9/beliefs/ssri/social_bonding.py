"""social_bonding -- Appraisal belief (SSRI, F9).

"The degree of social bonding facilitated by shared musical
experience and endorphin release."

Observe: 0.60*f02:social_bonding_index + 0.40*P1:endorphin_proxy
No predict/update cycle.

See Building/C3-Brain/F9-Social/beliefs/social-bonding.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SSRI output indices ---------------------------------------------------
_F02_SOCIAL_BONDING_INDEX = 1        # f02:social_bonding_index
_P1_ENDORPHIN_PROXY = 8              # P1:endorphin_proxy


class SocialBonding(AppraisalBelief):
    """Appraisal belief: music-driven social bonding index."""

    NAME = "social_bonding"
    FULL_NAME = "Social Bonding"
    FUNCTION = "F9"
    MECHANISM = "SSRI"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f02:social_bonding_index", 0.60),
        ("P1:endorphin_proxy", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe social bonding from SSRI output.

        Args:
            mechanism_output: ``(B, T, 11)`` SSRI output tensor.

        Returns:
            ``(B, T)`` observed social bonding index.
        """
        return (
            0.60 * mechanism_output[:, :, _F02_SOCIAL_BONDING_INDEX]
            + 0.40 * mechanism_output[:, :, _P1_ENDORPHIN_PROXY]
        )
