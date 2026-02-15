"""CLAM -- Closed-Loop Affective Modulation.

Unit: ARU | Tier: beta | Output: 11D
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


class CLAM(BaseModel):
    """Closed-Loop Affective Modulation.

    ARU-beta | 11D
    """

    NAME = "CLAM"
    FULL_NAME = "Closed-Loop Affective Modulation"
    UNIT = "ARU"
    TIER = "beta"
    OUTPUT_DIM = 11
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("clam_e0", "clam_e1", "clam_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("clam_m0", "clam_m1", "clam_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("clam_p0", "clam_p1", "clam_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("clam_f0", "clam_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(14, "brightness_kuttruff", 6, "200ms", 0, "value", 2, "integration", "CLAM temporal", "Closed-Loop Affective Modulation"),
            H3DemandSpec(14, "brightness_kuttruff", 9, "400ms", 0, "value", 2, "integration", "CLAM temporal", "Closed-Loop Affective Modulation"),
            H3DemandSpec(21, "spectral_flux", 6, "200ms", 0, "value", 2, "integration", "CLAM temporal", "Closed-Loop Affective Modulation"),
            H3DemandSpec(21, "spectral_flux", 9, "400ms", 0, "value", 2, "integration", "CLAM temporal", "Closed-Loop Affective Modulation"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("clam_e0", "clam_e1", "clam_e2", "clam_m0", "clam_m1", "clam_m2", "clam_p0", "clam_p1", "clam_p2", "clam_f0", "clam_f1",)

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
                Citation("Author", 2020, "Closed-Loop Affective Modulation primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Closed-Loop Affective Modulation predictions must correlate with neural data",
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
