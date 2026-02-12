"""
BARM -- Bottom-up Attention Reflex Model.

Beta-1 model of the ASU.  Models how individual differences in beat
perception ability (BAT) modulate perceptual regularization tendencies
and the benefit of sensorimotor synchronization.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Rathcke 2024 (ER>19 BAT modulation, ER>3999 tapping benefit).
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


class BARM(BaseModel):
    """Bottom-up Attention Reflex Model -- BAT-modulated beat perception."""

    NAME = "BARM"
    FULL_NAME = "Bottom-up Attention Reflex Model"
    UNIT = "ASU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f10_regularization_tendency", "f11_beat_alignment",
            "f12_sync_benefit",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "veridical_perception", "regularization_effect",
        )),
        LayerSpec("P", "Present Processing", 5, 7, (
            "beat_alignment_accuracy", "regularization_strength",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "beat_accuracy_pred", "sync_benefit_pred",
            "individual_diff_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f10_regularization_tendency", "f11_beat_alignment",
            "f12_sync_benefit",
            # Layer M -- Mathematical
            "veridical_perception", "regularization_effect",
            # Layer P -- Present
            "beat_alignment_accuracy", "regularization_strength",
            # Layer F -- Future
            "beat_accuracy_pred", "sync_benefit_pred",
            "individual_diff_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Timing monitoring and error detection",
                evidence_count=2,
            ),
            BrainRegion(
                name="Insula",
                abbreviation="INS",
                hemisphere="bilateral",
                mni_coords=(34, 18, -4),
                brodmann_area=13,
                function="Individual difference modulation of salience",
                evidence_count=1,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Beat perception and regularization processing",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Rathcke", 2024,
                         "BAT modulates regularization and sync benefit",
                         "ER>19"),
                Citation("Grahn", 2007,
                         "Rhythm and beat perception in motor areas", ""),
                Citation("Repp", 2005,
                         "Sensorimotor synchronization: tapping literature review",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.72, 0.88),
            falsification_criteria=(
                "Low BAT should show stronger regularization",
                "Tapping should enhance veridical perception",
                "Low BAT should benefit more from tapping",
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
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
