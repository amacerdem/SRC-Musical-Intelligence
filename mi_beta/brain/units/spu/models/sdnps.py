"""
SDNPS -- Stimulus-Dependent Neural Pitch Scaling.

Gamma-1 model of the SPU.  Models the stimulus dependency of brainstem NPS:
NPS validity degrades for complex/natural timbres compared to simple/synthetic
stimuli.  Roughness correlation is stimulus-invariant (r=-0.57).

Output: 10D per frame (172.27 Hz).
Mechanisms: PPC (Pitch Processing Chain).
Evidence: Cousineau 2015 (r=0.34->-0.10 degradation), Bidelman 2009.
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


class SDNPS(BaseModel):
    """Stimulus-Dependent Neural Pitch Scaling -- NPS generalization limits."""

    NAME = "SDNPS"
    FULL_NAME = "Stimulus-Dependent Neural Pitch Scaling"
    UNIT = "SPU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f01_nps_value", "f02_stimulus_dependency",
            "f03_roughness_correlation",
        )),
        LayerSpec("M", "Mathematical Model", 3, 4, (
            "nps_stimulus_function",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "ffr_encoding", "harmonicity_proxy", "roughness_interference",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "behavioral_consonance_pred", "roughness_response_pred",
            "generalization_limit",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_nps_value", "f02_stimulus_dependency",
            "f03_roughness_correlation",
            "nps_stimulus_function",
            "ffr_encoding", "harmonicity_proxy", "roughness_interference",
            "behavioral_consonance_pred", "roughness_response_pred",
            "generalization_limit",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Inferior Colliculus",
                abbreviation="IC",
                hemisphere="bilateral",
                mni_coords=(0, -32, -8),
                function="FFR encoding -- stimulus-dependent NPS",
                evidence_count=2,
            ),
            BrainRegion(
                name="Auditory Nerve",
                abbreviation="AN",
                hemisphere="bilateral",
                mni_coords=(0, -38, -40),
                function="Peripheral encoding limits for complex timbres",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Cousineau", 2015,
                         "NPS-consonance correlation degrades with spectral complexity",
                         "r=0.34 to -0.10"),
                Citation("Bidelman", 2009,
                         "FFR pitch salience for simple stimuli",
                         "r=0.81"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.45, 0.65),
            falsification_criteria=(
                "Roughness-NPS correlation must be invariant across stimulus types",
                "NPS validity must decrease as spectral complexity increases",
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
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
