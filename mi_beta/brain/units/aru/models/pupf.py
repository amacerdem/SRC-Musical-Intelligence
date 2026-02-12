"""
PUPF -- Pleasure-Uncertainty-Prediction Framework.

Beta-1 model of the ARU.  Models the nonlinear interaction between
uncertainty and surprise in generating musical pleasure (Cheung 2019
Goldilocks zone).  Extends SRP with explicit H x S interaction dynamics.

Output: 12D per frame (172.27 Hz).
Mechanisms: AED, CPD.
Evidence: Cheung 2019 (d=3.8-8.53), Pearce 2005, Gold 2019.
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


class PUPF(BaseModel):
    """Pleasure-Uncertainty-Prediction Framework -- Goldilocks zone model."""

    NAME = "PUPF"
    FULL_NAME = "Pleasure-Uncertainty-Prediction Framework"
    UNIT = "ARU"
    TIER = "beta"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("AED", "CPD")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f07_prediction_error", "f08_uncertainty",
        )),
        LayerSpec("U", "Uncertainty Components", 2, 5, (
            "entropy_H", "surprise_S", "HS_interaction",
        )),
        LayerSpec("G", "Goldilocks Outputs", 5, 7, (
            "pleasure_P", "goldilocks_zone",
        )),
        LayerSpec("P", "Present Processing", 7, 10, (
            "surprise_pleasure", "affective_outcome", "tempo_pred_error",
        )),
        LayerSpec("F", "Future Predictions", 10, 12, (
            "next_event_prob", "pleasure_forecast",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f07_prediction_error", "f08_uncertainty",
            "entropy_H", "surprise_S", "HS_interaction",
            "pleasure_P", "goldilocks_zone",
            "surprise_pleasure", "affective_outcome", "tempo_pred_error",
            "next_event_prob", "pleasure_forecast",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Amygdala",
                abbreviation="AMY",
                hemisphere="bilateral",
                mni_coords=(-19, -5, -14),
                function="Uncertainty x surprise interaction",
                evidence_count=3,
            ),
            BrainRegion(
                name="Hippocampus",
                abbreviation="HIP",
                hemisphere="bilateral",
                mni_coords=(20, -15, -20),
                function="Uncertainty x surprise interaction",
                evidence_count=3,
            ),
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(8, 4, -6),
                function="Uncertainty-driven reward prediction",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Cheung", 2019,
                         "Pleasure = nonlinear f(uncertainty, surprise)",
                         "d=3.8-8.53"),
                Citation("Pearce", 2005,
                         "IDyOM entropy models musical expectation", ""),
                Citation("Gold", 2019,
                         "NAcc RPE-related activity, reward for learning", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.90),
            falsification_criteria=(
                "High uncertainty + low surprise should produce pleasure",
                "Low uncertainty + high surprise should produce pleasure",
                "Both high uncertainty + high surprise should reduce pleasure",
            ),
            version="2.0.0",
            paper_count=6,
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
