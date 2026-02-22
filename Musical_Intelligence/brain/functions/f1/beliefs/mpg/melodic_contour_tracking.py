"""melodic_contour_tracking — Appraisal belief (MPG, F1).

"The current melodic contour is being tracked with this level of
complexity and directional change."

Dependency chain:
    MPG (Depth 0, Relay) → melodic_contour_tracking
    Without MPG mechanism output, this belief cannot be computed.

Observe: 0.45×P1:contour_state + 0.30×E2:contour_complexity
         + 0.25×E1:sequence_anterior
No predict/update cycle.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/mpg/melodic_contour_tracking.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# ── MPG output indices (10D) ─────────────────────────────────────────
_E1_SEQUENCE_ANTERIOR = 1     # E1:sequence_anterior
_E2_CONTOUR_COMPLEXITY = 2    # E2:contour_complexity
_P1_CONTOUR_STATE = 8         # P1:contour_state


class MelodicContourTracking(AppraisalBelief):
    """Appraisal belief: melodic contour tracking quality.

    Measures how actively the anterior auditory cortex is processing
    melodic contour — high values indicate complex, changing melodies;
    low values indicate fixed-pitch or simple sequences.

    Dependency: Requires MPG mechanism (Relay, Depth 0, no upstream).
    """

    NAME = "melodic_contour_tracking"
    FULL_NAME = "Melodic Contour Tracking"
    FUNCTION = "F1"
    MECHANISM = "MPG"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:contour_state", 0.45),
        ("E2:contour_complexity", 0.30),
        ("E1:sequence_anterior", 0.25),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe melodic contour tracking from MPG outputs.

        Args:
            mechanism_output: ``(B, T, 10)`` MPG output tensor.

        Returns:
            ``(B, T)`` melodic contour tracking strength.
        """
        return (
            0.45 * mechanism_output[:, :, _P1_CONTOUR_STATE]
            + 0.30 * mechanism_output[:, :, _E2_CONTOUR_COMPLEXITY]
            + 0.25 * mechanism_output[:, :, _E1_SEQUENCE_ANTERIOR]
        )
