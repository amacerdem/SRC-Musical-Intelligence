"""CHPI -- Cross-Modal Harmonic Predictive Integration.

Unit: PCU | Tier: beta | Output: 11D
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


class CHPI(BaseModel):
    """Cross-Modal Harmonic Predictive Integration.

    PCU-beta | 11D | Mechanisms: PPC, TPC, MEM
    """

    NAME = "CHPI"
    FULL_NAME = "Cross-Modal Harmonic Predictive Integration"
    UNIT = "PCU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "TPC", "MEM",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("chpi_e0", "chpi_e1", "chpi_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("chpi_m0", "chpi_m1", "chpi_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("chpi_p0", "chpi_p1", "chpi_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("chpi_f0", "chpi_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(22, "spectral_entropy", 0, "25ms", 0, "value", 2, "integration", "CHPI temporal", "Cross-Modal Harmonic Predictive Integration"),
            H3DemandSpec(22, "spectral_entropy", 3, "100ms", 0, "value", 2, "integration", "CHPI temporal", "Cross-Modal Harmonic Predictive Integration"),
            H3DemandSpec(23, "spectral_concentration", 0, "25ms", 0, "value", 2, "integration", "CHPI temporal", "Cross-Modal Harmonic Predictive Integration"),
            H3DemandSpec(23, "spectral_concentration", 3, "100ms", 0, "value", 2, "integration", "CHPI temporal", "Cross-Modal Harmonic Predictive Integration"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("chpi_e0", "chpi_e1", "chpi_e2", "chpi_m0", "chpi_m1", "chpi_m2", "chpi_p0", "chpi_p1", "chpi_p2", "chpi_f0", "chpi_f1",)

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
                Citation("Author", 2020, "Cross-Modal Harmonic Predictive Integration primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Cross-Modal Harmonic Predictive Integration predictions must correlate with neural data",
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

        out = torch.sigmoid(0.6 * m_proj + 0.4 * r3_proj)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
