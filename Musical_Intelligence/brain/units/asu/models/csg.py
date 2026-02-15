"""CSG -- Consonance-Salience Gradient.

Unit: ASU | Tier: alpha | Output: 12D
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


class CSG(BaseModel):
    """Consonance-Salience Gradient.

    ASU-alpha | 12D
    """

    NAME = "CSG"
    FULL_NAME = "Consonance-Salience Gradient"
    UNIT = "ASU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 4, ("csg_e0", "csg_e1", "csg_e2", "csg_e3",)),
        LayerSpec("M", "Mechanism", 4, 6, ("csg_m0", "csg_m1",)),
        LayerSpec("P", "Psychological", 6, 9, ("csg_p0", "csg_p1", "csg_p2",)),
        LayerSpec("F", "Forecast", 9, 12, ("csg_f0", "csg_f1", "csg_f2",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(8, "velocity_D", 3, "100ms", 0, "value", 2, "integration", "CSG temporal", "Consonance-Salience Gradient"),
            H3DemandSpec(8, "velocity_D", 6, "200ms", 0, "value", 2, "integration", "CSG temporal", "Consonance-Salience Gradient"),
            H3DemandSpec(9, "rms_energy", 3, "100ms", 0, "value", 2, "integration", "CSG temporal", "Consonance-Salience Gradient"),
            H3DemandSpec(9, "rms_energy", 6, "200ms", 0, "value", 2, "integration", "CSG temporal", "Consonance-Salience Gradient"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("csg_e0", "csg_e1", "csg_e2", "csg_e3", "csg_m0", "csg_m1", "csg_p0", "csg_p1", "csg_p2", "csg_f0", "csg_f1", "csg_f2",)

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
                Citation("Author", 2020, "Consonance-Salience Gradient primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Consonance-Salience Gradient predictions must correlate with neural data",
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
