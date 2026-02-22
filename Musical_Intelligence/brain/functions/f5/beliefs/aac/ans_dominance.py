"""ans_dominance — Appraisal belief (AAC, F5).

"Sympathetic/parasympathetic dominance."

Observe: E1:ans_response (1.0)
No predict/update cycle. Feeds F7 Motor (autonomic modulation).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- AAC output indices (14D) -------------------------------------------------
_E1_ANS_RESPONSE = 1          # E1:ans_response


class AnsDominance(AppraisalBelief):
    """Appraisal belief: ANS sympathetic/parasympathetic dominance.

    High = sympathetic dominant (aroused), low = parasympathetic (calm).
    Berntson 1991: autonomic space is 2D (SNS × PNS).

    Dependency: Requires AAC mechanism (Relay, Depth 0).
    """

    NAME = "ans_dominance"
    FULL_NAME = "ANS Dominance"
    FUNCTION = "F5"
    MECHANISM = "AAC"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E1:ans_response", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe ANS dominance from AAC outputs.

        Args:
            mechanism_output: ``(B, T, 14)`` AAC output tensor.

        Returns:
            ``(B, T)`` ANS dominance value.
        """
        return mechanism_output[:, :, _E1_ANS_RESPONSE]
