"""PSH — Prediction Silencing Hypothesis.

Hub nucleus (depth 5, reads all upstream) in PCU, Function F2. Models how
accurate top-down predictions "silence" (explain away) high-level stimulus
representations post-stimulus, while low-level representations persist —
demonstrating hierarchical dissociation in prediction.

Core principle:
    post_high = repr * (1 - accuracy)  ->  0 when prediction correct
    post_low  = repr * 1.0             ->  always persists

Dependency chain:
    PSH is a Hub (Depth 5) — reads ALL upstream PCU mechanisms.
    UPSTREAM_READS = (HTP, PWUP, WMED, UDP, MAA)
    Highest convergence point in F2 pipeline.

Upstream reads:
    HTP  [3]  E3:hierarchy_gradient     — hierarchical prediction quality
    PWUP [2]  M0:weighted_error         — precision-weighted PE
    UDP  [1]  E1:confirmation_reward    — prediction confirmation signal
    WMED [3]  M1:dissociation_index     — WM-entrainment dissociation
    MAA  [3]  M1:appreciation_composite — appreciation modulation

R3 Ontology Mapping (post-freeze 97D):
    sensory_pleasantness:  [4]   (A, high-level harmonic)
    periodicity:           [5]   (A, high-level tonal structure)
    amplitude:             [7]   (B, low-level sensory)
    onset_strength:        [11]  (B, change detection / PE trigger)
    tristimulus1-3:        [18:21] (C, high-level harmonic)
    spectral_flux:         [21]  (D, prediction error magnitude)

Output structure: E(2) + M(2) + P(3) + F(3) = 10D
  E-layer [0:2]  Extraction    (sigmoid)  scope=internal
  M-layer [2:4]  Memory        (sigmoid)  scope=internal
  P-layer [4:7]  Present       (sigmoid)  scope=hybrid
  F-layer [7:10] Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/psh/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Hub
from Musical_Intelligence.contracts.dataclasses import (
    Citation,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
    NeuroLink,
    RegionLink,
)

from .cognitive_present import compute_cognitive_present
from .extraction import compute_extraction
from .forecast import compute_forecast
from .temporal_integration import compute_temporal_integration

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    0: "25ms (gamma)",
    1: "50ms (gamma)",
    3: "100ms (alpha-beta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 16: "curvature", 20: "entropy",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 2: "integration"}


def _h3(
    r3_idx: int, r3_name: str, horizon: int, morph: int, law: int,
    purpose: str, citation: str,
) -> H3DemandSpec:
    """Shorthand factory for H3DemandSpec."""
    return H3DemandSpec(
        r3_idx=r3_idx,
        r3_name=r3_name,
        horizon=horizon,
        horizon_label=_H_LABELS.get(horizon, f"H{horizon}"),
        morph=morph,
        morph_name=_M_LABELS.get(morph, f"M{morph}"),
        law=law,
        law_name=_L_LABELS[law],
        purpose=purpose,
        citation=citation,
    )


# -- R3 feature indices (post-freeze 97D) ------------------------------------
_SENSORY_PLEAS = 4        # sensory_pleasantness (A group, high-level harmonic)
_PERIODICITY = 5          # periodicity (A group, high-level tonal structure)
_AMPLITUDE = 7            # amplitude (B group, low-level sensory)
_ONSET = 11               # onset_strength (B, change detection / PE trigger)
_SPECTRAL_FLUX = 21       # spectral_flux (D, prediction error magnitude)
_CHROMA_C = 25            # chroma_C (F, low-level coupling)
_H_COUPLING = 41          # H_coupling / tonal_stability (H, high-level coupling)


# -- 18 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H0(25ms) -> H1(50ms) -> H3(100ms) -> H8(500ms) -> H16(1s)

_PSH_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Amplitude / Low-level sensory (4 tuples) ===
    _h3(_AMPLITUDE, "amplitude", 0, 0, 2,
        "Instantaneous amplitude at 25ms — instant sensory",
        "de Vries & Wurm 2023"),
    _h3(_AMPLITUDE, "amplitude", 1, 0, 2,
        "Amplitude at 50ms — sensory window",
        "de Vries & Wurm 2023"),
    _h3(_AMPLITUDE, "amplitude", 3, 0, 2,
        "Amplitude at 100ms — sensory context",
        "Auksztulewicz 2017"),
    _h3(_AMPLITUDE, "amplitude", 3, 2, 2,
        "Amplitude variability at 100ms — sensory variability",
        "de Vries & Wurm 2023"),

    # === Onset Strength / PE trigger (2 tuples) ===
    _h3(_ONSET, "onset_strength", 0, 0, 2,
        "Instant onset detection at 25ms — PE onset",
        "Todorovic 2012"),
    _h3(_ONSET, "onset_strength", 3, 0, 2,
        "Onset at 100ms — PE context",
        "Todorovic 2012"),

    # === Spectral Flux / Error magnitude (3 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 1, 0, 2,
        "Spectral change at 50ms — error onset",
        "de Vries & Wurm 2023"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Spectral change at 100ms — error context",
        "Carbajal & Malmierca 2018"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 2, 2,
        "Spectral change variability at 100ms — error variability",
        "Wacongne 2012"),

    # === Chroma C / Low-level coupling (3 tuples) ===
    _h3(_CHROMA_C, "chroma_C", 0, 0, 2,
        "Chroma at 25ms — low-level coupling onset",
        "Auksztulewicz 2017"),
    _h3(_CHROMA_C, "chroma_C", 3, 0, 2,
        "Chroma at 100ms — low-level coupling",
        "Auksztulewicz 2017"),
    _h3(_CHROMA_C, "chroma_C", 3, 16, 2,
        "Chroma curvature at 100ms — coupling shape",
        "Carbajal & Malmierca 2018"),

    # === H Coupling / High-level coupling (4 tuples) ===
    _h3(_H_COUPLING, "tonal_stability", 3, 0, 0,
        "Tonal stability at 100ms — high-level coupling",
        "de Vries & Wurm 2023"),
    _h3(_H_COUPLING, "tonal_stability", 8, 0, 0,
        "Tonal stability at 500ms — sustained high-level",
        "de Vries & Wurm 2023"),
    _h3(_H_COUPLING, "tonal_stability", 16, 1, 0,
        "Mean tonal stability at 1s — long-range high-level",
        "Auksztulewicz 2017"),
    _h3(_H_COUPLING, "tonal_stability", 16, 20, 0,
        "Tonal stability entropy at 1s — high-level uncertainty",
        "Wacongne 2012"),

    # === Sensory Pleasantness / Harmonic context (1 tuple) ===
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 1, 0,
        "Mean consonance at 1s — harmonic context",
        "Todorovic 2012"),

    # === Periodicity / Tonal context (1 tuple) ===
    _h3(_PERIODICITY, "periodicity", 16, 1, 0,
        "Mean periodicity at 1s — tonal context",
        "Carbajal & Malmierca 2018"),
)

assert len(_PSH_H3_DEMANDS) == 18


class PSH(Hub):
    """Prediction Silencing Hypothesis — PCU Hub (depth 5, 10D).

    Models how accurate top-down predictions "silence" (explain away)
    high-level stimulus representations post-stimulus, while low-level
    representations persist — demonstrating hierarchical dissociation
    in prediction.

    Core formula:
        post_high = repr * (1 - accuracy)  ->  silenced when correct
        post_low  = repr * 1.0             ->  always persists

    de Vries & Wurm 2023: prediction silencing hypothesis, MEG N=22,
    eta_p^2=0.49, F(2)=19.9, p=8.3e-7.
    Auksztulewicz 2017: repetition suppression and prediction, MEG N=20.
    Carbajal & Malmierca 2018: SSA and deviance detection hierarchy.
    Todorovic 2012: repetition suppression as prediction, MEG N=16.
    Wacongne 2012: two cortical PE systems, EEG+fMRI N=20.

    Dependency chain:
        PSH is a Hub (Depth 5) — reads ALL upstream PCU mechanisms.
        UPSTREAM_READS = (HTP, PWUP, WMED, UDP, MAA)

    Downstream feeds:
        -> prediction_silencing belief (Core)
        -> hierarchical_dissociation, silencing_efficiency (Appraisal)
        -> post_stim_silencing, error_persistence (Anticipation)
    """

    NAME = "PSH"
    FULL_NAME = "Prediction Silencing Hypothesis"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 10
    PROCESSING_DEPTH = 5  # Override Hub default (4) to 5

    UPSTREAM_READS = ("HTP", "PWUP", "WMED", "UDP", "MAA")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:high_level_silencing", "E1:low_level_persistence"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 2, 4,
            ("M0:silencing_efficiency", "M1:hierarchy_dissociation"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:prediction_match", "P1:sensory_persistence",
             "P2:binding_check"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:post_stim_silencing", "F1:error_persistence",
             "F2:next_prediction"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PSH_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:high_level_silencing", "E1:low_level_persistence",
            "M0:silencing_efficiency", "M1:hierarchy_dissociation",
            "P0:prediction_match", "P1:sensory_persistence",
            "P2:binding_check",
            "F0:post_stim_silencing", "F1:error_persistence",
            "F2:next_prediction",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # A1/STG — low-level PE persistence
            RegionLink("E1:low_level_persistence", "STG", 0.80,
                       "de Vries & Wurm 2023"),
            # LOTC — high-level silencing
            RegionLink("E0:high_level_silencing", "LOTC", 0.75,
                       "de Vries & Wurm 2023"),
            # aIPL — high-level prediction silencing
            RegionLink("P0:prediction_match", "aIPL", 0.80,
                       "de Vries & Wurm 2023"),
            # IFG — top-down prediction source
            RegionLink("F2:next_prediction", "IFG", 0.70,
                       "Wacongne 2012"),
            # IC — subcortical SSA / repetition suppression
            RegionLink("M0:silencing_efficiency", "IC", 0.65,
                       "Carbajal & Malmierca 2018"),
            # MGB — thalamic deviance detection
            RegionLink("M1:hierarchy_dissociation", "MGB", 0.60,
                       "Carbajal & Malmierca 2018"),
            # Hippocampus — memory-based prediction
            RegionLink("F0:post_stim_silencing", "HIPP", 0.65,
                       "Todorovic 2012"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # PSH is purely predictive, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("de Vries & Wurm", 2023,
                         "Prediction silencing hypothesis: accurate top-down "
                         "predictions silence high-level representations "
                         "post-stimulus while low-level persist; "
                         "eta_p^2=0.49, F(2)=19.9, p=8.3e-7",
                         "MEG, N=22"),
                Citation("Auksztulewicz", 2017,
                         "Repetition suppression as prediction: MEG evidence "
                         "for hierarchical prediction updating; reduced "
                         "responses reflect fulfilled predictions",
                         "MEG, N=20"),
                Citation("Carbajal & Malmierca", 2018,
                         "SSA and deviance detection hierarchy from "
                         "subcortical IC through thalamic MGB to cortex; "
                         "review of hierarchical prediction mechanisms",
                         "Review (cellular)"),
                Citation("Todorovic", 2012,
                         "Repetition suppression is a form of prediction: "
                         "suppressed responses to predicted stimuli, "
                         "enhanced responses to deviants",
                         "MEG, N=16"),
                Citation("Wacongne", 2012,
                         "Two cortical prediction error systems: local "
                         "(auditory cortex) and global (frontal/parietal); "
                         "dissociable PE hierarchy",
                         "EEG + fMRI, N=20"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "High-level representations must be silenced when predictions "
                "are accurate (confirmed: de Vries & Wurm 2023)",
                "Low-level representations must persist regardless of "
                "prediction accuracy (confirmed: de Vries & Wurm 2023)",
                "Disrupting top-down predictions should abolish silencing "
                "(testable via TMS to aIPL/IFG)",
                "Novel stimuli should show no silencing at any level "
                "(testable via novelty paradigm)",
                "Subcortical SSA should correlate with cortical silencing "
                "(testable via simultaneous MEG + subcortical recording)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Transform R3/H3 + upstream into 10D prediction silencing output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"HTP": (B,T,12), "PWUP": (B,T,10),
                "WMED": (B,T,11), "UDP": (B,T,10), "MAA": (B,T,10)}``
            cross_unit_inputs: Optional cross-unit pathway data (unused).

        Returns:
            ``(B, T, 10)`` — E(2) + M(2) + P(3) + F(3)
        """
        e = compute_extraction(r3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(
            r3_features, h3_features, e, m, upstream_outputs,
        )
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
