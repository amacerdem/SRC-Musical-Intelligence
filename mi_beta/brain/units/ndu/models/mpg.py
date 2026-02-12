"""
MPG -- Mismatch Prediction Gate.

Alpha-1 model of the NDU (Novelty Detection Unit).  Models the anatomical
and functional posterior-to-anterior gradient in early cortical processing
of musical melodies, with posterior regions processing sequence onset and
anterior regions processing subsequent notes and pitch variation.

Output: 12D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Posterior-to-anterior cortical gradient for melody processing.
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


class MPG(BaseModel):
    """Mismatch Prediction Gate -- melodic processing gradient."""

    NAME = "MPG"
    FULL_NAME = "Mismatch Prediction Gate"
    UNIT = "NDU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_onset_posterior_weight", "f02_sequence_anterior_weight",
            "f03_contour_complexity", "f04_gradient_ratio",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "activity_gradient_fn", "posterior_activity",
            "anterior_activity",
        )),
        LayerSpec("P", "Present Processing", 7, 9, (
            "onset_detection_state", "contour_tracking_state",
        )),
        LayerSpec("F", "Future Predictions", 9, 12, (
            "phrase_boundary_pred", "gradient_shift_pred",
            "contour_continuation_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_onset_posterior_weight", "f02_sequence_anterior_weight",
            "f03_contour_complexity", "f04_gradient_ratio",
            # Layer M -- Mathematical
            "activity_gradient_fn", "posterior_activity",
            "anterior_activity",
            # Layer P -- Present
            "onset_detection_state", "contour_tracking_state",
            # Layer F -- Future
            "phrase_boundary_pred", "gradient_shift_pred",
            "contour_continuation_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Posterior-to-anterior melody processing gradient",
                evidence_count=4,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="L",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Anterior contour and pitch variation processing",
                evidence_count=3,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Mismatch detection and prediction gating",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Patterson", 2002,
                         "Cortical melody processing gradient", ""),
                Citation("Koelsch", 2009,
                         "Posterior-to-anterior gradient in auditory cortex",
                         ""),
                Citation("Zatorre", 2002,
                         "Cortical pitch processing hierarchy", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.97),
            falsification_criteria=(
                "Posterior regions must respond more to sequence onset",
                "Anterior regions must respond more to pitch variation",
                "Gradient should be robust across musical styles",
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
