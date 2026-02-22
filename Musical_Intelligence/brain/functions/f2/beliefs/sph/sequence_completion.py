"""sequence_completion — Anticipation belief (SPH, F2).

"The current sequence is approaching completion."

Observe: F1:sequence_completion_2s (1.0) — SPH cingulate boundary forecast.
No predict/update cycle. Feeds F4 Memory and F8 Learning as context.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/sph/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- SPH output index ---------------------------------------------------------
_F1_SEQUENCE_COMPLETION = 12     # F1:sequence_completion_2s


class SequenceCompletion(AnticipationBelief):
    """Anticipation belief: sequence completion prediction.

    Forward prediction for whether the current auditory sequence is
    approaching a structural boundary or completion point. Based on
    long-range tonal stability, spectral coupling, and chroma context.

    Feeds into memory encoding (F4) — sequence boundaries trigger
    consolidation, and learning (F8) — boundary detection resets
    statistical models.

    Bonetti et al. 2024: cingulate assumes top position at final tone,
    indicating sequence evaluation/completion.
    Rimmele et al. 2021: delta oscillations underpin phrase-level chunking.
    """

    NAME = "sequence_completion"
    FULL_NAME = "Sequence Completion"
    FUNCTION = "F2"
    MECHANISM = "SPH"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:sequence_completion_2s", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe sequence completion from SPH F1:sequence_completion_2s.

        Args:
            mechanism_output: ``(B, T, 14)`` SPH output tensor.

        Returns:
            ``(B, T)`` forward sequence completion prediction.
        """
        return mechanism_output[:, :, _F1_SEQUENCE_COMPLETION]
