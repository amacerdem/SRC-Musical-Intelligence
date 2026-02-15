"""PCCR -- Pitch Chroma Cortical Representation.

Unit: SPU | Tier: alpha | Output: 11D
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


class PCCR(BaseModel):
    """Pitch Chroma Cortical Representation.

    SPU-alpha | 11D
    """

    NAME = "PCCR"
    FULL_NAME = "Pitch Chroma Cortical Representation"
    UNIT = "SPU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("pccr_e0", "pccr_e1", "pccr_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("pccr_m0", "pccr_m1", "pccr_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("pccr_p0", "pccr_p1", "pccr_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("pccr_f0", "pccr_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(3, "stumpf_fusion", 0, "25ms", 0, "value", 2, "integration", "PCCR temporal", "Pitch Chroma Cortical Representation"),
            H3DemandSpec(3, "stumpf_fusion", 3, "100ms", 0, "value", 2, "integration", "PCCR temporal", "Pitch Chroma Cortical Representation"),
            H3DemandSpec(5, "inharmonicity", 0, "25ms", 0, "value", 2, "integration", "PCCR temporal", "Pitch Chroma Cortical Representation"),
            H3DemandSpec(5, "inharmonicity", 3, "100ms", 0, "value", 2, "integration", "PCCR temporal", "Pitch Chroma Cortical Representation"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("pccr_e0", "pccr_e1", "pccr_e2", "pccr_m0", "pccr_m1", "pccr_m2", "pccr_p0", "pccr_p1", "pccr_p2", "pccr_f0", "pccr_f1",)

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
                Citation("Author", 2020, "Pitch Chroma Cortical Representation primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Pitch Chroma Cortical Representation predictions must correlate with neural data",
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
