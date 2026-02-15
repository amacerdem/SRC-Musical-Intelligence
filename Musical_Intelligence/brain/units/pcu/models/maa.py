"""MAA -- Multifactorial Atonal Appreciation.

Unit: PCU | Tier: gamma | Output: 5D
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


class MAA(BaseModel):
    """Multifactorial Atonal Appreciation.

    PCU-gamma | 5D
    """

    NAME = "MAA"
    FULL_NAME = "Multifactorial Atonal Appreciation"
    UNIT = "PCU"
    TIER = "gamma"
    OUTPUT_DIM = 5
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 2, ("maa_e0", "maa_e1",)),
        LayerSpec("M", "Mechanism", 2, 3, ("maa_m0",)),
        LayerSpec("P", "Psychological", 3, 4, ("maa_p0",)),
        LayerSpec("F", "Forecast", 4, 5, ("maa_f0",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(24, "delta_energy", 0, "25ms", 0, "value", 2, "integration", "MAA temporal", "Multifactorial Atonal Appreciation"),
            H3DemandSpec(24, "delta_energy", 3, "100ms", 0, "value", 2, "integration", "MAA temporal", "Multifactorial Atonal Appreciation"),
            H3DemandSpec(0, "roughness_sethares", 0, "25ms", 0, "value", 2, "integration", "MAA temporal", "Multifactorial Atonal Appreciation"),
            H3DemandSpec(0, "roughness_sethares", 3, "100ms", 0, "value", 2, "integration", "MAA temporal", "Multifactorial Atonal Appreciation"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("maa_e0", "maa_e1", "maa_m0", "maa_p0", "maa_f0",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Auditory Cortex", "AC", "bilateral", (52, -20, 8), 42, "Auditory prediction"),
            BrainRegion("Inferior Frontal Gyrus", "IFG", "L", (-48, 16, 8), 44, "Sequence processing"),
            BrainRegion("Superior Temporal Sulcus", "STS", "bilateral", (56, -32, 0), 21, "Temporal prediction"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Multifactorial Atonal Appreciation primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Multifactorial Atonal Appreciation predictions must correlate with neural data",
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
