"""
MTNE -- Music Training Neural Efficiency.

Gamma-3 model of the STU.  Models how music training improves executive
function with stable or decreased neural activation, suggesting enhanced
neural efficiency rather than increased neural recruitment.

Output: 10D per frame (172.27 Hz).
Mechanisms: BEP.
Evidence: Moreno 2011, Schellenberg 2004.
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


class MTNE(BaseModel):
    """Music Training Neural Efficiency -- expertise-driven processing economy."""

    NAME = "MTNE"
    FULL_NAME = "Music Training Neural Efficiency"
    UNIT = "STU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_neural_efficiency", "f02_executive_function",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "efficiency_index", "activation_reduction",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "processing_load", "activation_level", "task_performance",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "efficiency_trajectory", "transfer_potential", "training_effect_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_neural_efficiency", "f02_executive_function",
            "efficiency_index", "activation_reduction",
            "processing_load", "activation_level", "task_performance",
            "efficiency_trajectory", "transfer_potential", "training_effect_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Dorsolateral Prefrontal Cortex",
                abbreviation="dlPFC",
                hemisphere="bilateral",
                mni_coords=(-44, 30, 28),
                function="Executive function with training-dependent efficiency",
                evidence_count=2,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 30, 24),
                function="Conflict monitoring with reduced activation in musicians",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Moreno", 2011,
                         "Music training affects executive function efficiency", ""),
                Citation("Schellenberg", 2004,
                         "Music lessons enhance IQ via executive function", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Musicians must show equal or better performance with less activation",
                "Training duration must predict efficiency gains",
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
