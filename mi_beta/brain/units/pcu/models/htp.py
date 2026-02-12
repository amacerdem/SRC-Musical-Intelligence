"""
HTP -- Harmonic Tension Prediction.

Alpha-1 model of the PCU (Predictive Coding Unit).  Models how predictive
representations follow a hierarchical temporal pattern: high-level abstract
features are predicted earlier (~500 ms) than low-level features (~110 ms).

Output: 12D per frame (172.27 Hz).
Mechanisms: PPC (Pitch Processing Chain), C0P (C0 Projection).
Evidence: de Vries 2023 (ηp² = 0.49, n=22).
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


class HTP(BaseModel):
    """Harmonic Tension Prediction -- hierarchical temporal prediction."""

    NAME = "HTP"
    FULL_NAME = "Harmonic Tension Prediction"
    UNIT = "PCU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("PPC", "C0P")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_high_level_lead", "f02_mid_level_lead",
            "f03_low_level_lead", "f04_hierarchy_gradient",
        )),
        LayerSpec("M", "Mathematical Model", 4, 7, (
            "latency_high_500ms", "latency_mid_200ms", "latency_low_110ms",
        )),
        LayerSpec("P", "Present Processing", 7, 10, (
            "sensory_match", "pitch_prediction", "abstract_prediction",
        )),
        LayerSpec("F", "Future Predictions", 10, 12, (
            "abstract_future_500ms", "midlevel_future_200ms",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        """Placeholder -- H3 tuples required (see HTP.md Section 5)."""
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_high_level_lead", "f02_mid_level_lead",
            "f03_low_level_lead", "f04_hierarchy_gradient",
            # Layer M -- Mathematical
            "latency_high_500ms", "latency_mid_200ms", "latency_low_110ms",
            # Layer P -- Present
            "sensory_match", "pitch_prediction", "abstract_prediction",
            # Layer F -- Future
            "abstract_future_500ms", "midlevel_future_200ms",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Auditory prediction hierarchy -- low/mid level",
                evidence_count=3,
            ),
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -4, 60),
                brodmann_area=6,
                function="Temporal prediction timing",
                evidence_count=2,
            ),
            BrainRegion(
                name="Dorsolateral Prefrontal Cortex",
                abbreviation="dlPFC",
                hemisphere="bilateral",
                mni_coords=(-44, 36, 20),
                brodmann_area=46,
                function="High-level abstract prediction",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("de Vries", 2023,
                         "Hierarchical temporal prediction: 500ms abstract, 110ms low-level",
                         "ηp²=0.49"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.97),
            falsification_criteria=(
                "Disrupting high-level areas should abolish early predictions",
                "High-level predictions must precede low-level temporally",
                "Post-stimulus high-level representations should be silenced",
            ),
            version="2.0.0",
            paper_count=1,
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
