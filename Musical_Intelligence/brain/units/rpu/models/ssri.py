"""SSRI -- Social Synchrony Reward Integration.

Unit: RPU | Tier: beta | Output: 11D
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


class SSRI(BaseModel):
    """Social Synchrony Reward Integration.

    RPU-beta | 11D
    """

    NAME = "SSRI"
    FULL_NAME = "Social Synchrony Reward Integration"
    UNIT = "RPU"
    TIER = "beta"
    OUTPUT_DIM = 11
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("ssri_e0", "ssri_e1", "ssri_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("ssri_m0", "ssri_m1", "ssri_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("ssri_p0", "ssri_p1", "ssri_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("ssri_f0", "ssri_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(25, "x_25", 6, "200ms", 0, "value", 2, "integration", "SSRI temporal", "Social Synchrony Reward Integration"),
            H3DemandSpec(25, "x_25", 9, "400ms", 0, "value", 2, "integration", "SSRI temporal", "Social Synchrony Reward Integration"),
            H3DemandSpec(30, "x_30", 6, "200ms", 0, "value", 2, "integration", "SSRI temporal", "Social Synchrony Reward Integration"),
            H3DemandSpec(30, "x_30", 9, "400ms", 0, "value", 2, "integration", "SSRI temporal", "Social Synchrony Reward Integration"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("ssri_e0", "ssri_e1", "ssri_e2", "ssri_m0", "ssri_m1", "ssri_m2", "ssri_p0", "ssri_p1", "ssri_p2", "ssri_f0", "ssri_f1",)

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
                Citation("Author", 2020, "Social Synchrony Reward Integration primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Social Synchrony Reward Integration predictions must correlate with neural data",
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
