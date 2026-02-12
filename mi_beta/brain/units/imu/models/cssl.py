"""
CSSL -- Cross-Species Song Learning.

Gamma-2 model of the IMU.  Models how song learning in birds (e.g., zebra
finch) shares neural mechanisms with human musical memory, suggesting
evolutionarily conserved memory systems for vocal/musical learning.

Output: 10D per frame (172.27 Hz).
Mechanisms: MEM.
Evidence: Zebra finch study 2020 (r=0.94), Bolhuis & Moorman 2015.
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


class CSSL(BaseModel):
    """Cross-Species Song Learning -- conserved musical memory mechanisms."""

    NAME = "CSSL"
    FULL_NAME = "Cross-Species Song Learning"
    UNIT = "IMU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("MEM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_conserved_mechanism", "f02_vocal_learning",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "cross_species_homology", "learning_efficiency",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "template_matching", "sensory_motor_mapping", "imitation_state",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "learning_trajectory", "crystallization_pred", "template_stability",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_conserved_mechanism", "f02_vocal_learning",
            "cross_species_homology", "learning_efficiency",
            "template_matching", "sensory_motor_mapping", "imitation_state",
            "learning_trajectory", "crystallization_pred", "template_stability",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(60, -32, 8),
                function="Auditory template storage (homologue of avian HVC)",
                evidence_count=2,
            ),
            BrainRegion(
                name="Hippocampus",
                abbreviation="HIP",
                hemisphere="bilateral",
                mni_coords=(20, -24, -12),
                function="Sequence learning conserved across species",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Zebra finch study", 2020,
                         "HVC and hippocampus in song learning",
                         "r=0.94"),
                Citation("Bolhuis", 2015,
                         "Birdsong, speech, and language: converging mechanisms",
                         ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.65),
            falsification_criteria=(
                "Cross-species homologues must show similar learning trajectories",
                "Template-based learning must be detectable in both species",
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
        """Stub -- returns zeros of correct shape."""
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
