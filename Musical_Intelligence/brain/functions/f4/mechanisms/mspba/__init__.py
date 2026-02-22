"""MSPBA -- Musical Syntax Processing in Broca's Area.

Encoder nucleus (depth 1) in IMU, Function F4. Models how Broca's area
(IFG BA 44/45) processes musical syntax, generating the mERAN response
to harmonic violations and supporting the Shared Syntactic Integration
Resource Hypothesis (SSIRH) between music and language.

Reads: PNH.ratio_encoding (intra-unit dependency via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, roughness_total)
    sethares_dissonance:    [1]      (A, sethares beating)
    helmholtz_kang:         [2]      (A, helmholtz consonance)
    stumpf_fusion:          [3]      (A, tonal fusion)
    sensory_pleasantness:   [4]      (A, pleasantness)
    inharmonicity:          [5]      (A, harmonic deviation)
    harmonic_deviation:     [6]      (A, partial misalignment)
    loudness:               [10]     (B, onset_strength proxy)
    onset_strength:         [11]     (B, event salience)
    entropy:                [22]     (D, spectral_flux / dynamic change)
    spectral_flux:          [23]     (D, spectral change)
    x_l0l5:                 [25:33]  (F, pitch-dissonance coupling)
    x_l4l5:                 [33:41]  (F, temporal violation)
    x_l5l7:                 [41:49]  (F, harmonic structure)

Output structure: S(3) + M(3) + P(2) + F(3) = 11D
  S-layer [0:3]   Syntactic Processing (sigmoid)  scope=internal
  M-layer [3:6]   Memory              (sigmoid)  scope=internal
  P-layer [6:8]   Present             (sigmoid)  scope=hybrid
  F-layer [8:11]  Forecast            (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mspba/
"""
from __future__ import annotations

from typing import Dict, Tuple

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
    10: "400ms (chord-level)",
    14: "700ms (progression-level)",
    18: "2000ms (phrase-level)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    14: "periodicity", 18: "trend", 19: "stability",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 1: "prediction", 2: "integration"}


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
_ROUGHNESS = 0
_SETHARES_DISSONANCE = 1
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_INHARMONICITY = 5
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_ENTROPY = 22
_SPECTRAL_FLUX = 23


# -- 16 H3 Demand Specifications -----------------------------------------------
# Musical syntax processing requires chord-level (H10) instantaneous features,
# progression-level (H14) aggregates, and phrase-level (H18) trends.

_MSPBA_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === S-layer: Chord-level instantaneous features (H10 L2) ===
    _h3(_ROUGHNESS, "roughness", 10, 0, 2,
        "Current dissonance at chord level for mERAN detection",
        "Maess 2001"),
    _h3(_SETHARES_DISSONANCE, "sethares_dissonance", 10, 0, 2,
        "Current beating dissonance for Neapolitan detection",
        "Koelsch 2000"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 10, 0, 2,
        "Current tonal fusion for expectation formation",
        "Patel 2003"),
    _h3(_INHARMONICITY, "inharmonicity", 10, 0, 2,
        "Current harmonic deviation for violation detection",
        "Kim 2021"),
    _h3(_ENTROPY, "entropy", 10, 0, 2,
        "Current harmonic unpredictability for syntactic complexity",
        "Egermann 2013"),
    _h3(_LOUDNESS, "loudness", 10, 0, 2,
        "Attention gating for mERAN salience modulation",
        "Maess 2001"),
    _h3(_ONSET_STRENGTH, "onset_strength", 10, 0, 2,
        "Chord onset detection for event-locked mERAN timing",
        "Koelsch 2000"),

    # === S+M-layer: Progression-level aggregates (H14 L0) ===
    _h3(_ROUGHNESS, "roughness", 14, 1, 0,
        "Average dissonance over chord progression for context",
        "Maess 2001"),
    _h3(_INHARMONICITY, "inharmonicity", 14, 1, 0,
        "Average harmonic deviation over progression",
        "Koelsch 2000"),
    _h3(_ENTROPY, "entropy", 14, 1, 0,
        "Average complexity over progression for violation norm",
        "Egermann 2013"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 14, 1, 0,
        "Average spectral change rate for synthesis signal",
        "Wohrle 2024"),
    _h3(_SETHARES_DISSONANCE, "sethares_dissonance", 14, 8, 0,
        "Rate of dissonance change for ERAN trajectory prediction",
        "Maess 2001"),

    # === S+P-layer: Integration features (H14 L2, H10 L2) ===
    _h3(_STUMPF_FUSION, "stumpf_fusion", 14, 1, 2,
        "Fusion stability over chord progression for context depth",
        "Patel 2003"),

    # === F-layer: Phrase-level trends (H18 L0) ===
    _h3(_ROUGHNESS, "roughness", 18, 18, 0,
        "Dissonance trajectory over phrase for repair forecast",
        "Wohrle 2024"),
    _h3(_ENTROPY, "entropy", 18, 18, 0,
        "Complexity trajectory over phrase for resolution forecast",
        "Egermann 2013"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 18, 19, 0,
        "Consonance stability over phrase for resolution prediction",
        "Wohrle 2024"),
)

assert len(_MSPBA_H3_DEMANDS) == 16


