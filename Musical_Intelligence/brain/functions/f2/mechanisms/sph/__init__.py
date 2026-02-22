"""SPH — Spatiotemporal Prediction Hierarchy.

Relay nucleus (depth 0) in PCU, Function F2. Models how auditory memory
recognition engages hierarchical feedforward-feedback loops between Heschl's
gyrus, hippocampus, and cingulate, with distinct oscillatory signatures:
gamma (>30Hz) for matched/memorised sequences, alpha-beta (2-20Hz) for
varied/prediction-error sequences.

Dependency chain:
    SPH is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Conceptually downstream of HTP (SPH extends HTP's hierarchical timing
    to spatiotemporal memory recognition), but computes independently from
    R3/H3 features.

R3 Ontology Mapping (old 49D -> 97D freeze):
    sensory_pleasantness:  [4]  -> [4]    (A, unchanged)
    amplitude:             [7]  -> [7]    (B, unchanged)
    onset_strength:        [10] -> [11]   (B, was spectral_flux, shifted+renamed)
    spectral_auto:         [25] -> [17]   (C, replaces dissolved x_l0l5)
    spectral_flux:         [21] -> [21]   (D, was spectral_change, renamed)
    distribution_entropy:  [22] -> [22]   (D, was energy_change, remapped)
    chroma_C:              [49] -> [25]   (F, v2 expansion, first chroma bin)
    pitch_height:          [61] -> [37]   (F, v2 expansion)
    pitch_salience:        [63] -> [39]   (F, v2 expansion)
    tonal_stability:       [41] -> [60]   (H, replaces dissolved x_l5l7)

Output structure: E(4) + M(4) + P(3) + F(3) = 14D
  E-layer [0:4]   Extraction    (sigmoid)  scope=internal
  M-layer [4:8]   Memory        (sigmoid)  scope=internal
  P-layer [8:11]  Present       (sigmoid)  scope=hybrid
  F-layer [11:14] Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/sph/
See Docs/C3/Models/PCU-a2-SPH/SPH.md (original model specification)
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Relay
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
    3: "100ms (alpha-beta)",
    4: "125ms (theta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    13: "entropy", 14: "periodicity",
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
_SENSORY_PLEAS = 4        # sensory_pleasantness (A group)
_AMPLITUDE = 7            # amplitude (B group)
_ONSET = 11               # onset_strength (B, was spectral_flux at old [10])
_SPECTRAL_AUTO = 17       # spectral_autocorrelation (C, replaces x_l0l5)
_SPECTRAL_FLUX = 21       # spectral_flux (D, was spectral_change)
_DIST_ENTROPY = 22        # distribution_entropy (D, was energy_change)
_CHROMA_C = 25            # chroma_C (F, v2 expansion)
_PITCH_HEIGHT = 37        # pitch_height (F, v2 expansion)
_PITCH_SALIENCE = 39      # pitch_salience (F, v2 expansion)
_TONAL_STABILITY = 60     # tonal_stability (H, replaces x_l5l7)


# -- 21 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H0(25ms) -> H3(100ms) -> H4(125ms) -> H8(500ms) -> H16(1s)

_SPH_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Onset Strength / Low-level (3 tuples) ===
    _h3(_ONSET, "onset_strength", 0, 0, 2,
        "Instantaneous onset at 25ms — event boundary detection",
        "Bonetti 2024"),
    _h3(_ONSET, "onset_strength", 3, 0, 2,
        "Onset at 100ms — sustained detection for deviation",
        "Bonetti 2024"),
    _h3(_ONSET, "onset_strength", 3, 14, 2,
        "Onset periodicity over 100ms — rhythmic regularity context",
        "de Vries & Wurm 2023"),

    # === Amplitude (2 tuples) ===
    _h3(_AMPLITUDE, "amplitude", 3, 0, 2,
        "Amplitude at 100ms — deviation detection input",
        "Norman-Haignere 2022"),
    _h3(_AMPLITUDE, "amplitude", 3, 2, 2,
        "Amplitude variability at 100ms — mismatch response",
        "Bonetti 2024"),

    # === Sensory Pleasantness / Consonance (2 tuples) ===
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 3, 0, 2,
        "Consonance at 100ms — memory match indicator",
        "Bonetti 2024"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 1, 0,
        "Mean consonance over 1s — long-range harmonic context",
        "Fernandez-Rubio 2022"),

    # === Spectral Flux / Change (2 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Spectral change at 100ms — deviation signal",
        "Carbajal & Malmierca 2018"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 2, 2,
        "Spectral change variability at 100ms — prediction error magnitude",
        "Bonetti 2024"),

    # === Distribution Entropy (1 tuple) ===
    _h3(_DIST_ENTROPY, "distribution_entropy", 4, 8, 0,
        "Entropy velocity at 125ms — rate of distributional change",
        "Fong 2020"),

    # === Spectral Autocorrelation / replaces x_l0l5 (2 tuples) ===
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 3, 0, 2,
        "Cross-band coupling at 100ms — feedforward pathway (replaces x_l0l5)",
        "Norman-Haignere 2022"),
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 16, 1, 0,
        "Mean cross-band coupling over 1s — sustained feedforward context",
        "Golesorkhi 2021"),

    # === Tonal Stability / replaces x_l5l7 (4 tuples) ===
    _h3(_TONAL_STABILITY, "tonal_stability", 3, 0, 2,
        "Tonal stability at 100ms — hierarchy position (replaces x_l5l7)",
        "Bonetti 2024"),
    _h3(_TONAL_STABILITY, "tonal_stability", 8, 1, 0,
        "Mean tonal stability over 500ms — mid-range structural context",
        "Golesorkhi 2021"),
    _h3(_TONAL_STABILITY, "tonal_stability", 16, 1, 0,
        "Mean tonal stability over 1s — long-range hierarchy template",
        "Bonetti 2024"),
    _h3(_TONAL_STABILITY, "tonal_stability", 16, 13, 0,
        "Tonal stability entropy over 1s — structural uncertainty",
        "Cheung 2019"),

    # === Pitch v2 Expansion (5 tuples) ===
    _h3(_CHROMA_C, "chroma_C", 3, 0, 2,
        "Chroma at 100ms — tonal identity for sequence matching",
        "Fernandez-Rubio 2022"),
    _h3(_CHROMA_C, "chroma_C", 16, 1, 0,
        "Mean chroma over 1s — long-range tonal context",
        "Fernandez-Rubio 2022"),
    _h3(_PITCH_HEIGHT, "pitch_height", 3, 0, 2,
        "Pitch height at 100ms — sequence element identification",
        "Bonetti 2024"),
    _h3(_PITCH_HEIGHT, "pitch_height", 8, 8, 0,
        "Pitch height velocity at 500ms — melodic contour prediction",
        "de Vries & Wurm 2023"),
    _h3(_PITCH_SALIENCE, "pitch_salience", 3, 0, 2,
        "Pitch salience at 100ms — pitch clarity modulates memory match",
        "Norman-Haignere 2022"),
)

assert len(_SPH_H3_DEMANDS) == 21


class SPH(Relay):
    """Spatiotemporal Prediction Hierarchy — PCU Relay (depth 0, 14D).

    Models auditory memory recognition through hierarchical feedforward-
    feedback loops. Distinct oscillatory signatures: gamma for matched
    (memorised) sequences, alpha-beta for varied (prediction error).
    Final tone reshapes hierarchy — cingulate assumes top position.

    Bonetti et al. 2024: feedforward Heschl→Hippocampus→Cingulate, feedback
    in reverse. Memorised=positive ~350ms, varied=negative ~250ms.
    Fernandez-Rubio et al. 2022: tonal recognition engages hippocampus +
    cingulate (p=0.002).
    Golesorkhi et al. 2021: intrinsic timescales follow core-periphery
    hierarchy (η²=0.86).

    Dependency chain:
        SPH is a Relay (Depth 0) — reads R3/H3 directly.
        Conceptually extends HTP hierarchical timing to memory recognition.

    Downstream feeds:
        -> ICEM (gamma match signal for information content)
        -> PWUP (prediction error for precision weighting)
        -> IMU (memory match + sequence completion signals)
        -> sequence_match belief (Core)
        -> error_propagation, oscillatory_signature beliefs (Appraisal)
        -> sequence_completion belief (Anticipation)
    """

    NAME = "SPH"
    FULL_NAME = "Spatiotemporal Prediction Hierarchy"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 14

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:gamma_match", "E1:alpha_beta_error",
             "E2:hierarchy_position", "E3:feedforward_feedback"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 8,
            ("M0:match_response", "M1:varied_response",
             "M2:gamma_power", "M3:alpha_beta_power"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 8, 11,
            ("P0:memory_match", "P1:prediction_error",
             "P2:deviation_detection"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 11, 14,
            ("F0:next_tone_pred_350ms", "F1:sequence_completion_2s",
             "F2:decision_evaluation"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SPH_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:gamma_match", "E1:alpha_beta_error",
            "E2:hierarchy_position", "E3:feedforward_feedback",
            "M0:match_response", "M1:varied_response",
            "M2:gamma_power", "M3:alpha_beta_power",
            "P0:memory_match", "P1:prediction_error",
            "P2:deviation_detection",
            "F0:next_tone_pred_350ms", "F1:sequence_completion_2s",
            "F2:decision_evaluation",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Heschl's Gyrus — auditory input, feedforward origin
            RegionLink("E0:gamma_match", "A1_HG", 0.85,
                       "Bonetti 2024"),
            # Hippocampus — memory match/mismatch comparison
            RegionLink("P0:memory_match", "HIPP", 0.80,
                       "Bonetti 2024"),
            # Anterior Cingulate — prediction error evaluation
            RegionLink("P1:prediction_error", "ACC", 0.75,
                       "Bonetti 2024"),
            # Medial Cingulate — sequence recognition, hierarchy top
            RegionLink("E2:hierarchy_position", "MC", 0.70,
                       "Bonetti 2024"),
            # STG — non-primary auditory processing
            RegionLink("P2:deviation_detection", "STG", 0.75,
                       "Norman-Haignere 2022"),
            # IFG — phrase-level chunking
            RegionLink("F1:sequence_completion_2s", "IFG", 0.60,
                       "Rimmele 2021"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # SPH is purely predictive, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bonetti et al.", 2024,
                         "Feedforward Heschl→Hippocampus→Cingulate; feedback "
                         "in reverse; memorised=positive ~350ms, varied="
                         "negative ~250ms; gamma M>N, alpha-beta N>M; "
                         "cingulate top at final tone; d=0.09-0.34",
                         "MEG + DCM, N=83"),
                Citation("Fernandez-Rubio et al.", 2022,
                         "Tonal recognition engages hippocampus + cingulate; "
                         "atonal engages auditory cortex; slow band (0.1-1Hz) "
                         "global recognition, fast band (2-8Hz) local; "
                         "F(3,280)=6.87, p=0.002",
                         "MEG, N=71"),
                Citation("Golesorkhi et al.", 2021,
                         "Intrinsic neural timescales follow core-periphery; "
                         "core (DMN/FPN) longer than periphery (sensory); "
                         "d=0.66-1.63, η²=0.86",
                         "MEG, N=89"),
                Citation("Norman-Haignere et al.", 2022,
                         "Hierarchical integration 50-400ms in auditory cortex; "
                         "short (<200ms)=spectrotemporal, long (>200ms)="
                         "category-selective; r>0.5 cross-context",
                         "iEEG, N=18"),
                Citation("de Vries & Wurm", 2023,
                         "Hierarchical prediction timing: 500ms abstract, "
                         "200ms view-dependent, 110ms low-level; "
                         "ηp²=0.49, F(2)=19.9, p=8.3e-7",
                         "MEG, N=22"),
                Citation("Carbajal & Malmierca", 2018,
                         "SSA + MMN = same deviance detection mechanism; "
                         "hierarchical from subcortical IC to cortex",
                         "Review (cellular)"),
                Citation("Fong et al.", 2020,
                         "MMN under predictive coding: prediction error "
                         "propagates upward; frontal cortex, STG, thalamus, "
                         "hippocampus generate MMN; peak 150-250ms",
                         "Review (EEG/MEG)"),
                Citation("Cheung et al.", 2019,
                         "Amygdala/hippocampus uncertainty x surprise; "
                         "NAc uncertainty; harmonic expectancy salience",
                         "fMRI, N=79"),
                Citation("Rimmele et al.", 2021,
                         "Cortical delta oscillations underpin prosodic "
                         "chunking at phrase-level timescale; p<0.001",
                         "MEG, N=19"),
                Citation("Sabat et al.", 2025,
                         "Neurons integrate within constrained temporal "
                         "windows ~15-150ms; windows increase primary→"
                         "non-primary auditory cortex",
                         "Single-neuron (ferret), N=541 neurons"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Hippocampal lesions should abolish memory-based predictions "
                "(testable via lesion studies)",
                "Novel sequences should show only varied (N) response pattern "
                "(testable via novelty paradigms)",
                "TMS disrupting gamma should reduce match signal "
                "(testable via TMS)",
                "Match response (350ms) follows error (250ms) in temporal order "
                "(confirmed: Bonetti 2024)",
                "Final tone reshapes hierarchy — cingulate assumes top position "
                "(confirmed: Bonetti 2024)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 14D spatiotemporal prediction hierarchy.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 14)`` — E(4) + M(4) + P(3) + F(3)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(r3_features, h3_features, e)
        p = compute_cognitive_present(h3_features, m)
        f = compute_forecast(h3_features, e)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
