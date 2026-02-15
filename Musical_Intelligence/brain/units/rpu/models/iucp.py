"""IUCP -- Inverted-U Complexity Preference.

Unit: RPU | Tier: beta | Output: 10D
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


class IUCP(BaseModel):
    """Inverted-U Complexity Preference.

    RPU-beta | 10D
    """

    NAME = "IUCP"
    FULL_NAME = "Inverted-U Complexity Preference"
    UNIT = "RPU"
    TIER = "beta"
    OUTPUT_DIM = 10
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("iucp_e0", "iucp_e1", "iucp_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("iucp_m0", "iucp_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("iucp_p0", "iucp_p1", "iucp_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("iucp_f0", "iucp_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(8, "velocity_D", 6, "200ms", 0, "value", 2, "integration", "IUCP temporal", "Inverted-U Complexity Preference"),
            H3DemandSpec(8, "velocity_D", 9, "400ms", 0, "value", 2, "integration", "IUCP temporal", "Inverted-U Complexity Preference"),
            H3DemandSpec(14, "brightness_kuttruff", 6, "200ms", 0, "value", 2, "integration", "IUCP temporal", "Inverted-U Complexity Preference"),
            H3DemandSpec(14, "brightness_kuttruff", 9, "400ms", 0, "value", 2, "integration", "IUCP temporal", "Inverted-U Complexity Preference"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("iucp_e0", "iucp_e1", "iucp_e2", "iucp_m0", "iucp_m1", "iucp_p0", "iucp_p1", "iucp_p2", "iucp_f0", "iucp_f1",)

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
                Citation("Author", 2020, "Inverted-U Complexity Preference primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Inverted-U Complexity Preference predictions must correlate with neural data",
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
