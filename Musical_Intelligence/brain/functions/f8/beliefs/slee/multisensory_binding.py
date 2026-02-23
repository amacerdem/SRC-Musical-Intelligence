"""multisensory_binding -- Appraisal belief (SLEE, F8).

"The degree of multisensory integration and cross-modal binding
in statistical learning."

Observe: 0.60*f03:multisensory_integration + 0.40*P1:cross_modal_binding
No predict/update cycle.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/multisensory-binding.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SLEE output indices ---------------------------------------------------
_F03_MULTISENSORY_INTEGRATION = 2    # f03:multisensory_integration
_P1_CROSS_MODAL_BINDING = 8          # P1:cross_modal_binding


class MultisensoryBinding(AppraisalBelief):
    """Appraisal belief: multisensory integration in learning."""

    NAME = "multisensory_binding"
    FULL_NAME = "Multisensory Binding"
    FUNCTION = "F8"
    MECHANISM = "SLEE"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f03:multisensory_integration", 0.60),
        ("P1:cross_modal_binding", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe multisensory binding from SLEE output.

        Args:
            mechanism_output: ``(B, T, 13)`` SLEE output tensor.

        Returns:
            ``(B, T)`` observed multisensory binding.
        """
        return (
            0.60 * mechanism_output[:, :, _F03_MULTISENSORY_INTEGRATION]
            + 0.40 * mechanism_output[:, :, _P1_CROSS_MODAL_BINDING]
        )
