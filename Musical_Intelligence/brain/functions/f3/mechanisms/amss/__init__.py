"""AMSS -- Attention-Modulated Stream Segregation.

Encoder nucleus (depth 1) in STU, Function F3. Models how attention modulates
auditory stream segregation: spectral and temporal cues are extracted from the
acoustic scene, then attention gates which stream is foregrounded. Competitive
interactions between streams produce alternating perceptual states (Elhilali 2009).

Dependency chain:
    AMSS is an Encoder (Depth 1) -- reads HMCE relay output (cross-unit, STU).
    Computed after HMCE in F3 pipeline.

R3 Ontology Mapping (post-freeze 97D):
    amplitude:          [7]  -> [7]    (A, velocity_A)
    loudness:           [8]  -> [8]    (A, velocity_D)
    spectral_flux:      [10] -> [10]   (B, onset_strength)
    onset_strength:     [11] -> [11]   (B, unchanged)
    tonalness:          [14] -> [14]   (C, brightness_kuttruff)
    spectral_centroid:  [15] -> [15]   (C, unchanged)
    spectral_change:    [21] -> [21]   (D, spectral_flux)
    x_l0l5:             [25] -> [25]   (F, coupling)

Output structure: E(5) + M(2) + P(2) + F(2) = 11D
  E-layer [0:5]   Extraction    (sigmoid)    scope=internal
  M-layer [5:7]   Memory        (sigmoid)    scope=internal
  P-layer [7:9]   Present       (sigmoid)    scope=hybrid
  F-layer [9:11]  Forecast      (sigmoid)    scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/amss/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Encoder
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
    4: "125ms (theta)",
    8: "500ms (delta)",
    14: "~900ms",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    14: "periodicity", 18: "trend",
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
_AMPLITUDE = 7            # velocity_A (A group)
_LOUDNESS = 8             # velocity_D (A group)
_SPECTRAL_FLUX = 10       # onset_strength (B group)
_ONSET_STRENGTH = 11      # onset_strength (B group)
_TONALNESS = 14           # brightness_kuttruff (C group)
_SPECTRAL_CENTROID = 15   # spectral_centroid (C group)
_SPECTRAL_CHANGE = 21     # spectral_flux (D group)
_X_L0L5 = 25             # coupling (F group)


# -- 16 H3 Demand Specifications ----------------------------------------------
# Stream segregation requires spectral identity (centroid, tonalness),
# temporal structure (onset, amplitude), and cross-band coupling (binding).

_AMSS_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Amplitude / Stream Energy (2 tuples) ===
    _h3(7, "amplitude", 8, 0, 2,
        "Amplitude value 500ms — stream energy",
        "Elhilali 2009"),
    _h3(7, "amplitude", 8, 1, 2,
        "Amplitude mean 500ms — stream level",
        "Elhilali 2009"),

    # === Tonalness / Harmonic Content (2 tuples) ===
    _h3(14, "tonalness", 8, 0, 2,
        "Tonalness value 500ms — harmonic content",
        "Alain 2007"),
    _h3(14, "tonalness", 14, 1, 0,
        "Tonalness mean ~900ms — sustained tonal",
        "Alain 2007"),

    # === Spectral Centroid / Spectral Identity (2 tuples) ===
    _h3(15, "spectral_centroid", 8, 0, 2,
        "Centroid value 500ms — spectral identity",
        "Elhilali 2009"),
    _h3(15, "spectral_centroid", 8, 2, 2,
        "Centroid std 500ms — spectral spread",
        "Elhilali 2009"),

    # === Spectral Change / Change Rate (1 tuple) ===
    _h3(21, "spectral_change", 8, 8, 0,
        "Spectral velocity 500ms — change rate",
        "Elhilali 2009"),

    # === Onset Strength / Event Boundaries (2 tuples) ===
    _h3(11, "onset_strength", 8, 0, 2,
        "Onset value 500ms — event boundary",
        "Bregman 1994"),
    _h3(11, "onset_strength", 8, 14, 2,
        "Onset periodicity 500ms — stream rhythm",
        "Bregman 1994"),

    # === Spectral Flux / Spectral Change (2 tuples) ===
    _h3(10, "spectral_flux", 8, 1, 2,
        "Flux mean 500ms — spectral change",
        "Elhilali 2009"),
    _h3(10, "spectral_flux", 14, 0, 0,
        "Flux value ~900ms — long change",
        "Elhilali 2009"),

    # === Loudness / Dynamic Range (2 tuples) ===
    _h3(8, "loudness", 8, 0, 2,
        "Loudness value 500ms — stream loudness",
        "Bregman 1994"),
    _h3(8, "loudness", 8, 2, 2,
        "Loudness std 500ms — dynamic range",
        "Bregman 1994"),

    # === Cross-band Coupling / Stream Binding (3 tuples) ===
    _h3(25, "x_l0l5", 8, 0, 2,
        "Coupling value 500ms — binding",
        "Elhilali 2009"),
    _h3(25, "x_l0l5", 16, 18, 0,
        "Coupling trend 1s — integration trend",
        "Elhilali 2009"),
    _h3(25, "x_l0l5", 16, 14, 2,
        "Coupling periodicity 1s — stream coherence",
        "Elhilali 2009"),
)

assert len(_AMSS_H3_DEMANDS) == 16


class AMSS(Encoder):
    """Attention-Modulated Stream Segregation -- STU Encoder (depth 1, 11D).

    Models how attention modulates auditory stream segregation in complex
    acoustic scenes. Elhilali et al. 2009: computational model of
    stream segregation driven by spectral coherence and temporal regularity,
    with attention as a top-down gain mechanism that biases competition
    between concurrent streams.

    Alain et al. 2007: ERP evidence (N=18) that stream segregation produces
    distinct object-related negativity (ORN) when harmonics are mistuned;
    attention modulates ORN amplitude, confirming top-down influence on
    pre-attentive segregation.

    Bregman 1994: foundational psychoacoustic framework for auditory scene
    analysis — frequency proximity, temporal regularity, and onset synchrony
    as primitive grouping cues; attention selects among pre-formed streams.

    Dependency chain:
        AMSS is an Encoder (Depth 1) -- reads HMCE cross-unit output.
        Computed after HMCE relay in pipeline.

    Downstream feeds:
        -> stream_segregation beliefs (Appraisal)
        -> attended_stream beliefs (Core)
        -> attention salience modulation for F3 integrators
    """

    NAME = "AMSS"
    FULL_NAME = "Attention-Modulated Stream Segregation"
    UNIT = "STU"
    FUNCTION = "F3"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ()
    CROSS_UNIT_READS = ("HMCE",)

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 5,
            ("E0:onset_tracking", "E1:harmonic_segregation",
             "E2:spectral_stream", "E3:temporal_stream",
             "E4:attention_gate"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 5, 7,
            ("M0:stream_coherence", "M1:segregation_depth"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 7, 9,
            ("P0:attended_stream", "P1:competition_state"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:stream_stability_pred", "F1:segregation_shift_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _AMSS_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:onset_tracking", "E1:harmonic_segregation",
            "E2:spectral_stream", "E3:temporal_stream",
            "E4:attention_gate",
            "M0:stream_coherence", "M1:segregation_depth",
            "P0:attended_stream", "P1:competition_state",
            "F0:stream_stability_pred", "F1:segregation_shift_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # lateral AC -- spectral stream segregation
            RegionLink("E2:spectral_stream", "lateral_AC", 0.85,
                       "Elhilali 2009"),
            # medial AC -- harmonic grouping
            RegionLink("E1:harmonic_segregation", "medial_AC", 0.80,
                       "Alain 2007"),
            # posterior STG -- stream coherence integration
            RegionLink("M0:stream_coherence", "posterior_STG", 0.75,
                       "Elhilali 2009"),
            # right AC -- attended stream selection
            RegionLink("P0:attended_stream", "right_AC", 0.70,
                       "Alain 2007"),
            # hippocampus -- stream memory / familiarity
            RegionLink("P1:competition_state", "hippocampus", 0.60,
                       "Bregman 1994"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Elhilali et al.", 2009,
                         "Computational model of auditory stream segregation "
                         "driven by spectral coherence and temporal regularity; "
                         "attention as top-down gain on stream competition; "
                         "predicts bistability and build-up effects",
                         "Computational model"),
                Citation("Alain et al.", 2007,
                         "ERP object-related negativity (ORN) indexes stream "
                         "segregation; attention modulates ORN amplitude; "
                         "mistuned harmonics segregate into separate objects",
                         "EEG, N=18"),
                Citation("Bregman", 1994,
                         "Auditory scene analysis: frequency proximity, "
                         "temporal regularity, and onset synchrony as "
                         "primitive grouping cues; attention selects among "
                         "pre-formed streams",
                         "Psychoacoustic review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Spectral stream (E2) should increase with frequency "
                "separation between concurrent sources (Elhilali 2009: "
                "coherence drops with delta-F)",
                "Attention gate (E4) should modulate stream selection "
                "(testable: Alain 2007 ORN amplitude under attend/ignore)",
                "Stream coherence (M0) should predict perceptual bistability "
                "duration (testable: Elhilali 2009 build-up paradigm)",
                "Competition state (P1) should increase with number of "
                "concurrent streams (testable: Bregman 1994 streaming "
                "paradigm with 2 vs 3 sources)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        relay_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Transform R3/H3 + HMCE relay output into 11D stream segregation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"HMCE": (B, T, hmce_dim)}``

        Returns:
            ``(B, T, 11)`` -- E(5) + M(2) + P(2) + F(2)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(e)
        p = compute_cognitive_present(e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
