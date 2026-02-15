"""STANM -- Spectrotemporal Attention Network Model.

Unit: ASU | Tier: beta | Output: 10D
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


class STANM(BaseModel):
    """Spectrotemporal Attention Network Model.

    ASU-beta | 10D
    """

    NAME = "STANM"
    FULL_NAME = "Spectrotemporal Attention Network Model"
    UNIT = "ASU"
    TIER = "beta"
    OUTPUT_DIM = 10
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("stanm_e0", "stanm_e1", "stanm_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("stanm_m0", "stanm_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("stanm_p0", "stanm_p1", "stanm_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("stanm_f0", "stanm_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(10, "onset_strength", 3, "100ms", 0, "value", 2, "integration", "STANM temporal", "Spectrotemporal Attention Network Model"),
            H3DemandSpec(10, "onset_strength", 6, "200ms", 0, "value", 2, "integration", "STANM temporal", "Spectrotemporal Attention Network Model"),
            H3DemandSpec(14, "brightness_kuttruff", 3, "100ms", 0, "value", 2, "integration", "STANM temporal", "Spectrotemporal Attention Network Model"),
            H3DemandSpec(14, "brightness_kuttruff", 6, "200ms", 0, "value", 2, "integration", "STANM temporal", "Spectrotemporal Attention Network Model"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("stanm_e0", "stanm_e1", "stanm_e2", "stanm_m0", "stanm_m1", "stanm_p0", "stanm_p1", "stanm_p2", "stanm_f0", "stanm_f1",)

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
                Citation("Author", 2020, "Spectrotemporal Attention Network Model primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Spectrotemporal Attention Network Model predictions must correlate with neural data",
            ),
            version="1.0.0",
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], "Tensor"],
        r3_features: "Tensor",
        cross_unit_inputs: Optional[Dict[str, "Tensor"]] = None,
    ) -> "Tensor":
        B, T, _ = r3_features.shape
        device = r3_features.device

        # Skeleton: R3 cycling + H3 modulation (to be replaced during build)
        r3_dim = r3_features.shape[-1]
        r3_idx = (torch.arange(self.OUTPUT_DIM) % r3_dim).to(device)
        out = torch.sigmoid(r3_features[..., r3_idx])

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
