"""SNEM -- Selective Neural Entrainment Model.

Unit: ASU | Tier: alpha | Output: 12D
Mechanisms: BEP, ASA
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


class SNEM(BaseModel):
    """Selective Neural Entrainment Model.

    ASU-alpha | 12D | Mechanisms: BEP, ASA
    """

    NAME = "SNEM"
    FULL_NAME = "Selective Neural Entrainment Model"
    UNIT = "ASU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES: Tuple[str, ...] = ("BEP", "ASA",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("snem_e0", "snem_e1", "snem_e2", "snem_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("snem_m0", "snem_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("snem_p0", "snem_p1", "snem_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("snem_f0", "snem_f1", "snem_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(0, "roughness_sethares", 3, "100ms", 0, "value", 2, "integration", "SNEM temporal", "Selective Neural Entrainment Model"),
            H3DemandSpec(0, "roughness_sethares", 6, "200ms", 0, "value", 2, "integration", "SNEM temporal", "Selective Neural Entrainment Model"),
            H3DemandSpec(7, "velocity_A", 3, "100ms", 0, "value", 2, "integration", "SNEM temporal", "Selective Neural Entrainment Model"),
            H3DemandSpec(7, "velocity_A", 6, "200ms", 0, "value", 2, "integration", "SNEM temporal", "Selective Neural Entrainment Model"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("snem_e0", "snem_e1", "snem_e2", "snem_e3", "snem_m0", "snem_m1", "snem_p0", "snem_p1", "snem_p2", "snem_f0", "snem_f1", "snem_f2",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Anterior Insula", "aIns", "bilateral", (34, 20, -4), None, "Salience detection"),
            BrainRegion("Dorsal Anterior Cingulate", "dACC", "bilateral", (0, 24, 32), 32, "Conflict monitoring"),
            BrainRegion("Temporoparietal Junction", "TPJ", "R", (52, -48, 24), 39, "Attention reorienting"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Selective Neural Entrainment Model primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Selective Neural Entrainment Model predictions must correlate with neural data",
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
