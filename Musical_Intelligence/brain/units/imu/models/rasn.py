"""RASN -- Rhythmic Auditory Stimulation Neuroplasticity.

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


class RASN(BaseModel):
    """Rhythmic Auditory Stimulation Neuroplasticity.

    IMU-beta | 10D
    """

    NAME = "RASN"
    FULL_NAME = "Rhythmic Auditory Stimulation Neuroplasticity"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 10
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("rasn_e0", "rasn_e1", "rasn_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("rasn_m0", "rasn_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("rasn_p0", "rasn_p1", "rasn_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("rasn_f0", "rasn_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(14, "brightness_kuttruff", 16, "2s", 0, "value", 2, "integration", "RASN temporal", "Rhythmic Auditory Stimulation Neuroplasticity"),
            H3DemandSpec(14, "brightness_kuttruff", 18, "4s", 0, "value", 2, "integration", "RASN temporal", "Rhythmic Auditory Stimulation Neuroplasticity"),
            H3DemandSpec(17, "spectral_autocorrelation", 16, "2s", 0, "value", 2, "integration", "RASN temporal", "Rhythmic Auditory Stimulation Neuroplasticity"),
            H3DemandSpec(17, "spectral_autocorrelation", 18, "4s", 0, "value", 2, "integration", "RASN temporal", "Rhythmic Auditory Stimulation Neuroplasticity"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("rasn_e0", "rasn_e1", "rasn_e2", "rasn_m0", "rasn_m1", "rasn_p0", "rasn_p1", "rasn_p2", "rasn_f0", "rasn_f1",)

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
                Citation("Author", 2020, "Rhythmic Auditory Stimulation Neuroplasticity primary evidence", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.7, 0.85),
            falsification_criteria=(
                "Rhythmic Auditory Stimulation Neuroplasticity predictions must correlate with neural data",
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
