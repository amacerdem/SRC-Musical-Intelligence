"""CTBB -- Cerebellar Theta-Burst Balance.

Unit: MPU | Tier: gamma | Output: 9D
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


class CTBB(BaseModel):
    """Cerebellar Theta-Burst Balance.

    MPU-gamma | 9D
    """

    NAME = "CTBB"
    FULL_NAME = "Cerebellar Theta-Burst Balance"
    UNIT = "MPU"
    TIER = "gamma"
    OUTPUT_DIM = 9
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("ctbb_e0", "ctbb_e1", "ctbb_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("ctbb_m0", "ctbb_m1",)),
        LayerSpec("P", "Psychological", 5, 7, ("ctbb_p0", "ctbb_p1",)),
        LayerSpec("F", "Forecast", 7, 9, ("ctbb_f0", "ctbb_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(24, "delta_energy", 6, "200ms", 0, "value", 2, "integration", "CTBB temporal", "Cerebellar Theta-Burst Balance"),
            H3DemandSpec(24, "delta_energy", 9, "400ms", 0, "value", 2, "integration", "CTBB temporal", "Cerebellar Theta-Burst Balance"),
            H3DemandSpec(7, "velocity_A", 6, "200ms", 0, "value", 2, "integration", "CTBB temporal", "Cerebellar Theta-Burst Balance"),
            H3DemandSpec(7, "velocity_A", 9, "400ms", 0, "value", 2, "integration", "CTBB temporal", "Cerebellar Theta-Burst Balance"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("ctbb_e0", "ctbb_e1", "ctbb_e2", "ctbb_m0", "ctbb_m1", "ctbb_p0", "ctbb_p1", "ctbb_f0", "ctbb_f1",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Supplementary Motor Area", "SMA", "bilateral", (0, -4, 56), 6, "Motor planning"),
            BrainRegion("Premotor Cortex", "PMC", "bilateral", (-44, -4, 48), 6, "Motor preparation"),
            BrainRegion("Cerebellum", "Cb", "bilateral", (0, -64, -28), None, "Timing coordination"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Cerebellar Theta-Burst Balance primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Cerebellar Theta-Burst Balance predictions must correlate with neural data",
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
