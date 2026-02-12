"""
CLAM -- Cognitive-Load-Arousal Modulation.

Beta-2 model of the ARU.  Models closed-loop brain-computer interface (BCI)
modulation of affective state via music.  EEG-decoded affect drives real-time
music parameter adjustment through a P-control law.

Output: 11D per frame (172.27 Hz).
Mechanisms: AED.
Evidence: Ehrlich 2019 (r=0.74 arousal, r=0.52 valence), Daly 2015.
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


class CLAM(BaseModel):
    """Cognitive-Load-Arousal Modulation -- BCI affective control loop."""

    NAME = "CLAM"
    FULL_NAME = "Cognitive-Load-Arousal Modulation"
    UNIT = "ARU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("AED",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f09_affective_modulation", "loop_coherence",
        )),
        LayerSpec("B", "BCI State", 2, 5, (
            "decoded_affect", "target_affect", "affect_error",
        )),
        LayerSpec("C", "Control Outputs", 5, 7, (
            "control_output", "music_param_delta",
        )),
        LayerSpec("P", "Present Processing", 7, 9, (
            "arousal_modulation", "valence_tracking",
        )),
        LayerSpec("F", "Future Predictions", 9, 11, (
            "target_affect_pred", "modulation_success",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f09_affective_modulation", "loop_coherence",
            "decoded_affect", "target_affect", "affect_error",
            "control_output", "music_param_delta",
            "arousal_modulation", "valence_tracking",
            "target_affect_pred", "modulation_success",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Prefrontal Cortex",
                abbreviation="PFC",
                hemisphere="bilateral",
                mni_coords=(-40, 30, 20),
                brodmann_area=46,
                function="EEG gamma-band decode for affective state",
                evidence_count=3,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(-10, 38, 14),
                brodmann_area=32,
                function="Affect error monitoring and control",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Ehrlich", 2019,
                         "Closed-loop BCI affective modulation via music",
                         "r=0.74"),
                Citation("Daly", 2015,
                         "EEG-based music BCI for affective regulation", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Control loop must converge: affect error should decrease over time",
                "Music parameter changes must produce measurable EEG shift",
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
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
