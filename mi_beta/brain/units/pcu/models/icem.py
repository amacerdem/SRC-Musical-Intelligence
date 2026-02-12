"""
ICEM -- Imagery-Cognition Emotion Mapping.

Alpha-3 model of the PCU (Predictive Coding Unit).  Models how computational
Information Content (IC) peaks predict psychophysiological emotional responses:
high IC (unexpected) -> increased arousal, SCR; decreased HR, valence.

Output: 11D per frame (172.27 Hz).
Mechanisms: AED (Affective Entrainment Dynamics), C0P (C0 Projection).
Evidence: Egermann 2013 (n=48-50, p<0.001).
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


class ICEM(BaseModel):
    """Imagery-Cognition Emotion Mapping -- IC predicts emotional responses."""

    NAME = "ICEM"
    FULL_NAME = "Imagery-Cognition Emotion Mapping"
    UNIT = "PCU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("AED", "C0P")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_information_content", "f02_arousal_response",
            "f03_valence_response", "f04_defense_cascade",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "ic_neg_log2_p", "arousal_linear", "valence_linear",
        )),
        LayerSpec("P", "Present Processing", 7, 9, (
            "surprise_signal", "emotional_evaluation",
        )),
        LayerSpec("F", "Future Predictions", 9, 11, (
            "arousal_change_1_3s", "valence_shift_2_5s",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_information_content", "f02_arousal_response",
            "f03_valence_response", "f04_defense_cascade",
            # Layer M -- Mathematical
            "ic_neg_log2_p", "arousal_linear", "valence_linear",
            # Layer P -- Present
            "surprise_signal", "emotional_evaluation",
            # Layer F -- Future
            "arousal_change_1_3s", "valence_shift_2_5s",
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
                function="Emotional valence evaluation",
                evidence_count=3,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Information content computation",
                evidence_count=2,
            ),
            BrainRegion(
                name="Hippocampus",
                abbreviation="Hipp",
                hemisphere="bilateral",
                mni_coords=(28, -24, -12),
                function="Imagery-based emotional processing",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Egermann", 2013,
                         "IC peaks predict psychophysiological emotional responses",
                         "n=48-50"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Altering IC should change emotional responses proportionally",
                "Autonomic blockade should reduce SCR/HR effects",
                "Contextual priming should shift IC calculations",
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
