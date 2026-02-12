"""
ONI -- Oddball Novelty Index.

Gamma-2 model of the NDU.  Describes preliminary observation that musical
interventions in preterm infants may lead to "over-normalization" where
the intervention group exceeds full-term controls in certain neural measures.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Over-normalization in preterm singing intervention (eta^2=0.23).
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


class ONI(BaseModel):
    """Oddball Novelty Index -- over-normalization in intervention."""

    NAME = "ONI"
    FULL_NAME = "Oddball Novelty Index"
    UNIT = "NDU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_over_normalization_idx", "f02_compensatory_response",
            "f03_attention_enhancement", "f04_intervention_ceiling",
        )),
        LayerSpec("M", "Mathematical Model", 4, 6, (
            "intervention_dosage", "full_term_comparison",
        )),
        LayerSpec("P", "Present Processing", 6, 8, (
            "enhanced_mmr", "attentional_state",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "long_term_outcomes_pred", "intervention_optimization_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_over_normalization_idx", "f02_compensatory_response",
            "f03_attention_enhancement", "f04_intervention_ceiling",
            # Layer M -- Mathematical
            "intervention_dosage", "full_term_comparison",
            # Layer P -- Present
            "enhanced_mmr", "attentional_state",
            # Layer F -- Future
            "long_term_outcomes_pred", "intervention_optimization_pred",
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
                function="Enhanced MMR generation beyond full-term norms",
                evidence_count=2,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Heightened attentional orienting",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Virtala", 2023,
                         "Musical intervention may lead to over-normalization",
                         "eta^2=0.23"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.45, 0.65),
            falsification_criteria=(
                "Over-normalization must replicate in independent samples",
                "Mechanistic explanation for exceeding norms is required",
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
