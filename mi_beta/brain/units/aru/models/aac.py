"""
AAC -- Autonomic-Affective Coupling.

Alpha-2 model of the ARU.  Models how subjective emotional intensity
correlates with measurable autonomic nervous system (ANS) responses during
music listening.  Shares AED/CPD mechanisms with SRP, adds ASA mechanism.

Output: 14D per frame (172.27 Hz).
Mechanisms: AED, CPD, ASA (Auditory Scene Analysis).
Evidence: 60+ papers, d=0.71 (Salimpoor 2011), d=0.85-1.5 (Egermann 2013).
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


class AAC(BaseModel):
    """Autonomic-Affective Coupling -- ANS responses to music."""

    NAME = "AAC"
    FULL_NAME = "Autonomic-Affective Coupling"
    UNIT = "ARU"
    TIER = "alpha"
    OUTPUT_DIM = 14
    MECHANISM_NAMES = ("AED", "CPD", "ASA")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Emotional Arousal", 0, 2, (
            "f04_emotional_arousal", "f06_ans_response",
        )),
        LayerSpec("A", "Autonomic Markers", 2, 7, (
            "scr", "hr", "respr", "bvp", "temp",
        )),
        LayerSpec("I", "Integration", 7, 9, (
            "chills_intensity", "ans_composite",
        )),
        LayerSpec("P", "Present Processing", 9, 12, (
            "current_intensity", "driving_signal", "perceptual_arousal",
        )),
        LayerSpec("F", "Future Predictions", 12, 14, (
            "scr_pred_1s", "hr_pred_2s",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        """Placeholder -- ~50 H3 tuples required."""
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Emotional Arousal
            "f04_emotional_arousal", "f06_ans_response",
            # Layer A -- Autonomic Markers
            "scr", "hr", "respr", "bvp", "temp",
            # Layer I -- Integration
            "chills_intensity", "ans_composite",
            # Layer P -- Present
            "current_intensity", "driving_signal", "perceptual_arousal",
            # Layer F -- Future
            "scr_pred_1s", "hr_pred_2s",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Amygdala",
                abbreviation="AMY",
                hemisphere="bilateral",
                mni_coords=(-19, -5, -14),
                function="Arousal evaluation and salience detection",
                evidence_count=6,
            ),
            BrainRegion(
                name="Anterior Insula",
                abbreviation="aINS",
                hemisphere="bilateral",
                mni_coords=(34, 18, 2),
                function="Interoceptive awareness of bodily states",
                evidence_count=5,
            ),
            BrainRegion(
                name="Hypothalamus",
                abbreviation="HYP",
                hemisphere="bilateral",
                mni_coords=(0, -4, -8),
                function="Autonomic output control via brainstem",
                evidence_count=4,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Salimpoor", 2011,
                         "DA release -> ANS composite during chills", "d=0.71"),
                Citation("Egermann", 2013,
                         "Expectation violation -> SCR up, HR down",
                         "d=0.85-1.5"),
                Citation("Ferreri", 2019,
                         "Levodopa -> SCR increase (p=0.033)", "t(25)=-2.26"),
                Citation("Guhn", 2007,
                         "Musical chills produce measurable piloerection", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "SCR must increase with arousal-inducing passages",
                "HR should decelerate at peak emotional moments (vagal brake)",
                "Levodopa should increase ANS responses to music",
            ),
            version="2.0.0",
            paper_count=10,
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
