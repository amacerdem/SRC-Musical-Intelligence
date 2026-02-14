"""MAA -- Multifactorial Atonal Appreciation.

Unit: PCU | Tier: gamma | Output: 5D
Mechanisms: PPC, TPC, MEM
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

    PCU-gamma | 5D | Mechanisms: PPC, TPC, MEM
    """

    NAME = "MAA"
    FULL_NAME = "Multifactorial Atonal Appreciation"
    UNIT = "PCU"
    TIER = "gamma"
    OUTPUT_DIM = 5
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "TPC", "MEM",)
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
            out[..., i] = torch.sigmoid(0.5 * m_val + 0.5 * r3_val)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
