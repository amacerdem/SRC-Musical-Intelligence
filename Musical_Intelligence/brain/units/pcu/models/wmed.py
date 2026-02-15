"""WMED -- Working Memory-Entrainment Dissociation.

Unit: PCU | Tier: beta | Output: 10D
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


class WMED(BaseModel):
    """Working Memory-Entrainment Dissociation.

    PCU-beta | 10D
    """

    NAME = "WMED"
    FULL_NAME = "Working Memory-Entrainment Dissociation"
    UNIT = "PCU"
    TIER = "beta"
    OUTPUT_DIM = 10
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("wmed_e0", "wmed_e1", "wmed_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("wmed_m0", "wmed_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("wmed_p0", "wmed_p1", "wmed_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("wmed_f0", "wmed_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(18, "tristimulus_1", 0, "25ms", 0, "value", 2, "integration", "WMED temporal", "Working Memory-Entrainment Dissociation"),
            H3DemandSpec(18, "tristimulus_1", 3, "100ms", 0, "value", 2, "integration", "WMED temporal", "Working Memory-Entrainment Dissociation"),
            H3DemandSpec(21, "spectral_flux", 0, "25ms", 0, "value", 2, "integration", "WMED temporal", "Working Memory-Entrainment Dissociation"),
            H3DemandSpec(21, "spectral_flux", 3, "100ms", 0, "value", 2, "integration", "WMED temporal", "Working Memory-Entrainment Dissociation"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("wmed_e0", "wmed_e1", "wmed_e2", "wmed_m0", "wmed_m1", "wmed_p0", "wmed_p1", "wmed_p2", "wmed_f0", "wmed_f1",)

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
                Citation("Author", 2020, "Working Memory-Entrainment Dissociation primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Working Memory-Entrainment Dissociation predictions must correlate with neural data",
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
