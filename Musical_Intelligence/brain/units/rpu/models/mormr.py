"""MORMR -- Mu-Opioid Receptor Music Reward.

Unit: RPU | Tier: alpha | Output: 11D
Mechanisms: AED, CPD, C0P
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


class MORMR(BaseModel):
    """Mu-Opioid Receptor Music Reward.

    RPU-alpha | 11D | Mechanisms: AED, CPD, C0P
    """

    NAME = "MORMR"
    FULL_NAME = "Mu-Opioid Receptor Music Reward"
    UNIT = "RPU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES: Tuple[str, ...] = ("AED", "CPD", "C0P",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("mormr_e0", "mormr_e1", "mormr_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("mormr_m0", "mormr_m1", "mormr_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("mormr_p0", "mormr_p1", "mormr_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("mormr_f0", "mormr_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(1, "roughness_vassilakis", 6, "200ms", 0, "value", 2, "integration", "MORMR temporal", "Mu-Opioid Receptor Music Reward"),
            H3DemandSpec(1, "roughness_vassilakis", 9, "400ms", 0, "value", 2, "integration", "MORMR temporal", "Mu-Opioid Receptor Music Reward"),
            H3DemandSpec(7, "velocity_A", 6, "200ms", 0, "value", 2, "integration", "MORMR temporal", "Mu-Opioid Receptor Music Reward"),
            H3DemandSpec(7, "velocity_A", 9, "400ms", 0, "value", 2, "integration", "MORMR temporal", "Mu-Opioid Receptor Music Reward"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("mormr_e0", "mormr_e1", "mormr_e2", "mormr_m0", "mormr_m1", "mormr_m2", "mormr_p0", "mormr_p1", "mormr_p2", "mormr_f0", "mormr_f1",)

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
                Citation("Author", 2020, "Mu-Opioid Receptor Music Reward primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Mu-Opioid Receptor Music Reward predictions must correlate with neural data",
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
