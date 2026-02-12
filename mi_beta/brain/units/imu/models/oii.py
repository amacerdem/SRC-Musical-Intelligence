"""
OII -- Oscillatory Intelligence Integration.

Beta-3 model of the IMU.  Models how fluid intelligence involves
frequency-specific functional connectivity, with slow oscillations
(theta, alpha) supporting integration and gamma supporting local processing.

Output: 10D per frame (172.27 Hz).
Mechanisms: MEM.
Evidence: Thut 2012, Roux & Uhlhaas 2014.
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


class OII(BaseModel):
    """Oscillatory Intelligence Integration -- frequency-specific cognition."""

    NAME = "OII"
    FULL_NAME = "Oscillatory Intelligence Integration"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("MEM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_theta_alpha_integration", "f02_gamma_local",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "oscillatory_coupling", "intelligence_index",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "theta_power", "alpha_coherence", "gamma_binding",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "integration_forecast", "cognitive_load_pred", "frequency_shift_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_theta_alpha_integration", "f02_gamma_local",
            "oscillatory_coupling", "intelligence_index",
            "theta_power", "alpha_coherence", "gamma_binding",
            "integration_forecast", "cognitive_load_pred", "frequency_shift_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Prefrontal Cortex",
                abbreviation="PFC",
                hemisphere="bilateral",
                mni_coords=(-40, 44, 20),
                function="Theta-mediated long-range integration for fluid intelligence",
                evidence_count=3,
            ),
            BrainRegion(
                name="Parietal Cortex",
                abbreviation="PAR",
                hemisphere="bilateral",
                mni_coords=(-38, -54, 46),
                function="Alpha-gamma coupling for working memory maintenance",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Thut", 2012,
                         "Alpha phase modulates local cortical excitability", ""),
                Citation("Roux", 2014,
                         "Oscillatory connectivity in cognitive function", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Theta-alpha coupling must correlate with integration tasks",
                "Gamma power must predict local processing efficiency",
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
        """Stub -- returns zeros of correct shape."""
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
