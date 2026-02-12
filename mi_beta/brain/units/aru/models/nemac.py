"""
NEMAC -- Nostalgia-Enhanced Memory-Affect Coupling.

Beta-4 model of the ARU.  Models how familiar/self-relevant music triggers
hippocampal-mPFC co-activation that enhances emotional response through
autobiographical memory retrieval (nostalgia pathway).

Output: 11D per frame (172.27 Hz).
Mechanisms: AED, MEM (Memory Integration).
Evidence: Sakakibara 2025 (d=0.711), Janata 2007, Salimpoor 2011.
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


class NEMAC(BaseModel):
    """Nostalgia-Enhanced Memory-Affect Coupling -- nostalgia pathway."""

    NAME = "NEMAC"
    FULL_NAME = "Nostalgia-Enhanced Memory-Affect Coupling"
    UNIT = "ARU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("AED", "MEM")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f05_chills", "f11_nostalgia",
        )),
        LayerSpec("M", "Memory Integration", 2, 5, (
            "mpfc_activation", "hippocampus_activation", "memory_vividness",
        )),
        LayerSpec("W", "Well-being", 5, 7, (
            "nostalgia_intensity", "wellbeing_enhancement",
        )),
        LayerSpec("P", "Present Processing", 7, 9, (
            "nostalgia_correlation", "memory_reward_link",
        )),
        LayerSpec("F", "Future Predictions", 9, 11, (
            "wellbeing_pred", "vividness_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f05_chills", "f11_nostalgia",
            "mpfc_activation", "hippocampus_activation", "memory_vividness",
            "nostalgia_intensity", "wellbeing_enhancement",
            "nostalgia_correlation", "memory_reward_link",
            "wellbeing_pred", "vividness_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Medial Prefrontal Cortex",
                abbreviation="mPFC",
                hemisphere="bilateral",
                mni_coords=(0, 52, 10),
                brodmann_area=10,
                function="Self-referential processing (this is MY music)",
                evidence_count=4,
            ),
            BrainRegion(
                name="Hippocampus",
                abbreviation="HIP",
                hemisphere="bilateral",
                mni_coords=(20, -15, -20),
                function="Episodic memory retrieval / pattern completion",
                evidence_count=5,
            ),
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(8, 4, -6),
                function="Reward from memory-affect convergence",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Sakakibara", 2025,
                         "Nostalgia-enhanced emotional response to music",
                         "d=0.711"),
                Citation("Janata", 2007,
                         "mPFC mediates music-evoked autobiographical memories",
                         ""),
                Citation("Salimpoor", 2011,
                         "Chills correlate with DA release", "r=0.84"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Familiar music must produce stronger nostalgia than novel",
                "mPFC and hippocampus must co-activate during nostalgic episodes",
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
