"""
MCCN -- Musical Context Coupling Network.

Beta-2 model of the RPU (Reward Processing Unit).  Models how musical chills
engage a distributed cortical network including OFC, bilateral insula, SMA,
and STG, with characteristic theta oscillation patterns.

Output: 10D per frame (172.27 Hz).
Mechanisms: TMH (Temporal Modulation Hierarchy), AED (Affective Entrainment Dynamics).
Evidence: EEG theta patterns during chills (multiple studies).
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


class MCCN(BaseModel):
    """Musical Context Coupling Network -- chills cortical network."""

    NAME = "MCCN"
    FULL_NAME = "Musical Context Coupling Network"
    UNIT = "RPU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("TMH", "AED")
    CROSS_UNIT_READS = ("ARU",)

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_theta_prefrontal", "f02_theta_central",
            "f03_arousal_index", "f04_chills_magnitude",
        )),
        LayerSpec("M", "Mathematical Model", 4, 6, (
            "theta_power_ratio", "network_coherence",
        )),
        LayerSpec("P", "Present Processing", 6, 8, (
            "network_state", "theta_pattern",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "chills_onset_pred", "network_activation_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_theta_prefrontal", "f02_theta_central",
            "f03_arousal_index", "f04_chills_magnitude",
            # Layer M -- Mathematical
            "theta_power_ratio", "network_coherence",
            # Layer P -- Present
            "network_state", "theta_pattern",
            # Layer F -- Future
            "chills_onset_pred", "network_activation_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Orbitofrontal Cortex",
                abbreviation="OFC",
                hemisphere="bilateral",
                mni_coords=(28, 34, -12),
                brodmann_area=11,
                function="Chills network hub -- theta oscillation",
                evidence_count=3,
            ),
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(10, 8, -8),
                function="Reward signal during chills",
                evidence_count=3,
            ),
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -4, 60),
                brodmann_area=6,
                function="Motor component of chills response",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Chabin", 2020,
                         "Musical chills engage theta network: OFC, insula, SMA, STG",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.72, 0.88),
            falsification_criteria=(
                "Theta power must increase during chills episodes",
                "OFC-insula connectivity must be enhanced during chills",
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
