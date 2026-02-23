"""harmonic_tension — Appraisal belief (SRP, F6).

"Harmonic tension level in the current musical context."

Observe: M0:harmonic_tension (1.0) — direct mechanism output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/harmonic-tension.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SRP output index -------------------------------------------------------
_M0_HARMONIC_TENSION = 10


class HarmonicTension(AppraisalBelief):
    """Appraisal belief: harmonic tension level."""

    NAME = "harmonic_tension"
    FULL_NAME = "Harmonic Tension"
    FUNCTION = "F6"
    MECHANISM = "SRP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("M0:harmonic_tension", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe harmonic tension from SRP M0:harmonic_tension.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` harmonic tension value.
        """
        return mechanism_output[:, :, _M0_HARMONIC_TENSION]
