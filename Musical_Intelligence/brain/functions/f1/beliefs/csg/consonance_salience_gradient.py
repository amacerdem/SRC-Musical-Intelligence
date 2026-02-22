"""consonance_salience_gradient — Appraisal belief (CSG, F1).

"The current consonance level is modulating salience network activation."

Dependency chain:
    CSG (Depth 0, Relay) -> consonance_salience_gradient
    Without CSG mechanism output, this belief cannot be computed.

Observe: 0.40*P0:salience_network + 0.30*E0:salience_activation
         + 0.30*M0:salience_response
No predict/update cycle.

See Building/C3-Brain/F1-Sensory-Processing/beliefs/csg/consonance_salience_gradient.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- CSG output indices (12D) -------------------------------------------------
_E0_SALIENCE_ACTIVATION = 0    # E0:salience_activation
_M0_SALIENCE_RESPONSE = 3      # M0:salience_response
_P0_SALIENCE_NETWORK = 6       # P0:salience_network


class ConsonanceSalienceGradient(AppraisalBelief):
    """Appraisal belief: consonance-salience gradient assessment.

    Measures how strongly the current consonance/dissonance level is
    driving salience network activation. High values indicate strong
    dissonance-driven ACC/AI activation or high processing demand.
    Low values indicate consonant input with efficient processing.

    Dependency: Requires CSG mechanism (Relay, Depth 0, no upstream).
    """

    NAME = "consonance_salience_gradient"
    FULL_NAME = "Consonance-Salience Gradient"
    FUNCTION = "F1"
    MECHANISM = "CSG"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:salience_network", 0.40),
        ("E0:salience_activation", 0.30),
        ("M0:salience_response", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe consonance-salience gradient from CSG outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` CSG output tensor.

        Returns:
            ``(B, T)`` observed consonance-salience gradient value.
        """
        return (
            0.40 * mechanism_output[:, :, _P0_SALIENCE_NETWORK]
            + 0.30 * mechanism_output[:, :, _E0_SALIENCE_ACTIVATION]
            + 0.30 * mechanism_output[:, :, _M0_SALIENCE_RESPONSE]
        )
