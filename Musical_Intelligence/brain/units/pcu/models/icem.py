"""ICEM -- Information Content Emotion Model.

Unit: PCU | Tier: alpha | Output: 11D
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


class ICEM(BaseModel):
    """Information Content Emotion Model.

    PCU-alpha | 11D | Mechanisms: PPC, TPC, MEM
    """

    NAME = "ICEM"
    FULL_NAME = "Information Content Emotion Model"
    UNIT = "PCU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "TPC", "MEM",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("icem_e0", "icem_e1", "icem_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("icem_m0", "icem_m1", "icem_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("icem_p0", "icem_p1", "icem_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("icem_f0", "icem_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(14, "brightness_kuttruff", 0, "25ms", 0, "value", 2, "integration", "ICEM temporal", "Information Content Emotion Model"),
            H3DemandSpec(14, "brightness_kuttruff", 3, "100ms", 0, "value", 2, "integration", "ICEM temporal", "Information Content Emotion Model"),
            H3DemandSpec(17, "spectral_autocorrelation", 0, "25ms", 0, "value", 2, "integration", "ICEM temporal", "Information Content Emotion Model"),
            H3DemandSpec(17, "spectral_autocorrelation", 3, "100ms", 0, "value", 2, "integration", "ICEM temporal", "Information Content Emotion Model"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("icem_e0", "icem_e1", "icem_e2", "icem_m0", "icem_m1", "icem_m2", "icem_p0", "icem_p1", "icem_p2", "icem_f0", "icem_f1",)

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
                Citation("Author", 2020, "Information Content Emotion Model primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Information Content Emotion Model predictions must correlate with neural data",
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
            out[..., i] = torch.sigmoid(0.7 * m_val + 0.3 * r3_val)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
