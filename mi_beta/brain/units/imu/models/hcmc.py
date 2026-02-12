"""
HCMC -- Hippocampal-Cortical Memory Consolidation.

Beta-4 model of the IMU.  Models how musical memory is mediated by a core
hippocampal-cortical circuit, with temporal encoding in hippocampus and
long-term storage in cortical networks.

Output: 11D per frame (172.27 Hz).
Mechanisms: MEM.
Evidence: Watanabe 2008, Albouy 2017.
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


class HCMC(BaseModel):
    """Hippocampal-Cortical Memory Consolidation -- musical memory circuit."""

    NAME = "HCMC"
    FULL_NAME = "Hippocampal-Cortical Memory Consolidation"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("MEM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_encoding_strength", "f02_consolidation_state",
        )),
        LayerSpec("M", "Mathematical Model", 2, 5, (
            "hippocampal_binding", "cortical_transfer", "consolidation_index",
        )),
        LayerSpec("P", "Present Processing", 5, 8, (
            "encoding_state", "replay_activity", "storage_phase",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "consolidation_forecast", "retrieval_readiness", "decay_prediction",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_encoding_strength", "f02_consolidation_state",
            "hippocampal_binding", "cortical_transfer", "consolidation_index",
            "encoding_state", "replay_activity", "storage_phase",
            "consolidation_forecast", "retrieval_readiness", "decay_prediction",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Hippocampus",
                abbreviation="HIP",
                hemisphere="bilateral",
                mni_coords=(20, -24, -12),
                function="Rapid encoding and temporal binding of musical sequences",
                evidence_count=4,
            ),
            BrainRegion(
                name="Auditory Cortex",
                abbreviation="AC",
                hemisphere="bilateral",
                mni_coords=(-54, -22, 8),
                function="Long-term cortical storage of musical representations",
                evidence_count=3,
            ),
            BrainRegion(
                name="Medial Prefrontal Cortex",
                abbreviation="mPFC",
                hemisphere="bilateral",
                mni_coords=(0, 52, 12),
                function="Schema-based consolidation and retrieval organization",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Watanabe", 2008,
                         "Hippocampal involvement in musical memory encoding", ""),
                Citation("Albouy", 2017,
                         "Hippocampus and auditory memory consolidation", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.88),
            falsification_criteria=(
                "Hippocampal lesions must impair new musical memory formation",
                "Consolidation must show time-dependent cortical transfer",
            ),
            version="2.0.0",
            paper_count=4,
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
