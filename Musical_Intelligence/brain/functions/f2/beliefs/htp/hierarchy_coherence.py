"""hierarchy_coherence — Appraisal belief (HTP, F2).

"The hierarchical prediction structure is coherent."

Observe: 0.50*E3:hierarchy_gradient + 0.30*P2:abstract_prediction
         + 0.20*P1:pitch_prediction
No predict/update cycle.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/htp/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- HTP output indices (12D) -------------------------------------------------
_E3_HIERARCHY_GRADIENT = 3     # E3:hierarchy_gradient
_P1_PITCH_PREDICTION = 8      # P1:pitch_prediction
_P2_ABSTRACT_PREDICTION = 9   # P2:abstract_prediction


class HierarchyCoherence(AppraisalBelief):
    """Appraisal belief: hierarchical prediction coherence.

    Measures how coherently the hierarchical prediction structure is
    operating. High values indicate that all levels are producing
    consistent predictions with a clear gradient from abstract to sensory.
    Low values indicate incoherent or fragmented prediction.

    Dependency: Requires HTP mechanism (Relay, Depth 0, no upstream).
    """

    NAME = "hierarchy_coherence"
    FULL_NAME = "Hierarchy Coherence"
    FUNCTION = "F2"
    MECHANISM = "HTP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E3:hierarchy_gradient", 0.50),
        ("P2:abstract_prediction", 0.30),
        ("P1:pitch_prediction", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe hierarchy coherence from HTP outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` HTP output tensor.

        Returns:
            ``(B, T)`` observed hierarchy coherence value.
        """
        return (
            0.50 * mechanism_output[:, :, _E3_HIERARCHY_GRADIENT]
            + 0.30 * mechanism_output[:, :, _P2_ABSTRACT_PREDICTION]
            + 0.20 * mechanism_output[:, :, _P1_PITCH_PREDICTION]
        )
