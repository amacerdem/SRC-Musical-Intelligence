"""
SDL -- Stimulus-Driven Listening.

Gamma-3 model of the ASU.  Proposes that hemispheric lateralization for
auditory processing is dynamically modulated by salience demands, not
fixed by stimulus category, challenging the traditional speech-left /
music-right dichotomy.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Dynamic network reconfiguration driven by attention and salience.
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


class SDL(BaseModel):
    """Stimulus-Driven Listening -- salience-dependent lateralization."""

    NAME = "SDL"
    FULL_NAME = "Stimulus-Driven Listening"
    UNIT = "ASU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f25_dynamic_lateralization", "f26_local_clustering",
            "f27_hemispheric_oscillation",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "lateralization_index", "salience_demand",
        )),
        LayerSpec("P", "Present Processing", 5, 7, (
            "dynamic_lateralization", "hemispheric_engagement",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "network_config_pred", "processing_efficiency_pred",
            "lateralization_shift_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f25_dynamic_lateralization", "f26_local_clustering",
            "f27_hemispheric_oscillation",
            # Layer M -- Mathematical
            "lateralization_index", "salience_demand",
            # Layer P -- Present
            "dynamic_lateralization", "hemispheric_engagement",
            # Layer F -- Future
            "network_config_pred", "processing_efficiency_pred",
            "lateralization_shift_pred",
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
                function="Dynamic hemispheric specialization",
                evidence_count=2,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Top-down lateralization control",
                evidence_count=1,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Salience demand monitoring",
                evidence_count=1,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Coffey", 2017,
                         "Salience-dependent hemispheric reconfiguration",
                         ""),
                Citation("Zatorre", 2002,
                         "Spectral and temporal processing in auditory cortex",
                         ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Lateralization should shift with salience demands",
                "Stimulus category alone should not predict lateralization",
            ),
            version="2.0.0",
            paper_count=2,
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
