"""TPRD -- Tonotopy-Pitch Representation Dissociation.

Unit: IMU | Tier: beta | Output: 11D
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


class TPRD(BaseModel):
    """Tonotopy-Pitch Representation Dissociation.

    IMU-beta | 11D
    """

    NAME = "TPRD"
    FULL_NAME = "Tonotopy-Pitch Representation Dissociation"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 11
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("tprd_e0", "tprd_e1", "tprd_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("tprd_m0", "tprd_m1", "tprd_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("tprd_p0", "tprd_p1", "tprd_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("tprd_f0", "tprd_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(2, "helmholtz_kang", 16, "2s", 0, "value", 2, "integration", "TPRD temporal", "Tonotopy-Pitch Representation Dissociation"),
            H3DemandSpec(2, "helmholtz_kang", 18, "4s", 0, "value", 2, "integration", "TPRD temporal", "Tonotopy-Pitch Representation Dissociation"),
            H3DemandSpec(7, "velocity_A", 16, "2s", 0, "value", 2, "integration", "TPRD temporal", "Tonotopy-Pitch Representation Dissociation"),
            H3DemandSpec(7, "velocity_A", 18, "4s", 0, "value", 2, "integration", "TPRD temporal", "Tonotopy-Pitch Representation Dissociation"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("tprd_e0", "tprd_e1", "tprd_e2", "tprd_m0", "tprd_m1", "tprd_m2", "tprd_p0", "tprd_p1", "tprd_p2", "tprd_f0", "tprd_f1",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Hippocampus", "Hipp", "bilateral", (-28, -20, -12), None, "Memory encoding"),
            BrainRegion("Medial Prefrontal Cortex", "mPFC", "bilateral", (0, 52, 8), 10, "Memory consolidation"),
            BrainRegion("Parahippocampal Gyrus", "PHG", "bilateral", (-24, -32, -12), 36, "Contextual memory"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Tonotopy-Pitch Representation Dissociation primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Tonotopy-Pitch Representation Dissociation predictions must correlate with neural data",
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
