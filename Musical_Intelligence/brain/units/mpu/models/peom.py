"""PEOM -- Period Entrainment Optimization Model.

Unit: MPU | Tier: alpha | Output: 12D
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple

import torch

from .....contracts.bases.base_model import BaseModel
from .....contracts.dataclasses import (
    BrainRegion,
    Citation,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
)

if TYPE_CHECKING:
    from torch import Tensor


class PEOM(BaseModel):
    """Period Entrainment Optimization Model.

    MPU-alpha | 12D
    """

    NAME = "PEOM"
    FULL_NAME = "Period Entrainment Optimization Model"
    UNIT = "MPU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("peom_e0", "peom_e1", "peom_e2", "peom_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("peom_m0", "peom_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("peom_p0", "peom_p1", "peom_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("peom_f0", "peom_f1", "peom_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(7, "velocity_A", 6, "200ms", 0, "value", 2, "integration", "PEOM temporal", "Period Entrainment Optimization Model"),
            H3DemandSpec(7, "velocity_A", 9, "400ms", 0, "value", 2, "integration", "PEOM temporal", "Period Entrainment Optimization Model"),
            H3DemandSpec(8, "velocity_D", 6, "200ms", 0, "value", 2, "integration", "PEOM temporal", "Period Entrainment Optimization Model"),
            H3DemandSpec(8, "velocity_D", 9, "400ms", 0, "value", 2, "integration", "PEOM temporal", "Period Entrainment Optimization Model"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("peom_e0", "peom_e1", "peom_e2", "peom_e3", "peom_m0", "peom_m1", "peom_p0", "peom_p1", "peom_p2", "peom_f0", "peom_f1", "peom_f2",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Supplementary Motor Area", "SMA", "bilateral", (0, -4, 56), 6, "Motor planning"),
            BrainRegion("Premotor Cortex", "PMC", "bilateral", (-44, -4, 48), 6, "Motor preparation"),
            BrainRegion("Cerebellum", "Cb", "bilateral", (0, -64, -28), None, "Timing coordination"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Period Entrainment Optimization Model primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Period Entrainment Optimization Model predictions must correlate with neural data",
            ),
            version="1.0.0",
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], "Tensor"],
        r3_features: "Tensor",
        cross_unit_inputs: Optional[Dict[str, "Tensor"]] = None,
    ) -> "Tensor":
        B, T, _ = r3_features.shape
        device = r3_features.device

        # Skeleton: R3 cycling + H3 modulation (to be replaced during build)
        r3_dim = r3_features.shape[-1]
        r3_idx = (torch.arange(self.OUTPUT_DIM) % r3_dim).to(device)
        out = torch.sigmoid(r3_features[..., r3_idx])

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
