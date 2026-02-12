"""
SNEM -- Salience Network Engagement Model.

Alpha-1 model of the ASU (Auditory Salience Unit).  Models how the brain
selectively enhances neural oscillations at beat and meter frequencies
through steady-state evoked potentials (SS-EPs), even when acoustic energy
is not predominant at these frequencies.

Output: 12D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Nozaradan 2012 (SS-EPs enhanced at beat/meter > envelope).
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


class SNEM(BaseModel):
    """Salience Network Engagement Model -- selective neural entrainment."""

    NAME = "SNEM"
    FULL_NAME = "Salience Network Engagement Model"
    UNIT = "ASU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f01_beat_entrainment", "f02_meter_entrainment",
            "f03_selective_enhancement",
        )),
        LayerSpec("M", "Mathematical Model", 3, 6, (
            "ssep_enhancement", "enhancement_index", "beat_salience",
        )),
        LayerSpec("P", "Present Processing", 6, 9, (
            "beat_locked_activity", "entrainment_strength",
            "selective_gain",
        )),
        LayerSpec("F", "Future Predictions", 9, 12, (
            "beat_onset_pred", "meter_position_pred",
            "enhancement_magnitude_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_beat_entrainment", "f02_meter_entrainment",
            "f03_selective_enhancement",
            # Layer M -- Mathematical
            "ssep_enhancement", "enhancement_index", "beat_salience",
            # Layer P -- Present
            "beat_locked_activity", "entrainment_strength",
            "selective_gain",
            # Layer F -- Future
            "beat_onset_pred", "meter_position_pred",
            "enhancement_magnitude_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Salience network hub -- beat entrainment monitoring",
                evidence_count=3,
            ),
            BrainRegion(
                name="Anterior Insula",
                abbreviation="AI",
                hemisphere="bilateral",
                mni_coords=(34, 18, -4),
                brodmann_area=13,
                function="Salience detection and attentional gating",
                evidence_count=2,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="SS-EP generation at beat/meter frequencies",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Nozaradan", 2012,
                         "Selective neuronal entrainment to beat and meter",
                         "p<0.0001"),
                Citation("Nozaradan", 2011,
                         "Tagging neuronal entrainment to beat and meter",
                         ""),
                Citation("Large", 2002,
                         "Perceiving temporal regularity in music", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.97),
            falsification_criteria=(
                "Disrupting rhythmic stability should abolish enhancement",
                "Tempi outside 1-4 Hz should show reduced enhancement",
                "Non-beat frequencies should not show selective enhancement",
            ),
            version="2.0.0",
            paper_count=3,
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
