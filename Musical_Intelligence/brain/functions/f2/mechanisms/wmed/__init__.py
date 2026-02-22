"""WMED -- Working Memory-Entrainment Dissociation.

Associator nucleus (depth 2, reads relay + encoder outputs) in PCU,
Function F2. Models the paradoxical dissociation between neural
entrainment and working memory in rhythm processing.

Core finding (Noboa 2025): Stronger neural entrainment (SS-EP) to
simple rhythms predicts WORSE tapping accuracy (beta=-0.418,
R2adj=0.27, EEG N=60). Two dissociable routes process rhythm:
  Route 1 — Entrainment: SS-EP -> motor coupling (paradox route)
  Route 2 — WM: capacity -> cognitive control (standard route)

Dependency chain:
    HTP  (Depth 0, Relay)  ──→ PWUP (Depth 1, Encoder) ──→ WMED (Depth 2, Associator)
    │                           │                              │
    │                           │ M0:weighted_error ──────────>│ (P2 engagement)
    │                           │ M1:uncertainty_index ───────>│ (P1 segmentation)
    │                           │ P0:tonal_precision_weight ──>│ (P0 phase lock)
    └───────────────────────────┘                              │
                                                               ▼
                                                         11D rhythm output

Without PWUP: P-layer loses precision weighting, falls back to E/M + H3.

R3 Ontology Mapping (97D freeze):
    amplitude:             [7]   (B, beat strength)
    onset_strength:        [10]  (B, loudness proxy -- was spectral_flux)
    onset_strength:        [11]  (B, beat marker)
    spectral_change:       [21]  (D, timing variability)
    distribution_entropy:  [22]  (D, syncopation detection)

Output structure: E(2) + M(2) + P(3) + F(4) = 11D
  E-layer [0:2]   Extraction   (sigmoid)  scope=internal
  M-layer [2:4]   Memory       (sigmoid)  scope=internal
  P-layer [4:7]   Present      (sigmoid)  scope=hybrid
  F-layer [7:11]  Forecast     (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/wmed/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Associator
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
    3: "100ms (alpha-beta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 14: "periodicity", 20: "entropy",
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
_AMPLITUDE = 7              # amplitude (B group, beat strength)
_ONSET_LOUD = 10            # onset_strength (B, loudness proxy)
_ONSET_BEAT = 11            # onset_strength (B, beat marker)
_SPECTRAL_CHANGE = 21       # spectral_change (D, timing variability)
_DIST_ENTROPY = 22          # distribution_entropy (D, syncopation)
_CHROMA_C = 25              # chroma_C (F, first chroma bin)
_H_COUPLING = 41            # H_coupling (H, tonal coupling)


# -- 16 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H3(100ms) -> H8(500ms) -> H16(1s)
# Laws: L0=memory(backward), L2=integration(bidirectional)

_WMED_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Onset Strength / Entrainment detection (5 tuples) ===
    _h3(_ONSET_LOUD, "onset_strength", 3, 0, 2,
        "Onset loudness value at 100ms -- instantaneous beat energy",
        "Nozaradan 2011"),
    _h3(_ONSET_LOUD, "onset_strength", 3, 14, 2,
        "Onset loudness periodicity at 100ms -- entrainment regularity",
        "Nozaradan 2011"),
    _h3(_ONSET_LOUD, "onset_strength", 16, 14, 2,
        "Onset loudness periodicity at 1s -- beat-scale entrainment",
        "Nozaradan 2011"),
    _h3(_ONSET_BEAT, "onset_strength", 3, 0, 2,
        "Onset beat value at 100ms -- event detection",
        "Nozaradan 2011"),
    _h3(_ONSET_BEAT, "onset_strength", 16, 14, 2,
        "Onset beat periodicity at 1s -- meter-scale regularity",
        "Nozaradan 2011"),

    # === Amplitude / Motor timing (2 tuples) ===
    _h3(_AMPLITUDE, "amplitude", 3, 2, 2,
        "Amplitude std at 100ms -- beat strength variability",
        "Grahn 2007"),
    _h3(_AMPLITUDE, "amplitude", 16, 1, 2,
        "Amplitude mean at 1s -- sustained beat level for motor timing",
        "Grahn 2007"),

    # === Chroma C / Harmonic periodicity (3 tuples) ===
    _h3(_CHROMA_C, "chroma_C", 3, 14, 2,
        "Chroma periodicity at 100ms -- harmonic regularity supporting entrainment",
        "Large 2008"),
    _h3(_CHROMA_C, "chroma_C", 16, 14, 2,
        "Chroma periodicity at 1s -- long-range harmonic pattern",
        "Large 2008"),
    _h3(_CHROMA_C, "chroma_C", 16, 21, 2,
        "Chroma M21 at 1s -- harmonic contour integration",
        "Large 2008"),

    # === H_coupling / Tonal stability (3 tuples) ===
    _h3(_H_COUPLING, "H_coupling", 8, 0, 0,
        "Tonal coupling value at 500ms -- stability context for rhythm",
        "Large 2008"),
    _h3(_H_COUPLING, "H_coupling", 16, 1, 0,
        "Tonal coupling mean at 1s -- sustained tonal stability",
        "Large 2008"),
    _h3(_H_COUPLING, "H_coupling", 16, 20, 0,
        "Tonal coupling entropy at 1s -- rhythmic uncertainty",
        "Noboa 2025"),

    # === Spectral Change / Timing variability (3 tuples) ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 3, 0, 2,
        "Spectral change value at 100ms -- timing variability instantaneous",
        "Noboa 2025"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 2, 0,
        "Spectral change std at 1s -- timing irregularity over beat scale",
        "Noboa 2025"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 19, 0,
        "Spectral change M19 at 1s -- temporal pattern boundary proxy",
        "Noboa 2025"),
)

assert len(_WMED_H3_DEMANDS) == 16


class WMED(Associator):
    """Working Memory-Entrainment Dissociation -- PCU Associator (depth 2, 11D).

    Models the paradoxical dissociation between neural entrainment and
    working memory in rhythm processing. Stronger SS-EP entrainment to
    simple rhythms predicts worse tapping accuracy (Noboa 2025,
    beta=-0.418, R2adj=0.27).

    Two dissociable routes:
      Route 1 (Entrainment): SS-EP -> motor coupling (paradox route).
      Route 2 (WM): capacity -> cognitive control (standard route).

    Dependency chain:
        HTP (Depth 0) -> PWUP (Depth 1) -> WMED (Depth 2)

    Upstream reads:
        PWUP: M0:weighted_error [2], M1:uncertainty_index [3],
              P0:tonal_precision_weight [4]

    Downstream feeds:
        -> prediction_accuracy, prediction_hierarchy beliefs
        -> motor timing, rhythmic engagement assessments
    """

    NAME = "WMED"
    FULL_NAME = "Working Memory-Entrainment Dissociation"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("PWUP",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:entrainment_strength", "E1:wm_contribution"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 2, 4,
            ("M0:tapping_accuracy", "M1:dissociation_index"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:phase_locking_strength", "P1:pattern_segmentation",
             "P2:rhythmic_engagement"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 11,
            ("F0:next_beat_pred", "F1:tapping_accuracy_pred",
             "F2:wm_interference_pred", "F3:paradox_strength_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _WMED_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:entrainment_strength", "E1:wm_contribution",
            "M0:tapping_accuracy", "M1:dissociation_index",
            "P0:phase_locking_strength", "P1:pattern_segmentation",
            "P2:rhythmic_engagement",
            "F0:next_beat_pred", "F1:tapping_accuracy_pred",
            "F2:wm_interference_pred", "F3:paradox_strength_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # STG -- SS-EP maximal at fronto-central, projects to STG
            RegionLink("E0:entrainment_strength", "STG", 0.75,
                       "Nozaradan 2011"),
            # SMA -- motor timing for tapping
            RegionLink("M0:tapping_accuracy", "SMA", 0.80,
                       "Grahn 2007"),
            # DLPFC -- working memory capacity
            RegionLink("E1:wm_contribution", "DLPFC", 0.70,
                       "Baddeley 2000"),
            # Basal Ganglia -- beat tracking and prediction
            RegionLink("P0:phase_locking_strength", "BG", 0.75,
                       "Grahn 2007"),
            RegionLink("F0:next_beat_pred", "BG", 0.70,
                       "Grahn 2007"),
            # Cerebellum -- rhythmic synchronization
            RegionLink("P2:rhythmic_engagement", "CBLM", 0.65,
                       "Grahn 2007"),
            # STG -- WM processing and SS-EP convergence
            RegionLink("P1:pattern_segmentation", "STG", 0.60,
                       "Noboa 2025"),
            RegionLink("M1:dissociation_index", "STG", 0.55,
                       "Noboa 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # WMED is rhythm-predictive, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Noboa", 2025,
                         "Working memory-entrainment paradox: stronger SS-EP "
                         "entrainment to simple rhythms predicts worse tapping; "
                         "beta=-0.418, R2adj=0.27",
                         "EEG, N=60"),
                Citation("Nozaradan", 2011,
                         "Tagging meter with EEG: steady-state evoked potentials "
                         "at beat frequency and harmonics",
                         "EEG, N=12"),
                Citation("Grahn", 2007,
                         "Rhythm perception and basal ganglia: beat-based "
                         "timing engages BG-SMA loop",
                         "fMRI, N=14"),
                Citation("Large", 2008,
                         "Neural resonance theory: nonlinear oscillators "
                         "entrain to periodic auditory stimuli",
                         "Review"),
                Citation("Baddeley", 2000,
                         "Multicomponent working memory model: central "
                         "executive, phonological loop, visuospatial sketchpad",
                         "Review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Entrainment-tapping dissociation must replicate Noboa 2025 "
                "negative beta (beta=-0.418) in simple rhythms; if positive "
                "beta observed, paradox route is invalid",
                "WM route must show standard positive WM-tapping correlation "
                "for complex rhythms; failure = dual-route model invalid",
                "SS-EP amplitude at beat frequency must correlate with E0; "
                "absence of frequency-tagged response invalidates entrainment "
                "extraction",
                "BG lesion patients should show impaired beat prediction (F0) "
                "but intact WM route (E1); if both impaired, routes not "
                "dissociable",
                "Increasing rhythmic complexity should shift reliance from "
                "Route 1 to Route 2 (E0 decreases, E1 increases); failure = "
                "single-route model sufficient",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Transform R3/H3 + PWUP upstream into 11D WM-entrainment dissociation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"PWUP": (B, T, 10)}``

        Returns:
            ``(B, T, 11)`` -- E(2) + M(2) + P(3) + F(4)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(
            r3_features, h3_features, e, m, upstream_outputs,
        )
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
