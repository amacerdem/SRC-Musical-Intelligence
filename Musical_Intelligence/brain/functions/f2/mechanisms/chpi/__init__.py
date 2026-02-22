"""CHPI -- Cross-Modal Harmonic Predictive Integration.

Integrator nucleus (depth 3, reads all upstream) in PCU, Function F2. Models
how the brain predicts harmonic progressions through cross-modal integration
of visual, motor, and auditory information. Cross-modal cues (visual gesture,
motor planning) provide anticipatory signals that modulate auditory harmonic
prediction, improving chord-change detection and voice-leading tracking.

Dependency chain:
    CHPI is an Integrator (Depth 3) -- reads all upstream F2 mechanisms:
        HTP  (Relay,  12D) -- hierarchy gradient, sensory/pitch/abstract prediction
        ICEM (Relay,  13D) -- information content, surprise signal
        PWUP (depth 1, 10D) -- precision weights, uncertainty index
        WMED (depth 2, 11D) -- entrainment strength, working memory

R3 Ontology Mapping (97D freeze):
    roughness:                [0]      (A, harmonic tension proxy)
    sensory_pleasantness:     [4]      (A, chord consonance)
    periodicity:              [5]      (A, harmonic periodicity)
    harmonic_change:          [6]      (A, chord transition marker)
    tonalness:                [14]     (C, key clarity)
    tristimulus1-3:           [18:21]  (C, harmonic structure)
    spectral_change:          [21]     (D, voice-leading velocity)
    distribution_entropy:     [22]     (D, chord accent)

Output structure: E(2) + M(2) + P(3) + F(4) = 11D
  E-layer [0:2]   Extraction    (sigmoid)  scope=internal
  M-layer [2:4]   Memory        (sigmoid)  scope=internal
  P-layer [4:7]   Present       (sigmoid)  scope=hybrid
  F-layer [7:11]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/chpi/
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
    4: "125ms (theta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 4: "max", 8: "velocity",
    14: "periodicity", 18: "trend", 20: "entropy",
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
_ROUGHNESS = 0               # roughness (A group, harmonic tension proxy)
_SENSORY_PLEAS = 4           # sensory_pleasantness (A, chord consonance)
_PERIODICITY = 5             # periodicity (A, harmonic periodicity)
_HARMONIC_CHANGE = 6         # harmonic_change (A, chord transition marker)
_ONSET = 10                  # onset_strength (B, event detection)
_TONALNESS = 14              # tonalness (C, key clarity)
_TRISTIMULUS_START = 18      # tristimulus1-3 (C, harmonic structure)
_TRISTIMULUS_END = 21
_SPECTRAL_CHANGE = 21        # spectral_change (D, voice-leading velocity)
_DIST_ENTROPY = 22           # distribution_entropy (D, chord accent)
_DIST_CONCENTRATION = 23     # distribution_concentration (D)
_CHROMA_C = 25               # chroma_C (F, first chroma bin)
_CHROMA_I = 33               # chroma_I (F, 9th chroma bin, pitch_height_proxy)


# -- 20 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H0(25ms) -> H1(50ms) -> H3(100ms) -> H4(125ms) -> H8(500ms) -> H16(1s)

_CHPI_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Harmonic Change / chord transitions (3 tuples) ===
    _h3(_HARMONIC_CHANGE, "harmonic_change", 0, 0, 2,
        "Instantaneous harmonic change at 25ms -- chord onset detection",
        "Tillmann 2003"),
    _h3(_HARMONIC_CHANGE, "harmonic_change", 3, 0, 2,
        "Harmonic change at 100ms -- chord transition context",
        "Koelsch 2005"),
    _h3(_HARMONIC_CHANGE, "harmonic_change", 3, 4, 2,
        "Harmonic change max at 100ms -- peak chord transition strength",
        "Koelsch 2005"),

    # === Onset Strength / event boundary (2 tuples) ===
    _h3(_ONSET, "onset_strength", 1, 0, 2,
        "Onset at 50ms -- cross-modal event alignment",
        "Musacchia 2007"),
    _h3(_ONSET, "onset_strength", 3, 14, 2,
        "Onset periodicity at 100ms -- harmonic rhythm regularity",
        "Vuust 2022"),

    # === Roughness / harmonic tension (2 tuples) ===
    _h3(_ROUGHNESS, "roughness", 3, 0, 2,
        "Roughness at 100ms -- current harmonic tension level",
        "Koelsch 2005"),
    _h3(_ROUGHNESS, "roughness", 8, 1, 0,
        "Mean roughness over 500ms -- sustained tension context",
        "Tillmann 2003"),

    # === Sensory Pleasantness / consonance (3 tuples) ===
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 3, 0, 2,
        "Consonance at 100ms -- chord quality evaluation",
        "Tillmann 2003"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 1, 0,
        "Mean consonance over 1s -- long-range harmonic context",
        "Koelsch 2005"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 20, 0,
        "Consonance entropy over 1s -- harmonic variability",
        "Vuust 2022"),

    # === Spectral Change / voice-leading velocity (2 tuples) ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 3, 8, 0,
        "Voice-leading velocity at 100ms -- stepwise motion tracking",
        "Calvert 2001"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 4, 0, 0,
        "Spectral change at 125ms -- mid-timescale voice-leading",
        "Koelsch 2005"),

    # === Distribution Concentration (1 tuple) ===
    _h3(_DIST_CONCENTRATION, "distribution_concentration", 3, 8, 2,
        "Distribution concentration velocity at 100ms -- spectral focus change",
        "Vuust 2022"),

    # === Chroma C / tonal context (2 tuples) ===
    _h3(_CHROMA_C, "chroma_C", 3, 0, 2,
        "Chroma at 100ms -- tonal identity for chord prediction",
        "Tillmann 2003"),
    _h3(_CHROMA_C, "chroma_C", 8, 1, 0,
        "Mean chroma over 500ms -- sustained tonal context",
        "Koelsch 2005"),

    # === Chroma I (pitch_height_proxy) / pitch context (2 tuples) ===
    _h3(_CHROMA_I, "chroma_I", 4, 8, 0,
        "Pitch height velocity at 125ms -- melodic motion for voice-leading",
        "Musacchia 2007"),
    _h3(_CHROMA_I, "chroma_I", 8, 0, 0,
        "Pitch height at 500ms -- registral context for chord prediction",
        "Vuust 2022"),

    # === Tonalness / key clarity (2 tuples) ===
    _h3(_TONALNESS, "tonalness", 8, 1, 0,
        "Mean tonalness over 500ms -- tonal grounding for harmonic syntax",
        "Tillmann 2003"),
    _h3(_TONALNESS, "tonalness", 16, 1, 0,
        "Mean tonalness over 1s -- long-range key stability",
        "Koelsch 2005"),

    # === Periodicity / harmonic rhythm (1 tuple) ===
    _h3(_PERIODICITY, "periodicity", 16, 18, 0,
        "Periodicity trend over 1s -- harmonic rhythm evolution",
        "Vuust 2022"),
)

assert len(_CHPI_H3_DEMANDS) == 20


class CHPI(Integrator):
    """Cross-Modal Harmonic Predictive Integration -- PCU Integrator (depth 3, 11D).

    Models how the brain predicts harmonic progressions through cross-modal
    integration of visual, motor, and auditory information. Cross-modal cues
    provide anticipatory signals that modulate auditory harmonic prediction,
    enabling improved chord-change detection, voice-leading tracking, and
    harmonic trajectory forecasting.

    Tillmann et al. 2003: Implicit harmonic priming in STG/IFG (fMRI, N=12).
    Koelsch 2005: Neural correlates of music-syntactic processing (fMRI review).
    Vuust et al. 2022: Music in the brain (Nature Neuroscience review).
    Musacchia et al. 2007: Cross-modal brainstem AV processing (ABR, N=20).
    Calvert et al. 2001: Cross-modal integration STS convergence (fMRI, N=9).

    Dependency chain:
        CHPI is an Integrator (Depth 3) -- reads all upstream F2 mechanisms.
        HTP  -> hierarchy gradient, sensory/pitch/abstract prediction
        ICEM -> information content, surprise signal
        PWUP -> precision weights, uncertainty index
        WMED -> entrainment strength, working memory

    Downstream feeds:
        -> Scheduler beliefs: harmonic_prediction, crossmodal_integration
        -> Relay exports: harmonic_trajectory, integration_confidence
    """

    NAME = "CHPI"
    FULL_NAME = "Cross-Modal Harmonic Predictive Integration"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("HTP", "ICEM", "PWUP", "WMED")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:crossmodal_prediction_gain", "E1:voiceleading_parsimony"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 2, 4,
            ("M0:visual_motor_lead", "M1:harmonic_surprise_mod"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:harmonic_context_strength", "P1:crossmodal_convergence",
             "P2:voiceleading_smoothness"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 11,
            ("F0:next_chord_prediction", "F1:crossmodal_anticipation",
             "F2:harmonic_trajectory", "F3:integration_confidence"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _CHPI_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:crossmodal_prediction_gain", "E1:voiceleading_parsimony",
            "M0:visual_motor_lead", "M1:harmonic_surprise_mod",
            "P0:harmonic_context_strength", "P1:crossmodal_convergence",
            "P2:voiceleading_smoothness",
            "F0:next_chord_prediction", "F1:crossmodal_anticipation",
            "F2:harmonic_trajectory", "F3:integration_confidence",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # A1/HG -- harmonic pitch processing
            RegionLink("E0:crossmodal_prediction_gain", "A1_HG", 0.80,
                       "Koelsch 2005"),
            # STG -- harmonic syntax processing
            RegionLink("P0:harmonic_context_strength", "STG", 0.85,
                       "Tillmann 2003"),
            # STS -- cross-modal audiovisual convergence
            RegionLink("P1:crossmodal_convergence", "STS", 0.80,
                       "Calvert 2001"),
            # IFG -- harmonic syntax (music ERAN)
            RegionLink("F0:next_chord_prediction", "IFG", 0.75,
                       "Koelsch 2005"),
            # Left IFOF -- audiovisual pathway
            RegionLink("F1:crossmodal_anticipation", "L_IFOF", 0.65,
                       "Musacchia 2007"),
            # IPS/Precuneus -- cross-modal feature binding
            RegionLink("P2:voiceleading_smoothness", "IPS", 0.70,
                       "Vuust 2022"),
            # Anterior Insula -- multisensory salience
            RegionLink("F3:integration_confidence", "AI", 0.60,
                       "Vuust 2022"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # CHPI is purely predictive, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Tillmann et al.", 2003,
                         "Implicit harmonic priming: STG/IFG activation to "
                         "harmonically related vs unrelated chords; harmonic "
                         "syntax processed in auditory association cortex",
                         "fMRI, N=12"),
                Citation("Koelsch", 2005,
                         "Neural correlates of music-syntactic processing: "
                         "ERAN in IFG/STG for harmonic expectancy violations; "
                         "hierarchical harmonic structure engages Broca homolog",
                         "fMRI review"),
                Citation("Vuust et al.", 2022,
                         "Music in the brain: predictive processing framework "
                         "for music perception; cross-modal integration of "
                         "auditory, visual, motor predictions",
                         "Nature Neuroscience review"),
                Citation("Musacchia et al.", 2007,
                         "Musicians show enhanced cross-modal brainstem "
                         "processing: audiovisual training strengthens ABR "
                         "encoding of speech/music fundamentals",
                         "ABR, N=20"),
                Citation("Calvert et al.", 2001,
                         "Crossmodal integration in STS: superadditive "
                         "responses to congruent AV stimuli; STS as "
                         "convergence zone for multisensory binding",
                         "fMRI, N=9"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Harmonic priming should activate STG/IFG network "
                "(confirmed: Tillmann 2003, Koelsch 2005)",
                "Cross-modal congruent stimuli should enhance prediction "
                "(testable via AV congruency paradigm)",
                "Musicians should show stronger cross-modal integration "
                "(confirmed: Musacchia 2007)",
                "Disrupting STS should reduce cross-modal harmonic benefit "
                "(testable via TMS)",
                "Voice-leading smoothness should correlate with harmonic "
                "expectancy fulfillment (testable via behavioral priming)",
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
        """Transform R3/H3 + upstream into 11D cross-modal harmonic prediction.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"HTP": (B,T,12), "ICEM": (B,T,13),
                                 "PWUP": (B,T,10), "WMED": (B,T,11)}``
            cross_unit_inputs: Optional cross-unit pathway data (unused).

        Returns:
            ``(B, T, 11)`` -- E(2) + M(2) + P(3) + F(4)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m,
                                      upstream_outputs)
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
