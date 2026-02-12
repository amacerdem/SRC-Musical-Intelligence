"""
STANM -- Spectro-Temporal Attention Network Model.

Beta-2 model of the ASU.  Models how attention modulates network topology
for spectral vs temporal processing, with lateralized effects in auditory
regions depending on task goal and acoustic cue availability.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Task-directed network reconfiguration with lateralized effects.
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


class STANM(BaseModel):
    """Spectro-Temporal Attention Network Model -- network topology modulation."""

    NAME = "STANM"
    FULL_NAME = "Spectro-Temporal Attention Network Model"
    UNIT = "ASU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f13_temporal_attention", "f14_spectral_attention",
            "f15_network_topology",
        )),
        LayerSpec("M", "Mathematical Model", 3, 6, (
            "network_topology_fn", "local_clustering",
            "lateralization_index",
        )),
        LayerSpec("P", "Present Processing", 6, 8, (
            "temporal_attention_alloc", "spectral_attention_alloc",
        )),
        LayerSpec("F", "Future Predictions", 8, 10, (
            "network_state_pred", "lateralization_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f13_temporal_attention", "f14_spectral_attention",
            "f15_network_topology",
            # Layer M -- Mathematical
            "network_topology_fn", "local_clustering",
            "lateralization_index",
            # Layer P -- Present
            "temporal_attention_alloc", "spectral_attention_alloc",
            # Layer F -- Future
            "network_state_pred", "lateralization_pred",
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
                function="Lateralized spectral/temporal processing",
                evidence_count=3,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-48, 18, 4),
                brodmann_area=44,
                function="Attentional network reconfiguration",
                evidence_count=2,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Task-directed attention control",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Coffey", 2017,
                         "Attention modulates network topology for spectral vs temporal",
                         ""),
                Citation("Albouy", 2019,
                         "Lateralized auditory cortex during spectral/temporal tasks",
                         ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Network topology must change with attentional goal",
                "Signal degradation should increase local clustering",
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
