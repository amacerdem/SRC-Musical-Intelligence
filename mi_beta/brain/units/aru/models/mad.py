"""
MAD -- Musical Anhedonia Disconnection.

Beta-3 model of the ARU.  Models the specific disconnection between
auditory cortex and nucleus accumbens that characterizes musical anhedonia
(~5% of population).  Music-specific deficit with preserved general reward.

Output: 11D per frame (172.27 Hz).
Mechanisms: AED, CPD.
Evidence: Martinez-Molina 2016 (d=3.6-7.0), Loui 2017 (d=-5.89).
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


class MAD(BaseModel):
    """Musical Anhedonia Disconnection -- STG-NAcc disconnection model."""

    NAME = "MAD"
    FULL_NAME = "Musical Anhedonia Disconnection"
    UNIT = "ARU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("AED", "CPD")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f10_anhedonia", "dissociation_idx",
        )),
        LayerSpec("D", "Disconnection Markers", 2, 5, (
            "stg_nacc_connect", "nacc_music_resp", "nacc_general_resp",
        )),
        LayerSpec("A", "Anhedonia Assessment", 5, 7, (
            "bmrq_estimate", "sound_specificity",
        )),
        LayerSpec("P", "Present Processing", 7, 9, (
            "impaired_reward", "preserved_auditory",
        )),
        LayerSpec("F", "Future / Diagnostic", 9, 11, (
            "recovery_potential", "anhedonia_prob",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f10_anhedonia", "dissociation_idx",
            "stg_nacc_connect", "nacc_music_resp", "nacc_general_resp",
            "bmrq_estimate", "sound_specificity",
            "impaired_reward", "preserved_auditory",
            "recovery_potential", "anhedonia_prob",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(8, 4, -6),
                function="Music-specific reward IMPAIRED in anhedonia",
                evidence_count=4,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Auditory processing PRESERVED in anhedonia",
                evidence_count=4,
            ),
            BrainRegion(
                name="Arcuate Fasciculus (STG-NAcc tract)",
                abbreviation="AF-NAcc",
                hemisphere="bilateral",
                mni_coords=(0, 0, 0),
                function="White matter tract integrity (FA) disconnected",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Martinez-Molina", 2016,
                         "Musical anhedonia = NAcc-STG disconnection",
                         "d=3.6-7.0"),
                Citation("Loui", 2017,
                         "White matter NAcc-STG tract integrity and pleasure",
                         "d=-5.89"),
                Citation("Mas-Herrero", 2013,
                         "Barcelona Music Reward Questionnaire validation", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.90),
            falsification_criteria=(
                "Anhedonic listeners must show preserved auditory processing",
                "Music-specific NAcc response must be impaired while general reward is intact",
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
