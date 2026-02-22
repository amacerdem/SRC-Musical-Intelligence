"""midlevel_future — Anticipation belief (HTP, F2).

"Upcoming mid-level features ~200ms ahead."

Observe: F1:midlevel_future_200ms (1.0) — HTP mid-level forecast.
No predict/update cycle. Feeds period_entrainment.predict() as context (F7).

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/htp/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- HTP output index ---------------------------------------------------------
_F1_MIDLEVEL_FUTURE = 11     # F1:midlevel_future_200ms


class MidlevelFuture(AnticipationBelief):
    """Anticipation belief: mid-level feature prediction ~200ms ahead.

    Forward prediction for mid-level perceptual features (pitch contour,
    timbral trajectory, spectral dynamics). Feeds motor prediction (F7)
    and attention (F3) as context.

    de Vries & Wurm 2023: view-dependent predictions at ~200ms.
    Norman-Haignere 2022: belt cortex integration windows 200-400ms.
    """

    NAME = "midlevel_future"
    FULL_NAME = "Midlevel Future"
    FUNCTION = "F2"
    MECHANISM = "HTP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:midlevel_future_200ms", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe midlevel future from HTP F1:midlevel_future_200ms.

        Args:
            mechanism_output: ``(B, T, 12)`` HTP output tensor.

        Returns:
            ``(B, T)`` forward mid-level feature prediction.
        """
        return mechanism_output[:, :, _F1_MIDLEVEL_FUTURE]
