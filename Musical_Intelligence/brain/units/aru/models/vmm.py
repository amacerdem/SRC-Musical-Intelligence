"""VMM -- Valence-Mode Mapping.

Unit: ARU | Tier: alpha | Output: 12D
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


class VMM(BaseModel):
    """Valence-Mode Mapping.

    ARU-alpha | 12D
    """

    NAME = "VMM"
    FULL_NAME = "Valence-Mode Mapping"
    UNIT = "ARU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("vmm_e0", "vmm_e1", "vmm_e2", "vmm_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("vmm_m0", "vmm_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("vmm_p0", "vmm_p1", "vmm_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("vmm_f0", "vmm_f1", "vmm_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(7, "velocity_A", 6, "200ms", 0, "value", 2, "integration", "VMM temporal", "Valence-Mode Mapping"),
            H3DemandSpec(7, "velocity_A", 9, "400ms", 0, "value", 2, "integration", "VMM temporal", "Valence-Mode Mapping"),
            H3DemandSpec(8, "velocity_D", 6, "200ms", 0, "value", 2, "integration", "VMM temporal", "Valence-Mode Mapping"),
            H3DemandSpec(8, "velocity_D", 9, "400ms", 0, "value", 2, "integration", "VMM temporal", "Valence-Mode Mapping"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("vmm_e0", "vmm_e1", "vmm_e2", "vmm_e3", "vmm_m0", "vmm_m1", "vmm_p0", "vmm_p1", "vmm_p2", "vmm_f0", "vmm_f1", "vmm_f2",)

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
                Citation("Author", 2020, "Valence-Mode Mapping primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Valence-Mode Mapping predictions must correlate with neural data",
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
