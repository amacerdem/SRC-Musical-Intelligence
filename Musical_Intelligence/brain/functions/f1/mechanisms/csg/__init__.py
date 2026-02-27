"""CSG — Consonance-Salience Gradient.

Relay nucleus (depth 0) in ASU, Function F1. Models how dissonance
level systematically modulates salience network activation: strong
dissonance activates ACC/AI (d=5.16), intermediate dissonance
increases Heschl's gyrus load (d=1.9), consonance enables efficient
processing with positive valence (d=3.31).

Dependency chain:
    CSG is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with BCH, MIAA, MPG, SDED at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:              [0]  -> [0]    (A, unchanged)
    sethares:               [1]  -> [1]    (A, unchanged)
    sensory_pleasantness:   [4]  -> [4]    (A, unchanged)
    loudness:               [8]  -> [10]   (B, shifted)
    spectral_centroid:      [9]  -> [9]    (B, unchanged)
    warmth:                 [12] -> [12]   (C, unchanged)
    spectral_flux:          [21] -> [21]   (D, was spectral_change)
    energy_change:          [22] -> [22]   (D, unchanged)
    spectral_auto:          [17] -> [17]   (C, replaces dissolved x_l0l5[25])

Output structure: E(3) + M(3) + P(3) + F(3) = 12D
  E-layer [0:3]   Extraction    (sigmoid+tanh)    scope=internal
  M-layer [3:6]   Memory        (sigmoid)          scope=internal
  P-layer [6:9]   Present       (sigmoid+tanh)     scope=hybrid
  F-layer [9:12]  Forecast      (sigmoid+tanh)     scope=external

NOTE: Valence dimensions use tanh [-1, 1]:
  E2:consonance_valence, P1:affective_evaluation, F0:valence_pred

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/csg/CSG-*.md
See Docs/C3/Models/ASU-a3-CSG/CSG.md (original model specification)
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
_M_LABELS = {0: "value", 1: "mean", 2: "std", 8: "velocity", 13: "entropy"}

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
_ROUGHNESS = 0            # roughness (A group, unchanged)
_SETHARES = 1             # sethares_dissonance (A group, unchanged)
_PLEAS = 4                # sensory_pleasantness (A group, unchanged)
_CENTROID = 9             # spectral_centroid (B group, unchanged)
_LOUDNESS = 10            # loudness (B group, shifted from old [8])
_WARMTH = 12              # warmth (C group, unchanged)
_SPECTRAL_AUTO = 17       # spectral_autocorrelation (C, replaces dissolved x_l0l5)
_SPECTRAL_FLUX = 21       # spectral_flux (D, was spectral_change)
_ENERGY_CHANGE = 22       # energy_change (D group, unchanged)


# -- 17 H3 Demand Specifications ----------------------------------------------
# Multi-scale: H0(25ms) -> H3(100ms) -> H4(125ms) -> H8(500ms) -> H16(1000ms)

_CSG_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Roughness (4 tuples: H0 value, H3 mean+std, H16 mean) ===
    _h3(_ROUGHNESS, "roughness", 0, 0, 2,
        "Instant roughness at brainstem timescale",
        "Fishman 2001"),
    _h3(_ROUGHNESS, "roughness", 3, 1, 2,
        "Mean roughness over 100ms — dissonance context",
        "Bravo 2017"),
    _h3(_ROUGHNESS, "roughness", 3, 2, 2,
        "Roughness variability over 100ms — sensory evidence",
        "Bravo 2017"),
    _h3(_ROUGHNESS, "roughness", 16, 1, 2,
        "Long-range roughness context over 1s",
        "Bravo 2017"),

    # === Sensory Pleasantness (3 tuples: H3 value+velocity, H16 mean) ===
    _h3(_PLEAS, "sensory_pleasantness", 3, 0, 2,
        "Consonance proxy at 100ms",
        "Bravo 2017"),
    _h3(_PLEAS, "sensory_pleasantness", 3, 8, 2,
        "Pleasantness velocity — valence change rate",
        "Bravo 2017"),
    _h3(_PLEAS, "sensory_pleasantness", 16, 1, 2,
        "Sustained pleasantness over 1s — aesthetic basis",
        "Sarasso 2019"),

    # === Loudness (3 tuples: H3 value+entropy, H16 mean) ===
    _h3(_LOUDNESS, "loudness", 3, 0, 2,
        "Loudness at 100ms — intensity for salience",
        "Bravo 2017"),
    _h3(_LOUDNESS, "loudness", 3, 13, 2,
        "Loudness entropy over 100ms — salience unpredictability",
        "Cheung 2019"),
    _h3(_LOUDNESS, "loudness", 16, 1, 2,
        "Mean loudness over 1s — sustained intensity",
        "Bravo 2017"),

    # === Sethares (2 tuples: H3 value, H8 velocity) ===
    _h3(_SETHARES, "sethares_dissonance", 3, 0, 2,
        "Psychoacoustic dissonance at 100ms",
        "Plomp & Levelt 1965"),
    _h3(_SETHARES, "sethares_dissonance", 8, 8, 0,
        "Dissonance velocity over 500ms — salience dynamics",
        "Bravo 2017"),

    # === Spectral Flux (1 tuple: H4 velocity) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 4, 8, 0,
        "Spectral change velocity at 125ms — processing demand",
        "Bravo 2017"),

    # === Spectral Autocorrelation (2 tuples: replaces dissolved x_l0l5) ===
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 3, 0, 2,
        "Cross-band salience coupling at 100ms (replaces x_l0l5)",
        "Koelsch"),
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 8, 0, 2,
        "Cross-band coupling at 500ms — medium-term integration",
        "Kim"),

    # === Energy Change (1 tuple: H3 velocity) ===
    _h3(_ENERGY_CHANGE, "energy_change", 3, 8, 0,
        "Energy change velocity at 100ms — arousal dynamics",
        "Bravo 2017"),

    # === Spectral Centroid (1 tuple: H3 value) ===
    _h3(_CENTROID, "spectral_centroid", 3, 0, 2,
        "Brightness at 100ms — timbral salience for RT",
        "Bravo 2017"),
)

assert len(_CSG_H3_DEMANDS) == 17


class CSG(Relay):
    """Consonance-Salience Gradient — ASU Relay (depth 0, 12D).

    Models how consonance level systematically modulates salience
    network activation. Bravo 2017: strong dissonance activates
    ACC/bilateral AI (d=5.16, fMRI N=12); intermediate dissonance
    increases Heschl's gyrus processing (d=1.9); consonance enables
    efficient processing. Sarasso 2019: consonant > dissonant
    aesthetic appreciation (d=2.008, EEG N=22).

    Dependency chain:
        CSG is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> AACM (aesthetic attention modulation)
        -> IACM (salience network complement)
        -> ARU.affect (valence information)
        -> consonance_salience_gradient belief (Appraisal)
    """

    NAME = "CSG"
    FULL_NAME = "Consonance-Salience Gradient"
    UNIT = "ASU"
    FUNCTION = "F1"
    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:salience_activation", "E1:sensory_evidence",
             "E2:consonance_valence"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 6,
            ("M0:salience_response", "M1:rt_valence_judgment",
             "M2:aesthetic_appreciation"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 9,
            ("P0:salience_network", "P1:affective_evaluation",
             "P2:sensory_load"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 12,
            ("F0:valence_pred", "F1:processing_pred",
             "F2:aesthetic_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _CSG_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:salience_activation", "E1:sensory_evidence",
            "E2:consonance_valence",
            "M0:salience_response", "M1:rt_valence_judgment",
            "M2:aesthetic_appreciation",
            "P0:salience_network", "P1:affective_evaluation",
            "P2:sensory_load",
            "F0:valence_pred", "F1:processing_pred",
            "F2:aesthetic_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # ACC — salience hub for dissonance
            RegionLink("E0:salience_activation", "ACC", 0.85,
                       "Bravo 2017"),
            # Anterior insula — salience network partner
            RegionLink("E0:salience_activation", "AI", 0.75,
                       "Bravo 2017"),
            # Heschl's gyrus — sensory evidence weighting
            RegionLink("E1:sensory_evidence", "A1_HG", 0.80,
                       "Bravo 2017"),
            RegionLink("P2:sensory_load", "A1_HG", 0.60,
                       "Bravo 2017"),
            # STG — consonance discrimination
            RegionLink("P0:salience_network", "STG", 0.65,
                       "Foo 2016"),
            # Amygdala — dissonance-driven salience
            RegionLink("P0:salience_network", "AMY", 0.60,
                       "Koelsch"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Consonance -> weak dopamine via NAc pathway
            NeuroLink("M2:aesthetic_appreciation", 0, "produce", 0.15,
                      "Koelsch"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bravo", 2017,
                         "Intermediate dissonance -> R.Heschl's (d=1.9); "
                         "strong dissonance -> ACC/bilateral AI (d=5.16); "
                         "linear consonance-valence trend (d=3.31); "
                         "RT intermediate=6792ms > consonant=4333ms",
                         "fMRI, N=45 behavioral + N=12 imaging"),
                Citation("Sarasso", 2019,
                         "Consonant > dissonant aesthetic appreciation "
                         "(d=2.008, p<0.001); N1/P2 enhanced for consonant "
                         "intervals (80-194ms)",
                         "EEG ERP, N=22"),
                Citation("Koelsch", 2006,
                         "Dissonant -> amygdala/hippocampus; consonant -> "
                         "anterior insula/Heschl's/ventral striatum; "
                         "full salience gradient circuit",
                         "fMRI, N=11"),
                Citation("Kim", 2017,
                         "Dissonance -> decreased STG/insula BOLD; "
                         "vmPFC/NAc interaction for spectral-temporal "
                         "reward integration",
                         "fMRI"),
                Citation("Cheung", 2019,
                         "Amygdala/hippocampus reflect uncertainty x "
                         "surprise; NAc reflects uncertainty; harmonic "
                         "expectancy salience integration",
                         "fMRI, N=79"),
                Citation("Fishman", 2001,
                         "Phase-locked A1 activity graded by consonance-"
                         "dissonance; direct cortical graded response",
                         "intracranial AEP/ECoG"),
                Citation("Foo", 2016,
                         "Right STG high-gamma (70-150Hz) for dissonance; "
                         "75-200ms; differential consonance processing",
                         "ECoG, N=8"),
                Citation("Wöhrle", 2024,
                         "N1m graded by consonance/dissonance within "
                         "chord progressions; MEG graded salience",
                         "MEG, N=30"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Parametric consonance should produce graded salience "
                "response (confirmed: Bravo 2017)",
                "Intermediate dissonance should produce longest RT "
                "(confirmed: RT_intermediate=6792ms > RT_consonant=4333ms)",
                "Consonance-valence should be monotonic "
                "(confirmed: d=3.31, p<0.01)",
                "ACC lesions should reduce dissonance salience (testable)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 12D consonance-salience representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        NOTE: Output is clamped to [-1, 1] instead of [0, 1] because
        valence dimensions (E2, P1, F0) use tanh activation.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 12)`` — E(3) + M(3) + P(3) + F(3)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(r3_features, h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(r3_features, h3_features, e, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(-1.0, 1.0)
