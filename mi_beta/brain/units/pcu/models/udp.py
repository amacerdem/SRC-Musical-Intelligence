"""
UDP -- Uncertainty-Driven Prediction.

Beta-3 model of the PCU (Predictive Coding Unit).  Models how in
high-uncertainty contexts (atonal music), correct predictions become more
rewarding than prediction errors, signaling model improvement and reduced
uncertainty.

Output: 10D per frame (172.27 Hz).
Mechanisms: C0P (C0 Projection).
Evidence: Mencke 2019 (theoretical + empirical).
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


class UDP(BaseModel):
    """Uncertainty-Driven Prediction -- confirmation reward in uncertainty."""

    NAME = "UDP"
    FULL_NAME = "Uncertainty-Driven Prediction"
    UNIT = "PCU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("C0P",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_uncertainty_level", "f02_confirmation_reward",
            "f03_error_reward", "f04_pleasure_index",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "context_assessment", "prediction_accuracy",
            "reward_computation",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "reward_expectation", "model_improvement",
            "pleasure_anticipation_1_3s",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_uncertainty_level", "f02_confirmation_reward",
            "f03_error_reward", "f04_pleasure_index",
            # Layer P -- Present
            "context_assessment", "prediction_accuracy",
            "reward_computation",
            # Layer F -- Future
            "reward_expectation", "model_improvement",
            "pleasure_anticipation_1_3s",
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
                function="Reward valuation under uncertainty",
                evidence_count=2,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Context uncertainty assessment",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Mencke", 2019,
                         "Correct predictions in high-uncertainty are more rewarding",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Tonal context: error must be more rewarding than confirmation",
                "Atonal context: confirmation must be more rewarding than error",
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
