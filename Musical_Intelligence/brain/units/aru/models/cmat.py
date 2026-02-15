"""CMAT -- Cross-Modal Affective Transfer.

Unit: ARU | Tier: gamma | Output: 10D
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


class CMAT(BaseModel):
    """Cross-Modal Affective Transfer.

    ARU-gamma | 10D
    """

    NAME = "CMAT"
    FULL_NAME = "Cross-Modal Affective Transfer"
    UNIT = "ARU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("cmat_e0", "cmat_e1", "cmat_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("cmat_m0", "cmat_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("cmat_p0", "cmat_p1", "cmat_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("cmat_f0", "cmat_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(35, "x_35", 6, "200ms", 0, "value", 2, "integration", "CMAT temporal", "Cross-Modal Affective Transfer"),
            H3DemandSpec(35, "x_35", 9, "400ms", 0, "value", 2, "integration", "CMAT temporal", "Cross-Modal Affective Transfer"),
            H3DemandSpec(0, "roughness_sethares", 6, "200ms", 0, "value", 2, "integration", "CMAT temporal", "Cross-Modal Affective Transfer"),
            H3DemandSpec(0, "roughness_sethares", 9, "400ms", 0, "value", 2, "integration", "CMAT temporal", "Cross-Modal Affective Transfer"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("cmat_e0", "cmat_e1", "cmat_e2", "cmat_m0", "cmat_m1", "cmat_p0", "cmat_p1", "cmat_p2", "cmat_f0", "cmat_f1",)

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
                Citation("Author", 2020, "Cross-Modal Affective Transfer primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Cross-Modal Affective Transfer predictions must correlate with neural data",
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
