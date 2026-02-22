"""IGFE -- Individual Gamma Frequency Enhancement.

Integrator nucleus (depth 3, reads all upstream) in PCU, Function F2.
Models how auditory stimulation at an individual's peak gamma frequency
(30-80 Hz) enhances cognitive performance (memory, executive control)
through frequency-specific entrainment. The 40 Hz auditory steady-state
response (ASSR) is the canonical example, but the optimal frequency
varies across individuals.

Dependency chain:
    IGFE is an Integrator (Depth 3) -- reads R3/H3 + all upstream outputs.
    Upstream: HTP (12D), WMED (11D).

R3 Ontology Mapping (97D freeze):
    periodicity:       [5]  (A, frequency structure / gamma proxy)
    amplitude:         [7]  (B, stimulus intensity)
    onset_strength:    [11] (B, temporal modulation rate)
    warmth:            [12] (C, spectral center proxy)
    tonalness:         [14] (C, harmonic structure / IGF match)

Output structure: E(2) + M(2) + P(3) + F(2) = 9D
  E-layer [0:2]  Extraction    (sigmoid)  scope=internal
  M-layer [2:4]  Memory        (sigmoid)  scope=internal
  P-layer [4:7]  Present       (sigmoid)  scope=hybrid
  F-layer [7:9]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/igfe/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Integrator
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
    0: "value", 1: "mean", 2: "std", 8: "velocity", 14: "periodicity",
    18: "trend",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 1: "forward", 2: "integration"}


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
_PERIODICITY = 5          # periodicity (A group, frequency structure / gamma proxy)
_AMPLITUDE = 7            # amplitude (B group, stimulus intensity)
_ONSET_STRENGTH = 11      # onset_strength (B, temporal modulation rate)
_WARMTH = 12              # warmth (C, spectral center proxy)
_TONALNESS = 14           # tonalness (C, harmonic structure / IGF match)
_CHROMA_C = 25            # chroma_C (F, gamma coupling proxy)
_H_COUPLING = 41          # H_coupling (H, cognitive coupling)


# -- 18 H3 Demand Specifications -----------------------------------------------
# Gamma-scale entrainment at fast timescales, cognitive effects at slower

_IGFE_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Periodicity / Gamma proxy (4 tuples) ===
    _h3(_PERIODICITY, "periodicity", 0, 0, 2,
        "Periodicity at 25ms — gamma-scale onset detection",
        "Galambos 1981"),
    _h3(_PERIODICITY, "periodicity", 1, 0, 2,
        "Periodicity at 50ms — gamma cycle tracking",
        "Galambos 1981"),
    _h3(_PERIODICITY, "periodicity", 3, 1, 2,
        "Mean periodicity at 100ms — sustained gamma entrainment",
        "Herrmann 2016"),
    _h3(_PERIODICITY, "periodicity", 16, 1, 0,
        "Mean periodicity at 1s — stable gamma frequency memory",
        "Bolland 2025"),

    # === Tonalness / IGF match (2 tuples) ===
    _h3(_TONALNESS, "tonalness", 3, 0, 2,
        "Tonalness at 100ms — harmonic structure match to IGF",
        "Herrmann 2016"),
    _h3(_TONALNESS, "tonalness", 16, 1, 0,
        "Mean tonalness at 1s — sustained harmonic alignment",
        "Bolland 2025"),

    # === Amplitude / Stimulus intensity (2 tuples) ===
    _h3(_AMPLITUDE, "amplitude", 3, 0, 2,
        "Amplitude at 100ms — stimulus intensity for entrainment",
        "Galambos 1981"),
    _h3(_AMPLITUDE, "amplitude", 16, 1, 2,
        "Mean amplitude at 1s — sustained stimulus intensity",
        "Bolland 2025"),

    # === Chroma C / Gamma coupling (4 tuples) ===
    _h3(_CHROMA_C, "chroma_C", 0, 0, 2,
        "Chroma C at 25ms — gamma coupling onset",
        "Herrmann 2016"),
    _h3(_CHROMA_C, "chroma_C", 1, 0, 2,
        "Chroma C at 50ms — gamma coupling cycle",
        "Herrmann 2016"),
    _h3(_CHROMA_C, "chroma_C", 3, 14, 2,
        "Chroma C periodicity at 100ms — frequency-specific entrainment",
        "Galambos 1981"),
    _h3(_CHROMA_C, "chroma_C", 16, 14, 2,
        "Chroma C periodicity at 1s — stable entrainment pattern",
        "Bolland 2025"),

    # === H_coupling / Cognitive coupling (3 tuples) ===
    _h3(_H_COUPLING, "H_coupling", 8, 0, 0,
        "H coupling at 500ms — cognitive coupling state memory",
        "Pastor 2002"),
    _h3(_H_COUPLING, "H_coupling", 16, 1, 0,
        "Mean H coupling at 1s — sustained cognitive coupling",
        "Pastor 2002"),
    _h3(_H_COUPLING, "H_coupling", 16, 18, 0,
        "H coupling trend at 1s — coupling trajectory",
        "Polanía 2012"),

    # === Onset Strength / Modulation rate (3 tuples) ===
    _h3(_ONSET_STRENGTH, "onset_strength", 0, 0, 2,
        "Onset strength at 25ms — modulation onset detection",
        "Galambos 1981"),
    _h3(_ONSET_STRENGTH, "onset_strength", 1, 14, 2,
        "Onset strength periodicity at 50ms — modulation periodicity",
        "Herrmann 2016"),
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 1, 2,
        "Mean onset strength at 100ms — sustained modulation rate",
        "Bolland 2025"),
)

assert len(_IGFE_H3_DEMANDS) == 18


class IGFE(Integrator):
    """Individual Gamma Frequency Enhancement -- PCU Integrator (depth 3, 9D).

    Models how auditory stimulation at an individual's peak gamma frequency
    (30-80 Hz) enhances cognitive performance through frequency-specific
    neural entrainment. The 40 Hz ASSR is the canonical case, but the
    optimal stimulation frequency varies across individuals.

    Bolland et al. 2025: 62-study systematic review of gamma entrainment;
    meta-analysis of auditory 40 Hz stimulation effects on cognition.
    Galambos et al. 1981: discovery of 40 Hz auditory steady-state response
    (ASSR); EEG N=10, p<0.01.
    Herrmann et al. 2016: review of human EEG gamma oscillation responses
    to sensory stimulation.
    Pastor et al. 2002: gamma oscillations and memory binding; MEG N=12.
    Polanía et al. 2012: tACS gamma enhancement of working memory; N=15.

    Dependency chain:
        IGFE is an Integrator (Depth 3) -- reads all upstream PCU outputs.
        HTP (Depth 0, 12D) -- hierarchy gradient for prediction context.
        WMED (Depth ?, 11D) -- working memory baseline for enhancement.

    Downstream feeds:
        -> Beliefs: gamma_enhancement, entrainment_strength (Core)
        -> Beliefs: dose_response, cognitive_benefit (Appraisal)
        -> Beliefs: post_stimulation_pred (Anticipation)
    """

    NAME = "IGFE"
    FULL_NAME = "Individual Gamma Frequency Enhancement"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 9
    UPSTREAM_READS = ("HTP", "WMED")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:igf_match", "E1:memory_enhancement"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 2, 4,
            ("M0:executive_enhancement", "M1:dose_response"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:gamma_synchronization", "P1:dose_accumulation",
             "P2:memory_access"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 9,
            ("F0:memory_enhancement_post", "F1:executive_improve_post"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _IGFE_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:igf_match", "E1:memory_enhancement",
            "M0:executive_enhancement", "M1:dose_response",
            "P0:gamma_synchronization", "P1:dose_accumulation",
            "P2:memory_access",
            "F0:memory_enhancement_post", "F1:executive_improve_post",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # A1/STG -- gamma entrainment locus
            RegionLink("E0:igf_match", "STG", 0.80,
                       "Galambos 1981"),
            # Heschl's Gyrus -- 40 Hz ASSR generator
            RegionLink("P0:gamma_synchronization", "A1_HG", 0.85,
                       "Galambos 1981"),
            # Hippocampus -- memory enhancement via gamma binding
            RegionLink("P2:memory_access", "HIPP", 0.70,
                       "Pastor 2002"),
            # DLPFC -- executive control enhancement
            RegionLink("M0:executive_enhancement", "DLPFC", 0.65,
                       "Polanía 2012"),
            # Fronto-central FC/Cz -- entrainment maxima
            RegionLink("P1:dose_accumulation", "PFC", 0.60,
                       "Herrmann 2016"),
            # Sensorimotor/SMA -- auditory-motor coupling
            RegionLink("E1:memory_enhancement", "SMA", 0.55,
                       "Bolland 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # IGFE models entrainment effects, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bolland et al.", 2025,
                         "62-study systematic review of gamma entrainment; "
                         "auditory 40 Hz stimulation enhances memory and "
                         "executive function; effect sizes vary with "
                         "individual gamma frequency",
                         "Systematic review + meta-analysis, 62 studies"),
                Citation("Galambos et al.", 1981,
                         "Discovery of 40 Hz auditory steady-state response "
                         "(ASSR); maximal at fronto-central electrodes; "
                         "p<0.01",
                         "EEG, N=10"),
                Citation("Herrmann et al.", 2016,
                         "Human EEG gamma oscillation responses to sensory "
                         "stimulation; frequency-specific entrainment "
                         "30-80 Hz; individual variation in peak frequency",
                         "Review"),
                Citation("Pastor et al.", 2002,
                         "Gamma oscillations in hippocampus during memory "
                         "encoding; 40 Hz phase-locking to auditory stimuli "
                         "predicts recall; p<0.05",
                         "MEG, N=12"),
                Citation("Polanía et al.", 2012,
                         "tACS at individual gamma frequency enhances working "
                         "memory capacity; fronto-parietal gamma coupling; "
                         "p<0.05",
                         "EEG + tACS, N=15"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Stimulation at non-gamma frequencies should not enhance "
                "cognition (testable via frequency comparison paradigm)",
                "Individual gamma frequency mismatch should reduce "
                "enhancement effect (testable via personalized stimulation)",
                "Memory enhancement should correlate with hippocampal gamma "
                "synchronization (testable via concurrent MEG/EEG)",
                "Executive enhancement should depend on DLPFC gamma coupling "
                "(testable via frontal EEG)",
                "Dose-response should show saturation at prolonged exposure "
                "(testable via varying stimulation duration)",
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
        """Transform R3/H3 + upstream into 9D gamma enhancement output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"HTP": (B, T, 12), "WMED": (B, T, 11)}``
            cross_unit_inputs: Optional cross-unit pathway data (unused).

        Returns:
            ``(B, T, 9)`` -- E(2) + M(2) + P(3) + F(2)
        """
        e = compute_extraction(r3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(
            r3_features, h3_features, e, m, upstream_outputs,
        )
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
