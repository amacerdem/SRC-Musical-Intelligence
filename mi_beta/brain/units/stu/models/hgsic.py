"""
HGSIC -- Hierarchical Groove State Integration Circuit.

Beta-5 model of the STU.  Models how ECoG high gamma activity (70-170 Hz)
in posterior STG is highly correlated with sound intensity (r=0.49), with
auditory cortex activity preceding premotor/motor cortex by 110 ms via
the dorsal auditory-motor pathway.

Output: 11D per frame (172.27 Hz).
Mechanisms: BEP, TMH.
Evidence: Potes 2012 (r=0.49), Nourski 2014.
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


class HGSIC(BaseModel):
    """Hierarchical Groove State Integration Circuit -- high-gamma intensity coupling."""

    NAME = "HGSIC"
    FULL_NAME = "Hierarchical Groove State Integration Circuit"
    UNIT = "STU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "TMH")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_gamma_intensity_corr", "f02_groove_state",
        )),
        LayerSpec("M", "Mathematical Model", 2, 5, (
            "coupling_r", "groove_index", "hierarchical_integration",
        )),
        LayerSpec("P", "Present Processing", 5, 8, (
            "pstg_high_gamma", "intensity_tracking", "motor_transfer",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "groove_forecast", "intensity_predict", "motor_engage_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_gamma_intensity_corr", "f02_groove_state",
            "coupling_r", "groove_index", "hierarchical_integration",
            "pstg_high_gamma", "intensity_tracking", "motor_transfer",
            "groove_forecast", "intensity_predict", "motor_engage_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Posterior Superior Temporal Gyrus",
                abbreviation="pSTG",
                hemisphere="bilateral",
                mni_coords=(60, -28, 10),
                function="High gamma (70-170 Hz) tracking sound intensity",
                evidence_count=4,
            ),
            BrainRegion(
                name="Premotor Cortex",
                abbreviation="PMC",
                hemisphere="bilateral",
                mni_coords=(-46, 0, 50),
                function="Motor groove response via dorsal auditory-motor pathway",
                evidence_count=3,
            ),
            BrainRegion(
                name="Basal Ganglia",
                abbreviation="BG",
                hemisphere="bilateral",
                mni_coords=(14, 8, 4),
                function="Groove-related beat entrainment and reward processing",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Potes", 2012,
                         "High gamma in pSTG correlates with sound intensity",
                         "r=0.49"),
                Citation("Nourski", 2014,
                         "Hierarchical temporal processing in auditory cortex",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.88),
            falsification_criteria=(
                "High gamma must correlate with intensity at r > 0.3",
                "pSTG must precede motor cortex activation",
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
