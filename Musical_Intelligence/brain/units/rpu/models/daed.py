"""DAED -- Dopamine Anticipation-Experience Dissociation.

Unit: RPU | Tier: alpha | Output: 12D
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


class DAED(BaseModel):
    """Dopamine Anticipation-Experience Dissociation.

    RPU-alpha | 12D
    """

    NAME = "DAED"
    FULL_NAME = "Dopamine Anticipation-Experience Dissociation"
    UNIT = "RPU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("daed_e0", "daed_e1", "daed_e2", "daed_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("daed_m0", "daed_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("daed_p0", "daed_p1", "daed_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("daed_f0", "daed_f1", "daed_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(0, "roughness_sethares", 6, "200ms", 0, "value", 2, "integration", "DAED temporal", "Dopamine Anticipation-Experience Dissociation"),
            H3DemandSpec(0, "roughness_sethares", 9, "400ms", 0, "value", 2, "integration", "DAED temporal", "Dopamine Anticipation-Experience Dissociation"),
            H3DemandSpec(1, "roughness_vassilakis", 6, "200ms", 0, "value", 2, "integration", "DAED temporal", "Dopamine Anticipation-Experience Dissociation"),
            H3DemandSpec(1, "roughness_vassilakis", 9, "400ms", 0, "value", 2, "integration", "DAED temporal", "Dopamine Anticipation-Experience Dissociation"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("daed_e0", "daed_e1", "daed_e2", "daed_e3", "daed_m0", "daed_m1", "daed_p0", "daed_p1", "daed_p2", "daed_f0", "daed_f1", "daed_f2",)

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
                Citation("Author", 2020, "Dopamine Anticipation-Experience Dissociation primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Dopamine Anticipation-Experience Dissociation predictions must correlate with neural data",
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
