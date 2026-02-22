"""selective_gain — Appraisal belief (SNEM, F3).

"Attention-gated amplification: beat-frequency signals are boosted."

Observe: P2:selective_gain (1.0) — direct from SNEM.
No predict/update cycle. Feeds kernel salience mixer as multiplicative gate.
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SNEM output index --------------------------------------------------------
_P2_SELECTIVE_GAIN = 8         # P2:selective_gain


class SelectiveGain(AppraisalBelief):
    """Appraisal belief: attention-gated selective gain.

    Measures how strongly beat-locked oscillations amplify on-beat events.
    Used as multiplicative gate in kernel salience mixer:
    salience *= 1 + 0.3 × selective_gain.

    Dependency: Requires SNEM mechanism (Relay, Depth 0).
    """

    NAME = "selective_gain"
    FULL_NAME = "Selective Gain"
    FUNCTION = "F3"
    MECHANISM = "SNEM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P2:selective_gain", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe selective gain from SNEM P2:selective_gain.

        Args:
            mechanism_output: ``(B, T, 12)`` SNEM output tensor.

        Returns:
            ``(B, T)`` selective gain value.
        """
        return mechanism_output[:, :, _P2_SELECTIVE_GAIN]
