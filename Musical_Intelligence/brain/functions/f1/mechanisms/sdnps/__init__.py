"""SDNPS — Stimulus-Dependent Neural Pitch Salience.

Relay nucleus (depth 0) in SPU, Function F1. Models the critical finding
that brainstem FFR-derived Neural Pitch Salience predicts behavioral
consonance for synthetic tones but fails to generalize to natural sounds
(Cousineau et al. 2015). This is a constraint on BCH's universality claim.

Dependency chain:
    SDNPS is a Relay (Depth 0) — reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with BCH, SDED, MIAA, MPG, CSG at Phase 0a.

R3 Ontology Mapping (97D freeze):
    roughness:          [0]    (A group)
    sethares:           [1]    (A group)
    inharmonicity:      [5]    (A group)
    tonalness:          [14]   (C group)
    spectral_auto:      [17]   (C group)
    tristimulus1:       [18]   (C group)
    tristimulus2:       [19]   (C group)
    tristimulus3:       [20]   (C group)

Output structure: E(3) + M(1) + P(3) + F(3) = 10D
  E-layer [0:3]   Extraction    (sigmoid activation)       scope=internal
  M-layer [3:4]   Memory        (NPS×dependency product)   scope=internal
  P-layer [4:7]   Present       (FFR/harmonicity/roughness) scope=hybrid
  F-layer [7:10]  Forecast      (consonance/roughness pred) scope=external

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/sdnps/SDNPS-*.md
See Docs/C3/Models/SPU-g1-SDNPS/SDNPS.md (original model specification)
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
    6: "200ms (syllable)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {0: "value", 1: "mean", 14: "periodicity"}

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
_ROUGHNESS = 0
_INHARM = 5
_TONALNESS = 14
_SPECTRAL_AUTO = 17
_TRIST1 = 18
_TRIST2 = 19
_TRIST3 = 20


# -- 10 H3 Demand Specifications -----------------------------------------------
_SDNPS_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === L2 Integration / H0 Gamma (5 tuples) ===
    _h3(_ROUGHNESS, "roughness", 0, 0, 2,
        "Instant roughness at brainstem timescale (~25ms)",
        "Cousineau 2015"),
    _h3(2, "helmholtz_kang", 0, 0, 2,
        "Instant consonance — integer ratio detection",
        "Helmholtz 1863"),
    _h3(_INHARM, "inharmonicity", 0, 0, 2,
        "Instant spectral deviation from harmonic series",
        "Fletcher 1934"),
    _h3(_TONALNESS, "tonalness", 0, 0, 2,
        "Instant pitch clarity (harmonic-to-noise ratio)",
        "Bidelman 2013"),
    _h3(_TRIST1, "tristimulus1", 0, 0, 2,
        "F0 energy — spectral simplicity proxy",
        "Pollard & Jansson 1982"),

    # === L2 Integration / H3 Alpha-Beta (3 tuples) ===
    _h3(_ROUGHNESS, "roughness", 3, 1, 2,
        "Mean roughness over 100ms — correlation baseline",
        "Cousineau 2015"),
    _h3(_INHARM, "inharmonicity", 3, 1, 2,
        "Mean inharmonicity over 100ms — complexity trend",
        "Bidelman & Heinz 2011"),
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 3, 14, 2,
        "Harmonic periodicity over 100ms — FFR correlate",
        "Bidelman 2013"),

    # === L0 Memory (1 tuple) ===
    _h3(_TONALNESS, "tonalness", 3, 1, 0,
        "Tonalness mean 100ms — generalization limit predictor",
        "Penagos 2004"),

    # === L0 Memory / H6 Syllable (1 tuple) ===
    _h3(_ROUGHNESS, "roughness", 6, 14, 0,
        "Roughness periodicity 200ms — stimulus regularity",
        "Cousineau 2015"),
)

assert len(_SDNPS_H3_DEMANDS) == 10


class SDNPS(Relay):
    """Stimulus-Dependent Neural Pitch Salience — SPU Relay (depth 0, 10D).

    Models the finding that brainstem FFR-derived NPS predicts behavioral
    consonance judgments for synthetic tones (r=0.34, p<0.03) but fails
    for natural sounds (sax r=0.24 n.s., voice r=-0.10 n.s.).
    NPS ↔ roughness is stimulus-invariant (r=-0.57, p<1e-05).

    Cousineau, Bidelman, Peretz & Lehmann (2015), PLoS ONE 10(12), e0145439.

    Dependency chain:
        SDNPS is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> BCH (challenges universality: NPS validity is stimulus-dependent)
        -> PSCL (when brainstem NPS fails, cortex compensates)
        -> SDED (shared roughness interference pathway)
        -> ARU.SRP (gated consonance → pleasure)
    """

    NAME = "SDNPS"
    FULL_NAME = "Stimulus-Dependent Neural Pitch Salience"
    UNIT = "SPU"
    FUNCTION = "F1"
    OUTPUT_DIM = 10

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:nps_value", "E1:stimulus_dependency",
             "E2:roughness_corr"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 4,
            ("M0:nps_stimulus_function",),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:ffr_encoding", "P1:harmonicity_proxy",
             "P2:roughness_interference"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:behavioral_consonance_pred", "F1:roughness_response_pred",
             "F2:generalization_limit"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SDNPS_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:nps_value", "E1:stimulus_dependency",
            "E2:roughness_corr",
            "M0:nps_stimulus_function",
            "P0:ffr_encoding", "P1:harmonicity_proxy",
            "P2:roughness_interference",
            "F0:behavioral_consonance_pred", "F1:roughness_response_pred",
            "F2:generalization_limit",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Inferior Colliculus — FFR generator for NPS
            RegionLink("E0:nps_value", "IC", 0.80,
                       "Cousineau 2015"),
            RegionLink("P0:ffr_encoding", "IC", 0.75,
                       "Bidelman 2013"),
            # Anterolateral Heschl's Gyrus — cortical pitch salience
            RegionLink("P0:ffr_encoding", "A1_HG", 0.60,
                       "Penagos 2004"),
            RegionLink("F0:behavioral_consonance_pred", "A1_HG", 0.55,
                       "Tabas 2019"),
            # Right STG — dissonance-sensitive gradient
            RegionLink("P2:roughness_interference", "STG", 0.50,
                       "Foo 2016"),
        )

    @property
    def neuro_links(self) -> Tuple:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Cousineau", 2015,
                         "NPS predicts consonance for synthetic (r=0.34, p<0.03) "
                         "but NOT natural sounds (sax r=0.24 n.s., voice r=-0.10 n.s.); "
                         "NPS ↔ roughness r=-0.57 (stimulus-invariant)",
                         "FFR+behavioral, N=14 (14 intervals × 3 timbres)"),
                Citation("Penagos", 2004,
                         "Pitch salience encoded in anterolateral HG, NOT subcortical IC; "
                         "resolved > unresolved in alHG (p<.01); IC n.s.",
                         "fMRI 3T, N=6"),
                Citation("Briley", 2013,
                         "Pitch chroma representation identical for resolved/unresolved "
                         "harmonics; chroma×resolvability F(1,27)=0.026, p=.874",
                         "EEG+BESA, N=35"),
                Citation("Bidelman_Heinz", 2011,
                         "AN pitch salience best predictor of consonance hierarchy; "
                         "SNHL compresses pitch salience gradient",
                         "AN modeling"),
                Citation("Bidelman", 2013,
                         "Subcortical NPS graded for consonance; preserved in passive "
                         "listening/sleep; r~0.9 NPS ↔ consonance across studies",
                         "FFR review"),
                Citation("Fishman", 2001,
                         "Phase-locked oscillatory activity in HG for dissonance; "
                         "PT shows no phase-locking",
                         "intracranial, 3 monkeys + 2 humans"),
                Citation("Tabas", 2019,
                         "POR latency: dissonant 36ms slower than consonant; "
                         "decoder+sustainer model in alHG",
                         "MEG + model, N~15"),
                Citation("Basinski", 2025,
                         "Inharmonicity enhances P3a attentional capture; "
                         "est=-1.37, p=.0007; low pitch salience → different processing",
                         "EEG oddball, N=35"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.40, 0.70),
            falsification_criteria=(
                "NPS should NOT predict pleasantness for natural timbres "
                "(Cousineau 2015: sax r=0.24 n.s., voice r=-0.10 n.s.)",
                "NPS SHOULD predict pleasantness for synthetic tones "
                "(Cousineau 2015: r=0.34, p<0.03)",
                "NPS ↔ roughness should hold across ALL stimulus types "
                "(Cousineau 2015: r=-0.57, p<1e-05)",
                "Reducing spectral complexity should restore NPS predictive power",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 10D stimulus-dependent pitch salience.

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

        # Pre-compute tristimulus balance for P-layer reuse
        trist1 = r3_features[:, :, _TRIST1]
        trist2 = r3_features[:, :, _TRIST2]
        trist3 = r3_features[:, :, _TRIST3]
        trist_stack = torch.stack([trist1, trist2, trist3], dim=-1)
        trist_balance = 1.0 - torch.std(trist_stack, dim=-1, correction=0)

        p = compute_cognitive_present(r3_features, h3_features, e, m,
                                      trist_balance)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
