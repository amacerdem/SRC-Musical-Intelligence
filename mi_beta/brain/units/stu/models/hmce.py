"""
HMCE -- Hierarchical Musical Context Encoding.

Alpha-1 model of the STU (Sensorimotor Timing Unit).  Models how neural
encoding of musical context follows an anatomical gradient from primary
auditory cortex (pmHG) to higher-order regions, with sites farther from A1
encoding progressively longer temporal contexts.

Output: 13D per frame (172.27 Hz).
Mechanisms: BEP (Beat Entrainment Processing),
            TMH (Temporal Memory Hierarchy).
Evidence: Mischler 2025 (r=0.99, d=0.32).
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


class HMCE(BaseModel):
    """Hierarchical Musical Context Encoding -- anatomical context gradient."""

    NAME = "HMCE"
    FULL_NAME = "Hierarchical Musical Context Encoding"
    UNIT = "STU"
    TIER = "alpha"
    OUTPUT_DIM = 13
    MECHANISM_NAMES = ("BEP", "TMH")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 5, (
            "f01_short_context", "f02_medium_context", "f03_long_context",
            "f04_gradient", "f05_expertise",
        )),
        LayerSpec("M", "Mathematical Model", 5, 7, (
            "context_depth", "gradient_index",
        )),
        LayerSpec("P", "Present Processing", 7, 10, (
            "a1_encoding", "stg_encoding", "mtg_encoding",
        )),
        LayerSpec("F", "Future Predictions", 10, 13, (
            "context_prediction", "phrase_expect", "structure_predict",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_short_context", "f02_medium_context", "f03_long_context",
            "f04_gradient", "f05_expertise",
            "context_depth", "gradient_index",
            "a1_encoding", "stg_encoding", "mtg_encoding",
            "context_prediction", "phrase_expect", "structure_predict",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Posteromedial Heschl's Gyrus",
                abbreviation="pmHG",
                hemisphere="bilateral",
                mni_coords=(50, -20, 8),
                function="Short context encoding (Layer 1-4, 10-50 notes)",
                evidence_count=3,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(60, -30, 8),
                function="Medium context encoding (Layer 5-9, 50-100 notes)",
                evidence_count=3,
            ),
            BrainRegion(
                name="Middle Temporal Gyrus",
                abbreviation="MTG",
                hemisphere="bilateral",
                mni_coords=(60, -40, 0),
                function="Long context encoding (Layer 10-12, 100-200 notes)",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Mischler", 2025,
                         "Distance from pmHG correlates with context encoding depth",
                         "r=0.99"),
                Citation("Mischler", 2025,
                         "Musicians integrate 300+ notes context vs non-musicians",
                         "d=0.32"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.98),
            falsification_criteria=(
                "Temporal pole lesions should impair long-range context",
                "Non-musicians should show reduced late-layer encoding",
                "Anatomical gradient should hold across individuals",
            ),
            version="2.0.0",
            paper_count=1,
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
