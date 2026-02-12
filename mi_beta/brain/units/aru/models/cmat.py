"""
CMAT -- Cross-Modal Affective Transfer.

Gamma-2 model of the ARU.  Models how emotional affect transfers between
auditory and visual modalities through supramodal valence/arousal
representations and cross-modal binding in the STS.

Output: 10D per frame (172.27 Hz).
Mechanisms: AED.
Evidence: Vines 2006, Spence 2011, Calvert 2001.
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


class CMAT(BaseModel):
    """Cross-Modal Affective Transfer -- multi-sensory affect binding."""

    NAME = "CMAT"
    FULL_NAME = "Cross-Modal Affective Transfer"
    UNIT = "ARU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("AED",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 1, (
            "f13_cross_modal_transfer",
        )),
        LayerSpec("S", "Supramodal State", 1, 4, (
            "supramodal_valence", "supramodal_arousal", "cross_modal_binding",
        )),
        LayerSpec("T", "Transfer Dynamics", 4, 6, (
            "binding_temporal", "congruence_strength",
        )),
        LayerSpec("P", "Present Processing", 6, 8, (
            "multi_sensory_salience", "auditory_valence_contribution",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "coherence_pred", "generalization_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f13_cross_modal_transfer",
            "supramodal_valence", "supramodal_arousal", "cross_modal_binding",
            "binding_temporal", "congruence_strength",
            "multi_sensory_salience", "auditory_valence_contribution",
            "coherence_pred", "generalization_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Superior Temporal Sulcus",
                abbreviation="STS",
                hemisphere="bilateral",
                mni_coords=(-52, -28, 4),
                brodmann_area=22,
                function="Multi-sensory integration and binding",
                evidence_count=2,
            ),
            BrainRegion(
                name="Anterior Insula",
                abbreviation="aINS",
                hemisphere="bilateral",
                mni_coords=(34, 18, 2),
                function="Supramodal affect representation",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Vines", 2006,
                         "Cross-modal interactions in perception of musical performance",
                         ""),
                Citation("Spence", 2011,
                         "Crossmodal correspondences: a tutorial review", ""),
                Citation("Calvert", 2001,
                         "Crossmodal processing in the human brain", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.45, 0.65),
            falsification_criteria=(
                "Congruent audio-visual stimuli must produce stronger affect than incongruent",
                "STS must show enhanced activation for cross-modal binding",
            ),
            version="2.0.0",
            paper_count=4,
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
