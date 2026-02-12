"""
CDEM -- Context-Dependent Emotional Memory.

Gamma-3 model of the IMU.  Models how musical emotional memories are
context-dependent, with cross-modal information (visual, tactile) modulating
encoding and retrieval strength.

Output: 10D per frame (172.27 Hz).
Mechanisms: MEM.
Evidence: Context-dependent study 2021 (d=0.17), Eschrich 2008.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import (
    BaseModel,
    BrainRegion,
    Citation,
    LayerSpec,
    ModelMetadata,
)


class CDEM(BaseModel):
    """Context-Dependent Emotional Memory -- cross-modal memory modulation."""

    NAME = "CDEM"
    FULL_NAME = "Context-Dependent Emotional Memory"
    UNIT = "IMU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("MEM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_context_modulation", "f02_emotional_encoding",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "context_dependency_index", "cross_modal_enhancement",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "emotional_state", "context_match", "encoding_strength",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "retrieval_context_pred", "emotional_decay_fc",
            "recontextualization_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_context_modulation", "f02_emotional_encoding",
            "context_dependency_index", "cross_modal_enhancement",
            "emotional_state", "context_match", "encoding_strength",
            "retrieval_context_pred", "emotional_decay_fc",
            "recontextualization_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Hippocampus",
                abbreviation="HIP",
                hemisphere="bilateral",
                mni_coords=(20, -24, -12),
                function="Context-dependent encoding and retrieval of emotional memories",
                evidence_count=2,
            ),
            BrainRegion(
                name="Amygdala",
                abbreviation="AMY",
                hemisphere="bilateral",
                mni_coords=(24, -4, -20),
                function="Emotional tagging modulated by cross-modal context",
                evidence_count=2,
            ),
            BrainRegion(
                name="Superior Temporal Sulcus",
                abbreviation="STS",
                hemisphere="bilateral",
                mni_coords=(56, -36, 4),
                function="Multimodal integration for context-dependent memory",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Context-dependent study", 2021,
                         "Multimodal integration in STS and hippocampus",
                         "d=0.17"),
                Citation("Eschrich", 2008,
                         "Emotional context modulates musical memory encoding", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Same-context retrieval must outperform different-context retrieval",
                "Cross-modal information must enhance encoding strength",
            ),
            version="2.0.0",
            paper_count=3,
        )

    def compute(
        self,
        mechanism_outputs: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Stub -- returns zeros of correct shape."""
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
