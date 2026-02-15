"""PUPF -- Predictive Uncertainty-Pleasure Function.

Unit: ARU | Tier: beta | Output: 12D
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


class PUPF(BaseModel):
    """Predictive Uncertainty-Pleasure Function.

    ARU-beta | 12D
    """

    NAME = "PUPF"
    FULL_NAME = "Predictive Uncertainty-Pleasure Function"
    UNIT = "ARU"
    TIER = "beta"
    OUTPUT_DIM = 12
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("pupf_e0", "pupf_e1", "pupf_e2", "pupf_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("pupf_m0", "pupf_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("pupf_p0", "pupf_p1", "pupf_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("pupf_f0", "pupf_f1", "pupf_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(8, "velocity_D", 6, "200ms", 0, "value", 2, "integration", "PUPF temporal", "Predictive Uncertainty-Pleasure Function"),
            H3DemandSpec(8, "velocity_D", 9, "400ms", 0, "value", 2, "integration", "PUPF temporal", "Predictive Uncertainty-Pleasure Function"),
            H3DemandSpec(14, "brightness_kuttruff", 6, "200ms", 0, "value", 2, "integration", "PUPF temporal", "Predictive Uncertainty-Pleasure Function"),
            H3DemandSpec(14, "brightness_kuttruff", 9, "400ms", 0, "value", 2, "integration", "PUPF temporal", "Predictive Uncertainty-Pleasure Function"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("pupf_e0", "pupf_e1", "pupf_e2", "pupf_e3", "pupf_m0", "pupf_m1", "pupf_p0", "pupf_p1", "pupf_p2", "pupf_f0", "pupf_f1", "pupf_f2",)

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
                Citation("Author", 2020, "Predictive Uncertainty-Pleasure Function primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Predictive Uncertainty-Pleasure Function predictions must correlate with neural data",
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
