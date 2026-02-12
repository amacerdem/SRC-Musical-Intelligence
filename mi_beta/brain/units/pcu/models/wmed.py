"""
WMED -- Working Memory Emotion Dynamics.

Beta-2 model of the PCU (Predictive Coding Unit).  Models how neural
entrainment and working memory contribute independently to rhythm production,
with a paradoxical finding that stronger entrainment to simple rhythms
predicts worse tapping performance.

Output: 10D per frame (172.27 Hz).
Mechanisms: MEM (Memory), AED (Affective Entrainment Dynamics).
Evidence: Noboa 2025 (n=30, p<0.006).
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


class WMED(BaseModel):
    """Working Memory Emotion Dynamics -- entrainment-WM dissociation."""

    NAME = "WMED"
    FULL_NAME = "Working Memory Emotion Dynamics"
    UNIT = "PCU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("MEM", "AED")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_entrainment_strength", "f02_wm_contribution",
            "f03_tapping_accuracy", "f04_dissociation_index",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "phase_locking_strength", "pattern_segmentation",
            "rhythmic_engagement",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "next_beat_pred", "tapping_accuracy_pred",
            "wm_interference_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_entrainment_strength", "f02_wm_contribution",
            "f03_tapping_accuracy", "f04_dissociation_index",
            # Layer P -- Present
            "phase_locking_strength", "pattern_segmentation",
            "rhythmic_engagement",
            # Layer F -- Future
            "next_beat_pred", "tapping_accuracy_pred",
            "wm_interference_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -4, 60),
                brodmann_area=6,
                function="Neural entrainment to rhythm",
                evidence_count=3,
            ),
            BrainRegion(
                name="Dorsolateral Prefrontal Cortex",
                abbreviation="dlPFC",
                hemisphere="bilateral",
                mni_coords=(-44, 36, 20),
                brodmann_area=46,
                function="Working memory for rhythm patterns",
                evidence_count=2,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Auditory temporal processing",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Noboa", 2025,
                         "Neural entrainment and working memory contributions to rhythm",
                         "n=30"),
            ),
            evidence_tier="beta",
            confidence_range=(0.72, 0.88),
            falsification_criteria=(
                "Stronger entrainment to simple rhythms must predict worse tapping",
                "Higher WM capacity must predict better tapping consistency",
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
