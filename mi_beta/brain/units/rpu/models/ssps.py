"""
SSPS -- Social Signal Processing System.

Gamma-3 model of the RPU (Reward Processing Unit).  Proposes that musical
preference follows a saddle-shaped surface in the IC x entropy space:
highest liking at high uncertainty/low surprise OR low uncertainty/
intermediate surprise.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Scene Analysis).
Evidence: Gold 2019 (preliminary behavioral data).
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


class SSPS(BaseModel):
    """Social Signal Processing System -- saddle-shaped preference surface."""

    NAME = "SSPS"
    FULL_NAME = "Social Signal Processing System"
    UNIT = "RPU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ("ARU",)

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_ic_value", "f02_entropy_value",
            "f03_saddle_position", "f04_peak_proximity",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "ic_entropy_surface", "saddle_curvature",
            "optimal_distance",
        )),
        LayerSpec("P", "Present Processing", 7, 8, (
            "surface_position_state",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "optimal_zone_pred", "preference_trajectory_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_ic_value", "f02_entropy_value",
            "f03_saddle_position", "f04_peak_proximity",
            # Layer M -- Mathematical
            "ic_entropy_surface", "saddle_curvature",
            "optimal_distance",
            # Layer P -- Present
            "surface_position_state",
            # Layer F -- Future
            "optimal_zone_pred", "preference_trajectory_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(10, 8, -8),
                function="Preference surface computation",
                evidence_count=1,
            ),
            BrainRegion(
                name="Orbitofrontal Cortex",
                abbreviation="OFC",
                hemisphere="bilateral",
                mni_coords=(28, 34, -12),
                brodmann_area=11,
                function="Complexity-preference integration",
                evidence_count=1,
            ),
            BrainRegion(
                name="Ventromedial Prefrontal Cortex",
                abbreviation="vmPFC",
                hemisphere="bilateral",
                mni_coords=(0, 46, -10),
                brodmann_area=11,
                function="Optimal zone valuation",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Gold", 2019,
                         "Saddle-shaped preference surface in IC x entropy space",
                         ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.65),
            falsification_criteria=(
                "Preference surface must show saddle shape (not simple inverted-U)",
                "High uncertainty + low surprise must yield high liking",
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
