"""
MMP -- Musical Mnemonic Preservation.

Alpha-3 model of the IMU.  Models how musical memories are preferentially
preserved in neurodegenerative disease (Alzheimer's) due to distinct neural
substrates and reduced dependence on hippocampal integrity.  Has significant
clinical implications for dementia care.

Output: 12D per frame (172.27 Hz).
Mechanisms: MEM.
Evidence: Jacobsen 2015, Baird & Samson 2015.
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


class MMP(BaseModel):
    """Musical Mnemonic Preservation -- preserved memory in neurodegeneration."""

    NAME = "MMP"
    FULL_NAME = "Musical Mnemonic Preservation"
    UNIT = "IMU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("MEM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f01_preservation_index", "f02_hippocampal_independence",
            "f03_procedural_memory",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "preservation_score", "degradation_resistance",
        )),
        LayerSpec("P", "Present Processing", 5, 9, (
            "musical_recognition", "emotional_memory_intact",
            "procedural_pathway", "semantic_memory_state",
        )),
        LayerSpec("F", "Future Predictions", 9, 12, (
            "preservation_trajectory", "therapy_response_pred",
            "memory_resilience_fc",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_preservation_index", "f02_hippocampal_independence",
            "f03_procedural_memory",
            "preservation_score", "degradation_resistance",
            "musical_recognition", "emotional_memory_intact",
            "procedural_pathway", "semantic_memory_state",
            "preservation_trajectory", "therapy_response_pred",
            "memory_resilience_fc",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -6, 62),
                function="Procedural musical memory preserved in AD",
                evidence_count=3,
            ),
            BrainRegion(
                name="Cingulate Gyrus",
                abbreviation="CG",
                hemisphere="bilateral",
                mni_coords=(0, -10, 42),
                function="Musical memory regions showing reduced atrophy in AD",
                evidence_count=3,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(60, -32, 8),
                function="Preserved melodic recognition despite cortical atrophy",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Jacobsen", 2015,
                         "Musical memory regions show reduced atrophy in AD", ""),
                Citation("Baird", 2015,
                         "Music-evoked emotions preserved in dementia", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.95),
            falsification_criteria=(
                "Musical memory must be more preserved than verbal memory in AD",
                "SMA-related musical regions must show reduced atrophy",
            ),
            version="2.0.0",
            paper_count=5,
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
