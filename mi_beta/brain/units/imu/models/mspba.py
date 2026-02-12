"""
MSPBA -- Musical Syntax Processing Broca's Area.

Beta-6 model of the IMU.  Models how harmonic syntax violations (Neapolitan
chords) elicit mERAN responses localized in Broca's area (BA 44) and its
right-hemisphere homologue, indicating domain-general syntactic processing
shared with language.

Output: 11D per frame (172.27 Hz).
Mechanisms: SYN (Syntactic Processing).
Evidence: Koelsch 2005, Maess 2001.
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


class MSPBA(BaseModel):
    """Musical Syntax Processing Broca's Area -- shared music-language syntax."""

    NAME = "MSPBA"
    FULL_NAME = "Musical Syntax Processing Broca's Area"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("SYN",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_syntactic_violation", "f02_eran_amplitude",
        )),
        LayerSpec("M", "Mathematical Model", 2, 5, (
            "violation_magnitude", "syntactic_complexity", "domain_generality",
        )),
        LayerSpec("P", "Present Processing", 5, 8, (
            "harmonic_expectation", "broca_activation", "syntax_processing",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "resolution_expect", "syntactic_continuation", "eran_forecast",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_syntactic_violation", "f02_eran_amplitude",
            "violation_magnitude", "syntactic_complexity", "domain_generality",
            "harmonic_expectation", "broca_activation", "syntax_processing",
            "resolution_expect", "syntactic_continuation", "eran_forecast",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Broca's Area",
                abbreviation="BA44",
                hemisphere="left",
                mni_coords=(-48, 14, 16),
                function="Domain-general syntactic processing for music and language",
                evidence_count=4,
            ),
            BrainRegion(
                name="Right Inferior Frontal Gyrus",
                abbreviation="rIFG",
                hemisphere="right",
                mni_coords=(48, 18, 4),
                function="Right homologue for musical syntax (mERAN generator)",
                evidence_count=3,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(60, -32, 8),
                function="Harmonic expectation and violation detection",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Koelsch", 2005,
                         "ERAN localized to Broca's area for musical syntax", ""),
                Citation("Maess", 2001,
                         "Musical syntax is processed in Broca's area (MEG)", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.90),
            falsification_criteria=(
                "ERAN must be localized to BA44 and right homologue",
                "Musical syntax violations must interact with language syntax",
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
