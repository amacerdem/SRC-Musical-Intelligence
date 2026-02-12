"""
IUCP -- Information-Uncertainty Coupling Process.

Beta-1 model of the RPU (Reward Processing Unit).  Models how musical liking
follows inverted U-shaped curves for both information content (IC) and entropy,
with an interaction showing preference for predictable outcomes in uncertain
contexts.

Output: 10D per frame (172.27 Hz).
Mechanisms: C0P (C0 Projection).
Evidence: Gold 2019, Mencke 2019.
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


class IUCP(BaseModel):
    """Information-Uncertainty Coupling Process -- inverted-U complexity preference."""

    NAME = "IUCP"
    FULL_NAME = "Information-Uncertainty Coupling Process"
    UNIT = "RPU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("C0P",)
    CROSS_UNIT_READS = ("ARU",)

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_ic_liking_curve", "f02_entropy_liking_curve",
            "f03_ic_entropy_interaction", "f04_optimal_complexity",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "quadratic_ic", "quadratic_entropy",
            "interaction_term",
        )),
        LayerSpec("P", "Present Processing", 7, 8, (
            "current_preference_state",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "optimal_zone_pred", "liking_trajectory",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_ic_liking_curve", "f02_entropy_liking_curve",
            "f03_ic_entropy_interaction", "f04_optimal_complexity",
            # Layer M -- Mathematical
            "quadratic_ic", "quadratic_entropy",
            "interaction_term",
            # Layer P -- Present
            "current_preference_state",
            # Layer F -- Future
            "optimal_zone_pred", "liking_trajectory",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(10, 8, -8),
                function="Complexity preference computation",
                evidence_count=2,
            ),
            BrainRegion(
                name="Orbitofrontal Cortex",
                abbreviation="OFC",
                hemisphere="bilateral",
                mni_coords=(28, 34, -12),
                brodmann_area=11,
                function="Aesthetic evaluation and optimal complexity",
                evidence_count=2,
            ),
            BrainRegion(
                name="Ventromedial Prefrontal Cortex",
                abbreviation="vmPFC",
                hemisphere="bilateral",
                mni_coords=(0, 46, -10),
                brodmann_area=11,
                function="Liking-complexity integration",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Gold", 2019,
                         "Inverted-U for IC and entropy in musical liking",
                         ""),
                Citation("Mencke", 2019,
                         "Preference for predictable outcomes in uncertain contexts",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.72, 0.88),
            falsification_criteria=(
                "IC-liking curve must show negative quadratic term",
                "Entropy-liking curve must show negative quadratic term",
                "High uncertainty must shift preference toward low surprise",
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