class MSPBA(Encoder):
    """Musical Syntax Processing in Broca's Area -- IMU Encoder (depth 1, 11D).

    Models how Broca's area (IFG BA 44/45) processes musical harmonic syntax,
    generating the mERAN response to harmonic violations (e.g. Neapolitan
    chord substitutions) and supporting the Shared Syntactic Integration
    Resource Hypothesis (SSIRH) between music and language.

    Maess et al. 2001: mERAN localized in BA 44 and right homologue,
    ~200ms latency, position 5 = 2x amplitude vs position 3
    (MEG, N=28, p=0.005).

    Koelsch et al. 2000/2001: ERAN for Neapolitan chord violations in
    non-musicians, 150-180ms, right-anterior distribution
    (EEG, p<0.001).

    Patel 2003: Shared Syntactic Integration Resource Hypothesis --
    music and language share IFG resources for structural integration.

    Dependency chain:
        MSPBA is an Encoder (Depth 1) -- reads PNH relay output.
        Computed after PNH (Depth 0) in F4 pipeline.

    Downstream feeds:
        -> harmonic_stability beliefs (Core)
        -> prediction error: syntactic component (Appraisal)
        -> F6 Reward (resolution), F3 Attention (anticipated violation)
    """

    NAME = "MSPBA"
    FULL_NAME = "Musical Syntax Processing in Broca's Area"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("PNH",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "S", "Syntactic Processing", 0, 3,
            ("S0:musical_syntax", "S1:harmonic_prediction",
             "S2:broca_activation"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 6,
            ("M0:eran_amplitude", "M1:syntax_violation",
             "M2:from_synthesis"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 8,
            ("P0:harmonic_context", "P1:violation_state"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:resolution_fc", "F1:eran_trajectory_fc",
             "F2:syntax_repair_fc"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MSPBA_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "S0:musical_syntax", "S1:harmonic_prediction",
            "S2:broca_activation",
            "M0:eran_amplitude", "M1:syntax_violation",
            "M2:from_synthesis",
            "P0:harmonic_context", "P1:violation_state",
            "F0:resolution_fc", "F1:eran_trajectory_fc",
            "F2:syntax_repair_fc",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # L-IFG (BA 44) -- Broca's area syntactic processing
            RegionLink("S2:broca_activation", "L-IFG(BA44)", 0.85,
                       "Maess 2001"),
            # R-IFG (BA 44 homologue) -- mERAN primary generator
            RegionLink("S0:musical_syntax", "R-IFG(BA44)", 0.85,
                       "Maess 2001"),
            # L-IFG (BA 45) -- domain-general semantic integration
            RegionLink("S1:harmonic_prediction", "L-IFG(BA45)", 0.80,
                       "Patel 2003"),
            # STG -- prediction error integration
            RegionLink("P1:violation_state", "STG", 0.75,
                       "Kim 2021"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # MSPBA is a syntactic processor, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Maess et al.", 2001,
                         "mERAN localized in BA 44 and right homologue, "
                         "~200ms latency; position 5 = 2x amplitude vs "
                         "position 3 demonstrating context accumulation "
                         "effect on syntactic violation strength",
                         "MEG, N=28, p=0.005"),
                Citation("Koelsch et al.", 2000,
                         "ERAN for Neapolitan chord violations in "
                         "non-musicians; 150-180ms right-anterior "
                         "distribution confirms automatic harmonic "
                         "syntax processing without training",
                         "EEG, p<0.001"),
                Citation("Patel", 2003,
                         "Shared Syntactic Integration Resource Hypothesis: "
                         "music and language share IFG resources for "
                         "structural integration; concurrent processing "
                         "produces interference effects",
                         "review"),
                Citation("Tachibana et al.", 2024,
                         "Bilateral BA 45 activation during guitar "
                         "improvisation confirms syntactic processing "
                         "extends to production, not just perception",
                         "fNIRS, N=20"),
                Citation("Kim et al.", 2021,
                         "IFG connectivity enhanced for syntactic "
                         "irregularity; STG connectivity enhanced for "
                         "ambiguity -- double dissociation of syntactic "
                         "violation vs uncertainty processing",
                         "MEG, N=19, F=6.53, p=0.024"),
                Citation("Wohrle et al.", 2024,
                         "N1m evolves over chord progression, paralleling "
                         "mERAN position effect; resolution chord N1m "
                         "reflects preceding dominant chord dissonance",
                         "MEG, N=30, eta-p2=0.101"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "mERAN amplitude (M0) must show 2:1 ratio for position 5 "
                "vs position 3 violations (Maess 2001: MEG, N=28)",
                "Syntax violation (M1) must be higher for Neapolitan chords "
                "than diatonic chords (Koelsch 2000: EEG, p<0.001)",
                "Harmonic context (P0) must increase monotonically over "
                "chord progression within a phrase (position effect)",
                "Concurrent language syntax task must reduce S2 broca_activation "
                "for music (SSIRH interference, Patel 2003)",
                "Resolution forecast (F0) must predict tonic return after "
                "dominant chord (Wohrle 2024: N1m at resolution chord)",
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
        """Transform R3/H3 + PNH relay output into 11D syntactic processing.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"PNH": (B, T, 11)}``

        Returns:
            ``(B, T, 11)`` -- S(3) + M(3) + P(2) + F(3)
        """
        s = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(h3_features, s)
        p = compute_cognitive_present(h3_features, s, m)
        f = compute_forecast(h3_features, s, m, p)

        output = torch.stack([*s, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
