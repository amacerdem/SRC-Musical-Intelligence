"""MTNE -- Music Training Neural Efficiency.

Unit: STU | Tier: gamma | Output: 10D
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


class MTNE(BaseModel):
    """Music Training Neural Efficiency.

    STU-gamma | 10D
    """

    NAME = "MTNE"
    FULL_NAME = "Music Training Neural Efficiency"
    UNIT = "STU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("mtne_e0", "mtne_e1", "mtne_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("mtne_m0", "mtne_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("mtne_p0", "mtne_p1", "mtne_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("mtne_f0", "mtne_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(9, "rms_energy", 6, "200ms", 0, "value", 2, "integration", "MTNE temporal", "Music Training Neural Efficiency"),
            H3DemandSpec(9, "rms_energy", 9, "400ms", 0, "value", 2, "integration", "MTNE temporal", "Music Training Neural Efficiency"),
            H3DemandSpec(10, "onset_strength", 6, "200ms", 0, "value", 2, "integration", "MTNE temporal", "Music Training Neural Efficiency"),
            H3DemandSpec(10, "onset_strength", 9, "400ms", 0, "value", 2, "integration", "MTNE temporal", "Music Training Neural Efficiency"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("mtne_e0", "mtne_e1", "mtne_e2", "mtne_m0", "mtne_m1", "mtne_p0", "mtne_p1", "mtne_p2", "mtne_f0", "mtne_f1",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Supplementary Motor Area", "SMA", "bilateral", (0, -4, 56), 6, "Motor planning"),
            BrainRegion("Premotor Cortex", "PMC", "bilateral", (-44, -4, 48), 6, "Motor preparation"),
            BrainRegion("Cerebellum", "Cb", "bilateral", (0, -64, -28), None, "Timing coordination"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Music Training Neural Efficiency primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Music Training Neural Efficiency predictions must correlate with neural data",
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
