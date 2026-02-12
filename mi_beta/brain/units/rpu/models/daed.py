"""
DAED -- DA-Expectation Dynamics.

Alpha-1 model of the RPU (Reward Processing Unit).  Models the temporal-
anatomical dissociation of dopaminergic reward processing: caudate nucleus
during anticipation of peak pleasure, nucleus accumbens during experience
of peak pleasure.

Output: 12D per frame (172.27 Hz).
Mechanisms: AED (Affective Entrainment Dynamics), CPD (Chills and Peak Detection).
Evidence: Salimpoor 2011 PET (d=0.71, n=16, p<0.001).
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


class DAED(BaseModel):
    """DA-Expectation Dynamics -- dopamine anticipation-experience dissociation."""

    NAME = "DAED"
    FULL_NAME = "DA-Expectation Dynamics"
    UNIT = "RPU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("AED", "CPD")
    CROSS_UNIT_READS = ("ARU",)

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_anticipatory_da", "f02_consummatory_da",
            "f03_wanting_index", "f04_liking_index",
        )),
        LayerSpec("M", "Mathematical Model", 4, 8, (
            "caudate_da_proxy", "nacc_da_proxy",
            "dissociation_index", "temporal_phase",
        )),
        LayerSpec("P", "Present Processing", 8, 10, (
            "caudate_activation_state", "nacc_activation_state",
        )),
        LayerSpec("F", "Future Predictions", 10, 12, (
            "peak_timing_pred", "pleasure_magnitude_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_anticipatory_da", "f02_consummatory_da",
            "f03_wanting_index", "f04_liking_index",
            # Layer M -- Mathematical
            "caudate_da_proxy", "nacc_da_proxy",
            "dissociation_index", "temporal_phase",
            # Layer P -- Present
            "caudate_activation_state", "nacc_activation_state",
            # Layer F -- Future
            "peak_timing_pred", "pleasure_magnitude_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Caudate Nucleus",
                abbreviation="Caudate",
                hemisphere="bilateral",
                mni_coords=(10, 10, 8),
                function="Reward anticipation -- dopamine release (wanting)",
                evidence_count=4,
            ),
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(10, 8, -8),
                function="Reward consummation -- dopamine release (liking)",
                evidence_count=4,
            ),
            BrainRegion(
                name="Ventral Tegmental Area",
                abbreviation="VTA",
                hemisphere="bilateral",
                mni_coords=(0, -16, -8),
                function="Dopaminergic source -- mesolimbic pathway",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Salimpoor", 2011,
                         "DA release in striatum: caudate anticipation vs NAcc experience",
                         "d=0.71"),
                Citation("Salimpoor", 2011,
                         "Caudate-BP correlates with chills count",
                         "r=0.71"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.92, 0.98),
            falsification_criteria=(
                "DA antagonists should reduce both anticipatory and consummatory pleasure",
                "Caudate lesions should impair anticipatory but not consummatory responses",
                "NAcc lesions should impair consummatory but not anticipatory responses",
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
