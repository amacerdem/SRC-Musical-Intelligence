"""
SPH -- Spectral Pitch Height.

Alpha-2 model of the PCU (Predictive Coding Unit).  Models how auditory
memory recognition engages hierarchical feedforward-feedback loops between
auditory cortex (Heschl's gyrus), hippocampus, and cingulate, with distinct
oscillatory signatures for matched (gamma) vs. varied (alpha-beta) sequences.

Output: 11D per frame (172.27 Hz).
Mechanisms: PPC (Pitch Processing Chain).
Evidence: Bonetti 2024 (MEG, d=0.24-0.34, n=83).
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


class SPH(BaseModel):
    """Spectral Pitch Height -- spatiotemporal prediction hierarchy."""

    NAME = "SPH"
    FULL_NAME = "Spectral Pitch Height"
    UNIT = "PCU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("PPC",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_gamma_match", "f02_alpha_beta_error",
            "f03_hierarchy_position", "f04_feedforward_feedback",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "match_response_350ms", "varied_response_250ms",
            "gamma_power",
        )),
        LayerSpec("P", "Present Processing", 7, 9, (
            "memory_match", "prediction_error",
        )),
        LayerSpec("F", "Future Predictions", 9, 11, (
            "next_tone_pred", "sequence_completion_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_gamma_match", "f02_alpha_beta_error",
            "f03_hierarchy_position", "f04_feedforward_feedback",
            # Layer M -- Mathematical
            "match_response_350ms", "varied_response_250ms",
            "gamma_power",
            # Layer P -- Present
            "memory_match", "prediction_error",
            # Layer F -- Future
            "next_tone_pred", "sequence_completion_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Heschl's Gyrus",
                abbreviation="HG",
                hemisphere="bilateral",
                mni_coords=(42, -24, 8),
                brodmann_area=41,
                function="Auditory input -- bottom of hierarchy",
                evidence_count=4,
            ),
            BrainRegion(
                name="Hippocampus",
                abbreviation="Hipp",
                hemisphere="bilateral",
                mni_coords=(28, -24, -12),
                function="Memory comparison -- middle of hierarchy",
                evidence_count=6,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 32, 24),
                brodmann_area=32,
                function="Decision / evaluation -- top of hierarchy",
                evidence_count=5,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bonetti", 2024,
                         "Spatiotemporal brain dynamics of auditory memory recognition",
                         "d=0.24-0.34"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.96),
            falsification_criteria=(
                "Hippocampal lesions should abolish memory-based predictions",
                "Match response (350ms) must follow error response (250ms)",
                "Final tone must elevate cingulate hierarchy position",
            ),
            version="2.0.0",
            paper_count=1,
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
