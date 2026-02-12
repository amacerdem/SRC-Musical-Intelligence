"""
NEWMD -- Neural Entrainment-Working Memory Dissociation.

Gamma-2 model of the STU.  Models the paradoxical finding that stronger
automatic entrainment to simple rhythms predicts worse tapping performance,
while working memory capacity predicts better performance -- indicating
independent contributions of entrainment and working memory to rhythm production.

Output: 10D per frame (172.27 Hz).
Mechanisms: BEP.
Evidence: Nave-Blodgett 2021, Grahn & Rowe 2009.
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


class NEWMD(BaseModel):
    """Neural Entrainment-Working Memory Dissociation -- paradoxical rhythm production."""

    NAME = "NEWMD"
    FULL_NAME = "Neural Entrainment-Working Memory Dissociation"
    UNIT = "STU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_entrainment_strength", "f02_wm_contribution",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "entrainment_wm_dissociation", "performance_prediction",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "neural_entrainment", "wm_load", "tapping_precision",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "performance_forecast", "entrainment_decay", "wm_demand_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_entrainment_strength", "f02_wm_contribution",
            "entrainment_wm_dissociation", "performance_prediction",
            "neural_entrainment", "wm_load", "tapping_precision",
            "performance_forecast", "entrainment_decay", "wm_demand_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Auditory Cortex",
                abbreviation="AC",
                hemisphere="bilateral",
                mni_coords=(-54, -22, 8),
                function="Automatic neural entrainment to rhythmic patterns",
                evidence_count=2,
            ),
            BrainRegion(
                name="Dorsolateral Prefrontal Cortex",
                abbreviation="dlPFC",
                hemisphere="bilateral",
                mni_coords=(-44, 30, 28),
                function="Working memory for complex rhythm maintenance",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Nave-Blodgett", 2021,
                         "Entrainment and working memory dissociation in rhythm",
                         ""),
                Citation("Grahn", 2009,
                         "Beat-based and memory-based temporal processing", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Strong entrainment must inversely predict tapping performance",
                "Working memory capacity must positively predict performance",
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
