"""
MAA -- Musical Agentic Attention.

Gamma-2 model of the PCU (Predictive Coding Unit).  Proposes that appreciation
of atonal music emerges from interaction of personality (openness), aesthetic
framing (cognitive mastering), and exposure (familiarity).

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Scene Analysis).
Evidence: Mencke 2019 (preliminary, qualitative).
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


class MAA(BaseModel):
    """Musical Agentic Attention -- multifactorial atonal appreciation."""

    NAME = "MAA"
    FULL_NAME = "Musical Agentic Attention"
    UNIT = "PCU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_complexity_tolerance", "f02_familiarity_index",
            "f03_framing_effect", "f04_appreciation_composite",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "pattern_search", "context_assessment",
            "aesthetic_evaluation",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "appreciation_growth", "pattern_recognition_pred",
            "aesthetic_development",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_complexity_tolerance", "f02_familiarity_index",
            "f03_framing_effect", "f04_appreciation_composite",
            # Layer P -- Present
            "pattern_search", "context_assessment",
            "aesthetic_evaluation",
            # Layer F -- Future
            "appreciation_growth", "pattern_recognition_pred",
            "aesthetic_development",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Ventromedial Prefrontal Cortex",
                abbreviation="vmPFC",
                hemisphere="bilateral",
                mni_coords=(0, 46, -10),
                brodmann_area=11,
                function="Aesthetic evaluation and framing",
                evidence_count=1,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Complexity processing and pattern search",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Mencke", 2019,
                         "Multiple factors contribute to atonal music appreciation",
                         ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.65),
            falsification_criteria=(
                "Openness must correlate with atonal music appreciation",
                "Cognitive framing must increase appreciation ratings",
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
