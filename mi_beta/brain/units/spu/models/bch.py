"""
BCH -- Brainstem Consonance Hierarchy.

Alpha-1 model of the SPU (Spectral Processing Unit).  Models how brainstem
frequency-following responses (FFR) preferentially encode consonant musical
intervals over dissonant ones.  Foundation of the spectral processing hierarchy.

Output: 12D per frame (172.27 Hz).
Mechanisms: PPC (Pitch Processing Chain).
Evidence: Bidelman 2009 (r=0.81), Bidelman & Heinz 2011, Terhardt 1974.
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


class BCH(BaseModel):
    """Brainstem Consonance Hierarchy -- FFR consonance encoding."""

    NAME = "BCH"
    FULL_NAME = "Brainstem Consonance Hierarchy"
    UNIT = "SPU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("PPC",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_nps", "f02_harmonicity", "f03_hierarchy",
            "f04_ffr_behavior",
        )),
        LayerSpec("M", "Mathematical Model", 4, 6, (
            "nps_t", "harm_interval",
        )),
        LayerSpec("P", "Present Processing", 6, 9, (
            "consonance_signal", "template_match", "neural_pitch",
        )),
        LayerSpec("F", "Future Predictions", 9, 12, (
            "consonance_pred", "pitch_propagation", "interval_expect",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        """Placeholder -- 16 H3 tuples required (see BCH.md Section 5)."""
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_nps", "f02_harmonicity", "f03_hierarchy",
            "f04_ffr_behavior",
            # Layer M -- Mathematical
            "nps_t", "harm_interval",
            # Layer P -- Present
            "consonance_signal", "template_match", "neural_pitch",
            # Layer F -- Future
            "consonance_pred", "pitch_propagation", "interval_expect",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Inferior Colliculus",
                abbreviation="IC",
                hemisphere="bilateral",
                mni_coords=(0, -32, -8),
                function="FFR generation -- rostral brainstem",
                evidence_count=4,
            ),
            BrainRegion(
                name="Auditory Nerve",
                abbreviation="AN",
                hemisphere="bilateral",
                mni_coords=(0, -38, -40),
                function="Pitch salience encoding (70-fiber model)",
                evidence_count=5,
            ),
            BrainRegion(
                name="Cochlear Nucleus",
                abbreviation="CN",
                hemisphere="bilateral",
                mni_coords=(10, -38, -40),
                function="Early spectral processing",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bidelman", 2009,
                         "FFR pitch salience correlates with consonance ratings",
                         "r=0.81"),
                Citation("Bidelman", 2013,
                         "Harmonicity > roughness as consonance predictor", ""),
                Citation("Bidelman", 2011,
                         "AN population model predicts full consonance hierarchy",
                         ""),
                Citation("Terhardt", 1974,
                         "Virtual pitch computation in auditory system", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.97),
            falsification_criteria=(
                "Pure tones should NOT show consonance effects",
                "Non-Western listeners should show same neural hierarchy",
                "Removing harmonics should reduce NPS",
            ),
            version="2.0.0",
            paper_count=4,
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
