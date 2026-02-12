"""
VMM -- Valence-Mode Mapping.

Alpha-3 model of the ARU.  Models how musical mode (major/minor) and
consonance systematically activate distinct neural circuits that produce
emotional valence -- the "happy or sad" dimension of musical emotion.

Output: 12D per frame (172.27 Hz).
Mechanisms: AED, C0P.
Evidence: 14+ papers + k=70 meta-analytic, double dissociation (Mitterschiffthaler 2007).
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


class VMM(BaseModel):
    """Valence-Mode Mapping -- perceived emotion from mode/consonance."""

    NAME = "VMM"
    FULL_NAME = "Valence-Mode Mapping"
    UNIT = "ARU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("AED", "C0P")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("V", "Valence Core", 0, 3, (
            "f03_valence", "mode_signal", "consonance_valence",
        )),
        LayerSpec("R", "Regional Pathways", 3, 7, (
            "happy_pathway", "sad_pathway", "parahippocampal",
            "reward_evaluation",
        )),
        LayerSpec("P", "Perceived Emotion", 7, 10, (
            "perceived_happy", "perceived_sad", "emotion_certainty",
        )),
        LayerSpec("F", "Forecast", 10, 12, (
            "valence_forecast", "mode_shift_proximity",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        """Placeholder -- ~7 H3 tuples required (VMM-specific direct reads)."""
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer V -- Valence
            "f03_valence", "mode_signal", "consonance_valence",
            # Layer R -- Regional
            "happy_pathway", "sad_pathway", "parahippocampal",
            "reward_evaluation",
            # Layer P -- Perceived Emotion
            "perceived_happy", "perceived_sad", "emotion_certainty",
            # Layer F -- Forecast
            "valence_forecast", "mode_shift_proximity",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Ventral Striatum",
                abbreviation="VS",
                hemisphere="bilateral",
                mni_coords=(8, 4, -6),
                function="Reward circuit for major/consonant music",
                evidence_count=5,
            ),
            BrainRegion(
                name="Hippocampus",
                abbreviation="HIP",
                hemisphere="bilateral",
                mni_coords=(20, -15, -20),
                function="Memory-emotion circuit for minor/dissonant music",
                evidence_count=5,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(-10, 38, 14),
                brodmann_area=32,
                function="Reward evaluation and affect monitoring",
                evidence_count=4,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Mitterschiffthaler", 2007,
                         "Double dissociation: happy->VS, sad->HIP",
                         "t=4.58-4.88"),
                Citation("Koelsch", 2006,
                         "Consonant->VS (t=5.1), Dissonant->AMY (t=4.7)",
                         "t=4.2-6.9"),
                Citation("Fritz", 2009,
                         "Cross-cultural mode-valence recognition (Mafa)",
                         "F(2,39)=15.48"),
                Citation("Brattico", 2011,
                         "Perceived != felt emotion: separable circuits",
                         "Z>=3.5"),
                Citation("Carraturo", 2025,
                         "k=70 meta-analysis: major=positive, minor=negative",
                         "k=70"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.96),
            falsification_criteria=(
                "Major-mode passages must activate reward circuit more than minor",
                "Cross-cultural listeners must show same neural hierarchy direction",
                "Perceived happy must dissociate from felt pleasure (SRP)",
            ),
            version="2.0.0",
            paper_count=14,
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
