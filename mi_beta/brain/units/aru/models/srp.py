"""
SRP -- Striatal Reward Pathway.

Alpha-1 model of the ARU (Affective Resonance Unit).  Models how the human
brain generates musical pleasure through dopamine release in the striatum.
Decomposes reward into three dissociable systems: wanting (incentive salience),
liking (hedonic impact), and learning (prediction error).

Output: 19D per frame (172.27 Hz).
Mechanisms: AED (Affective Entrainment Dynamics),
            CPD (Chills & Peak Detection),
            C0P (Cognitive Projection).
Evidence: 12+ papers, r=0.84 (Salimpoor 2011), d=0.81 (Mas-Herrero 2021).
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


class SRP(BaseModel):
    """Striatal Reward Pathway -- musical pleasure via dopamine release."""

    NAME = "SRP"
    FULL_NAME = "Striatal Reward Pathway"
    UNIT = "ARU"
    TIER = "alpha"
    OUTPUT_DIM = 19
    MECHANISM_NAMES = ("AED", "CPD", "C0P")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("N", "Neurochemical Signals", 0, 3, (
            "da_caudate", "da_nacc", "opioid_proxy",
        )),
        LayerSpec("C", "Circuit Activation", 3, 6, (
            "vta_drive", "stg_nacc_coupling", "prediction_error",
        )),
        LayerSpec("P", "Psychological States", 6, 9, (
            "wanting", "liking", "pleasure",
        )),
        LayerSpec("T", "Temporal Response", 9, 13, (
            "tension", "prediction_match", "reaction", "appraisal",
        )),
        LayerSpec("M", "Musical Meaning", 13, 16, (
            "harmonic_tension", "dynamic_intensity", "peak_detection",
        )),
        LayerSpec("F", "Forecast", 16, 19, (
            "reward_forecast", "chills_proximity", "resolution_expect",
        )),
    )

    # ── Abstract property implementations ──────────────────────────────

    @property
    def h3_demand(self) -> Tuple:
        """Placeholder -- 124 H3 tuples required (see SRP.md Section 6)."""
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer N -- Neurochemical
            "da_caudate", "da_nacc", "opioid_proxy",
            # Layer C -- Circuit
            "vta_drive", "stg_nacc_coupling", "prediction_error",
            # Layer P -- Psychological
            "wanting", "liking", "pleasure",
            # Layer T -- Temporal (ITPRA)
            "tension", "prediction_match", "reaction", "appraisal",
            # Layer M -- Musical
            "harmonic_tension", "dynamic_intensity", "peak_detection",
            # Layer F -- Forecast
            "reward_forecast", "chills_proximity", "resolution_expect",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Nucleus Accumbens",
                abbreviation="NAcc",
                hemisphere="bilateral",
                mni_coords=(8, 4, -6),
                function="Ventral striatal DA release at consummation",
                evidence_count=8,
            ),
            BrainRegion(
                name="Caudate Nucleus",
                abbreviation="Caudate",
                hemisphere="bilateral",
                mni_coords=(-12, 14, 16),
                function="Dorsal striatal DA ramp during anticipation",
                evidence_count=6,
            ),
            BrainRegion(
                name="Ventral Tegmental Area",
                abbreviation="VTA",
                hemisphere="bilateral",
                mni_coords=(0, -16, -8),
                function="Source of DA neurons projecting to striatum",
                evidence_count=4,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Salimpoor", 2011,
                         "NAcc DA at consummation, Caudate DA at anticipation",
                         "r=0.84"),
                Citation("Salimpoor", 2013,
                         "NAcc-STG connectivity predicts reward value", ""),
                Citation("Cheung", 2019,
                         "Pleasure = f(uncertainty, surprise)", "d=3.8-8.53"),
                Citation("Ferreri", 2019,
                         "Levodopa causally modulates pleasure", "Z=1.97"),
                Citation("Mas-Herrero", 2021,
                         "TMS dlPFC causally modulates NAcc reward", "d=0.81"),
                Citation("Martinez-Molina", 2016,
                         "Musical anhedonia = NAcc-STG disconnection",
                         "d=3.6-7.0"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.98),
            falsification_criteria=(
                "Prediction error should go negative for deceptive cadences",
                "Wanting must peak BEFORE liking temporally",
                "Musical anhedonia should abolish NAcc response",
            ),
            version="4.0.0",
            paper_count=12,
        )

    # ── Compute ────────────────────────────────────────────────────────

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
