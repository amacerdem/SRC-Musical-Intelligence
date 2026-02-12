"""
DGTP -- Deviance-Gated Temporal Processing.

Gamma-2 model of the ASU.  Proposes that beat perception ability reflects
a domain-general mechanism of internal timekeeping shared between speech
and music processing.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: BAT scores predict temporal processing across auditory domains.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import (
    BaseModel,
    BrainRegion,
    Citation,
    LayerSpec,
    ModelMetadata,
)


class DGTP(BaseModel):
    """Deviance-Gated Temporal Processing -- domain-general timing."""

    NAME = "DGTP"
    FULL_NAME = "Deviance-Gated Temporal Processing"
    UNIT = "ASU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f22_music_timing", "f23_speech_timing",
            "f24_shared_mechanism",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "domain_correlation", "shared_variance",
        )),
        LayerSpec("P", "Present Processing", 5, 7, (
            "music_beat_perception", "domain_general_timing",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "cross_domain_transfer_pred", "training_transfer_pred",
            "timing_precision_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f22_music_timing", "f23_speech_timing",
            "f24_shared_mechanism",
            # Layer M -- Mathematical
            "domain_correlation", "shared_variance",
            # Layer P -- Present
            "music_beat_perception", "domain_general_timing",
            # Layer F -- Future
            "cross_domain_transfer_pred", "training_transfer_pred",
            "timing_precision_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Domain-general temporal processing",
                evidence_count=2,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Shared speech-music temporal analysis",
                evidence_count=2,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Cross-domain timing monitoring",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Rathcke", 2024,
                         "BAT predicts cross-domain temporal processing",
                         ""),
                Citation("Patel", 2003,
                         "Shared resources for speech and music timing", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Music training should transfer to speech timing",
                "BAT should correlate with speech rhythm perception",
            ),
            version="2.0.0",
            paper_count=2,
        )

    def compute(
        self,
        mechanism_outputs: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
