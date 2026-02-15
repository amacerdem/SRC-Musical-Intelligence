"""CDEM -- Context-Dependent Emotional Memory.

Unit: IMU | Tier: gamma | Output: 9D
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


class CDEM(BaseModel):
    """Context-Dependent Emotional Memory.

    IMU-gamma | 9D
    """

    NAME = "CDEM"
    FULL_NAME = "Context-Dependent Emotional Memory"
    UNIT = "IMU"
    TIER = "gamma"
    OUTPUT_DIM = 9
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("cdem_e0", "cdem_e1", "cdem_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("cdem_m0", "cdem_m1",)),
        LayerSpec("P", "Psychological", 5, 7, ("cdem_p0", "cdem_p1",)),
        LayerSpec("F", "Forecast", 7, 9, ("cdem_f0", "cdem_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(21, "spectral_flux", 16, "2s", 0, "value", 2, "integration", "CDEM temporal", "Context-Dependent Emotional Memory"),
            H3DemandSpec(21, "spectral_flux", 18, "4s", 0, "value", 2, "integration", "CDEM temporal", "Context-Dependent Emotional Memory"),
            H3DemandSpec(22, "spectral_entropy", 16, "2s", 0, "value", 2, "integration", "CDEM temporal", "Context-Dependent Emotional Memory"),
            H3DemandSpec(22, "spectral_entropy", 18, "4s", 0, "value", 2, "integration", "CDEM temporal", "Context-Dependent Emotional Memory"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("cdem_e0", "cdem_e1", "cdem_e2", "cdem_m0", "cdem_m1", "cdem_p0", "cdem_p1", "cdem_f0", "cdem_f1",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Hippocampus", "Hipp", "bilateral", (-28, -20, -12), None, "Memory encoding"),
            BrainRegion("Medial Prefrontal Cortex", "mPFC", "bilateral", (0, 52, 8), 10, "Memory consolidation"),
            BrainRegion("Parahippocampal Gyrus", "PHG", "bilateral", (-24, -32, -12), 36, "Contextual memory"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Context-Dependent Emotional Memory primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Context-Dependent Emotional Memory predictions must correlate with neural data",
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
