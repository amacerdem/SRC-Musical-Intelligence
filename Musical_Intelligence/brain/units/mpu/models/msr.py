"""MSR -- Musician Sensorimotor Reorganization.

Unit: MPU | Tier: alpha | Output: 12D
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


class MSR(BaseModel):
    """Musician Sensorimotor Reorganization.

    MPU-alpha | 12D
    """

    NAME = "MSR"
    FULL_NAME = "Musician Sensorimotor Reorganization"
    UNIT = "MPU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("msr_e0", "msr_e1", "msr_e2", "msr_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("msr_m0", "msr_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("msr_p0", "msr_p1", "msr_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("msr_f0", "msr_f1", "msr_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(8, "velocity_D", 6, "200ms", 0, "value", 2, "integration", "MSR temporal", "Musician Sensorimotor Reorganization"),
            H3DemandSpec(8, "velocity_D", 9, "400ms", 0, "value", 2, "integration", "MSR temporal", "Musician Sensorimotor Reorganization"),
            H3DemandSpec(9, "rms_energy", 6, "200ms", 0, "value", 2, "integration", "MSR temporal", "Musician Sensorimotor Reorganization"),
            H3DemandSpec(9, "rms_energy", 9, "400ms", 0, "value", 2, "integration", "MSR temporal", "Musician Sensorimotor Reorganization"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("msr_e0", "msr_e1", "msr_e2", "msr_e3", "msr_m0", "msr_m1", "msr_p0", "msr_p1", "msr_p2", "msr_f0", "msr_f1", "msr_f2",)

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
                Citation("Author", 2020, "Musician Sensorimotor Reorganization primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Musician Sensorimotor Reorganization predictions must correlate with neural data",
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
