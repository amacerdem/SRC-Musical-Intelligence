"""
SDD -- Spectral Deviance Detection.

Alpha-2 model of the NDU.  Models a supramodal mechanism for identifying
statistical irregularities across sensory modalities, with significant
multilinks (edge-to-edge correlations) between modality-specific deviance
detection networks.

Output: 11D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis), PPC (Pitch Processing Chain).
Evidence: Significant multilinks between deviance networks.
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


class SDD(BaseModel):
    """Spectral Deviance Detection -- supramodal deviance detection."""

    NAME = "SDD"
    FULL_NAME = "Spectral Deviance Detection"
    UNIT = "NDU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("ASA", "PPC")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_deviance_magnitude", "f02_multilink_count",
            "f03_supramodal_index", "f04_ifg_hub_activation",
        )),
        LayerSpec("M", "Mathematical Model", 4, 6, (
            "multilinks_fn", "supramodal_ratio",
        )),
        LayerSpec("P", "Present Processing", 6, 9, (
            "deviance_signal", "multilink_activation",
            "ifg_hub_state",
        )),
        LayerSpec("F", "Future Predictions", 9, 11, (
            "expectation_update_pred", "attention_reorienting_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_deviance_magnitude", "f02_multilink_count",
            "f03_supramodal_index", "f04_ifg_hub_activation",
            # Layer M -- Mathematical
            "multilinks_fn", "supramodal_ratio",
            # Layer P -- Present
            "deviance_signal", "multilink_activation",
            "ifg_hub_state",
            # Layer F -- Future
            "expectation_update_pred", "attention_reorienting_pred",
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
                function="MMN generation -- deviance detection",
                evidence_count=4,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="R",
                mni_coords=(48, 18, 4),
                brodmann_area=44,
                function="Supramodal hub for cross-network multilinks",
                evidence_count=3,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Attention reorienting after deviance",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Recasens", 2020,
                         "Supramodal deviance detection with significant multilinks",
                         ""),
                Citation("Naatanen", 2007,
                         "The mismatch negativity: an index of change detection",
                         ""),
                Citation("Schroger", 2015,
                         "Cross-modal deviance detection", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.88, 0.95),
            falsification_criteria=(
                "Multilinks must correlate across modalities",
                "IFG hub should show supramodal activation",
                "Deviance response should scale with statistical irregularity",
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
