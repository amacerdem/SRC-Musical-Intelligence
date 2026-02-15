"""VRIAP -- VR-Integrated Analgesia Paradigm.

Unit: IMU | Tier: beta | Output: 10D
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


class VRIAP(BaseModel):
    """VR-Integrated Analgesia Paradigm.

    IMU-beta | 10D
    """

    NAME = "VRIAP"
    FULL_NAME = "VR-Integrated Analgesia Paradigm"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 10
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("vriap_e0", "vriap_e1", "vriap_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("vriap_m0", "vriap_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("vriap_p0", "vriap_p1", "vriap_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("vriap_f0", "vriap_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(0, "roughness_sethares", 16, "2s", 0, "value", 2, "integration", "VRIAP temporal", "VR-Integrated Analgesia Paradigm"),
            H3DemandSpec(0, "roughness_sethares", 18, "4s", 0, "value", 2, "integration", "VRIAP temporal", "VR-Integrated Analgesia Paradigm"),
            H3DemandSpec(2, "helmholtz_kang", 16, "2s", 0, "value", 2, "integration", "VRIAP temporal", "VR-Integrated Analgesia Paradigm"),
            H3DemandSpec(2, "helmholtz_kang", 18, "4s", 0, "value", 2, "integration", "VRIAP temporal", "VR-Integrated Analgesia Paradigm"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("vriap_e0", "vriap_e1", "vriap_e2", "vriap_m0", "vriap_m1", "vriap_p0", "vriap_p1", "vriap_p2", "vriap_f0", "vriap_f1",)

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
                Citation("Author", 2020, "VR-Integrated Analgesia Paradigm primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "VR-Integrated Analgesia Paradigm predictions must correlate with neural data",
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
