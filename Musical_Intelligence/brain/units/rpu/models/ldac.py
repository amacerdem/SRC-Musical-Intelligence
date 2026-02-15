"""LDAC -- Liking-Dependent Auditory Cortex.

Unit: RPU | Tier: gamma | Output: 9D
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


class LDAC(BaseModel):
    """Liking-Dependent Auditory Cortex.

    RPU-gamma | 9D
    """

    NAME = "LDAC"
    FULL_NAME = "Liking-Dependent Auditory Cortex"
    UNIT = "RPU"
    TIER = "gamma"
    OUTPUT_DIM = 9
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("ldac_e0", "ldac_e1", "ldac_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("ldac_m0", "ldac_m1",)),
        LayerSpec("P", "Psychological", 5, 7, ("ldac_p0", "ldac_p1",)),
        LayerSpec("F", "Forecast", 7, 9, ("ldac_f0", "ldac_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(30, "x_30", 6, "200ms", 0, "value", 2, "integration", "LDAC temporal", "Liking-Dependent Auditory Cortex"),
            H3DemandSpec(30, "x_30", 9, "400ms", 0, "value", 2, "integration", "LDAC temporal", "Liking-Dependent Auditory Cortex"),
            H3DemandSpec(35, "x_35", 6, "200ms", 0, "value", 2, "integration", "LDAC temporal", "Liking-Dependent Auditory Cortex"),
            H3DemandSpec(35, "x_35", 9, "400ms", 0, "value", 2, "integration", "LDAC temporal", "Liking-Dependent Auditory Cortex"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("ldac_e0", "ldac_e1", "ldac_e2", "ldac_m0", "ldac_m1", "ldac_p0", "ldac_p1", "ldac_f0", "ldac_f1",)

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
                Citation("Author", 2020, "Liking-Dependent Auditory Cortex primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Liking-Dependent Auditory Cortex predictions must correlate with neural data",
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
