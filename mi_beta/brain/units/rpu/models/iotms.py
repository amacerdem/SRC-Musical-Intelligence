"""
IOTMS -- Individual Optimal Tempo Matching System.

Gamma-2 model of the RPU (Reward Processing Unit).  Proposes that individual
differences in baseline mu-opioid receptor (MOR) availability explain
individual differences in music reward propensity.

Output: 10D per frame (172.27 Hz).
Mechanisms: BEP (Beat Entrainment Processing).
Evidence: Putkinen 2025 (preliminary PET, individual differences).
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


class IOTMS(BaseModel):
    """Individual Optimal Tempo Matching System -- individual opioid tone sensitivity."""

    NAME = "IOTMS"
    FULL_NAME = "Individual Optimal Tempo Matching System"
    UNIT = "RPU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ("ARU",)

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_mor_baseline", "f02_pleasure_bold_slope",
            "f03_reward_propensity", "f04_music_reward_index",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "baseline_mor_availability", "sensitivity_slope",
            "individual_threshold",
        )),
        LayerSpec("P", "Present Processing", 7, 8, (
            "individual_sensitivity_state",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "pleasure_response_pred", "sensitivity_persistence_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_mor_baseline", "f02_pleasure_bold_slope",
            "f03_reward_propensity", "f04_music_reward_index",
            # Layer M -- Mathematical
            "baseline_mor_availability", "sensitivity_slope",
            "individual_threshold",
            # Layer P -- Present
            "individual_sensitivity_state",
            # Layer F -- Future
            "pleasure_response_pred", "sensitivity_persistence_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(10, 8, -8),
                function="Individual MOR availability baseline",
                evidence_count=1,
            ),
            BrainRegion(
                name="Ventral Tegmental Area",
                abbreviation="VTA",
                hemisphere="bilateral",
                mni_coords=(0, -16, -8),
                function="Opioid tone modulation",
                evidence_count=1,
            ),
            BrainRegion(
                name="Caudate Nucleus",
                abbreviation="Caudate",
                hemisphere="bilateral",
                mni_coords=(10, 10, 8),
                function="Reward propensity individual differences",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Putkinen", 2025,
                         "Individual MOR availability predicts music reward propensity",
                         ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.65),
            falsification_criteria=(
                "Baseline MOR must correlate with music reward questionnaire scores",
                "Individual MOR should predict BOLD response to pleasurable music",
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
