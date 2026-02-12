"""
CSG -- Cortical Salience Gating.

Alpha-3 model of the ASU.  Models how dissonance level systematically
modulates salience network activation: strong dissonance activates ACC/insula,
intermediate dissonance increases sensory processing in Heschl's gyrus,
and consonance enables efficient processing with positive valence.

Output: 11D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Bravo 2017 (d=5.16 salience), Sarasso 2019 (d=2.008).
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


class CSG(BaseModel):
    """Cortical Salience Gating -- consonance-salience gradient."""

    NAME = "CSG"
    FULL_NAME = "Cortical Salience Gating"
    UNIT = "ASU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f07_salience_activation", "f08_sensory_evidence",
            "f09_consonance_valence",
        )),
        LayerSpec("M", "Mathematical Model", 3, 6, (
            "salience_response", "rt_valence_judgment",
            "aesthetic_appreciation",
        )),
        LayerSpec("P", "Present Processing", 6, 9, (
            "salience_network", "affective_evaluation",
            "sensory_load",
        )),
        LayerSpec("F", "Future Predictions", 9, 11, (
            "valence_judgment_pred", "processing_demand_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f07_salience_activation", "f08_sensory_evidence",
            "f09_consonance_valence",
            # Layer M -- Mathematical
            "salience_response", "rt_valence_judgment",
            "aesthetic_appreciation",
            # Layer P -- Present
            "salience_network", "affective_evaluation",
            "sensory_load",
            # Layer F -- Future
            "valence_judgment_pred", "processing_demand_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Salience network hub -- dissonance detection",
                evidence_count=3,
            ),
            BrainRegion(
                name="Anterior Insula",
                abbreviation="AI",
                hemisphere="bilateral",
                mni_coords=(34, 18, -4),
                brodmann_area=13,
                function="Salience network -- arousal/interoception",
                evidence_count=2,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Consonance evaluation and decision making",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bravo", 2017,
                         "Strong dissonance activates ACC and bilateral AI",
                         "d=5.16"),
                Citation("Sarasso", 2019,
                         "ERP correlates of consonant vs dissonant intervals",
                         "d=2.008"),
                Citation("Plomp", 1965,
                         "Tonal consonance and critical bandwidth", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.88, 0.95),
            falsification_criteria=(
                "Parametric consonance should produce graded salience response",
                "Intermediate consonance should yield longest reaction times",
                "Consonance-valence relationship should be monotonic",
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
