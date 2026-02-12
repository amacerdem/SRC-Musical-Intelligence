"""
AMSC -- Auditory-Motor Stream Coupling.

Alpha-2 model of the STU.  Models the rapid auditory-to-motor pathway where
high-gamma activity in auditory cortex precedes premotor/motor cortex activity
by ~110 ms, establishing a direct sensorimotor link during music processing.

Output: 12D per frame (172.27 Hz).
Mechanisms: BEP, TMH.
Evidence: Potes 2012 (r=0.49), Zatorre 2007.
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


class AMSC(BaseModel):
    """Auditory-Motor Stream Coupling -- 110 ms auditory-motor pathway."""

    NAME = "AMSC"
    FULL_NAME = "Auditory-Motor Stream Coupling"
    UNIT = "STU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("BEP", "TMH")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f01_gamma_coupling", "f02_motor_lag", "f03_dorsal_stream",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "coupling_strength", "transfer_delay",
        )),
        LayerSpec("P", "Present Processing", 5, 9, (
            "pstg_gamma", "premotor_activation", "motor_readiness",
            "sensorimotor_binding",
        )),
        LayerSpec("F", "Future Predictions", 9, 12, (
            "motor_anticipation", "rhythm_predict", "coupling_forecast",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_gamma_coupling", "f02_motor_lag", "f03_dorsal_stream",
            "coupling_strength", "transfer_delay",
            "pstg_gamma", "premotor_activation", "motor_readiness",
            "sensorimotor_binding",
            "motor_anticipation", "rhythm_predict", "coupling_forecast",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Posterior Superior Temporal Gyrus",
                abbreviation="pSTG",
                hemisphere="bilateral",
                mni_coords=(60, -28, 10),
                function="High-gamma auditory encoding preceding motor cortex",
                evidence_count=4,
            ),
            BrainRegion(
                name="Premotor Cortex",
                abbreviation="PMC",
                hemisphere="bilateral",
                mni_coords=(-46, 0, 50),
                function="Motor preparation receiving auditory input at 110 ms lag",
                evidence_count=3,
            ),
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -6, 62),
                function="Beat-based motor timing and auditory-motor integration",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Potes", 2012,
                         "pSTG high-gamma correlates with sound intensity",
                         "r=0.49"),
                Citation("Zatorre", 2007,
                         "Dorsal auditory-motor stream for music production", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Motor cortex lag must be approximately 110 ms behind pSTG",
                "Dorsal stream lesions should disrupt auditory-motor coupling",
            ),
            version="2.0.0",
            paper_count=5,
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
