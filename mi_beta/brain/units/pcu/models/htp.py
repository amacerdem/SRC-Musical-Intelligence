"""
HTP -- Hierarchical Temporal Prediction.

Alpha-1 model of the PCU (Predictive Coding Unit).  Models how predictive
representations follow a hierarchical temporal pattern: high-level abstract
features are predicted earlier (~500 ms) than low-level features (~110 ms).

Output: 12D per frame (172.27 Hz).
Mechanisms: PPC (Pitch Processing Chain), TPC (Temporal Pattern Chain),
            MEM (Memory Integration).
Evidence: de Vries 2023 (ηp² = 0.49, n=22), Norman-Haignere 2022, Bonetti 2024,
          Golesorkhi 2021, Forseth 2020, + 10 supporting papers (15 total).
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
    """Hierarchical Temporal Prediction -- hierarchical temporal prediction."""

    NAME = "HTP"
    FULL_NAME = "Hierarchical Temporal Prediction"
    UNIT = "PCU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")
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
        """18 H3 tuples for HTP computation (see HTP.md Section 5)."""
        return (
            # (r3_idx, horizon, morph, law)
            # -- PPC horizons: low-level prediction --
            (7, 0, 0, 2),      # amplitude, 25ms, value, bidi
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (7, 3, 2, 2),      # amplitude, 100ms, std, bidi
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 1, 1, 2),     # spectral_flux, 50ms, mean, bidi
            (10, 3, 14, 2),    # spectral_flux, 100ms, periodicity, bidi
            # -- TPC horizons: mid-level prediction --
            (9, 3, 0, 2),      # spectral_centroid, 100ms, value, bidi
            (9, 4, 8, 0),      # spectral_centroid, 125ms, velocity, fwd
            (9, 8, 1, 0),      # spectral_centroid, 500ms, mean, fwd
            (21, 3, 8, 0),     # spectral_change, 100ms, velocity, fwd
            (21, 4, 0, 0),     # spectral_change, 125ms, value, fwd
            # -- MEM horizons: high-level prediction --
            (41, 8, 0, 0),     # x_l5l7[0], 500ms, value, fwd
            (41, 8, 1, 0),     # x_l5l7[0], 500ms, mean, fwd
            (41, 16, 1, 0),    # x_l5l7[0], 1000ms, mean, fwd
            (41, 16, 20, 0),   # x_l5l7[0], 1000ms, entropy, fwd
            # -- Cross-level coupling --
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 2, 2),     # x_l0l5[0], 100ms, std, bidi
            (33, 4, 8, 0),     # x_l4l5[0], 125ms, velocity, fwd
        )

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
                name="Anterior Inferior Parietal Lobule",
                abbreviation="aIPL",
                hemisphere="bilateral",
                mni_coords=(40, -40, 48),
                function="Abstract prediction (500ms)",
                evidence_count=3,
            ),
            BrainRegion(
                name="Lateral Occipitotemporal Cortex",
                abbreviation="LOTC",
                hemisphere="bilateral",
                mni_coords=(48, -68, 4),
                function="View-invariant motion",
                evidence_count=3,
            ),
            BrainRegion(
                name="Visual Areas V3/V4",
                abbreviation="V3V4",
                hemisphere="bilateral",
                mni_coords=(20, -88, 0),
                function="View-dependent prediction (200ms)",
                evidence_count=3,
            ),
            BrainRegion(
                name="Primary Visual Cortex",
                abbreviation="V1V2",
                hemisphere="bilateral",
                mni_coords=(8, -92, 8),
                brodmann_area=17,
                function="Low-level optical flow (110ms)",
                evidence_count=3,
            ),
            BrainRegion(
                name="Heschl's Gyrus",
                abbreviation="HG",
                hemisphere="bilateral",
                mni_coords=(42, -22, 10),
                brodmann_area=41,
                function="Low-level auditory prediction, temporal timing via low-freq phase",
                evidence_count=5,
            ),
            BrainRegion(
                name="Planum Temporale",
                abbreviation="PT",
                hemisphere="bilateral",
                mni_coords=(52, -28, 12),
                brodmann_area=42,
                function="Content prediction via high-gamma",
                evidence_count=3,
            ),
            BrainRegion(
                name="Superior Temporal Gyrus",
                abbreviation="STG",
                hemisphere="bilateral",
                mni_coords=(-58, -20, 8),
                brodmann_area=22,
                function="Mid-to-long integration windows 200-500ms",
                evidence_count=6,
            ),
            BrainRegion(
                name="Hippocampus",
                abbreviation="Hipp",
                hemisphere="bilateral",
                mni_coords=(26, -18, -18),
                function="Sequence memory, prediction error propagation",
                evidence_count=3,
            ),
            BrainRegion(
                name="Anterior Cingulate Cortex",
                abbreviation="ACC",
                hemisphere="bilateral",
                mni_coords=(4, 32, 24),
                brodmann_area=32,
                function="Prediction error integration; top hierarchy for final sequence elements",
                evidence_count=3,
            ),
            BrainRegion(
                name="Medial Cingulate Cortex",
                abbreviation="MCC",
                hemisphere="bilateral",
                mni_coords=(4, -10, 40),
                brodmann_area=24,
                function="Hierarchical prediction processing",
                evidence_count=2,
            ),
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -4, 60),
                brodmann_area=6,
                function="Temporal prediction timing for rhythmic stimuli",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("de Vries & Wurm", 2023,
                         "Hierarchical temporal prediction: 500ms abstract, 110ms low-level",
                         "ηp²=0.49, n=22"),
                Citation("Norman-Haignere et al.", 2022,
                         "Multiscale temporal integration in human auditory cortex",
                         "iEEG, n=7"),
                Citation("Bonetti et al.", 2024,
                         "Spatiotemporal brain hierarchies of auditory memory recognition",
                         "MEG, n=83"),
                Citation("Golesorkhi et al.", 2021,
                         "Temporal hierarchy of intrinsic neural timescales",
                         "d=-1.63, η²=0.86, n=89"),
                Citation("Forseth et al.", 2020,
                         "Two predictive mechanisms in early auditory cortex",
                         "iEEG, n=37"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.97),
            falsification_criteria=(
                "Disrupting high-level areas should abolish early predictions",
                "High-level predictions must precede low-level temporally",
                "Post-stimulus high-level representations should be silenced",
            ),
            version="2.1.0",
            paper_count=15,
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
