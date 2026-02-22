"""octave_equivalence — Appraisal belief (PCCR, F1).

"Tones separated by octaves are perceived as belonging to the same
chroma class."

Dependency chain:
    BCH (Depth 0) → PSCL (Depth 1) → PCCR (Depth 2) → octave_equivalence
    Without PCCR mechanism output, this belief cannot be computed.
    PCCR.P1 internally reads BCH.E1:harmonicity (critical for OE).

Observe: P1:octave_equivalence_index (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/pccr/octave_equivalence.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# ── PCCR output index (11D) ─────────────────────────────────────────
_P1_OCTAVE_EQUIV = 6          # P1:octave_equivalence_index


class OctaveEquivalence(AppraisalBelief):
    """Appraisal belief: octave-invariant chroma encoding quality.

    Dependency: Requires PCCR mechanism (which requires BCH → PSCL → PCCR).
    BCH.E1:harmonicity feeds PCCR.P1 with 25% weight — harmonic sounds
    have stronger octave equivalence.
    """

    NAME = "octave_equivalence"
    FULL_NAME = "Octave Equivalence"
    FUNCTION = "F1"
    MECHANISM = "PCCR"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P1:octave_equivalence_index", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe octave equivalence from PCCR P1:octave_equivalence_index.

        Args:
            mechanism_output: ``(B, T, 11)`` PCCR output tensor.

        Returns:
            ``(B, T)`` octave equivalence strength.
        """
        return mechanism_output[:, :, _P1_OCTAVE_EQUIV]
