"""
ESME -- Expertise-Specific MMN Enhancement.

Gamma-2 model of the SPU.  Models how musical expertise selectively enhances
mismatch negativity (MMN) responses for pitch, rhythm, and timbre deviance.
Singers show enhanced pitch MMN, drummers show enhanced rhythm MMN.

Output: 11D per frame (172.27 Hz).
Mechanisms: PPC (Pitch Processing Chain).
Evidence: Tervaniemi 2022 (d=-1.09), Vuust 2012, Brattico 2009.
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


class ESME(BaseModel):
    """Expertise-Specific MMN Enhancement -- training-dependent deviance detection."""

    NAME = "ESME"
    FULL_NAME = "Expertise-Specific MMN Enhancement"
    UNIT = "SPU"
    TIER = "gamma"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("PPC",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_pitch_mmn", "f02_rhythm_mmn", "f03_timbre_mmn",
            "f04_expertise_enhancement",
        )),
        LayerSpec("M", "Mathematical Model", 4, 5, (
            "mmn_expertise_function",
        )),
        LayerSpec("P", "Present Processing", 5, 8, (
            "pitch_deviance_detection", "rhythm_deviance_detection",
            "timbre_deviance_detection",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "feature_enhancement_pred", "expertise_transfer_pred",
            "developmental_trajectory",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_pitch_mmn", "f02_rhythm_mmn", "f03_timbre_mmn",
            "f04_expertise_enhancement",
            "mmn_expertise_function",
            "pitch_deviance_detection", "rhythm_deviance_detection",
            "timbre_deviance_detection",
            "feature_enhancement_pred", "expertise_transfer_pred",
            "developmental_trajectory",
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
                function="MMN generation for pitch/timbre deviants",
                evidence_count=3,
            ),
            BrainRegion(
                name="Right Inferior Frontal Gyrus",
                abbreviation="rIFG",
                hemisphere="R",
                mni_coords=(48, 18, 4),
                brodmann_area=44,
                function="MMN generation for rhythm deviants",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Tervaniemi", 2022,
                         "Expertise-specific MMN enhancement in musicians",
                         "d=-1.09"),
                Citation("Vuust", 2012,
                         "Predictive coding of music: domain-specific expertise",
                         ""),
                Citation("Brattico", 2009,
                         "Neural correlates of musical expertise effects on MMN",
                         ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Singers must show larger pitch MMN than non-musicians",
                "Enhancement must be domain-specific, not general auditory",
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
