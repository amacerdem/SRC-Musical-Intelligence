"""
STC -- Sensorimotor Timing Calibration.

Gamma-3 model of the MPU.  Proposes that singing training increases
resting-state connectivity between insula and speech/respiratory
sensorimotor areas, suggesting enhanced interoceptive-motor integration.

Output: 10D per frame (172.27 Hz).
Mechanisms: BEP (Beat Entrainment Processing).
Evidence: Singing training enhances insula-sensorimotor connectivity.
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


class STC(BaseModel):
    """Sensorimotor Timing Calibration -- singing training connectivity."""

    NAME = "STC"
    FULL_NAME = "Sensorimotor Timing Calibration"
    UNIT = "MPU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f28_interoceptive_motor_coupling", "f29_respiratory_control",
            "f30_vocal_precision",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "insula_connectivity_fn", "breathing_vocal_coupling",
        )),
        LayerSpec("P", "Present Processing", 5, 7, (
            "interoceptive_state", "vocal_motor_state",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "connectivity_change_pred", "vocal_improvement_pred",
            "respiratory_efficiency_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f28_interoceptive_motor_coupling", "f29_respiratory_control",
            "f30_vocal_precision",
            # Layer M -- Mathematical
            "insula_connectivity_fn", "breathing_vocal_coupling",
            # Layer P -- Present
            "interoceptive_state", "vocal_motor_state",
            # Layer F -- Future
            "connectivity_change_pred", "vocal_improvement_pred",
            "respiratory_efficiency_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -6, 58),
                brodmann_area=6,
                function="Speech motor planning for singing",
                evidence_count=2,
            ),
            BrainRegion(
                name="Premotor Cortex",
                abbreviation="PMC",
                hemisphere="bilateral",
                mni_coords=(-40, -8, 54),
                brodmann_area=6,
                function="Respiratory-motor coordination",
                evidence_count=1,
            ),
            BrainRegion(
                name="Cerebellum",
                abbreviation="CB",
                hemisphere="bilateral",
                mni_coords=(24, -64, -28),
                function="Vocal timing calibration",
                evidence_count=1,
            ),
            BrainRegion(
                name="Putamen",
                abbreviation="PUT",
                hemisphere="bilateral",
                mni_coords=(-24, 4, 4),
                function="Interoceptive-motor integration gating",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Kleber", 2023,
                         "Singing training increases insula-sensorimotor connectivity",
                         ""),
                Citation("Zarate", 2010,
                         "Neural regulation of singing voice", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.45, 0.65),
            falsification_criteria=(
                "Singing-specific connectivity change should differ from speech",
                "Insula-sensorimotor coupling must increase with training",
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
