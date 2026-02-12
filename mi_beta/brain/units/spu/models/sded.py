"""
SDED -- Sensory Dissonance Early Detection.

Gamma-3 model of the SPU.  Models pre-attentive sensory dissonance detection
at the earliest cortical level, including the dissociation between neural
detection (expertise-independent) and behavioral accuracy (expertise-dependent).

Output: 10D per frame (172.27 Hz).
Mechanisms: PPC (Pitch Processing Chain).
Evidence: Koelsch 2000, Brattico 2009, Schon 2005.
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


class SDED(BaseModel):
    """Sensory Dissonance Early Detection -- pre-attentive roughness detection."""

    NAME = "SDED"
    FULL_NAME = "Sensory Dissonance Early Detection"
    UNIT = "SPU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f01_early_detection", "f02_mmn_dissonance",
            "f03_behavioral_accuracy",
        )),
        LayerSpec("M", "Mathematical Model", 3, 4, (
            "detection_function",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "roughness_detection", "deviation_detection",
            "behavioral_response",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "dissonance_detection_pred", "behavioral_accuracy_pred",
            "training_effect_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_early_detection", "f02_mmn_dissonance",
            "f03_behavioral_accuracy",
            "detection_function",
            "roughness_detection", "deviation_detection",
            "behavioral_response",
            "dissonance_detection_pred", "behavioral_accuracy_pred",
            "training_effect_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Supratemporal Plane",
                abbreviation="STP",
                hemisphere="bilateral",
                mni_coords=(-54, -22, 8),
                brodmann_area=41,
                function="Pre-attentive dissonance MMN generation",
                evidence_count=2,
            ),
            BrainRegion(
                name="Right Inferior Frontal Gyrus",
                abbreviation="rIFG",
                hemisphere="R",
                mni_coords=(48, 18, 4),
                brodmann_area=44,
                function="Dissonance deviance detection and frontal MMN",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Koelsch", 2000,
                         "Pre-attentive processing of musical syntax violations",
                         ""),
                Citation("Brattico", 2009,
                         "Neural discrimination of non-prototypical chords", ""),
                Citation("Schon", 2005,
                         "Early detection of musical dissonance in AC", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.45, 0.65),
            falsification_criteria=(
                "Neural detection must occur regardless of expertise level",
                "Behavioral accuracy must improve with training while neural stays constant",
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
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
