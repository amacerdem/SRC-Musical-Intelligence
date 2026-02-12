"""
TPIO -- Timbre Perception-Imagery Overlap.

Beta-2 model of the STU.  Models how timbre imagery activates overlapping
neural substrates with timbre perception in posterior STG, with high
behavioral correlation (r=0.84) between perception and imagery judgments.

Output: 10D per frame (172.27 Hz).
Mechanisms: TPC (Timbral Processing Circuit).
Evidence: Halpern 2004 (r=0.84), Zatorre & Halpern 2005.
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


class TPIO(BaseModel):
    """Timbre Perception-Imagery Overlap -- shared timbre substrates."""

    NAME = "TPIO"
    FULL_NAME = "Timbre Perception-Imagery Overlap"
    UNIT = "STU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("TPC",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_perception_imagery_corr", "f02_timbre_representation",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "overlap_index", "imagery_fidelity",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "brightness_encoding", "attack_encoding", "spectral_shape",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "timbre_expectation", "imagery_activation_pred", "instrument_predict",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_perception_imagery_corr", "f02_timbre_representation",
            "overlap_index", "imagery_fidelity",
            "brightness_encoding", "attack_encoding", "spectral_shape",
            "timbre_expectation", "imagery_activation_pred", "instrument_predict",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Posterior Superior Temporal Gyrus",
                abbreviation="pSTG",
                hemisphere="bilateral",
                mni_coords=(58, -30, 6),
                function="Shared substrate for timbre perception and imagery",
                evidence_count=3,
            ),
            BrainRegion(
                name="Planum Temporale",
                abbreviation="PT",
                hemisphere="bilateral",
                mni_coords=(-52, -28, 12),
                function="Timbre feature extraction and spectral analysis",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Halpern", 2004,
                         "Timbre perception and imagery share neural substrates",
                         "r=0.84"),
                Citation("Zatorre", 2005,
                         "Auditory imagery and its neural basis", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.88),
            falsification_criteria=(
                "Posterior STG must activate for both timbre perception and imagery",
                "Behavioral perception-imagery correlation must exceed r=0.5",
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
