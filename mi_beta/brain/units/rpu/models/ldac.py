"""
LDAC -- Listener-Dependent Aesthetic Computation.

Gamma-1 model of the RPU (Reward Processing Unit).  Proposes that auditory
cortex (R STG) activity tracks moment-to-moment liking, suggesting
pleasure-dependent modulation of sensory processing.

Output: 10D per frame (172.27 Hz).
Mechanisms: AED (Affective Entrainment Dynamics).
Evidence: Gold 2023 fMRI (d=1.22, n=24, preliminary).
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


class LDAC(BaseModel):
    """Listener-Dependent Aesthetic Computation -- liking-dependent auditory cortex."""

    NAME = "LDAC"
    FULL_NAME = "Listener-Dependent Aesthetic Computation"
    UNIT = "RPU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("AED",)
    CROSS_UNIT_READS = ("ARU",)

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_stg_liking_coupling", "f02_pleasure_gating",
            "f03_ic_liking_interaction", "f04_moment_to_moment",
        )),
        LayerSpec("M", "Mathematical Model", 4, 6, (
            "stg_bold_liking_slope", "sensory_gating_strength",
        )),
        LayerSpec("P", "Present Processing", 6, 8, (
            "stg_modulation_state", "pleasure_feedback",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "sensory_gating_pred", "liking_trajectory_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_stg_liking_coupling", "f02_pleasure_gating",
            "f03_ic_liking_interaction", "f04_moment_to_moment",
            # Layer M -- Mathematical
            "stg_bold_liking_slope", "sensory_gating_strength",
            # Layer P -- Present
            "stg_modulation_state", "pleasure_feedback",
            # Layer F -- Future
            "sensory_gating_pred", "liking_trajectory_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Right Superior Temporal Gyrus",
                abbreviation="R-STG",
                hemisphere="right",
                mni_coords=(60, -20, 4),
                brodmann_area=22,
                function="Moment-to-moment liking tracking",
                evidence_count=2,
            ),
            BrainRegion(
                name="Orbitofrontal Cortex",
                abbreviation="OFC",
                hemisphere="bilateral",
                mni_coords=(28, 34, -12),
                brodmann_area=11,
                function="Top-down pleasure gating of sensory cortex",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Gold", 2023,
                         "R STG activity tracks moment-to-moment liking",
                         "d=1.22"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.68),
            falsification_criteria=(
                "R STG must correlate with continuous liking ratings",
                "Pleasure must modulate sensory processing in auditory cortex",
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
