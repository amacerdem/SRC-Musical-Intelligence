"""beat_prominence — Appraisal belief (HGSIC, F7).

"Beat events are prominent in the auditory scene."

Observe: 0.50*f01:beat_gamma + 0.50*pstg_activation
No predict/update cycle.

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/beat-prominence.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HGSIC output indices (11D) -----------------------------------------------
_F01_BEAT_GAMMA = 0            # f01:beat_gamma
_PSTG_ACTIVATION = 5           # pstg_activation


class BeatProminence(AppraisalBelief):
    """Appraisal belief: beat prominence.

    Measures how salient and prominent beat events are in the
    auditory scene. High values indicate clear, prominent beats.
    Low values indicate weak or ambiguous beats.

    Dependency: Requires HGSIC mechanism (Relay, Depth 0).
    """

    NAME = "beat_prominence"
    FULL_NAME = "Beat Prominence"
    FUNCTION = "F7"
    MECHANISM = "HGSIC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f01:beat_gamma", 0.50),
        ("pstg_activation", 0.50),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe beat prominence from HGSIC outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` HGSIC output tensor.

        Returns:
            ``(B, T)`` observed beat prominence value.
        """
        return (
            0.50 * mechanism_output[:, :, _F01_BEAT_GAMMA]
            + 0.50 * mechanism_output[:, :, _PSTG_ACTIVATION]
        )
