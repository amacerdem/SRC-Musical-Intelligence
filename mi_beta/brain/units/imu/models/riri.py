"""
RIRI -- Recognition-Recall Integration Recency Index.

Beta-5 model of the IMU.  Models the integration of recognition and recall
processes with recency effects, where RAS-intelligent rehabilitation
creates closed-loop adaptive therapy through multisensory integration
and temporal coherence.

Output: 10D per frame (172.27 Hz).
Mechanisms: MEM.
Evidence: Dowling 2008, Dalla Bella 2009.
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


class RIRI(BaseModel):
    """Recognition-Recall Integration Recency Index -- recognition vs recall dynamics."""

    NAME = "RIRI"
    FULL_NAME = "Recognition-Recall Integration Recency Index"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("MEM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_recognition_strength", "f02_recall_capacity",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "recency_index", "recognition_recall_ratio",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "familiarity_signal", "recollection_signal", "recency_weight",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "recognition_decay_pred", "recall_probability_fc",
            "recency_shift_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_recognition_strength", "f02_recall_capacity",
            "recency_index", "recognition_recall_ratio",
            "familiarity_signal", "recollection_signal", "recency_weight",
            "recognition_decay_pred", "recall_probability_fc",
            "recency_shift_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Hippocampus",
                abbreviation="HIP",
                hemisphere="bilateral",
                mni_coords=(20, -24, -12),
                function="Recollection-based recall of musical sequences",
                evidence_count=3,
            ),
            BrainRegion(
                name="Perirhinal Cortex",
                abbreviation="PRC",
                hemisphere="bilateral",
                mni_coords=(30, -10, -30),
                function="Familiarity-based recognition without recall",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Dowling", 2008,
                         "Recognition and recall in musical memory", ""),
                Citation("Dalla Bella", 2009,
                         "Memory for musical sequences: recency effects", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Recognition must dissociate from recall for unfamiliar music",
                "Recency effects must scale with temporal distance",
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
