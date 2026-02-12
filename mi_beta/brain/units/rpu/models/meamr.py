"""
MEAMR -- Memory-Affect Modulated Reward.

Beta-3 model of the RPU (Reward Processing Unit).  Models how familiar music
activates dorsal medial prefrontal cortex (dMPFC) in proportion to
autobiographical salience, integrating musical structure with self-referential
processing and reward.

Output: 10D per frame (172.27 Hz).
Mechanisms: MEM (Memory), AED (Affective Entrainment Dynamics).
Evidence: Janata 2009, multiple autobiographical memory studies.
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


class MEAMR(BaseModel):
    """Memory-Affect Modulated Reward -- music-evoked autobiographical memory reward."""

    NAME = "MEAMR"
    FULL_NAME = "Memory-Affect Modulated Reward"
    UNIT = "RPU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("MEM", "AED")
    CROSS_UNIT_READS = ("ARU",)

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_familiarity_index", "f02_autobio_salience",
            "f03_dmpfc_tracking", "f04_positive_affect",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "familiarity_gradient", "salience_score",
            "memory_reward_coupling",
        )),
        LayerSpec("P", "Present Processing", 7, 8, (
            "memory_activation_state",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "nostalgia_response_pred", "affect_persistence_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_familiarity_index", "f02_autobio_salience",
            "f03_dmpfc_tracking", "f04_positive_affect",
            # Layer M -- Mathematical
            "familiarity_gradient", "salience_score",
            "memory_reward_coupling",
            # Layer P -- Present
            "memory_activation_state",
            # Layer F -- Future
            "nostalgia_response_pred", "affect_persistence_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Ventromedial Prefrontal Cortex",
                abbreviation="vmPFC",
                hemisphere="bilateral",
                mni_coords=(0, 46, -10),
                brodmann_area=11,
                function="Self-referential processing and reward",
                evidence_count=3,
            ),
            BrainRegion(
                name="Caudate Nucleus",
                abbreviation="Caudate",
                hemisphere="bilateral",
                mni_coords=(10, 10, 8),
                function="Familiarity-reward coupling",
                evidence_count=2,
            ),
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(10, 8, -8),
                function="Nostalgia-driven hedonic response",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Janata", 2009,
                         "dMPFC tracks autobiographical salience during familiar music",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.72, 0.85),
            falsification_criteria=(
                "dMPFC activity must correlate with autobiographical salience ratings",
                "Unfamiliar music should not activate autobiographical network",
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
