"""AAC -- Autonomic-Affective Coupling.

Unit: ARU | Tier: alpha | Output: 14D
Mechanisms: AED, CPD
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


class AAC(BaseModel):
    """Autonomic-Affective Coupling.

    ARU-alpha | 14D | Mechanisms: AED, CPD
    """

    NAME = "AAC"
    FULL_NAME = "Autonomic-Affective Coupling"
    UNIT = "ARU"
    TIER = "alpha"
    OUTPUT_DIM = 14
    MECHANISM_NAMES: Tuple[str, ...] = ("AED", "CPD",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("aac_e0", "aac_e1", "aac_e2", "aac_e3",)),
        LayerSpec("M", "Mechanism", 4, 7, ("aac_m0", "aac_m1", "aac_m2",)),
        LayerSpec("P", "Psychological", 7, 11, ("aac_p0", "aac_p1", "aac_p2", "aac_p3",)),
        LayerSpec("F", "Forecast", 11, 14, ("aac_f0", "aac_f1", "aac_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(1, "roughness_vassilakis", 6, "200ms", 0, "value", 2, "integration", "AAC temporal", "Autonomic-Affective Coupling"),
            H3DemandSpec(1, "roughness_vassilakis", 9, "400ms", 0, "value", 2, "integration", "AAC temporal", "Autonomic-Affective Coupling"),
            H3DemandSpec(7, "velocity_A", 6, "200ms", 0, "value", 2, "integration", "AAC temporal", "Autonomic-Affective Coupling"),
            H3DemandSpec(7, "velocity_A", 9, "400ms", 0, "value", 2, "integration", "AAC temporal", "Autonomic-Affective Coupling"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("aac_e0", "aac_e1", "aac_e2", "aac_e3", "aac_m0", "aac_m1", "aac_m2", "aac_p0", "aac_p1", "aac_p2", "aac_p3", "aac_f0", "aac_f1", "aac_f2",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Nucleus Accumbens", "NAcc", "bilateral", (10, 12, -8), None, "Reward processing"),
            BrainRegion("Ventral Tegmental Area", "VTA", "bilateral", (0, -16, -8), None, "Dopamine signaling"),
            BrainRegion("Ventromedial Prefrontal Cortex", "vmPFC", "bilateral", (0, 44, -12), 11, "Value computation"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Autonomic-Affective Coupling primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Autonomic-Affective Coupling predictions must correlate with neural data",
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

        out = torch.sigmoid(0.7 * m_proj + 0.3 * r3_proj)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
