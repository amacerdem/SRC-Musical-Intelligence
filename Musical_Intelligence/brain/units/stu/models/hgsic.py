"""HGSIC -- Hierarchical Groove State Integration Circuit.

Unit: STU | Tier: beta | Output: 12D
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


class HGSIC(BaseModel):
    """Hierarchical Groove State Integration Circuit.

    STU-beta | 12D | Mechanisms: BEP, TMH
    """

    NAME = "HGSIC"
    FULL_NAME = "Hierarchical Groove State Integration Circuit"
    UNIT = "STU"
    TIER = "beta"
    OUTPUT_DIM = 12
    MECHANISM_NAMES: Tuple[str, ...] = ("BEP", "TMH",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("hgsic_e0", "hgsic_e1", "hgsic_e2", "hgsic_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("hgsic_m0", "hgsic_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("hgsic_p0", "hgsic_p1", "hgsic_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("hgsic_f0", "hgsic_f1", "hgsic_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(23, "spectral_concentration", 6, "200ms", 0, "value", 2, "integration", "HGSIC temporal", "Hierarchical Groove State Integration Circuit"),
            H3DemandSpec(23, "spectral_concentration", 9, "400ms", 0, "value", 2, "integration", "HGSIC temporal", "Hierarchical Groove State Integration Circuit"),
            H3DemandSpec(24, "delta_energy", 6, "200ms", 0, "value", 2, "integration", "HGSIC temporal", "Hierarchical Groove State Integration Circuit"),
            H3DemandSpec(24, "delta_energy", 9, "400ms", 0, "value", 2, "integration", "HGSIC temporal", "Hierarchical Groove State Integration Circuit"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("hgsic_e0", "hgsic_e1", "hgsic_e2", "hgsic_e3", "hgsic_m0", "hgsic_m1", "hgsic_p0", "hgsic_p1", "hgsic_p2", "hgsic_f0", "hgsic_f1", "hgsic_f2",)

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
                Citation("Author", 2020, "Hierarchical Groove State Integration Circuit primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Hierarchical Groove State Integration Circuit predictions must correlate with neural data",
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
            out[..., i] = torch.sigmoid(0.6 * m_val + 0.4 * r3_val)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
