"""SDED -- Sensory Dissonance Early Detection.

Unit: SPU | Tier: gamma | Output: 10D
Mechanisms: PPC, TPC
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


class SDED(BaseModel):
    """Sensory Dissonance Early Detection.

    SPU-gamma | 10D | Mechanisms: PPC, TPC
    """

    NAME = "SDED"
    FULL_NAME = "Sensory Dissonance Early Detection"
    UNIT = "SPU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "TPC",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("sded_e0", "sded_e1", "sded_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("sded_m0", "sded_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("sded_p0", "sded_p1", "sded_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("sded_f0", "sded_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(20, "tristimulus_3", 0, "25ms", 0, "value", 2, "integration", "SDED temporal", "Sensory Dissonance Early Detection"),
            H3DemandSpec(20, "tristimulus_3", 3, "100ms", 0, "value", 2, "integration", "SDED temporal", "Sensory Dissonance Early Detection"),
            H3DemandSpec(0, "roughness_sethares", 0, "25ms", 0, "value", 2, "integration", "SDED temporal", "Sensory Dissonance Early Detection"),
            H3DemandSpec(0, "roughness_sethares", 3, "100ms", 0, "value", 2, "integration", "SDED temporal", "Sensory Dissonance Early Detection"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("sded_e0", "sded_e1", "sded_e2", "sded_m0", "sded_m1", "sded_p0", "sded_p1", "sded_p2", "sded_f0", "sded_f1",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Heschl's Gyrus", "HG", "bilateral", (44, -18, 8), 41, "Primary auditory cortex"),
            BrainRegion("Superior Temporal Gyrus", "STG", "bilateral", (58, -22, 4), 22, "Auditory association"),
            BrainRegion("Planum Temporale", "PT", "L", (-52, -28, 12), 42, "Spectral processing"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Sensory Dissonance Early Detection primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Sensory Dissonance Early Detection predictions must correlate with neural data",
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
