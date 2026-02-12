"""
MPFS -- Musical Prodigy Flow State.

Gamma-5 model of the STU.  Proposes that musical prodigies are distinguished
from non-prodigies not by intelligence (IQ), but by their propensity for
flow states during musical performance (r=0.47), emerging when motor
automaticity (BEP) meets structural mastery (TMH).

Output: 10D per frame (172.27 Hz).
Mechanisms: BEP.
Evidence: Csikszentmihalyi 1990, Ruthsatz & Detterman 2003.
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


class MPFS(BaseModel):
    """Musical Prodigy Flow State -- flow via automaticity-mastery balance."""

    NAME = "MPFS"
    FULL_NAME = "Musical Prodigy Flow State"
    UNIT = "STU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_flow_propensity", "f02_challenge_skill_balance",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "flow_index", "automaticity_level",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "motor_automaticity", "structural_mastery", "absorption_state",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "flow_stability_pred", "performance_trajectory", "mastery_forecast",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_flow_propensity", "f02_challenge_skill_balance",
            "flow_index", "automaticity_level",
            "motor_automaticity", "structural_mastery", "absorption_state",
            "flow_stability_pred", "performance_trajectory", "mastery_forecast",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Dorsolateral Prefrontal Cortex",
                abbreviation="dlPFC",
                hemisphere="bilateral",
                mni_coords=(-44, 30, 28),
                function="Transient hypofrontality during flow states",
                evidence_count=2,
            ),
            BrainRegion(
                name="Basal Ganglia",
                abbreviation="BG",
                hemisphere="bilateral",
                mni_coords=(14, 8, 4),
                function="Motor automaticity enabling flow entry",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Csikszentmihalyi", 1990,
                         "Flow: optimal experience via challenge-skill balance", ""),
                Citation("Ruthsatz", 2003,
                         "Musical prodigies: flow propensity, not IQ",
                         "r=0.47"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.65),
            falsification_criteria=(
                "Flow propensity must predict prodigy status better than IQ",
                "Challenge-skill balance must be measurable in real-time",
            ),
            version="2.0.0",
            paper_count=3,
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
