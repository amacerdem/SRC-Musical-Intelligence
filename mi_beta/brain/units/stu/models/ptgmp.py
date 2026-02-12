"""
PTGMP -- Piano Training Grey Matter Plasticity.

Gamma-4 model of the STU.  Models how piano training in older adults
increases grey matter volume in DLPFC and cerebellum, demonstrating
structural neuroplasticity even in late life.

Output: 10D per frame (172.27 Hz).
Mechanisms: BEP.
Evidence: Guo 2021, Sluming 2002.
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


class PTGMP(BaseModel):
    """Piano Training Grey Matter Plasticity -- structural neuroplasticity."""

    NAME = "PTGMP"
    FULL_NAME = "Piano Training Grey Matter Plasticity"
    UNIT = "STU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_gm_volume_change", "f02_plasticity_index",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "volume_delta", "training_dose_response",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "motor_complexity", "bimanual_coordination", "sensorimotor_load",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "plasticity_forecast", "volume_trajectory", "functional_gain_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_gm_volume_change", "f02_plasticity_index",
            "volume_delta", "training_dose_response",
            "motor_complexity", "bimanual_coordination", "sensorimotor_load",
            "plasticity_forecast", "volume_trajectory", "functional_gain_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Dorsolateral Prefrontal Cortex",
                abbreviation="dlPFC",
                hemisphere="bilateral",
                mni_coords=(-44, 30, 28),
                function="Grey matter increase with piano training in older adults",
                evidence_count=2,
            ),
            BrainRegion(
                name="Cerebellum",
                abbreviation="CB",
                hemisphere="bilateral",
                mni_coords=(20, -62, -26),
                function="Motor learning plasticity and coordination gains",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Guo", 2021,
                         "Piano training increases grey matter in older adults", ""),
                Citation("Sluming", 2002,
                         "Grey matter differences in orchestral musicians", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Training must produce measurable grey matter increase",
                "Effects must persist after training cessation",
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
        """Stub -- returns zeros of correct shape."""
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
