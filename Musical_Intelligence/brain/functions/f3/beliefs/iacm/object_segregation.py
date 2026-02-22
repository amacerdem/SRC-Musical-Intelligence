"""object_segregation — Appraisal belief (IACM, F3).

"Multiple sound sources are segregating into separate streams."

Observe: 0.60*P1:spectral_encoding + 0.40*M2:object_perception_or
No predict/update cycle.
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- IACM output indices (11D) ------------------------------------------------
_M2_OBJECT_PERCEPTION = 5     # M2:object_perception_or
_P1_SPECTRAL_ENCODING = 7     # P1:spectral_encoding


class ObjectSegregation(AppraisalBelief):
    """Appraisal belief: auditory scene segregation state.

    Measures how actively the auditory system is parsing the scene
    into distinct sound objects. High values = active segregation.

    Dependency: Requires IACM mechanism (Relay, Depth 0).
    """

    NAME = "object_segregation"
    FULL_NAME = "Object Segregation"
    FUNCTION = "F3"
    MECHANISM = "IACM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:spectral_encoding", 0.60),
        ("M2:object_perception_or", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe object segregation from IACM outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` IACM output tensor.

        Returns:
            ``(B, T)`` observed object segregation value.
        """
        return (
            0.60 * mechanism_output[:, :, _P1_SPECTRAL_ENCODING]
            + 0.40 * mechanism_output[:, :, _M2_OBJECT_PERCEPTION]
        )
