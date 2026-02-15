"""SDL -- Salience-Dependent Lateralization.

Unit: ASU | Tier: gamma | Output: 9D
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


class SDL(BaseModel):
    """Salience-Dependent Lateralization.

    ASU-gamma | 9D
    """

    NAME = "SDL"
    FULL_NAME = "Salience-Dependent Lateralization"
    UNIT = "ASU"
    TIER = "gamma"
    OUTPUT_DIM = 9
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("sdl_e0", "sdl_e1", "sdl_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("sdl_m0", "sdl_m1",)),
        LayerSpec("P", "Psychological", 5, 7, ("sdl_p0", "sdl_p1",)),
        LayerSpec("F", "Forecast", 7, 9, ("sdl_f0", "sdl_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(24, "delta_energy", 3, "100ms", 0, "value", 2, "integration", "SDL temporal", "Salience-Dependent Lateralization"),
            H3DemandSpec(24, "delta_energy", 6, "200ms", 0, "value", 2, "integration", "SDL temporal", "Salience-Dependent Lateralization"),
            H3DemandSpec(0, "roughness_sethares", 3, "100ms", 0, "value", 2, "integration", "SDL temporal", "Salience-Dependent Lateralization"),
            H3DemandSpec(0, "roughness_sethares", 6, "200ms", 0, "value", 2, "integration", "SDL temporal", "Salience-Dependent Lateralization"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("sdl_e0", "sdl_e1", "sdl_e2", "sdl_m0", "sdl_m1", "sdl_p0", "sdl_p1", "sdl_f0", "sdl_f1",)

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
                Citation("Author", 2020, "Salience-Dependent Lateralization primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Salience-Dependent Lateralization predictions must correlate with neural data",
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
