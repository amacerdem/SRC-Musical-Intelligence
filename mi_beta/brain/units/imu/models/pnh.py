"""
PNH -- Pythagorean Neural Hierarchy.

Alpha-2 model of the IMU.  Models how neural responses to musical intervals
follow the Pythagorean ratio complexity hierarchy, where simpler ratios
(more consonant) produce less activation in conflict-monitoring regions.

Output: 11D per frame (172.27 Hz).
Mechanisms: MEM.
Evidence: Bidelman & Krishnan 2009, Schellenberg & Trehub 1996.
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


class PNH(BaseModel):
    """Pythagorean Neural Hierarchy -- ratio complexity and neural response."""

    NAME = "PNH"
    FULL_NAME = "Pythagorean Neural Hierarchy"
    UNIT = "IMU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("MEM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f01_consonance_hierarchy", "f02_ratio_complexity",
            "f03_conflict_monitoring",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "pythagorean_index", "neural_complexity_score",
        )),
        LayerSpec("P", "Present Processing", 5, 8, (
            "interval_encoding", "harmonic_template_match", "ratio_recognition",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "consonance_expect", "interval_predict", "resolution_forecast",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_consonance_hierarchy", "f02_ratio_complexity",
            "f03_conflict_monitoring",
            "pythagorean_index", "neural_complexity_score",
            "interval_encoding", "harmonic_template_match", "ratio_recognition",
            "consonance_expect", "interval_predict", "resolution_forecast",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Heschl's Gyrus",
                abbreviation="HG",
                hemisphere="bilateral",
                mni_coords=(48, -18, 6),
                function="Frequency ratio processing and consonance encoding",
                evidence_count=4,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="right",
                mni_coords=(48, 18, 4),
                function="Conflict monitoring for complex frequency ratios",
                evidence_count=3,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(60, -32, 8),
                function="Harmonic template matching and interval categorization",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bidelman", 2009,
                         "Brainstem encoding follows Pythagorean interval hierarchy",
                         ""),
                Citation("Schellenberg", 1996,
                         "Natural frequency ratios and consonance preferences",
                         ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.95),
            falsification_criteria=(
                "Simpler ratios must produce less conflict-related neural activity",
                "Pythagorean hierarchy must predict behavioral consonance judgments",
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
