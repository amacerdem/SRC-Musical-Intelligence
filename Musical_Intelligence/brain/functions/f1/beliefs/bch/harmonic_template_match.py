"""harmonic_template_match — Appraisal belief (BCH, F1).

"The partials of this sound fit a harmonic series template."

Observe: P1:template_match (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/harmonic-template-match.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# ── BCH output index ────────────────────────────────────────────────
_P1_TEMPLATE = 9


class HarmonicTemplateMatch(AppraisalBelief):
    """Appraisal belief: harmonic template structural fit."""

    NAME = "harmonic_template_match"
    FULL_NAME = "Harmonic Template Match"
    FUNCTION = "F1"
    MECHANISM = "BCH"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:template_match", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe harmonic template match from BCH P1:template_match.

        Args:
            mechanism_output: ``(B, T, 16)`` BCH output tensor.

        Returns:
            ``(B, T)`` template alignment value.
        """
        return mechanism_output[:, :, _P1_TEMPLATE]
