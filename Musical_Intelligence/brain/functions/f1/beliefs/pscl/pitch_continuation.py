"""pitch_continuation — Anticipation belief (PSCL, F1).

"Next event will contain a prominent pitch."

Observe: F0:pitch_continuation (1.0) — PSCL trend extrapolation.
No predict/update cycle. Feeds pitch_prominence.predict() as context.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/pitch-continuation.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# ── PSCL output index ───────────────────────────────────────────────
_F0_PITCH_CONTINUATION = 12


class PitchContinuation(AnticipationBelief):
    """Anticipation belief: pitch presence trend extrapolation."""

    NAME = "pitch_continuation"
    FULL_NAME = "Pitch Continuation"
    FUNCTION = "F1"
    MECHANISM = "PSCL"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F0:pitch_continuation", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe pitch continuation from PSCL F0:pitch_continuation.

        Args:
            mechanism_output: ``(B, T, 16)`` PSCL output tensor.

        Returns:
            ``(B, T)`` forward pitch trend.
        """
        return mechanism_output[:, :, _F0_PITCH_CONTINUATION]
