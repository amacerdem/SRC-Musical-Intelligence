"""
AACM -- Auditory Attention Control Model.

Beta-3 model of the ASU.  Models the bidirectional relationship between
aesthetic appreciation and attentional engagement: appreciated musical
intervals enhance N1/P2 engagement and N2/P3 motor inhibition, producing
a "savoring" effect with slower reaction times for preferred stimuli.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Sarasso 2019 (d=2.008 consonant > dissonant appreciation).
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


class AACM(BaseModel):
    """Auditory Attention Control Model -- aesthetic-attention coupling."""

    NAME = "AACM"
    FULL_NAME = "Auditory Attention Control Model"
    UNIT = "ASU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f16_attentional_engagement", "f17_motor_inhibition",
            "f18_savoring_effect",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "aesthetic_engagement", "rt_appreciation",
        )),
        LayerSpec("P", "Present Processing", 5, 7, (
            "n1p2_engagement", "aesthetic_judgment",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "behavioral_response_pred", "n2p3_inhibition_pred",
            "aesthetic_rating_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f16_attentional_engagement", "f17_motor_inhibition",
            "f18_savoring_effect",
            # Layer M -- Mathematical
            "aesthetic_engagement", "rt_appreciation",
            # Layer P -- Present
            "n1p2_engagement", "aesthetic_judgment",
            # Layer F -- Future
            "behavioral_response_pred", "n2p3_inhibition_pred",
            "aesthetic_rating_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Aesthetic evaluation and motor inhibition",
                evidence_count=2,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="N1/P2 attentional engagement to intervals",
                evidence_count=3,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Conflict monitoring during savoring response",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Sarasso", 2019,
                         "ERP correlates of aesthetic experience to intervals",
                         "d=2.008"),
                Citation("Brattico", 2009,
                         "Neural correlates of musical pleasantness", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Appreciated intervals must enhance N1/P2 amplitude",
                "RT should be slower for preferred intervals (savoring)",
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
