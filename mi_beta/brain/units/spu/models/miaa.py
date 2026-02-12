"""
MIAA -- Musical Imagery Auditory Activation.

Beta-3 model of the SPU.  Models auditory cortex activation during musical
imagery (internal hearing without external sound), including familiarity-
dependent enhancement in BA22 and content-type modulation.

Output: 11D per frame (172.27 Hz).
Mechanisms: TPC (Timbre Processing Chain).
Evidence: Kraemer 2005 (p<0.0001, p<0.0005), Zatorre 2007, Halpern 2004.
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


class MIAA(BaseModel):
    """Musical Imagery Auditory Activation -- AC during internal hearing."""

    NAME = "MIAA"
    FULL_NAME = "Musical Imagery Auditory Activation"
    UNIT = "SPU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("TPC",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f01_imagery_activation", "f02_familiarity_enhancement",
            "f03_a1_modulation",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "activation_function", "familiarity_effect",
        )),
        LayerSpec("P", "Present Processing", 5, 8, (
            "melody_retrieval", "continuation_prediction",
            "phrase_structure",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "melody_continuation_pred", "ac_activation_pred",
            "recognition_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_imagery_activation", "f02_familiarity_enhancement",
            "f03_a1_modulation",
            "activation_function", "familiarity_effect",
            "melody_retrieval", "continuation_prediction",
            "phrase_structure",
            "melody_continuation_pred", "ac_activation_pred",
            "recognition_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Secondary Auditory Cortex (BA22)",
                abbreviation="A2",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Auditory cortex active during imagery silence",
                evidence_count=3,
            ),
            BrainRegion(
                name="Primary Auditory Cortex",
                abbreviation="A1",
                hemisphere="bilateral",
                mni_coords=(-48, -22, 8),
                brodmann_area=41,
                function="Content-type modulation (instrumental > lyrics)",
                evidence_count=3,
            ),
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -2, 62),
                brodmann_area=6,
                function="Motor imagery component of musical playback",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Kraemer", 2005,
                         "AC active during silent gaps in familiar music",
                         "p<0.0001"),
                Citation("Zatorre", 2007,
                         "When the brain plays music: auditory-motor imagery",
                         ""),
                Citation("Halpern", 2004,
                         "Behavioral and neural correlates of musical imagery",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.72, 0.85),
            falsification_criteria=(
                "Familiar music must produce stronger AC activation during gaps",
                "Instrumental passages should modulate A1 more than vocal/lyrics",
            ),
            version="2.0.0",
            paper_count=6,
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
