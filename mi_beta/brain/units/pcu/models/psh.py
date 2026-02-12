"""
PSH -- Perceptual Salience Hierarchy.

Gamma-3 model of the PCU (Predictive Coding Unit).  Proposes that accurate
top-down predictions "silence" (explain away) high-level stimulus
representations post-stimulus, while low-level representations persist.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Scene Analysis).
Evidence: de Vries 2023 (n=22, p<0.01, preliminary).
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


class PSH(BaseModel):
    """Perceptual Salience Hierarchy -- prediction silencing hypothesis."""

    NAME = "PSH"
    FULL_NAME = "Perceptual Salience Hierarchy"
    UNIT = "PCU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_high_level_silencing", "f02_low_level_persistence",
            "f03_silencing_efficiency", "f04_hierarchy_dissociation",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "prediction_match", "sensory_persistence",
            "binding_check",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "post_stim_silencing_500ms", "error_persistence_500ms",
            "next_prediction_pre_stim",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_high_level_silencing", "f02_low_level_persistence",
            "f03_silencing_efficiency", "f04_hierarchy_dissociation",
            # Layer P -- Present
            "prediction_match", "sensory_persistence",
            "binding_check",
            # Layer F -- Future
            "post_stim_silencing_500ms", "error_persistence_500ms",
            "next_prediction_pre_stim",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Low-level persistence (error signal)",
                evidence_count=2,
            ),
            BrainRegion(
                name="Dorsolateral Prefrontal Cortex",
                abbreviation="dlPFC",
                hemisphere="bilateral",
                mni_coords=(-44, 36, 20),
                brodmann_area=46,
                function="High-level silencing (explaining away)",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("de Vries", 2023,
                         "High-level lagged representations absent post-stimulus",
                         "n=22"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.65),
            falsification_criteria=(
                "High-level representations must be silenced post-stimulus",
                "Low-level representations must persist post-stimulus",
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
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
