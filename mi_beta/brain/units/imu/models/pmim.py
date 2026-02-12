"""
PMIM -- Predictive Memory Integration Matrix.

Beta-2 model of the IMU.  Models how music processing involves continuous
prediction and comparison with stored representations (ERAN for long-term,
MMN for short-term), with prediction errors driving memory updating.

Output: 11D per frame (172.27 Hz).
Mechanisms: MEM, TMH.
Evidence: Koelsch 2009, Pearce & Wiggins 2012.
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


class PMIM(BaseModel):
    """Predictive Memory Integration Matrix -- prediction error-driven memory update."""

    NAME = "PMIM"
    FULL_NAME = "Predictive Memory Integration Matrix"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("MEM", "TMH")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_prediction_error", "f02_memory_update",
        )),
        LayerSpec("M", "Mathematical Model", 2, 5, (
            "eran_signal", "mmn_signal", "prediction_precision",
        )),
        LayerSpec("P", "Present Processing", 5, 8, (
            "expectation_state", "stored_representation", "comparison_result",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "next_event_pred", "update_magnitude_fc", "model_confidence_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_prediction_error", "f02_memory_update",
            "eran_signal", "mmn_signal", "prediction_precision",
            "expectation_state", "stored_representation", "comparison_result",
            "next_event_pred", "update_magnitude_fc", "model_confidence_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="right",
                mni_coords=(48, 18, 4),
                function="ERAN generation for harmonic prediction violations",
                evidence_count=4,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(60, -32, 8),
                function="MMN generation for short-term auditory predictions",
                evidence_count=3,
            ),
            BrainRegion(
                name="Hippocampus",
                abbreviation="HIP",
                hemisphere="bilateral",
                mni_coords=(20, -24, -12),
                function="Long-term musical representation storage and update",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Koelsch", 2009,
                         "ERAN reflects long-term musical syntax expectations", ""),
                Citation("Pearce", 2012,
                         "Predictive statistical learning model for music (IDyOM)",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.88),
            falsification_criteria=(
                "ERAN must emerge for syntactic but not random violations",
                "Prediction error magnitude must drive memory update strength",
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
