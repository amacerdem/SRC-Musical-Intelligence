"""ESME -- Expertise-Specific MMN Enhancement.

Unit: SPU | Tier: gamma | Output: 11D
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


class ESME(BaseModel):
    """Expertise-Specific MMN Enhancement.

    SPU-gamma | 11D | Mechanisms: PPC, TPC
    """

    NAME = "ESME"
    FULL_NAME = "Expertise-Specific MMN Enhancement"
    UNIT = "SPU"
    TIER = "gamma"
    OUTPUT_DIM = 11
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "TPC",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("esme_e0", "esme_e1", "esme_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("esme_m0", "esme_m1", "esme_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("esme_p0", "esme_p1", "esme_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("esme_f0", "esme_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(19, "tristimulus_2", 0, "25ms", 0, "value", 2, "integration", "ESME temporal", "Expertise-Specific MMN Enhancement"),
            H3DemandSpec(19, "tristimulus_2", 3, "100ms", 0, "value", 2, "integration", "ESME temporal", "Expertise-Specific MMN Enhancement"),
            H3DemandSpec(20, "tristimulus_3", 0, "25ms", 0, "value", 2, "integration", "ESME temporal", "Expertise-Specific MMN Enhancement"),
            H3DemandSpec(20, "tristimulus_3", 3, "100ms", 0, "value", 2, "integration", "ESME temporal", "Expertise-Specific MMN Enhancement"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("esme_e0", "esme_e1", "esme_e2", "esme_m0", "esme_m1", "esme_m2", "esme_p0", "esme_p1", "esme_p2", "esme_f0", "esme_f1",)

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
                Citation("Author", 2020, "Expertise-Specific MMN Enhancement primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Expertise-Specific MMN Enhancement predictions must correlate with neural data",
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
            out[..., i] = torch.sigmoid(0.5 * m_val + 0.5 * r3_val)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
