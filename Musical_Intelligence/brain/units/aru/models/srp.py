"""SRP -- Striatal Reward Pathway.

Unit: ARU | Tier: alpha | Output: 19D
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


class SRP(BaseModel):
    """Striatal Reward Pathway.

    ARU-alpha | 19D
    """

    NAME = "SRP"
    FULL_NAME = "Striatal Reward Pathway"
    UNIT = "ARU"
    TIER = "alpha"
    OUTPUT_DIM = 19
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 6, ("srp_e0", "srp_e1", "srp_e2", "srp_e3", "srp_e4", "srp_e5",)),
        LayerSpec("M", "Mechanism", 6, 10, ("srp_m0", "srp_m1", "srp_m2", "srp_m3",)),
        LayerSpec("P", "Psychological", 10, 15, ("srp_p0", "srp_p1", "srp_p2", "srp_p3", "srp_p4",)),
        LayerSpec("F", "Forecast", 15, 19, ("srp_f0", "srp_f1", "srp_f2", "srp_f3",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(0, "roughness_sethares", 6, "200ms", 0, "value", 2, "integration", "SRP temporal", "Striatal Reward Pathway"),
            H3DemandSpec(0, "roughness_sethares", 9, "400ms", 0, "value", 2, "integration", "SRP temporal", "Striatal Reward Pathway"),
            H3DemandSpec(1, "roughness_vassilakis", 6, "200ms", 0, "value", 2, "integration", "SRP temporal", "Striatal Reward Pathway"),
            H3DemandSpec(1, "roughness_vassilakis", 9, "400ms", 0, "value", 2, "integration", "SRP temporal", "Striatal Reward Pathway"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("srp_e0", "srp_e1", "srp_e2", "srp_e3", "srp_e4", "srp_e5", "srp_m0", "srp_m1", "srp_m2", "srp_m3", "srp_p0", "srp_p1", "srp_p2", "srp_p3", "srp_p4", "srp_f0", "srp_f1", "srp_f2", "srp_f3",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Nucleus Accumbens", "NAcc", "bilateral", (10, 12, -8), None, "Reward processing"),
            BrainRegion("Ventral Tegmental Area", "VTA", "bilateral", (0, -16, -8), None, "Dopamine signaling"),
            BrainRegion("Ventromedial Prefrontal Cortex", "vmPFC", "bilateral", (0, 44, -12), 11, "Value computation"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Striatal Reward Pathway primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Striatal Reward Pathway predictions must correlate with neural data",
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
