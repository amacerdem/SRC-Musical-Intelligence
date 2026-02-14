"""STAI -- Spectral-Temporal Aesthetic Integration.

Unit: SPU | Tier: beta | Output: 12D
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


class STAI(BaseModel):
    """Spectral-Temporal Aesthetic Integration.

    SPU-beta | 12D | Mechanisms: PPC, TPC
    """

    NAME = "STAI"
    FULL_NAME = "Spectral-Temporal Aesthetic Integration"
    UNIT = "SPU"
    TIER = "beta"
    OUTPUT_DIM = 12
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "TPC",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("stai_e0", "stai_e1", "stai_e2", "stai_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("stai_m0", "stai_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("stai_p0", "stai_p1", "stai_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("stai_f0", "stai_f1", "stai_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(5, "inharmonicity", 0, "25ms", 0, "value", 2, "integration", "STAI temporal", "Spectral-Temporal Aesthetic Integration"),
            H3DemandSpec(5, "inharmonicity", 3, "100ms", 0, "value", 2, "integration", "STAI temporal", "Spectral-Temporal Aesthetic Integration"),
            H3DemandSpec(14, "brightness_kuttruff", 0, "25ms", 0, "value", 2, "integration", "STAI temporal", "Spectral-Temporal Aesthetic Integration"),
            H3DemandSpec(14, "brightness_kuttruff", 3, "100ms", 0, "value", 2, "integration", "STAI temporal", "Spectral-Temporal Aesthetic Integration"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("stai_e0", "stai_e1", "stai_e2", "stai_e3", "stai_m0", "stai_m1", "stai_p0", "stai_p1", "stai_p2", "stai_f0", "stai_f1", "stai_f2",)

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
                Citation("Author", 2020, "Spectral-Temporal Aesthetic Integration primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Spectral-Temporal Aesthetic Integration predictions must correlate with neural data",
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
