"""
TMRM -- Tempo Memory Reproduction Matrix.

Gamma-1 model of the STU.  Models how tempo memory accuracy is enhanced by
sensory support during recall compared to motor reproduction, with optimal
accuracy around 120 BPM and positive effects of musical expertise.

Output: 10D per frame (172.27 Hz).
Mechanisms: BEP, TMH.
Evidence: Leow & Grahn 2014, Collier & Ogden 2004.
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


class TMRM(BaseModel):
    """Tempo Memory Reproduction Matrix -- tempo recall modalities."""

    NAME = "TMRM"
    FULL_NAME = "Tempo Memory Reproduction Matrix"
    UNIT = "STU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP", "TMH")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_sensory_recall", "f02_motor_recall",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "recall_accuracy", "optimal_tempo_proximity",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "current_tempo_memory", "beat_stability", "reproduction_error",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "recall_decay_pred", "accuracy_forecast", "tempo_drift_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_sensory_recall", "f02_motor_recall",
            "recall_accuracy", "optimal_tempo_proximity",
            "current_tempo_memory", "beat_stability", "reproduction_error",
            "recall_decay_pred", "accuracy_forecast", "tempo_drift_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -6, 62),
                function="Internal beat generation and tempo memory maintenance",
                evidence_count=2,
            ),
            BrainRegion(
                name="Basal Ganglia",
                abbreviation="BG",
                hemisphere="bilateral",
                mni_coords=(14, 8, 4),
                function="Beat-based timing and tempo reproduction accuracy",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Leow", 2014,
                         "Sensory vs motor tempo recall modalities", ""),
                Citation("Collier", 2004,
                         "Preferred tempo peaks near 120 BPM", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Sensory recall must outperform motor reproduction",
                "Optimal tempo zone around 120 BPM must replicate",
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
