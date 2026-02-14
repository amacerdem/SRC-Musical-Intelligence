"""NEWMD -- Neural Entrainment-Working Memory Dissociation.

Unit: STU | Tier: gamma | Output: 10D
Mechanisms: BEP, TMH
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


class NEWMD(BaseModel):
    """Neural Entrainment-Working Memory Dissociation.

    STU-gamma | 10D | Mechanisms: BEP, TMH
    """

    NAME = "NEWMD"
    FULL_NAME = "Neural Entrainment-Working Memory Dissociation"
    UNIT = "STU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES: Tuple[str, ...] = ("BEP", "TMH",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("newmd_e0", "newmd_e1", "newmd_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("newmd_m0", "newmd_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("newmd_p0", "newmd_p1", "newmd_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("newmd_f0", "newmd_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(8, "velocity_D", 6, "200ms", 0, "value", 2, "integration", "NEWMD temporal", "Neural Entrainment-Working Memory Dissociation"),
            H3DemandSpec(8, "velocity_D", 9, "400ms", 0, "value", 2, "integration", "NEWMD temporal", "Neural Entrainment-Working Memory Dissociation"),
            H3DemandSpec(9, "rms_energy", 6, "200ms", 0, "value", 2, "integration", "NEWMD temporal", "Neural Entrainment-Working Memory Dissociation"),
            H3DemandSpec(9, "rms_energy", 9, "400ms", 0, "value", 2, "integration", "NEWMD temporal", "Neural Entrainment-Working Memory Dissociation"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("newmd_e0", "newmd_e1", "newmd_e2", "newmd_m0", "newmd_m1", "newmd_p0", "newmd_p1", "newmd_p2", "newmd_f0", "newmd_f1",)

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
                Citation("Author", 2020, "Neural Entrainment-Working Memory Dissociation primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Neural Entrainment-Working Memory Dissociation predictions must correlate with neural data",
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
        mech = torch.cat(parts, dim=-1)  # (B, T, total_mech)
        total_m = mech.shape[-1]

        # Vectorized projection: sample mechanism dims evenly
        m_idx = torch.linspace(0, total_m - 1, self.OUTPUT_DIM).long().to(device)
        m_proj = mech[..., m_idx]  # (B, T, OUTPUT_DIM)

        # Vectorized R3 cycling
        r3_dim = r3_features.shape[-1]
        r3_idx = (torch.arange(self.OUTPUT_DIM) % r3_dim).to(device)
        r3_proj = r3_features[..., r3_idx]  # (B, T, OUTPUT_DIM)

        out = torch.sigmoid(0.5 * m_proj + 0.5 * r3_proj)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
