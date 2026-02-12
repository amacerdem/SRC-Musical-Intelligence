"""
PSH -- Prediction Silencing Hypothesis.

Gamma-3 model of the PCU (Predictive Coding Unit).  Proposes that accurate
top-down predictions "silence" (explain away) high-level stimulus
representations post-stimulus, while low-level representations persist.

Output: 10D per frame (172.27 Hz).
Mechanisms: PPC, TPC, MEM.
Evidence: de Vries & Wurm 2023, Millidge et al. 2022, Carbajal & Malmierca 2018,
          Fong et al. 2020, Schilling et al. 2023, + 7 supporting papers (12 total).
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


class PSH(BaseModel):
    """Prediction Silencing Hypothesis -- hierarchical prediction silencing."""

    NAME = "PSH"
    FULL_NAME = "Prediction Silencing Hypothesis"
    UNIT = "PCU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 4, (
            "f01_high_level_silencing", "f02_low_level_persistence",
            "f03_silencing_efficiency", "f04_hierarchy_dissociation",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "prediction_match", "sensory_persistence",
            "binding_check",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "post_stim_silencing_500ms", "error_persistence_500ms",
            "next_prediction_pre_stim",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return (
            # (r3_idx, horizon, morph, law)
            # -- Low-level persistence (fast, gamma-alpha) --
            (7, 0, 0, 2),      # amplitude, 25ms, value, bidi
            (7, 1, 0, 2),      # amplitude, 50ms, value, bidi
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (7, 3, 2, 2),      # amplitude, 100ms, std, bidi
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            # -- PE / error signal --
            (21, 1, 0, 2),     # spectral_change, 50ms, value, bidi
            (21, 3, 0, 2),     # spectral_change, 100ms, value, bidi
            (21, 3, 2, 2),     # spectral_change, 100ms, std, bidi
            # -- Low-level coupling (persistence) --
            (25, 0, 0, 2),     # x_l0l5[0], 25ms, value, bidi
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 16, 2),    # x_l0l5[0], 100ms, curvature, bidi
            # -- High-level coupling (silencing) --
            (41, 3, 0, 0),     # x_l5l7[0], 100ms, value, fwd
            (41, 8, 0, 0),     # x_l5l7[0], 500ms, value, fwd
            (41, 16, 1, 0),    # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 20, 0),   # x_l5l7[0], 1000ms, entropy, fwd
            # -- Context --
            (4, 16, 1, 0),     # sensory_pleasantness, 1000ms, mean, fwd
            (5, 16, 1, 0),     # periodicity, 1000ms, mean, fwd
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E -- Explicit
            "f01_high_level_silencing", "f02_low_level_persistence",
            "f03_silencing_efficiency", "f04_hierarchy_dissociation",
            # Layer P -- Present
            "prediction_match", "sensory_persistence",
            "binding_check",
            # Layer F -- Future
            "post_stim_silencing_500ms", "error_persistence_500ms",
            "next_prediction_pre_stim",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Superior Temporal Gyrus / Auditory Cortex",
                abbreviation="STG/A1",
                hemisphere="bilateral",
                mni_coords=(-52, -22, 8),
                brodmann_area=22,
                function="Low-level persistence (PE signal)",
                evidence_count=6,
            ),
            BrainRegion(
                name="Lateral Occipitotemporal Cortex",
                abbreviation="LOTC",
                hemisphere="bilateral",
                mni_coords=(-44, -62, -8),
                brodmann_area=None,
                function="High-level silencing (view-invariant)",
                evidence_count=1,
            ),
            BrainRegion(
                name="Anterior Inferior Parietal Lobule",
                abbreviation="aIPL",
                hemisphere="bilateral",
                mni_coords=(-44, -40, 48),
                brodmann_area=None,
                function="High-level silencing (prediction-modulated)",
                evidence_count=1,
            ),
            BrainRegion(
                name="Inferior Frontal Gyrus",
                abbreviation="IFG",
                hemisphere="bilateral",
                mni_coords=(-44, 18, 8),
                brodmann_area=44,
                function="Top-down prediction source (ERAN/MMN generator)",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("de Vries & Wurm", 2023,
                         "High-level motion representations silenced post-stimulus",
                         "n=22, eta_p2=0.49"),
                Citation("Millidge, Seth & Buckley", 2022,
                         "Predictive coding review: repetition/expectation suppression",
                         "meta-review"),
                Citation("Carbajal & Malmierca", 2018,
                         "SSA/MMN decomposition into repetition suppression + PE",
                         "review, single-unit"),
                Citation("Fong, Law, Uka & Koike", 2020,
                         "Auditory MMN under predictive coding framework",
                         "review"),
                Citation("Schilling et al.", 2023,
                         "Predictive coding as top-down silencing mechanism",
                         "computational model"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "High-level representations must be silenced post-stimulus",
                "Low-level representations must persist post-stimulus",
            ),
            version="2.1.0",
            paper_count=12,
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
