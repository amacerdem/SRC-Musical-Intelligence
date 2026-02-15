"""DGTP -- Domain-General Temporal Processing.

Unit: ASU | Tier: gamma | Output: 10D
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


class DGTP(BaseModel):
    """Domain-General Temporal Processing.

    ASU-gamma | 10D
    """

    NAME = "DGTP"
    FULL_NAME = "Domain-General Temporal Processing"
    UNIT = "ASU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("dgtp_e0", "dgtp_e1", "dgtp_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("dgtp_m0", "dgtp_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("dgtp_p0", "dgtp_p1", "dgtp_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("dgtp_f0", "dgtp_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(22, "spectral_entropy", 3, "100ms", 0, "value", 2, "integration", "DGTP temporal", "Domain-General Temporal Processing"),
            H3DemandSpec(22, "spectral_entropy", 6, "200ms", 0, "value", 2, "integration", "DGTP temporal", "Domain-General Temporal Processing"),
            H3DemandSpec(24, "delta_energy", 3, "100ms", 0, "value", 2, "integration", "DGTP temporal", "Domain-General Temporal Processing"),
            H3DemandSpec(24, "delta_energy", 6, "200ms", 0, "value", 2, "integration", "DGTP temporal", "Domain-General Temporal Processing"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("dgtp_e0", "dgtp_e1", "dgtp_e2", "dgtp_m0", "dgtp_m1", "dgtp_p0", "dgtp_p1", "dgtp_p2", "dgtp_f0", "dgtp_f1",)

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
                Citation("Author", 2020, "Domain-General Temporal Processing primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Domain-General Temporal Processing predictions must correlate with neural data",
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
