"""
STAI -- Spectral-Temporal Aesthetic Interaction.

Beta-1 model of the SPU.  Models the interaction between spectral integrity
(consonance preservation) and temporal integrity (forward direction quality)
in aesthetic evaluation.  vmPFC-IFG connectivity as integration marker.

Output: 12D per frame (172.27 Hz).
Mechanisms: TPC (Timbre Processing Chain).
Evidence: Brattico 2009, Alluri 2012, Trost 2012.
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


class STAI(BaseModel):
    """Spectral-Temporal Aesthetic Interaction -- beauty from spectral x temporal."""

    NAME = "STAI"
    FULL_NAME = "Spectral-Temporal Aesthetic Interaction"
    UNIT = "SPU"
    TIER = "beta"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("TPC",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_spectral_integrity", "f02_temporal_integrity",
            "f03_aesthetic_integration", "f04_vmpfc_ifg_connectivity",
        )),
        LayerSpec("M", "Mathematical Model", 4, 6, (
            "aesthetic_value", "spectral_temporal_interaction",
        )),
        LayerSpec("P", "Present Processing", 6, 9, (
            "spectral_quality", "temporal_quality", "aesthetic_response",
        )),
        LayerSpec("F", "Future Predictions", 9, 12, (
            "aesthetic_rating_pred", "reward_response_pred",
            "connectivity_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_spectral_integrity", "f02_temporal_integrity",
            "f03_aesthetic_integration", "f04_vmpfc_ifg_connectivity",
            "aesthetic_value", "spectral_temporal_interaction",
            "spectral_quality", "temporal_quality", "aesthetic_response",
            "aesthetic_rating_pred", "reward_response_pred",
            "connectivity_pred",
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
                function="Aesthetic integration network hub",
                evidence_count=3,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Musical syntax and temporal pattern processing",
                evidence_count=3,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Consonance preservation tracking",
                evidence_count=4,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Brattico", 2009,
                         "Neural correlates of musical pleasantness", ""),
                Citation("Alluri", 2012,
                         "Large-scale brain networks emerge from musical features",
                         ""),
                Citation("Trost", 2012,
                         "vmPFC-IFG connectivity during aesthetic experience",
                         "r=0.52"),
            ),
            evidence_tier="beta",
            confidence_range=(0.72, 0.88),
            falsification_criteria=(
                "Spectral x temporal interaction must explain variance beyond additive",
                "vmPFC-IFG connectivity must correlate with aesthetic ratings",
            ),
            version="2.0.0",
            paper_count=7,
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
