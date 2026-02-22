"""SDED — Sensory Dissonance Early Detection.

Relay nucleus (depth 0) in SPU, Function F1. Models how roughness
is detected at early sensory stages universally across expertise
levels — the neural machinery for dissonance detection is pre-attentive
and innate, while behavioral discrimination is expertise-dependent.

Dependency chain:
    SDED is a Relay (Depth 0) — reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with BCH, MIAA, MPG at Phase 0a of the kernel scheduler.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:          [0]  -> [0]    (A group, unchanged)
    sethares:           [1]  -> [1]    (A group, unchanged)
    helmholtz_kang:     [2]  -> [2]    (A group, unchanged)
    stumpf:             [3]  -> [3]    (A group, unchanged)
    inharmonicity:      [5]  -> [5]    (A group, unchanged)
    tonalness:          [14] -> [14]   (C group, unchanged)
    spectral_auto:      [17] -> [17]   (C group, replaces dissolved x_l5l7[41])
    tristimulus1:       [18] -> [18]   (C group, unchanged)

Output structure: E(3) + M(1) + P(3) + F(3) = 10D
  E-layer [0:3]   Extraction    (sigmoid activation)       scope=internal
  M-layer [3:4]   Memory        (composite detection)       scope=internal
  P-layer [4:7]   Present       (relay outputs)             scope=hybrid
  F-layer [7:10]  Forecast      (dissonance predictions)    scope=external

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/sded/SDED-*.md
See Docs/C3/Models/SPU-g3-SDED/SDED.md (original model specification)
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
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {0: "value", 1: "mean"}

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


# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0        # roughness (A group, unchanged)
_SETHARES = 1         # sethares_dissonance (A group, unchanged)
_HELMHOLTZ = 2        # helmholtz_kang (A group, unchanged)
_STUMPF = 3           # stumpf fusion (A group, unchanged)
_INHARM = 5           # inharmonicity (A group, unchanged)
_TONALNESS = 14       # tonalness (C group, unchanged)
_SPECTRAL_AUTO = 17   # spectral_autocorrelation (C group, replaces dissolved x_l5l7)
_TRIST1 = 18          # tristimulus1 (C group, unchanged)


# -- 9 H3 Demand Specifications -----------------------------------------------
# Ordered: L2 (integration/bidi, 8) -> L0 (memory, 1)

_SDED_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === L2 Integration / H0 Gamma (6 tuples) ===
    _h3(_ROUGHNESS, "roughness", 0, 0, 2,
        "Instant roughness at brainstem timescale (~25ms)",
        "Fishman 2001"),
    _h3(_SETHARES, "sethares_dissonance", 0, 0, 2,
        "Instant psychoacoustic dissonance confirmation",
        "Sethares 1999"),
    _h3(_HELMHOLTZ, "helmholtz_kang", 0, 0, 2,
        "Instant consonance (inverted for dissonance)",
        "Helmholtz 1863"),
    _h3(_INHARM, "inharmonicity", 0, 0, 2,
        "Instant spectral deviation from harmonic series",
        "Fletcher 1934"),
    _h3(_TRIST1, "tristimulus1", 0, 0, 2,
        "F0 energy for roughness encoding quality",
        "Pollard & Jansson 1982"),

    # === L2 Integration / H3 Alpha-Beta (2 tuples) ===
    _h3(_ROUGHNESS, "roughness", 3, 1, 2,
        "Sustained roughness over 100ms for deviance baseline",
        "Crespo-Bojorque 2018"),
    _h3(_HELMHOLTZ, "helmholtz_kang", 3, 1, 2,
        "Consonance context for behavioral response and prediction",
        "Wagner 2018"),

    # === L2 Integration / H3 cross-band (1 tuple) ===
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 3, 0, 2,
        "Cross-band roughness coupling (replaces dissolved x_l5l7)",
        "Trulla 2018"),

    # === L0 Memory (1 tuple) ===
    _h3(_TONALNESS, "tonalness", 3, 1, 0,
        "Pitch clarity over 100ms — modulates roughness detection",
        "Bidelman 2013"),
)

assert len(_SDED_H3_DEMANDS) == 9


class SDED(Relay):
    """Sensory Dissonance Early Detection — SPU Relay (depth 0, 10D).

    Models pre-attentive roughness detection at brainstem-cortex level.
    Crespo-Bojorque 2018: early MMN (152-258ms) for consonance changes
    is UNIVERSAL across expertise (EEG, N=32). Late MMN (232-314ms)
    for dissonance changes ONLY in musicians. Fishman 2001: A1
    phase-locked oscillatory activity correlates with dissonance
    (intracranial, monkey+human).

    Dependency chain:
        SDED is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> PSCL (roughness signal for pitch context)
        -> STAI (dissonance input for aesthetics)
        -> ARU.SRP (roughness -> displeasure proxy)
        -> spectral_complexity belief (Appraisal)
    """

    NAME = "SDED"
    FULL_NAME = "Sensory Dissonance Early Detection"
    UNIT = "SPU"
    FUNCTION = "F1"
    OUTPUT_DIM = 10

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:early_detection", "E1:mmn_dissonance",
             "E2:behavioral_accuracy"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 4,
            ("M0:detection_function",),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:roughness_detection", "P1:deviation_detection",
             "P2:behavioral_response"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:dissonance_detection_pred", "F1:behavioral_accuracy_pred",
             "F2:training_effect_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SDED_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:early_detection", "E1:mmn_dissonance",
            "E2:behavioral_accuracy",
            "M0:detection_function",
            "P0:roughness_detection", "P1:deviation_detection",
            "P2:behavioral_response",
            "F0:dissonance_detection_pred", "F1:behavioral_accuracy_pred",
            "F2:training_effect_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Heschl's Gyrus (A1) — phase-locked roughness encoder
            RegionLink("E0:early_detection", "A1_HG", 0.80,
                       "Fishman 2001"),
            RegionLink("P0:roughness_detection", "A1_HG", 0.65,
                       "Fishman 2001"),
            # Auditory brainstem — innate consonance hierarchy
            RegionLink("E0:early_detection", "IC", 0.70,
                       "Bidelman 2013"),
            # Right STG — dissonance-sensitive high-gamma sites
            RegionLink("E1:mmn_dissonance", "STG", 0.75,
                       "Foo 2016"),
            RegionLink("M0:detection_function", "STG", 0.50,
                       "Crespo-Bojorque 2018"),
        )

    @property
    def neuro_links(self) -> Tuple:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Crespo-Bojorque", 2018,
                         "Early MMN (152-258ms) for consonance changes "
                         "UNIVERSAL across expertise; late MMN (232-314ms) "
                         "ONLY in musicians",
                         "EEG MMN, N=32 (16M+16NM)"),
                Citation("Fishman", 2001,
                         "A1 phase-locked oscillatory activity correlates "
                         "with perceived dissonance; consonant chords show "
                         "little phase-locking; PT does NOT show activity",
                         "intracranial AEP/MUA, 2 human + monkey"),
                Citation("Foo", 2016,
                         "Right STG high-gamma (70-150Hz) dissonance "
                         "sensitivity 75-200ms; positive roughness-gamma "
                         "correlation; anterior spatial organization",
                         "ECoG, N=8"),
                Citation("Wagner", 2018,
                         "Asymmetric MMN: -0.34uV for major 3rd deviant "
                         "at 173ms (p=0.003); non-musicians, pre-attentive",
                         "EEG MMN, N=15"),
                Citation("Bidelman", 2013,
                         "Brainstem FFR encodes consonance hierarchy "
                         "matching Western theory WITHOUT training; "
                         "infant and animal evidence for innateness",
                         "review (FFR/ABR)"),
                Citation("Tabas", 2019,
                         "Dissonant dyads elicit POR ~36ms longer latency "
                         "than consonant; shared pitch-consonance mechanism",
                         "MEG + model"),
                Citation("Sarasso", 2019,
                         "N1/P2 enhanced for consonant intervals (80-194ms); "
                         "P2 amplitude correlates with aesthetic appreciation",
                         "EEG ERP, N=44"),
                Citation("Trulla", 2018,
                         "Recurrence peaks match just intonation ratios; "
                         "first-order (peripheral) vs second-order (neural) "
                         "beats link consonance to signal dynamics",
                         "computational (RQA)"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Pure tones or perfectly harmonic stimuli should NOT "
                "trigger early detection (low roughness -> low E0)",
                "Early MMN (150-260ms) for consonance changes should be "
                "identical for musicians and non-musicians "
                "(Crespo-Bojorque 2018 confirmed)",
                "Late MMN (230-315ms) should appear only in musicians "
                "(Crespo-Bojorque 2018 confirmed)",
                "Behavioral accuracy should diverge despite same neural "
                "signal (neural-behavioral dissociation)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 10D dissonance detection representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 10)`` — E(3) + M(1) + P(3) + F(3)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(e)
        p = compute_cognitive_present(h3_features, e, m)
        f = compute_forecast(h3_features, e, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
