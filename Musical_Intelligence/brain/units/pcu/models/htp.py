"""HTP -- Hierarchical Temporal Prediction.

Unit: PCU | Tier: alpha | Output: 12D
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


class HTP(BaseModel):
    """Hierarchical Temporal Prediction.

    PCU-alpha | 12D | Mechanisms: PPC, TPC, MEM
    """

    NAME = "HTP"
    FULL_NAME = "Hierarchical Temporal Prediction"
    UNIT = "PCU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "TPC", "MEM",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("htp_e0", "htp_e1", "htp_e2", "htp_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("htp_m0", "htp_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("htp_p0", "htp_p1", "htp_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("htp_f0", "htp_f1", "htp_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(0, "roughness_sethares", 0, "25ms", 0, "value", 2, "integration", "HTP temporal", "Hierarchical Temporal Prediction"),
            H3DemandSpec(0, "roughness_sethares", 3, "100ms", 0, "value", 2, "integration", "HTP temporal", "Hierarchical Temporal Prediction"),
            H3DemandSpec(2, "helmholtz_kang", 0, "25ms", 0, "value", 2, "integration", "HTP temporal", "Hierarchical Temporal Prediction"),
            H3DemandSpec(2, "helmholtz_kang", 3, "100ms", 0, "value", 2, "integration", "HTP temporal", "Hierarchical Temporal Prediction"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("htp_e0", "htp_e1", "htp_e2", "htp_e3", "htp_m0", "htp_m1", "htp_p0", "htp_p1", "htp_p2", "htp_f0", "htp_f1", "htp_f2",)

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
                Citation("Author", 2020, "Hierarchical Temporal Prediction primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Hierarchical Temporal Prediction predictions must correlate with neural data",
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
