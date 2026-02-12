"""
ETAM -- Entrainment Tempo Attention Modulation.

Beta-4 model of the STU.  Models how attention modulates cortical envelope
tracking of polyphonic music, with attended instruments showing significantly
better tracking at specific delay windows (150-220 ms, 320-360 ms, 410-450 ms).

Output: 11D per frame (172.27 Hz).
Mechanisms: BEP.
Evidence: Hausfeld 2021 (d=0.6), O'Sullivan 2015.
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


class ETAM(BaseModel):
    """Entrainment Tempo Attention Modulation -- hierarchical envelope tracking."""

    NAME = "ETAM"
    FULL_NAME = "Entrainment Tempo Attention Modulation"
    UNIT = "STU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_envelope_tracking", "f02_attention_enhancement",
        )),
        LayerSpec("M", "Mathematical Model", 2, 5, (
            "tracking_gain", "delay_window_index", "modulation_depth",
        )),
        LayerSpec("P", "Present Processing", 5, 8, (
            "attended_envelope", "unattended_envelope", "tracking_quality",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "envelope_continuation", "attention_modulation_pred",
            "tracking_forecast",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_envelope_tracking", "f02_attention_enhancement",
            "tracking_gain", "delay_window_index", "modulation_depth",
            "attended_envelope", "unattended_envelope", "tracking_quality",
            "envelope_continuation", "attention_modulation_pred",
            "tracking_forecast",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Auditory Cortex",
                abbreviation="AC",
                hemisphere="bilateral",
                mni_coords=(-54, -22, 8),
                function="Envelope tracking with attention-dependent gain",
                evidence_count=4,
            ),
            BrainRegion(
                name="Superior Temporal Sulcus",
                abbreviation="STS",
                hemisphere="bilateral",
                mni_coords=(56, -36, 4),
                function="Multi-stream envelope separation and attention modulation",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Hausfeld", 2021,
                         "Attention modulates envelope tracking at 150-450 ms delays",
                         "d=0.6"),
                Citation("O'Sullivan", 2015,
                         "Attentional selection in a cocktail party environment",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.88),
            falsification_criteria=(
                "Attention must enhance tracking at specific delay windows",
                "Polyphonic advantage must exceed monophonic for attention effects",
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
