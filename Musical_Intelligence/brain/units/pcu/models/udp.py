"""UDP -- Uncertainty-Driven Pleasure.

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


class UDP(BaseModel):
    """Uncertainty-Driven Pleasure.

    PCU-beta | 10D
    """

    NAME = "UDP"
    FULL_NAME = "Uncertainty-Driven Pleasure"
    UNIT = "PCU"
    TIER = "beta"
    OUTPUT_DIM = 10
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("udp_e0", "udp_e1", "udp_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("udp_m0", "udp_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("udp_p0", "udp_p1", "udp_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("udp_f0", "udp_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(21, "spectral_flux", 0, "25ms", 0, "value", 2, "integration", "UDP temporal", "Uncertainty-Driven Pleasure"),
            H3DemandSpec(21, "spectral_flux", 3, "100ms", 0, "value", 2, "integration", "UDP temporal", "Uncertainty-Driven Pleasure"),
            H3DemandSpec(22, "spectral_entropy", 0, "25ms", 0, "value", 2, "integration", "UDP temporal", "Uncertainty-Driven Pleasure"),
            H3DemandSpec(22, "spectral_entropy", 3, "100ms", 0, "value", 2, "integration", "UDP temporal", "Uncertainty-Driven Pleasure"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("udp_e0", "udp_e1", "udp_e2", "udp_m0", "udp_m1", "udp_p0", "udp_p1", "udp_p2", "udp_f0", "udp_f1",)

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
                Citation("Author", 2020, "Uncertainty-Driven Pleasure primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Uncertainty-Driven Pleasure predictions must correlate with neural data",
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
