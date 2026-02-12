"""
NSCP -- Neural Substrate Choreographic Planning.

Gamma-1 model of the MPU.  Proposes that population-level neural synchrony
(inter-subject correlation) during music listening predicts commercial
success.

Output: 10D per frame (172.27 Hz).
Mechanisms: BEP (Beat Entrainment Processing).
Evidence: ISC during music listening correlates with commercial success.
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


class NSCP(BaseModel):
    """Neural Substrate Choreographic Planning -- neural synchrony commercial prediction."""

    NAME = "NSCP"
    FULL_NAME = "Neural Substrate Choreographic Planning"
    UNIT = "MPU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f22_isc_magnitude", "f23_engagement_consistency",
            "f24_population_synchrony",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "isc_fn", "commercial_prediction_index",
        )),
        LayerSpec("P", "Present Processing", 5, 7, (
            "current_isc_state", "engagement_level",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "sustained_engagement_pred", "synchrony_trajectory_pred",
            "preference_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f22_isc_magnitude", "f23_engagement_consistency",
            "f24_population_synchrony",
            # Layer M -- Mathematical
            "isc_fn", "commercial_prediction_index",
            # Layer P -- Present
            "current_isc_state", "engagement_level",
            # Layer F -- Future
            "sustained_engagement_pred", "synchrony_trajectory_pred",
            "preference_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -6, 58),
                brodmann_area=6,
                function="Population-level motor entrainment",
                evidence_count=1,
            ),
            BrainRegion(
                name="Premotor Cortex",
                abbreviation="PMC",
                hemisphere="bilateral",
                mni_coords=(-40, -8, 54),
                brodmann_area=6,
                function="Shared motor representations for music",
                evidence_count=1,
            ),
            BrainRegion(
                name="Cerebellum",
                abbreviation="CB",
                hemisphere="bilateral",
                mni_coords=(24, -64, -28),
                function="Timing consistency across listeners",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Berns", 2010,
                         "Neural synchrony predicts commercial success",
                         ""),
                Citation("Hasson", 2004,
                         "Intersubject correlation as engagement measure",
                         ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.45, 0.65),
            falsification_criteria=(
                "ISC must predict success above chance",
                "Individual preference should correlate with ISC",
            ),
            version="2.0.0",
            paper_count=2,
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
