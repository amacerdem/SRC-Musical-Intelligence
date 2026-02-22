"""chills_intensity — Appraisal belief (AAC, F5).

"Experiencing chills/frisson, intensity X."

Observe: I0:chills_intensity (1.0)
No predict/update cycle. Feeds F6 Reward (peak emotional marker).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- AAC output indices (14D) -------------------------------------------------
_I0_CHILLS_INTENSITY = 7      # I0:chills_intensity


class ChillsIntensity(AppraisalBelief):
    """Appraisal belief: chills/frisson intensity.

    Musical chills are peak emotional moments with co-activation of
    SCR (up) + HR (down) — Berntson's co-activation quadrant.

    Blood & Zatorre 2001: chills correlate with DA release in
    caudate and NAcc (PET, N=10).
    Dependency: Requires AAC mechanism (Relay, Depth 0).
    """

    NAME = "chills_intensity"
    FULL_NAME = "Chills Intensity"
    FUNCTION = "F5"
    MECHANISM = "AAC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("I0:chills_intensity", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe chills intensity from AAC outputs.

        Args:
            mechanism_output: ``(B, T, 14)`` AAC output tensor.

        Returns:
            ``(B, T)`` chills intensity value.
        """
        return mechanism_output[:, :, _I0_CHILLS_INTENSITY]
