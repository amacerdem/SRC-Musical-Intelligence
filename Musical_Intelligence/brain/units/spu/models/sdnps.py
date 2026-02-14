"""SDNPS -- Stimulus-Dependent Neural Pitch Salience.

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


class SDNPS(BaseModel):
    """Stimulus-Dependent Neural Pitch Salience.

    SPU-gamma | 10D | Mechanisms: PPC, TPC
    """

    NAME = "SDNPS"
    FULL_NAME = "Stimulus-Dependent Neural Pitch Salience"
    UNIT = "SPU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "TPC",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("sdnps_e0", "sdnps_e1", "sdnps_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("sdnps_m0", "sdnps_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("sdnps_p0", "sdnps_p1", "sdnps_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("sdnps_f0", "sdnps_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(18, "tristimulus_1", 0, "25ms", 0, "value", 2, "integration", "SDNPS temporal", "Stimulus-Dependent Neural Pitch Salience"),
            H3DemandSpec(18, "tristimulus_1", 3, "100ms", 0, "value", 2, "integration", "SDNPS temporal", "Stimulus-Dependent Neural Pitch Salience"),
            H3DemandSpec(19, "tristimulus_2", 0, "25ms", 0, "value", 2, "integration", "SDNPS temporal", "Stimulus-Dependent Neural Pitch Salience"),
            H3DemandSpec(19, "tristimulus_2", 3, "100ms", 0, "value", 2, "integration", "SDNPS temporal", "Stimulus-Dependent Neural Pitch Salience"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("sdnps_e0", "sdnps_e1", "sdnps_e2", "sdnps_m0", "sdnps_m1", "sdnps_p0", "sdnps_p1", "sdnps_p2", "sdnps_f0", "sdnps_f1",)

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
                Citation("Author", 2020, "Stimulus-Dependent Neural Pitch Salience primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Stimulus-Dependent Neural Pitch Salience predictions must correlate with neural data",
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
