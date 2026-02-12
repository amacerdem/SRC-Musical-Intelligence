"""
MEAMN -- Music-Evoked Autobiographical Memory Network.

Alpha-1 model of the IMU (Integrative Memory Unit).  Models how music
uniquely activates autobiographical memory networks, engaging hippocampus,
mPFC, and temporal regions to retrieve personal memories with strong
emotional coloring.

Output: 12D per frame (172.27 Hz).
Mechanisms: MEM (Memory Encoding & Retrieval),
            TMH (Temporal Memory Hierarchy).
Evidence: Janata 2009, Neonatal care review (d=0.53 pooled).
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


class MEAMN(BaseModel):
    """Music-Evoked Autobiographical Memory Network -- music-triggered personal memories."""

    NAME = "MEAMN"
    FULL_NAME = "Music-Evoked Autobiographical Memory Network"
    UNIT = "IMU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("MEM", "TMH")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Episodic Memory Features", 0, 3, (
            "f01_retrieval", "f02_nostalgia", "f03_emotion",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "meam_retrieval", "p_recall",
        )),
        LayerSpec("P", "Present Processing", 5, 8, (
            "memory_state", "emotional_coloring", "nostalgia_link",
        )),
        LayerSpec("F", "Future Predictions", 8, 12, (
            "mem_vividness_fc", "emo_response_fc", "self_ref_fc", "reserved",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_retrieval", "f02_nostalgia", "f03_emotion",
            "meam_retrieval", "p_recall",
            "memory_state", "emotional_coloring", "nostalgia_link",
            "mem_vividness_fc", "emo_response_fc", "self_ref_fc", "reserved",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Hippocampus",
                abbreviation="HIP",
                hemisphere="bilateral",
                mni_coords=(20, -24, -12),
                function="Episodic encoding and autobiographical memory retrieval",
                evidence_count=8,
            ),
            BrainRegion(
                name="Medial Prefrontal Cortex",
                abbreviation="mPFC",
                hemisphere="bilateral",
                mni_coords=(0, 52, 12),
                function="Self-referential processing for personal memories",
                evidence_count=4,
            ),
            BrainRegion(
                name="Amygdala",
                abbreviation="AMY",
                hemisphere="bilateral",
                mni_coords=(24, -4, -20),
                function="Emotional tagging of autobiographical memories",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Janata", 2009,
                         "Neural architecture of music-evoked autobiographical memories",
                         ""),
                Citation("Neonatal care review", 2023,
                         "Music affects hippocampus, amygdala in neonatal care",
                         "scoping"),
                Citation("Context-dependent study", 2021,
                         "Multimodal integration in STS and hippocampus",
                         "d=0.17"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Hippocampal lesions should impair music-evoked autobiographical memory",
                "Novel music should not trigger autobiographical memories",
                "Emotional intensity should correlate with memory vividness",
            ),
            version="2.0.0",
            paper_count=6,
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
