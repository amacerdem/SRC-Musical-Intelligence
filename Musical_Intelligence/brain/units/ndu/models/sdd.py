"""SDD -- Supramodal Deviance Detection.

Unit: NDU | Tier: alpha | Output: 11D
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


class SDD(BaseModel):
    """Supramodal Deviance Detection.

    NDU-alpha | 11D
    """

    NAME = "SDD"
    FULL_NAME = "Supramodal Deviance Detection"
    UNIT = "NDU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("sdd_e0", "sdd_e1", "sdd_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("sdd_m0", "sdd_m1", "sdd_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("sdd_p0", "sdd_p1", "sdd_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("sdd_f0", "sdd_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(7, "velocity_A", 0, "25ms", 0, "value", 2, "integration", "SDD temporal", "Supramodal Deviance Detection"),
            H3DemandSpec(7, "velocity_A", 3, "100ms", 0, "value", 2, "integration", "SDD temporal", "Supramodal Deviance Detection"),
            H3DemandSpec(8, "velocity_D", 0, "25ms", 0, "value", 2, "integration", "SDD temporal", "Supramodal Deviance Detection"),
            H3DemandSpec(8, "velocity_D", 3, "100ms", 0, "value", 2, "integration", "SDD temporal", "Supramodal Deviance Detection"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("sdd_e0", "sdd_e1", "sdd_e2", "sdd_m0", "sdd_m1", "sdd_m2", "sdd_p0", "sdd_p1", "sdd_p2", "sdd_f0", "sdd_f1",)

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
                Citation("Author", 2020, "Supramodal Deviance Detection primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Supramodal Deviance Detection predictions must correlate with neural data",
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
