"""OII -- Oscillatory Intelligence Integration.

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


class OII(BaseModel):
    """Oscillatory Intelligence Integration.

    IMU-beta | 10D | Mechanisms: MEM, TMH
    """

    NAME = "OII"
    FULL_NAME = "Oscillatory Intelligence Integration"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES: Tuple[str, ...] = ("MEM", "TMH",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("oii_e0", "oii_e1", "oii_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("oii_m0", "oii_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("oii_p0", "oii_p1", "oii_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("oii_f0", "oii_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(21, "spectral_flux", 16, "2s", 0, "value", 2, "integration", "OII temporal", "Oscillatory Intelligence Integration"),
            H3DemandSpec(21, "spectral_flux", 18, "4s", 0, "value", 2, "integration", "OII temporal", "Oscillatory Intelligence Integration"),
            H3DemandSpec(22, "spectral_entropy", 16, "2s", 0, "value", 2, "integration", "OII temporal", "Oscillatory Intelligence Integration"),
            H3DemandSpec(22, "spectral_entropy", 18, "4s", 0, "value", 2, "integration", "OII temporal", "Oscillatory Intelligence Integration"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("oii_e0", "oii_e1", "oii_e2", "oii_m0", "oii_m1", "oii_p0", "oii_p1", "oii_p2", "oii_f0", "oii_f1",)

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
                Citation("Author", 2020, "Oscillatory Intelligence Integration primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Oscillatory Intelligence Integration predictions must correlate with neural data",
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
