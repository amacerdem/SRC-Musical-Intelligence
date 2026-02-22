"""contour_continuation — Anticipation belief (MPG, F1).

"The melodic contour will continue / a phrase boundary is approaching."

Dependency chain:
    MPG (Depth 0, Relay) → contour_continuation
    Without MPG mechanism output, this belief cannot be computed.

Observe: F0:phrase_boundary_pred (1.0) — MPG forecast output.
No predict/update cycle. Feeds Core beliefs' predict() methods as context.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/mpg/contour_continuation.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# ── MPG output index ─────────────────────────────────────────────────
_F0_PHRASE_BOUNDARY = 9       # F0:phrase_boundary_pred


class ContourContinuation(AnticipationBelief):
    """Anticipation belief: melodic contour continuation/boundary prediction.

    High values indicate an approaching phrase boundary; low values
    indicate the current contour will continue. Feeds into Core beliefs
    (e.g., pitch_identity.predict()) as forward-looking context.

    Dependency: Requires MPG mechanism (Relay, Depth 0, no upstream).
    """

    NAME = "contour_continuation"
    FULL_NAME = "Contour Continuation"
    FUNCTION = "F1"
    MECHANISM = "MPG"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F0:phrase_boundary_pred", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe contour continuation from MPG F0:phrase_boundary_pred.

        Args:
            mechanism_output: ``(B, T, 10)`` MPG output tensor.

        Returns:
            ``(B, T)`` phrase boundary prediction strength.
        """
        return mechanism_output[:, :, _F0_PHRASE_BOUNDARY]
