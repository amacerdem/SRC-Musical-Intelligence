"""nostalgia_peak_pred — Anticipation belief (NEMAC, F5).

"Nostalgic peak moment approaching."

Observe: F1:vividness_pred (1.0)
No predict/update cycle. Feeds precision engine (pi_pred for nostalgia).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- NEMAC output indices (11D) ------------------------------------------------
_F1_VIVIDNESS_PRED = 10        # F1:vividness_pred


class NostalgiaPeakPred(AnticipationBelief):
    """Anticipation belief: nostalgia peak prediction.

    Forward prediction of upcoming nostalgic peak moment.
    Feeds precision engine for nostalgia-related predictions.

    Dependency: Requires NEMAC mechanism (Encoder, Depth 1).
    """

    NAME = "nostalgia_peak_pred"
    FULL_NAME = "Nostalgia Peak Prediction"
    FUNCTION = "F5"
    MECHANISM = "NEMAC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:vividness_pred", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe nostalgia peak prediction from NEMAC outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` NEMAC output tensor.

        Returns:
            ``(B, T)`` nostalgia peak prediction value.
        """
        return mechanism_output[:, :, _F1_VIVIDNESS_PRED]
