"""SLEE -- Statistical Learning Expertise Enhancement.

Unit: NDU | Tier: beta | Output: 10D
Mechanisms: PPC, ASA
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


class SLEE(BaseModel):
    """Statistical Learning Expertise Enhancement.

    NDU-beta | 10D | Mechanisms: PPC, ASA
    """

    NAME = "SLEE"
    FULL_NAME = "Statistical Learning Expertise Enhancement"
    UNIT = "NDU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES: Tuple[str, ...] = ("PPC", "ASA",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("slee_e0", "slee_e1", "slee_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("slee_m0", "slee_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("slee_p0", "slee_p1", "slee_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("slee_f0", "slee_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(14, "brightness_kuttruff", 0, "25ms", 0, "value", 2, "integration", "SLEE temporal", "Statistical Learning Expertise Enhancement"),
            H3DemandSpec(14, "brightness_kuttruff", 3, "100ms", 0, "value", 2, "integration", "SLEE temporal", "Statistical Learning Expertise Enhancement"),
            H3DemandSpec(21, "spectral_flux", 0, "25ms", 0, "value", 2, "integration", "SLEE temporal", "Statistical Learning Expertise Enhancement"),
            H3DemandSpec(21, "spectral_flux", 3, "100ms", 0, "value", 2, "integration", "SLEE temporal", "Statistical Learning Expertise Enhancement"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("slee_e0", "slee_e1", "slee_e2", "slee_m0", "slee_m1", "slee_p0", "slee_p1", "slee_p2", "slee_f0", "slee_f1",)

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
                Citation("Author", 2020, "Statistical Learning Expertise Enhancement primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Statistical Learning Expertise Enhancement predictions must correlate with neural data",
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
