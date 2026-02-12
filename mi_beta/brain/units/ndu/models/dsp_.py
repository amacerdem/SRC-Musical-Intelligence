"""
DSP_ -- Deviance Salience Processing.

Beta-1 model of the NDU.  Models how music therapist-guided parental singing
enhances auditory processing in preterm infants through quality-dependent
neural plasticity mechanisms, with sex-dependent response patterns.

Note: Trailing underscore in filename avoids collision with Python's ``dsp``
      namespace.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Quality-dependent singing intervention in preterm infants.
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


class DSP_(BaseModel):
    """Deviance Salience Processing -- developmental singing plasticity."""

    NAME = "DSP_"
    FULL_NAME = "Deviance Salience Processing"
    UNIT = "NDU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_singing_quality", "f02_attention_engagement",
            "f03_plasticity_index", "f04_sex_modulation",
        )),
        LayerSpec("M", "Mathematical Model", 4, 6, (
            "cumulative_exposure", "voice_familiarity",
        )),
        LayerSpec("P", "Present Processing", 6, 8, (
            "auditory_orienting", "vocal_pattern_learning",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "auditory_development_pred", "mmr_enhancement_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_singing_quality", "f02_attention_engagement",
            "f03_plasticity_index", "f04_sex_modulation",
            # Layer M -- Mathematical
            "cumulative_exposure", "voice_familiarity",
            # Layer P -- Present
            "auditory_orienting", "vocal_pattern_learning",
            # Layer F -- Future
            "auditory_development_pred", "mmr_enhancement_pred",
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
                function="Auditory cortex maturation via singing exposure",
                evidence_count=2,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Voice familiarity and pattern learning",
                evidence_count=1,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Attention orienting to singing stimuli",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Virtala", 2023,
                         "Music therapist-guided singing enhances preterm auditory processing",
                         ""),
                Citation("McMahon", 2012,
                         "Parental singing intervention for preterm infants",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Singing quality should predict neural benefit more than quantity",
                "Sex-dependent patterns should replicate across samples",
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
