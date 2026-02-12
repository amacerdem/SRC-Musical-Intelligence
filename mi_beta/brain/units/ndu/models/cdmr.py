"""
CDMR -- Context-Dependent Mismatch Response.

Beta-2 model of the NDU.  Models how musical expertise enhances mismatch
responses selectively in complex melodic contexts (not in simple oddball
paradigms), revealing that expertise enhances integrated processing.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis), TMH (Temporal Memory Hierarchy).
Evidence: Musicians show enhanced MMR only in complex melodic contexts.
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


class CDMR(BaseModel):
    """Context-Dependent Mismatch Response -- expertise-context interaction."""

    NAME = "CDMR"
    FULL_NAME = "Context-Dependent Mismatch Response"
    UNIT = "NDU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA", "TMH")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_mismatch_amplitude", "f02_context_modulation",
            "f03_subadditivity_index", "f04_expertise_effect",
        )),
        LayerSpec("M", "Mathematical Model", 4, 6, (
            "melodic_context", "deviance_history",
        )),
        LayerSpec("P", "Present Processing", 6, 8, (
            "mismatch_signal", "context_modulation_state",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "next_deviance_pred", "context_continuation_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_mismatch_amplitude", "f02_context_modulation",
            "f03_subadditivity_index", "f04_expertise_effect",
            # Layer M -- Mathematical
            "melodic_context", "deviance_history",
            # Layer P -- Present
            "mismatch_signal", "context_modulation_state",
            # Layer F -- Future
            "next_deviance_pred", "context_continuation_pred",
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
                function="MMN generation -- context-dependent enhancement",
                evidence_count=3,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="R",
                mni_coords=(48, 18, 4),
                brodmann_area=44,
                function="Context integration and expertise gating",
                evidence_count=2,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Mismatch evaluation in complex contexts",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Putkinen", 2014,
                         "Musicians show enhanced MMR in complex melodic contexts",
                         ""),
                Citation("Tervaniemi", 2014,
                         "Expertise enhances integrated not basic deviance detection",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.72, 0.88),
            falsification_criteria=(
                "Expertise enhancement must be context-dependent",
                "Simple oddball should not show expertise differences",
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
