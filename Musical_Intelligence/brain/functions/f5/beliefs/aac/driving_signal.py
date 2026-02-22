"""driving_signal — Anticipation belief (AAC, F5).

"Fast tempo driving ANS arousal."

Observe: P1:driving_signal (1.0)
No predict/update cycle. Feeds F7 Motor (tempo-driven entrainment).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- AAC output indices (14D) -------------------------------------------------
_P1_DRIVING_SIGNAL = 10       # P1:driving_signal


class DrivingSignal(AnticipationBelief):
    """Anticipation belief: tempo-driven ANS arousal prediction.

    Forward prediction of ANS entrainment from fast-tempo music.
    Feeds motor system preparation via F7.

    Dependency: Requires AAC mechanism (Relay, Depth 0).
    """

    NAME = "driving_signal"
    FULL_NAME = "Driving Signal"
    FUNCTION = "F5"
    MECHANISM = "AAC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:driving_signal", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe driving signal from AAC outputs.

        Args:
            mechanism_output: ``(B, T, 14)`` AAC output tensor.

        Returns:
            ``(B, T)`` driving signal value.
        """
        return mechanism_output[:, :, _P1_DRIVING_SIGNAL]
