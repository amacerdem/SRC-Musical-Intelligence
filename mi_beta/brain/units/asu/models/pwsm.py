"""
PWSM -- Pop-out Warning Salience Model.

Gamma-1 model of the ASU.  Proposes that salience detection is governed
by precision-weighting: high-precision contexts (stable, predictable)
generate stronger prediction error signals, while low-precision contexts
suppress error signals.

Output: 10D per frame (172.27 Hz).
Mechanisms: ASA (Auditory Salience Analysis).
Evidence: Basinski 2025 (changing jitter abolishes MMN, d=0.01 n.s.).
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


class PWSM(BaseModel):
    """Pop-out Warning Salience Model -- precision-weighted prediction error."""

    NAME = "PWSM"
    FULL_NAME = "Pop-out Warning Salience Model"
    UNIT = "ASU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("ASA",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 3, (
            "f19_precision_weighting", "f20_error_suppression",
            "f21_stability_encoding",
        )),
        LayerSpec("M", "Mathematical Model", 3, 5, (
            "pe_weighted", "precision_estimate",
        )),
        LayerSpec("P", "Present Processing", 5, 7, (
            "weighted_error_signal", "precision_state",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "mmn_presence_pred", "context_reliability_pred",
            "salience_threshold_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f19_precision_weighting", "f20_error_suppression",
            "f21_stability_encoding",
            # Layer M -- Mathematical
            "pe_weighted", "precision_estimate",
            # Layer P -- Present
            "weighted_error_signal", "precision_state",
            # Layer F -- Future
            "mmn_presence_pred", "context_reliability_pred",
            "salience_threshold_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(0, 24, 32),
                brodmann_area=32,
                function="Precision-weighted error monitoring",
                evidence_count=2,
            ),
            BrainRegion(
                name="Insula",
                abbreviation="INS",
                hemisphere="bilateral",
                mni_coords=(34, 18, -4),
                brodmann_area=13,
                function="Context stability assessment",
                evidence_count=1,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="MMN generation -- precision-gated",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Basinski", 2025,
                         "Changing jitter abolishes MMN via precision suppression",
                         "d=0.01 n.s."),
                Citation("Friston", 2005,
                         "Precision-weighting in predictive coding", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "High-precision contexts must yield stronger PE signals",
                "Low-precision contexts should abolish MMN",
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
