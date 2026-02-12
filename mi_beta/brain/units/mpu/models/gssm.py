"""
GSSM -- Groove-State Sensorimotor Model.

Alpha-3 model of the MPU.  Demonstrates how simultaneous stimulation of
SMA and M1 synchronized to gait phase reduces stride variability and
improves balance in neurological patients.

Output: 11D per frame (172.27 Hz).
Mechanisms: BEP (Beat Entrainment Processing).
Evidence: Gait-synchronized dual-site stimulation reduces stride CV.
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


class GSSM(BaseModel):
    """Groove-State Sensorimotor Model -- gait-synchronized stimulation."""

    NAME = "GSSM"
    FULL_NAME = "Groove-State Sensorimotor Model"
    UNIT = "MPU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f07_stride_variability", "f08_balance_control",
            "f09_dual_site_coupling",
        )),
        LayerSpec("M", "Mathematical Model", 3, 6, (
            "sma_m1_coupling_fn", "cv_stride_t",
            "phase_sync_index",
        )),
        LayerSpec("P", "Present Processing", 6, 9, (
            "gait_phase_state", "sma_m1_sync_strength",
            "stride_regularity",
        )),
        LayerSpec("F", "Future Predictions", 9, 11, (
            "next_stride_pred", "balance_stability_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f07_stride_variability", "f08_balance_control",
            "f09_dual_site_coupling",
            # Layer M -- Mathematical
            "sma_m1_coupling_fn", "cv_stride_t",
            "phase_sync_index",
            # Layer P -- Present
            "gait_phase_state", "sma_m1_sync_strength",
            "stride_regularity",
            # Layer F -- Future
            "next_stride_pred", "balance_stability_pred",
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
                function="Temporal encoding for gait phase",
                evidence_count=3,
            ),
            BrainRegion(
                name="Putamen",
                abbreviation="PUT",
                hemisphere="bilateral",
                mni_coords=(-24, 4, 4),
                function="Gait timing and rhythm regulation",
                evidence_count=2,
            ),
            BrainRegion(
                name="Cerebellum",
                abbreviation="CB",
                hemisphere="bilateral",
                mni_coords=(24, -64, -28),
                function="Balance control and stride calibration",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Wessel", 2023,
                         "Dual-site SMA+M1 stimulation reduces stride variability",
                         ""),
                Citation("Thaut", 2015,
                         "Rhythmic auditory stimulation for gait rehabilitation",
                         ""),
                Citation("Grahn", 2009,
                         "Basal ganglia and beat processing", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.88, 0.95),
            falsification_criteria=(
                "SMA+M1 stimulation must reduce stride CV more than single-site",
                "Phase-synchronized stimulation must outperform random",
                "Balance improvements must correlate with coupling strength",
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
