"""sensory_load — Appraisal belief (CSG cross-function, F3).

"Processing resource demand is high/low."

Observe: 0.60*P2:sensory_load + 0.40*E1:sensory_evidence
No predict/update cycle. Feeds F8 Learning (load-adjusted learning rate).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- CSG output indices (12D) -------------------------------------------------
_E1_SENSORY_EVIDENCE = 1       # E1:sensory_evidence
_P2_SENSORY_LOAD = 8           # P2:sensory_load


class SensoryLoad(AppraisalBelief):
    """Appraisal belief: sensory processing load.

    Measures current processing resource demand. High values
    indicate heavy sensory load (complex/ambiguous consonance).

    CSG is F1-primary; this belief is cross-function to F3.
    Dependency: Requires CSG mechanism (Relay, Depth 0, F1).
    """

    NAME = "sensory_load"
    FULL_NAME = "Sensory Load"
    FUNCTION = "F3"
    MECHANISM = "CSG"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P2:sensory_load", 0.60),
        ("E1:sensory_evidence", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe sensory load from CSG outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` CSG output tensor.

        Returns:
            ``(B, T)`` observed sensory load value.
        """
        return (
            0.60 * mechanism_output[:, :, _P2_SENSORY_LOAD]
            + 0.40 * mechanism_output[:, :, _E1_SENSORY_EVIDENCE]
        )
