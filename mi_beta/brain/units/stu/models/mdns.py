"""
MDNS -- Melody Decoding Neural Signals.

Alpha-3 model of the STU.  Demonstrates that melodies can be accurately
decoded from EEG responses during both perception and imagery using temporal
response function methods, revealing shared neural substrates for external
and internal musical representation.

Output: 12D per frame (172.27 Hz).
Mechanisms: BEP.
Evidence: Di Liberto 2020, Crosse 2016.
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


class MDNS(BaseModel):
    """Melody Decoding Neural Signals -- TRF-based melody decoding."""

    NAME = "MDNS"
    FULL_NAME = "Melody Decoding Neural Signals"
    UNIT = "STU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f01_perception_decode", "f02_imagery_decode",
            "f03_perception_imagery_overlap",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "trf_accuracy", "decoding_confidence",
        )),
        LayerSpec("P", "Present Processing", 5, 9, (
            "pitch_tracking", "contour_encoding", "onset_precision",
            "melodic_binding",
        )),
        LayerSpec("F", "Future Predictions", 9, 12, (
            "next_pitch_pred", "contour_continuation", "imagery_forecast",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_perception_decode", "f02_imagery_decode",
            "f03_perception_imagery_overlap",
            "trf_accuracy", "decoding_confidence",
            "pitch_tracking", "contour_encoding", "onset_precision",
            "melodic_binding",
            "next_pitch_pred", "contour_continuation", "imagery_forecast",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(60, -32, 8),
                function="Auditory cortex encoding of melodic features",
                evidence_count=4,
            ),
            BrainRegion(
                name="Heschl's Gyrus",
                abbreviation="HG",
                hemisphere="bilateral",
                mni_coords=(48, -18, 6),
                function="Primary auditory cortex for pitch processing",
                evidence_count=3,
            ),
            BrainRegion(
                name="Planum Temporale",
                abbreviation="PT",
                hemisphere="left",
                mni_coords=(-52, -28, 12),
                function="Pitch pattern decoding and imagery generation",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Di Liberto", 2020,
                         "EEG melody decoding during perception and imagery", ""),
                Citation("Crosse", 2016,
                         "Temporal response function framework for neural decoding",
                         ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.95),
            falsification_criteria=(
                "Melody decoding must work for both perception and imagery",
                "TRF accuracy must exceed chance for real melodies",
            ),
            version="2.0.0",
            paper_count=4,
        )

    def compute(
        self,
        mechanism_outputs: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Stub -- returns zeros of correct shape."""
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
