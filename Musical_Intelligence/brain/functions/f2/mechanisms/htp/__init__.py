"""HTP — Hierarchical Temporal Prediction.

Relay nucleus (depth 0) in PCU, Function F2. Models how predictive
representations follow a hierarchical temporal pattern: high-level
abstract features are predicted ~500ms before input, mid-level ~200ms,
low-level ~110ms. Post-stimulus, high-level representations are
"silenced" (explained away) while low-level persist as prediction errors.

Dependency chain:
    HTP is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    First mechanism computed in F2 pipeline.

R3 Ontology Mapping (old 49D -> 97D freeze):
    amplitude:           [7]  -> [7]    (B, unchanged)
    onset_strength:      [10] -> [11]   (B, was spectral_flux, shifted+renamed)
    sharpness:           [9]  -> [13]   (C, was spectral_centroid, remapped)
    spectral_auto:       [25] -> [17]   (C, replaces dissolved x_l0l5)
    tristimulus1-3:      [18:21] -> [18:21] (C, unchanged, R3 direct)
    spectral_flux:       [21] -> [21]   (D, was spectral_change, renamed)
    pitch_salience:      [33] -> [39]   (F, replaces dissolved x_l4l5)
    tonal_stability:     [41] -> [60]   (H, replaces dissolved x_l5l7)

Output structure: E(4) + M(3) + P(3) + F(2) = 12D
  E-layer [0:4]   Extraction    (sigmoid)  scope=internal
  M-layer [4:7]   Memory        (sigmoid)  scope=internal
  P-layer [7:10]  Present       (sigmoid)  scope=hybrid
  F-layer [10:12] Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/htp/
See Docs/C3/Models/PCU-a1-HTP/HTP.md (original model specification)
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
    1: "50ms (gamma)",
    3: "100ms (alpha-beta)",
    4: "125ms (theta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity", 13: "entropy", 14: "periodicity",
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
_AMPLITUDE = 7            # amplitude (B group, unchanged)
_ONSET = 11               # onset_strength (B, was spectral_flux at old [10])
_SHARPNESS = 13           # sharpness (C, proxy for spectral_centroid)
_SPECTRAL_AUTO = 17       # spectral_autocorrelation (C, replaces x_l0l5)
_SPECTRAL_FLUX = 21       # spectral_flux (D, was spectral_change)
_PITCH_SALIENCE = 39      # pitch_salience (F, replaces x_l4l5)
_TONAL_STABILITY = 60     # tonal_stability (H, replaces x_l5l7)


# -- 18 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H0(25ms) -> H1(50ms) -> H3(100ms) -> H4(125ms) -> H8(500ms) -> H16(1s)

_HTP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Amplitude / Low-level (3 tuples) ===
    _h3(_AMPLITUDE, "amplitude", 0, 0, 2,
        "Instantaneous amplitude at 25ms — low-level sensory",
        "de Vries & Wurm 2023"),
    _h3(_AMPLITUDE, "amplitude", 3, 0, 2,
        "Amplitude at 100ms — sensory context",
        "Norman-Haignere 2022"),
    _h3(_AMPLITUDE, "amplitude", 3, 2, 2,
        "Amplitude variability over 100ms — prediction error proxy",
        "de Vries & Wurm 2023"),

    # === Onset Strength / Low-level (3 tuples) ===
    _h3(_ONSET, "onset_strength", 0, 0, 2,
        "Instant onset detection at 25ms — event boundary",
        "Forseth 2020"),
    _h3(_ONSET, "onset_strength", 1, 1, 2,
        "Mean onset over 50ms — sustained detection",
        "Forseth 2020"),
    _h3(_ONSET, "onset_strength", 3, 14, 2,
        "Onset periodicity over 100ms — rhythmic regularity",
        "de Vries & Wurm 2023"),

    # === Sharpness / Mid-level (3 tuples, replaces spectral_centroid) ===
    _h3(_SHARPNESS, "sharpness", 3, 0, 2,
        "Brightness at 100ms — mid-level prediction target",
        "Norman-Haignere 2022"),
    _h3(_SHARPNESS, "sharpness", 4, 8, 0,
        "Brightness velocity at 125ms — pitch/timbre dynamics",
        "de Vries & Wurm 2023"),
    _h3(_SHARPNESS, "sharpness", 8, 1, 0,
        "Mean brightness over 500ms — sustained timbral context",
        "Golesorkhi 2021"),

    # === Spectral Flux / Change (2 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 8, 0,
        "Spectral change velocity at 100ms — prediction error trigger",
        "Carbajal & Malmierca 2018"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 4, 0, 0,
        "Spectral change at 125ms — mid-timescale dynamics",
        "de Vries & Wurm 2023"),

    # === Tonal Stability / High-level (4 tuples, replaces x_l5l7) ===
    _h3(_TONAL_STABILITY, "tonal_stability", 8, 0, 0,
        "Tonal stability at 500ms — high-level structure (replaces x_l5l7)",
        "Bonetti 2024"),
    _h3(_TONAL_STABILITY, "tonal_stability", 8, 1, 0,
        "Mean tonal stability over 500ms — sustained structure",
        "Golesorkhi 2021"),
    _h3(_TONAL_STABILITY, "tonal_stability", 16, 1, 0,
        "Mean tonal stability over 1s — long-range prediction template",
        "Bonetti 2024"),
    _h3(_TONAL_STABILITY, "tonal_stability", 16, 13, 0,
        "Tonal stability entropy over 1s — structural uncertainty",
        "Cheung 2019"),

    # === Spectral Autocorrelation / Low-level coupling (2 tuples, replaces x_l0l5) ===
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 3, 0, 2,
        "Cross-band coupling at 100ms — low-level integration (replaces x_l0l5)",
        "Norman-Haignere 2022"),
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 3, 2, 2,
        "Cross-band coupling variability — prediction error at low level",
        "Norman-Haignere 2022"),

    # === Pitch Salience / Mid-level coupling (1 tuple, replaces x_l4l5) ===
    _h3(_PITCH_SALIENCE, "pitch_salience", 4, 8, 0,
        "Pitch salience velocity at 125ms — mid-level dynamics (replaces x_l4l5)",
        "Forseth 2020"),
)

assert len(_HTP_H3_DEMANDS) == 18


class HTP(Relay):
    """Hierarchical Temporal Prediction — PCU Relay (depth 0, 12D).

    Models hierarchical temporal prediction: high-level abstract features
    are predicted ~500ms ahead, mid-level ~200ms, low-level ~110ms.
    Post-stimulus, high-level representations are silenced (explained
    away) while low-level persist as prediction errors.

    de Vries & Wurm 2023: ηp² = 0.49 (large), F(2)=19.9, p=8.3e-7.
    Norman-Haignere 2022: hierarchical integration 50-400ms (iEEG).
    Bonetti 2024: feedforward auditory cortex → hippocampus/cingulate.
    Golesorkhi 2021: intrinsic timescales follow core-periphery (η²=0.86).

    Dependency chain:
        HTP is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> SPH (hierarchical timing for spatiotemporal prediction)
        -> ICEM (abstract prediction modulates surprise)
        -> PWUP (hierarchy sets precision weights)
        -> PSH (sensory match for silencing)
        -> prediction_hierarchy, prediction_accuracy beliefs (Core)
        -> hierarchy_coherence belief (Appraisal)
        -> abstract_future, midlevel_future beliefs (Anticipation)
    """

    NAME = "HTP"
    FULL_NAME = "Hierarchical Temporal Prediction"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:high_level_lead", "E1:mid_level_lead",
             "E2:low_level_lead", "E3:hierarchy_gradient"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 7,
            ("M0:latency_high", "M1:latency_mid", "M2:latency_low"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 7, 10,
            ("P0:sensory_match", "P1:pitch_prediction",
             "P2:abstract_prediction"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 10, 12,
            ("F0:abstract_future_500ms", "F1:midlevel_future_200ms"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _HTP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:high_level_lead", "E1:mid_level_lead",
            "E2:low_level_lead", "E3:hierarchy_gradient",
            "M0:latency_high", "M1:latency_mid", "M2:latency_low",
            "P0:sensory_match", "P1:pitch_prediction",
            "P2:abstract_prediction",
            "F0:abstract_future_500ms", "F1:midlevel_future_200ms",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # aIPL — abstract prediction (~500ms)
            RegionLink("E0:high_level_lead", "aIPL", 0.80,
                       "de Vries & Wurm 2023"),
            # STG — mid-to-long integration 200-500ms
            RegionLink("P2:abstract_prediction", "STG", 0.75,
                       "Norman-Haignere 2022"),
            # A1/HG — low-level prediction (110ms)
            RegionLink("P0:sensory_match", "A1_HG", 0.85,
                       "Forseth 2020"),
            # Planum temporale — content prediction via high-gamma
            RegionLink("P1:pitch_prediction", "PT", 0.70,
                       "Forseth 2020"),
            # Hippocampus — sequence memory / prediction error
            RegionLink("P2:abstract_prediction", "HIPP", 0.65,
                       "Bonetti 2024"),
            # ACC — prediction error integration
            RegionLink("F0:abstract_future_500ms", "ACC", 0.60,
                       "Bonetti 2024"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # HTP is purely predictive, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("de Vries & Wurm", 2023,
                         "500ms abstract, 200ms view-dependent, 110ms low-level "
                         "prediction; high-level silenced post-stimulus; "
                         "ηp²=0.49, F(2)=19.9, p=8.3e-7",
                         "MEG, N=22"),
                Citation("Norman-Haignere", 2022,
                         "Hierarchical integration 50-400ms in auditory cortex; "
                         "short (<200ms)=spectrotemporal, long (>200ms)="
                         "category-selective; r>0.5 cross-context",
                         "iEEG, N=7"),
                Citation("Bonetti", 2024,
                         "Feedforward auditory cortex → hippocampus/cingulate; "
                         "feedback in reverse; musical sequence recognition; "
                         "p<0.001",
                         "MEG, N=83"),
                Citation("Golesorkhi", 2021,
                         "Intrinsic neural timescales follow core-periphery; "
                         "core (DMN/FPN) longer than periphery (sensory); "
                         "d=-1.63, η²=0.86",
                         "MEG, N=89"),
                Citation("Forseth", 2020,
                         "Dual prediction in early auditory cortex: HG "
                         "(timing, low-freq phase) + PT (content, high-gamma); "
                         "p<0.001",
                         "iEEG, N=37"),
                Citation("Carbajal & Malmierca", 2018,
                         "SSA + MMN = same deviance detection mechanism; "
                         "hierarchical from subcortical IC to cortex; "
                         "MMN peak 150-250ms",
                         "Review (cellular)"),
                Citation("Cheung", 2019,
                         "Amygdala/hippocampus uncertainty x surprise; "
                         "NAc uncertainty; harmonic expectancy salience",
                         "fMRI, N=79"),
                Citation("Egermann", 2013,
                         "IDyOM predicts expectation violations; high-IC "
                         "events produce arousal (SCR, EMG); p<0.05",
                         "Behavioral + psychophysiology, N=50"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "High-level predictions must precede low-level by ~390ms "
                "(confirmed: de Vries & Wurm 2023)",
                "Post-stimulus high-level should be silenced "
                "(confirmed: de Vries & Wurm 2023)",
                "Disrupting high-level areas should abolish 500ms predictions "
                "(testable via TMS/lesion)",
                "Novel stimuli should show delayed prediction timing "
                "(testable via novelty paradigm)",
                "Learning should shift prediction timing earlier "
                "(testable via training study)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 12D hierarchical temporal prediction.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 12)`` — E(4) + M(3) + P(3) + F(2)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, m)
        f = compute_forecast(h3_features, e)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
