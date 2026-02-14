"""ECT -- Expertise Compartmentalization Trade-off.

Unit: NDU | Tier: gamma | Output: 9D
Mechanisms: PPC, ASA
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


class ECT(BaseModel):
    """Expertise Compartmentalization Trade-off.

    NDU-gamma | 9D | Mechanisms: PPC, ASA
    """

    NAME = "ECT"
    FULL_NAME = "Expertise Compartmentalization Trade-off"
    UNIT = "NDU"
    TIER = "gamma"
    OUTPUT_DIM = 9
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "ASA",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("ect_e0", "ect_e1", "ect_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("ect_m0", "ect_m1",)),
        LayerSpec("P", "Psychological", 5, 7, ("ect_p0", "ect_p1",)),
        LayerSpec("F", "Forecast", 7, 9, ("ect_f0", "ect_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(24, "delta_energy", 0, "25ms", 0, "value", 2, "integration", "ECT temporal", "Expertise Compartmentalization Trade-off"),
            H3DemandSpec(24, "delta_energy", 3, "100ms", 0, "value", 2, "integration", "ECT temporal", "Expertise Compartmentalization Trade-off"),
            H3DemandSpec(0, "roughness_sethares", 0, "25ms", 0, "value", 2, "integration", "ECT temporal", "Expertise Compartmentalization Trade-off"),
            H3DemandSpec(0, "roughness_sethares", 3, "100ms", 0, "value", 2, "integration", "ECT temporal", "Expertise Compartmentalization Trade-off"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("ect_e0", "ect_e1", "ect_e2", "ect_m0", "ect_m1", "ect_p0", "ect_p1", "ect_f0", "ect_f1",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Anterior Insula", "aIns", "bilateral", (34, 20, -4), None, "Salience detection"),
            BrainRegion("Dorsal Anterior Cingulate", "dACC", "bilateral", (0, 24, 32), 32, "Conflict monitoring"),
            BrainRegion("Temporoparietal Junction", "TPJ", "R", (52, -48, 24), 39, "Attention reorienting"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Expertise Compartmentalization Trade-off primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Expertise Compartmentalization Trade-off predictions must correlate with neural data",
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
