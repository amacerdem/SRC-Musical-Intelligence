"""
TAR -- Therapeutic Affective Resonance.

Gamma-3 model of the ARU.  Models the dose-response relationship between
music-based interventions and clinical outcomes (anxiety, depression).
Provides therapeutic target parameters for music-assisted therapy.

Output: 10D per frame (172.27 Hz).
Mechanisms: AED.
Evidence: Koelsch 2014, Chanda & Levitin 2013, Bradt 2013.
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


class TAR(BaseModel):
    """Therapeutic Affective Resonance -- clinical music intervention model."""

    NAME = "TAR"
    FULL_NAME = "Therapeutic Affective Resonance"
    UNIT = "ARU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("AED",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 1, (
            "f14_therapeutic_efficacy",
        )),
        LayerSpec("T", "Therapeutic Targets", 1, 5, (
            "arousal_mod_target", "valence_mod_target",
            "anxiety_reduction", "depression_improvement",
        )),
        LayerSpec("I", "Intervention Parameters", 5, 7, (
            "rec_tempo_norm", "rec_consonance",
        )),
        LayerSpec("P", "Present Processing", 7, 8, (
            "therapeutic_reward",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "mood_improvement_pred", "stress_reduction_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f14_therapeutic_efficacy",
            "arousal_mod_target", "valence_mod_target",
            "anxiety_reduction", "depression_improvement",
            "rec_tempo_norm", "rec_consonance",
            "therapeutic_reward",
            "mood_improvement_pred", "stress_reduction_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Amygdala",
                abbreviation="AMY",
                hemisphere="bilateral",
                mni_coords=(-19, -5, -14),
                function="Anxiety reduction target (amygdala downregulation)",
                evidence_count=2,
            ),
            BrainRegion(
                name="Ventral Striatum",
                abbreviation="VS",
                hemisphere="bilateral",
                mni_coords=(8, 4, -6),
                function="Depression improvement target (DA upregulation)",
                evidence_count=2,
            ),
            BrainRegion(
                name="Hypothalamic-Pituitary-Adrenal Axis",
                abbreviation="HPA",
                hemisphere="bilateral",
                mni_coords=(0, -4, -8),
                function="Cortisol reduction via parasympathetic activation",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Koelsch", 2014,
                         "Brain correlates of music-evoked emotions", ""),
                Citation("Chanda", 2013,
                         "Neurochemistry of music: evidence for health outcomes",
                         ""),
                Citation("Bradt", 2013,
                         "Music interventions for mechanically ventilated patients",
                         ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.40, 0.60),
            falsification_criteria=(
                "Anxiolytic music must reduce cortisol levels measurably",
                "Therapeutic parameters must predict clinical outcome better than chance",
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
