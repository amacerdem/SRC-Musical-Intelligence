"""
SPMC -- Sensory-Predictive Motor Coupling.

Beta-4 model of the MPU.  Models how motor planning for music is primarily
mediated by a core hierarchical SMA-premotor-M1 circuit, with temporal
encoding in SMA and execution in M1.

Output: 10D per frame (172.27 Hz).
Mechanisms: BEP (Beat Entrainment Processing).
Evidence: SMA-PMC-M1 hierarchical motor circuit for music.
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


class SPMC(BaseModel):
    """Sensory-Predictive Motor Coupling -- SMA-premotor-M1 circuit."""

    NAME = "SPMC"
    FULL_NAME = "Sensory-Predictive Motor Coupling"
    UNIT = "MPU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f19_sma_temporal_encoding", "f20_pmc_sequence_planning",
            "f21_m1_execution_precision",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "hierarchical_flow_fn", "timing_precision",
        )),
        LayerSpec("P", "Present Processing", 5, 7, (
            "sma_pmc_m1_state", "motor_sequence_complexity",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "sequence_execution_pred", "timing_accuracy_pred",
            "circuit_efficiency_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f19_sma_temporal_encoding", "f20_pmc_sequence_planning",
            "f21_m1_execution_precision",
            # Layer M -- Mathematical
            "hierarchical_flow_fn", "timing_precision",
            # Layer P -- Present
            "sma_pmc_m1_state", "motor_sequence_complexity",
            # Layer F -- Future
            "sequence_execution_pred", "timing_accuracy_pred",
            "circuit_efficiency_pred",
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
                function="Temporal encoding -- sequence timing",
                evidence_count=3,
            ),
            BrainRegion(
                name="Premotor Cortex",
                abbreviation="PMC",
                hemisphere="bilateral",
                mni_coords=(-40, -8, 54),
                brodmann_area=6,
                function="Sequence planning -- motor program selection",
                evidence_count=3,
            ),
            BrainRegion(
                name="Putamen",
                abbreviation="PUT",
                hemisphere="bilateral",
                mni_coords=(-24, 4, 4),
                function="Motor execution gating",
                evidence_count=2,
            ),
            BrainRegion(
                name="Cerebellum",
                abbreviation="CB",
                hemisphere="bilateral",
                mni_coords=(24, -64, -28),
                function="Execution precision and error correction",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Chen", 2008,
                         "SMA-PMC-M1 hierarchical motor circuit",
                         ""),
                Citation("Zatorre", 2007,
                         "Auditory-motor interaction in music performance",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.72, 0.88),
            falsification_criteria=(
                "SMA lesions should impair temporal encoding but not execution",
                "Hierarchical flow from SMA to M1 must be directional",
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
