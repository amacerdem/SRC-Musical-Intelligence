"""CMAPCC -- Cross-Modal Action-Perception Common Code.

Unit: IMU | Tier: beta | Output: 10D
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


class CMAPCC(BaseModel):
    """Cross-Modal Action-Perception Common Code.

    IMU-beta | 10D | Mechanisms: MEM, TMH
    """

    NAME = "CMAPCC"
    FULL_NAME = "Cross-Modal Action-Perception Common Code"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES: Tuple[str, ...] = ("MEM", "TMH",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("cmapcc_e0", "cmapcc_e1", "cmapcc_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("cmapcc_m0", "cmapcc_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("cmapcc_p0", "cmapcc_p1", "cmapcc_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("cmapcc_f0", "cmapcc_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(7, "velocity_A", 16, "2s", 0, "value", 2, "integration", "CMAPCC temporal", "Cross-Modal Action-Perception Common Code"),
            H3DemandSpec(7, "velocity_A", 18, "4s", 0, "value", 2, "integration", "CMAPCC temporal", "Cross-Modal Action-Perception Common Code"),
            H3DemandSpec(14, "brightness_kuttruff", 16, "2s", 0, "value", 2, "integration", "CMAPCC temporal", "Cross-Modal Action-Perception Common Code"),
            H3DemandSpec(14, "brightness_kuttruff", 18, "4s", 0, "value", 2, "integration", "CMAPCC temporal", "Cross-Modal Action-Perception Common Code"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("cmapcc_e0", "cmapcc_e1", "cmapcc_e2", "cmapcc_m0", "cmapcc_m1", "cmapcc_p0", "cmapcc_p1", "cmapcc_p2", "cmapcc_f0", "cmapcc_f1",)

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
                Citation("Author", 2020, "Cross-Modal Action-Perception Common Code primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Cross-Modal Action-Perception Common Code predictions must correlate with neural data",
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
            out[..., i] = torch.sigmoid(0.6 * m_val + 0.4 * r3_val)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
