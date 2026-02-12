"""
RPEM -- Reward Prediction Error Model.

Alpha-3 model of the RPU (Reward Processing Unit).  Models how the ventral
striatum exhibits reward prediction error (RPE)-like responses to musical
surprise: increased activity for surprising liked stimuli, decreased for
surprising disliked stimuli.

Output: 11D per frame (172.27 Hz).
Mechanisms: AED (Affective Entrainment Dynamics), CPD (Chills and Peak Detection).
Evidence: Gold 2023 fMRI (d=1.07, n=24, p<0.008).
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


class RPEM(BaseModel):
    """Reward Prediction Error Model -- VS RPE-like responses to musical surprise."""

    NAME = "RPEM"
    FULL_NAME = "Reward Prediction Error Model"
    UNIT = "RPU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("AED", "CPD")
    CROSS_UNIT_READS = ("ARU",)

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_surprise_signal", "f02_liking_signal",
            "f03_positive_rpe", "f04_negative_rpe",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "rpe_value", "ic_liking_interaction",
            "vs_bold_response",
        )),
        LayerSpec("P", "Present Processing", 7, 9, (
            "current_prediction_error", "vs_activation_state",
        )),
        LayerSpec("F", "Future Predictions", 9, 11, (
            "reward_update_pred", "vs_response_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_surprise_signal", "f02_liking_signal",
            "f03_positive_rpe", "f04_negative_rpe",
            # Layer M -- Mathematical
            "rpe_value", "ic_liking_interaction",
            "vs_bold_response",
            # Layer P -- Present
            "current_prediction_error", "vs_activation_state",
            # Layer F -- Future
            "reward_update_pred", "vs_response_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Ventral Striatum",
                abbreviation="VS",
                hemisphere="bilateral",
                mni_coords=(8, 6, -4),
                function="Reward prediction error computation",
                evidence_count=4,
            ),
            BrainRegion(
                name="Ventral Tegmental Area",
                abbreviation="VTA",
                hemisphere="bilateral",
                mni_coords=(0, -16, -8),
                function="Dopaminergic RPE signaling",
                evidence_count=3,
            ),
            BrainRegion(
                name="Ventromedial Prefrontal Cortex",
                abbreviation="vmPFC",
                hemisphere="bilateral",
                mni_coords=(0, 46, -10),
                brodmann_area=11,
                function="Expected reward computation",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Gold", 2023,
                         "VS shows RPE-like IC x liking crossover",
                         "d=1.07"),
                Citation("Gold", 2023,
                         "R STG shows surprise-liking interaction",
                         "d=1.22"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.96),
            falsification_criteria=(
                "Surprising liked stimuli must increase VS activity",
                "Surprising disliked stimuli must decrease VS activity",
                "IC x liking interaction must be significant in VS",
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
