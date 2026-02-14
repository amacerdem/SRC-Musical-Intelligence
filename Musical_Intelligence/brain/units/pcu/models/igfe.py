"""IGFE -- Individual Gamma Frequency Enhancement.

Unit: PCU | Tier: gamma | Output: 9D
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


class IGFE(BaseModel):
    """Individual Gamma Frequency Enhancement.

    PCU-gamma | 9D | Mechanisms: PPC, TPC, MEM
    """

    NAME = "IGFE"
    FULL_NAME = "Individual Gamma Frequency Enhancement"
    UNIT = "PCU"
    TIER = "gamma"
    OUTPUT_DIM = 9
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "TPC", "MEM",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("igfe_e0", "igfe_e1", "igfe_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("igfe_m0", "igfe_m1",)),
        LayerSpec("P", "Psychological", 5, 7, ("igfe_p0", "igfe_p1",)),
        LayerSpec("F", "Forecast", 7, 9, ("igfe_f0", "igfe_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(23, "spectral_concentration", 0, "25ms", 0, "value", 2, "integration", "IGFE temporal", "Individual Gamma Frequency Enhancement"),
            H3DemandSpec(23, "spectral_concentration", 3, "100ms", 0, "value", 2, "integration", "IGFE temporal", "Individual Gamma Frequency Enhancement"),
            H3DemandSpec(24, "delta_energy", 0, "25ms", 0, "value", 2, "integration", "IGFE temporal", "Individual Gamma Frequency Enhancement"),
            H3DemandSpec(24, "delta_energy", 3, "100ms", 0, "value", 2, "integration", "IGFE temporal", "Individual Gamma Frequency Enhancement"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("igfe_e0", "igfe_e1", "igfe_e2", "igfe_m0", "igfe_m1", "igfe_p0", "igfe_p1", "igfe_f0", "igfe_f1",)

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
                Citation("Author", 2020, "Individual Gamma Frequency Enhancement primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Individual Gamma Frequency Enhancement predictions must correlate with neural data",
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
