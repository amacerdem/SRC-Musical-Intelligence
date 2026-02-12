"""
AMSS -- Attention-Modulated Stream Segregation.

Beta-1 model of the STU.  Models how attention to specific instruments in
polyphonic music enhances neural envelope tracking of attended streams, with
distinct temporal dynamics for different instruments.

Output: 11D per frame (172.27 Hz).
Mechanisms: BEP.
Evidence: Hausfeld 2021 (d=0.60-0.68), Mesgarani & Chang 2012.
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


class AMSS(BaseModel):
    """Attention-Modulated Stream Segregation -- polyphonic attention."""

    NAME = "AMSS"
    FULL_NAME = "Attention-Modulated Stream Segregation"
    UNIT = "STU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_attended_tracking", "f02_unattended_suppression",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "attention_gain", "segregation_index",
        )),
        LayerSpec("P", "Present Processing", 4, 8, (
            "stream_envelope", "instrument_identity", "timbre_separation",
            "envelope_neural_coupling",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "stream_continuation", "attention_shift_pred", "segregation_forecast",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_attended_tracking", "f02_unattended_suppression",
            "attention_gain", "segregation_index",
            "stream_envelope", "instrument_identity", "timbre_separation",
            "envelope_neural_coupling",
            "stream_continuation", "attention_shift_pred", "segregation_forecast",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Auditory Cortex",
                abbreviation="AC",
                hemisphere="bilateral",
                mni_coords=(-54, -22, 8),
                function="Envelope tracking of attended auditory streams",
                evidence_count=4,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(60, -32, 8),
                function="Stream segregation and instrument identification",
                evidence_count=3,
            ),
            BrainRegion(
                name="Intraparietal Sulcus",
                abbreviation="IPS",
                hemisphere="bilateral",
                mni_coords=(-30, -56, 48),
                function="Top-down attentional control for stream selection",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Hausfeld", 2021,
                         "Attention enhances envelope tracking in polyphonic music",
                         "d=0.60-0.68"),
                Citation("Mesgarani", 2012,
                         "Selective cortical representation of attended speaker",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.90),
            falsification_criteria=(
                "Attended streams must show higher tracking than unattended",
                "Instrument timbre must modulate segregation ease",
            ),
            version="2.0.0",
            paper_count=5,
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
