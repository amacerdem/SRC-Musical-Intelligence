"""
VRIAP -- VR-Induced Analgesia Paradigm.

Beta-7 model of the IMU.  Models how active VR mode (motor interaction with
music) shows better analgesic effect than passive mode (listening only) through
enhanced visual-sensorimotor cortical activation and reduced pain processing
connectivity.

Output: 10D per frame (172.27 Hz).
Mechanisms: MEM.
Evidence: Hoffman 2011, Wiederhold 2014.
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


class VRIAP(BaseModel):
    """VR-Induced Analgesia Paradigm -- active vs passive music analgesia."""

    NAME = "VRIAP"
    FULL_NAME = "VR-Induced Analgesia Paradigm"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("MEM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_active_analgesia", "f02_passive_analgesia",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "analgesia_index", "active_passive_ratio",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "sensorimotor_engagement", "pain_modulation", "immersion_state",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "analgesia_duration_pred", "engagement_forecast",
            "pain_reduction_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_active_analgesia", "f02_passive_analgesia",
            "analgesia_index", "active_passive_ratio",
            "sensorimotor_engagement", "pain_modulation", "immersion_state",
            "analgesia_duration_pred", "engagement_forecast",
            "pain_reduction_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 30, 24),
                function="Pain processing modulated by music-VR interaction",
                evidence_count=2,
            ),
            BrainRegion(
                name="Insula",
                abbreviation="INS",
                hemisphere="bilateral",
                mni_coords=(-38, -2, 6),
                function="Pain perception reduction during active music engagement",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Hoffman", 2011,
                         "VR analgesia: active mode superior to passive", ""),
                Citation("Wiederhold", 2014,
                         "Music-enhanced VR for pain management", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Active VR-music must produce greater analgesia than passive",
                "Sensorimotor cortex activation must mediate the active advantage",
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
