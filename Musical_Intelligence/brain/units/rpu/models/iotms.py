"""IOTMS -- Individual Opioid Tone Music Sensitivity.

Unit: RPU | Tier: gamma | Output: 5D
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


class IOTMS(BaseModel):
    """Individual Opioid Tone Music Sensitivity.

    RPU-gamma | 5D
    """

    NAME = "IOTMS"
    FULL_NAME = "Individual Opioid Tone Music Sensitivity"
    UNIT = "RPU"
    TIER = "gamma"
    OUTPUT_DIM = 5
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 2, ("iotms_e0", "iotms_e1",)),
        LayerSpec("M", "Mechanism", 2, 3, ("iotms_m0",)),
        LayerSpec("P", "Psychological", 3, 4, ("iotms_p0",)),
        LayerSpec("F", "Forecast", 4, 5, ("iotms_f0",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(35, "x_35", 6, "200ms", 0, "value", 2, "integration", "IOTMS temporal", "Individual Opioid Tone Music Sensitivity"),
            H3DemandSpec(35, "x_35", 9, "400ms", 0, "value", 2, "integration", "IOTMS temporal", "Individual Opioid Tone Music Sensitivity"),
            H3DemandSpec(0, "roughness_sethares", 6, "200ms", 0, "value", 2, "integration", "IOTMS temporal", "Individual Opioid Tone Music Sensitivity"),
            H3DemandSpec(0, "roughness_sethares", 9, "400ms", 0, "value", 2, "integration", "IOTMS temporal", "Individual Opioid Tone Music Sensitivity"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("iotms_e0", "iotms_e1", "iotms_m0", "iotms_p0", "iotms_f0",)

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
                Citation("Author", 2020, "Individual Opioid Tone Music Sensitivity primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Individual Opioid Tone Music Sensitivity predictions must correlate with neural data",
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
