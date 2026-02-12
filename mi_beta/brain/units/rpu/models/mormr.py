"""
MORMR -- Model-Optimal Reward Modulation Relay.

Alpha-2 model of the RPU (Reward Processing Unit).  Models the endogenous
opioid system's role in mediating musical pleasure: mu-opioid receptor (MOR)
binding in reward regions correlates with subjective chills and individual
differences in music reward sensitivity.

Output: 11D per frame (172.27 Hz).
Mechanisms: AED (Affective Entrainment Dynamics), C0P (C0 Projection).
Evidence: Putkinen 2025 PET (d=4.8, p<0.05).
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


class MORMR(BaseModel):
    """Model-Optimal Reward Modulation Relay -- mu-opioid receptor music reward."""

    NAME = "MORMR"
    FULL_NAME = "Model-Optimal Reward Modulation Relay"
    UNIT = "RPU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("AED", "C0P")
    CROSS_UNIT_READS = ("ARU",)

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_opioid_release", "f02_chills_count",
            "f03_nacc_binding", "f04_reward_sensitivity",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "mor_binding_potential", "pleasure_intensity_proxy",
            "individual_sensitivity",
        )),
        LayerSpec("P", "Present Processing", 7, 9, (
            "current_opioid_tone", "reward_association",
        )),
        LayerSpec("F", "Future Predictions", 9, 11, (
            "chills_onset_pred", "pleasure_duration_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_opioid_release", "f02_chills_count",
            "f03_nacc_binding", "f04_reward_sensitivity",
            # Layer M -- Mathematical
            "mor_binding_potential", "pleasure_intensity_proxy",
            "individual_sensitivity",
            # Layer P -- Present
            "current_opioid_tone", "reward_association",
            # Layer F -- Future
            "chills_onset_pred", "pleasure_duration_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(10, 8, -8),
                function="Opioid-mediated hedonic pleasure",
                evidence_count=4,
            ),
            BrainRegion(
                name="Ventral Tegmental Area",
                abbreviation="VTA",
                hemisphere="bilateral",
                mni_coords=(0, -16, -8),
                function="Endogenous opioid source modulation",
                evidence_count=3,
            ),
            BrainRegion(
                name="Orbitofrontal Cortex",
                abbreviation="OFC",
                hemisphere="bilateral",
                mni_coords=(28, 34, -12),
                brodmann_area=11,
                function="Reward valuation and MOR binding",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Putkinen", 2025,
                         "Music increases mu-opioid receptor binding in reward regions",
                         "d=4.8"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.96),
            falsification_criteria=(
                "Naltrexone (opioid antagonist) should reduce musical pleasure",
                "Individual MOR availability must predict music reward sensitivity",
                "Non-pleasurable music should not increase MOR binding",
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
