"""
ECT -- Error Correction Trace.

Gamma-3 model of the NDU.  Proposes that musical expertise involves a
trade-off: increased within-network efficiency comes at the cost of
reduced cross-network integration, potentially limiting flexibility.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: 106 edges musicians>non-musicians within, 192 edges opposite between.
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


class ECT(BaseModel):
    """Error Correction Trace -- expertise compartmentalization trade-off."""

    NAME = "ECT"
    FULL_NAME = "Error Correction Trace"
    UNIT = "NDU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_within_efficiency", "f02_between_reduction",
            "f03_trade_off_ratio", "f04_flexibility_index",
        )),
        LayerSpec("M", "Mathematical Model", 4, 6, (
            "training_years", "network_configuration",
        )),
        LayerSpec("P", "Present Processing", 6, 8, (
            "within_network_binding", "network_isolation",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "transfer_limitation_pred", "flexibility_recovery_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_within_efficiency", "f02_between_reduction",
            "f03_trade_off_ratio", "f04_flexibility_index",
            # Layer M -- Mathematical
            "training_years", "network_configuration",
            # Layer P -- Present
            "within_network_binding", "network_isolation",
            # Layer F -- Future
            "transfer_limitation_pred", "flexibility_recovery_pred",
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
                function="Within-network efficiency gain",
                evidence_count=2,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Cross-network integration reduction",
                evidence_count=1,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Trade-off monitoring and flexibility",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Recasens", 2020,
                         "Expertise trade-off: 106 within vs 192 between edges",
                         ""),
                Citation("Herholz", 2012,
                         "Musical expertise and network reorganization", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.45, 0.65),
            falsification_criteria=(
                "Trade-off must be functionally demonstrated",
                "Flexibility cost should correlate with specialization gain",
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
