"""MMP -- Musical Mnemonic Preservation.

Unit: IMU | Tier: alpha | Output: 11D
Mechanisms: MEM, TMH
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


class MMP(BaseModel):
    """Musical Mnemonic Preservation.

    IMU-alpha | 11D | Mechanisms: MEM, TMH
    """

    NAME = "MMP"
    FULL_NAME = "Musical Mnemonic Preservation"
    UNIT = "IMU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES: Tuple[str, ...] = ("MEM", "TMH",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("mmp_e0", "mmp_e1", "mmp_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("mmp_m0", "mmp_m1", "mmp_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("mmp_p0", "mmp_p1", "mmp_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("mmp_f0", "mmp_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(7, "velocity_A", 16, "2s", 0, "value", 2, "integration", "MMP temporal", "Musical Mnemonic Preservation"),
            H3DemandSpec(7, "velocity_A", 18, "4s", 0, "value", 2, "integration", "MMP temporal", "Musical Mnemonic Preservation"),
            H3DemandSpec(14, "brightness_kuttruff", 16, "2s", 0, "value", 2, "integration", "MMP temporal", "Musical Mnemonic Preservation"),
            H3DemandSpec(14, "brightness_kuttruff", 18, "4s", 0, "value", 2, "integration", "MMP temporal", "Musical Mnemonic Preservation"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("mmp_e0", "mmp_e1", "mmp_e2", "mmp_m0", "mmp_m1", "mmp_m2", "mmp_p0", "mmp_p1", "mmp_p2", "mmp_f0", "mmp_f1",)

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
                Citation("Author", 2020, "Musical Mnemonic Preservation primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Musical Mnemonic Preservation predictions must correlate with neural data",
            ),
            version="1.0.0",
        )

    def compute(
        self,
        mechanism_outputs: Dict[str, "Tensor"],
        h3_features: Dict[Tuple[int, int, int, int], "Tensor"],
        r3_features: "Tensor",
        cross_unit_inputs: Optional[Dict[str, "Tensor"]] = None,
    ) -> "Tensor":
        B, T, _ = r3_features.shape
        device = r3_features.device

        # Gather mechanism features
        parts = []
        for name in self.MECHANISM_NAMES:
            parts.append(
                mechanism_outputs.get(name, torch.zeros(B, T, 30, device=device))
            )
        mech = torch.cat(parts, dim=-1)
        total_m = mech.shape[-1]

        # Project mechanism + R3 to output dims
        out = torch.zeros(B, T, self.OUTPUT_DIM, device=device)
        for i in range(self.OUTPUT_DIM):
            ms = (i * total_m) // self.OUTPUT_DIM
            me = ((i + 1) * total_m) // self.OUTPUT_DIM
            m_val = mech[..., ms:me].mean(dim=-1)
            r3_val = r3_features[..., i % r3_features.shape[-1]]
            out[..., i] = torch.sigmoid(0.7 * m_val + 0.3 * r3_val)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
