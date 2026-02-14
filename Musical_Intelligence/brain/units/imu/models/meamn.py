"""MEAMN -- Music-Evoked Autobiographical Memory Network.

Unit: IMU | Tier: alpha | Output: 14D
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


class MEAMN(BaseModel):
    """Music-Evoked Autobiographical Memory Network.

    IMU-alpha | 14D | Mechanisms: MEM, TMH
    """

    NAME = "MEAMN"
    FULL_NAME = "Music-Evoked Autobiographical Memory Network"
    UNIT = "IMU"
    TIER = "alpha"
    OUTPUT_DIM = 14
    MECHANISM_NAMES: Tuple[str, ...] = ("MEM", "TMH",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("meamn_e0", "meamn_e1", "meamn_e2", "meamn_e3",)),
        LayerSpec("M", "Mechanism", 4, 7, ("meamn_m0", "meamn_m1", "meamn_m2",)),
        LayerSpec("P", "Psychological", 7, 11, ("meamn_p0", "meamn_p1", "meamn_p2", "meamn_p3",)),
        LayerSpec("F", "Forecast", 11, 14, ("meamn_f0", "meamn_f1", "meamn_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(0, "roughness_sethares", 16, "2s", 0, "value", 2, "integration", "MEAMN temporal", "Music-Evoked Autobiographical Memory Network"),
            H3DemandSpec(0, "roughness_sethares", 18, "4s", 0, "value", 2, "integration", "MEAMN temporal", "Music-Evoked Autobiographical Memory Network"),
            H3DemandSpec(2, "helmholtz_kang", 16, "2s", 0, "value", 2, "integration", "MEAMN temporal", "Music-Evoked Autobiographical Memory Network"),
            H3DemandSpec(2, "helmholtz_kang", 18, "4s", 0, "value", 2, "integration", "MEAMN temporal", "Music-Evoked Autobiographical Memory Network"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("meamn_e0", "meamn_e1", "meamn_e2", "meamn_e3", "meamn_m0", "meamn_m1", "meamn_m2", "meamn_p0", "meamn_p1", "meamn_p2", "meamn_p3", "meamn_f0", "meamn_f1", "meamn_f2",)

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
                Citation("Author", 2020, "Music-Evoked Autobiographical Memory Network primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Music-Evoked Autobiographical Memory Network predictions must correlate with neural data",
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
