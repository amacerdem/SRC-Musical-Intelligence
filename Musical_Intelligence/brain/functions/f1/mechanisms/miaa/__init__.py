"""MIAA — Musical Imagery Auditory Activation.

Relay nucleus (depth 0) in SPU, Function F1. Models auditory cortex
activation during musical imagery — when a listener imagines music
without physical sound. Familiarity enhances activation in BA22,
while instrumental (vs lyrics) content modulates A1 recruitment.

Dependency chain:
    MIAA is a Relay (Depth 0) — reads R³/H³ directly, no upstream dependencies.
    Runs in parallel with BCH, MPG at Phase 0a of the kernel scheduler.

R³ Ontology Mapping (v1 → 97D freeze):
    loudness:           [8]  → [10]   (shifted within B)
    spectral_flatness:  [15] → [15]   "clarity" (inverted concept — use directly)
    spectral_change:    [21] → [21]   renamed "spectral_flux"
    x_l5l7:             [41:49] → DISSOLVED → spectral_autocorrelation [17]
    inharmonicity:      [5]  → [5]    (unchanged)
    tonalness:          [14] → [14]   (unchanged)
    warmth:             [12] → [12]   (unchanged)
    tristimulus1-3:     [18:21] → [18:21] (unchanged)

Output structure: E(3) + M(2) + P(3) + F(3) = 11D
  E-layer [0:3]   Extraction    (sigmoid activation)       scope=internal
  M-layer [3:5]   Memory        (composite dynamics)        scope=internal
  P-layer [5:8]   Present       (relay outputs)             scope=hybrid
  F-layer [8:11]  Forecast      (imagery predictions)       scope=external

See Building/C³-Brain/F1-Sensory-Processing/mechanisms/miaa/MIAA-*.md
See Docs/C³/Models/SPU-β3-MIAA/MIAA.md (original model specification)
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

# ── Horizon labels ────────────────────────────────────────────────────
_H_LABELS = {
    2: "17ms (gamma)",
    5: "46ms (alpha-beta)",
    8: "300ms (syllable)",
}

# ── Morph labels ──────────────────────────────────────────────────────
_M_LABELS = {0: "value", 1: "mean", 13: "entropy"}

# ── Law labels ────────────────────────────────────────────────────────
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


# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
_INHARM = 5           # inharmonicity (A group, unchanged)
_LOUDNESS = 10        # loudness (B group, shifted from old [8])
_WARMTH = 12          # warmth (C group, unchanged)
_TONALNESS = 14       # tonalness (C group, unchanged)
_CLARITY = 15         # clarity (C group, was "spectral_flatness" inverted)
_SPECTRAL_AUTO = 17   # spectral_autocorrelation (C group, replaces dissolved x_l5l7)
_TRIST1 = 18          # tristimulus1 (C group, unchanged)
_TRIST2 = 19          # tristimulus2 (C group, unchanged)
_TRIST3 = 20          # tristimulus3 (C group, unchanged)
_SPECTRAL_FLUX = 21   # spectral_flux (D group, was "spectral_change")


# ── 11 H³ Demand Specifications ──────────────────────────────────────
# Ordered: L2 (integration, 5) → L0 (memory, 6)

_MIAA_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === L2 Integration (5 tuples) ===
    _h3(_TONALNESS, "tonalness", 2, 0, 2,
        "Tonal clarity at gamma rate — imagery template quality",
        "Kraemer 2005"),
    _h3(_TRIST1, "tristimulus1", 2, 0, 2,
        "Fundamental energy at gamma rate — harmonic template anchor",
        "Pollard & Jansson 1982"),
    _h3(_TRIST2, "tristimulus2", 2, 0, 2,
        "Mid-harmonic energy at gamma rate — timbre body",
        "Pollard & Jansson 1982"),
    _h3(_TRIST3, "tristimulus3", 2, 0, 2,
        "High-harmonic energy at gamma rate — timbre brightness",
        "Pollard & Jansson 1982"),
    _h3(_INHARM, "inharmonicity", 5, 0, 2,
        "Instrument type detection at alpha-beta rate",
        "McDermott 2010"),

    # === L0 Memory (6 tuples) ===
    _h3(_TONALNESS, "tonalness", 5, 1, 0,
        "Sustained tonal clarity over alpha-beta window",
        "Di Liberto 2021"),
    _h3(_WARMTH, "warmth", 5, 1, 0,
        "Timbre quality for imagery template at alpha-beta",
        "Halpern 2004"),
    _h3(_CLARITY, "clarity", 8, 1, 0,
        "Tonal vs noise over syllable window — imagery vividness",
        "Kraemer 2005"),
    _h3(_LOUDNESS, "loudness", 8, 1, 0,
        "Intensity context for imagery at syllable rate",
        "Kraemer 2005"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 8, 13, 0,
        "Spectral change entropy — vividness proxy over 300ms",
        "Di Liberto 2021"),
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 8, 1, 0,
        "Timbre-structure binding for imagery coherence",
        "Halpern 2004"),
)

assert len(_MIAA_H3_DEMANDS) == 11


class MIAA(Relay):
    """Musical Imagery Auditory Activation — SPU Relay (depth 0, 11D).

    Models auditory cortex activation during musical imagery.
    Kraemer 2005: AC active in silence — region×music-type interaction
    F(1,14)=48.92, p<.0001 (fMRI, n=15). Familiarity enhances BA22
    activation (p<.0001). Instrumental > lyrics in A1 (p<.0005).

    Dependency chain:
        MIAA is a Relay (Depth 0) — reads R³/H³ directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        → MEAMN (imagery activation for memory binding)
        → TPIO (timbre perception-imagery overlap)
        → timbral_character belief (Core, τ=0.5)
        → imagery_recognition belief (Anticipation)
    """

    NAME = "MIAA"
    FULL_NAME = "Musical Imagery Auditory Activation"
    UNIT = "SPU"
    FUNCTION = "F1"
    OUTPUT_DIM = 11

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:imagery_activation", "E1:familiarity_enhancement",
             "E2:a1_modulation"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:activation_function", "M1:familiarity_effect"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 8,
            ("P0:melody_retrieval", "P1:continuation_prediction",
             "P2:phrase_structure"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:melody_continuation_pred", "F1:ac_activation_pred",
             "F2:recognition_pred"),
            scope="external",
        ),
    )

    # ── Abstract property implementations ─────────────────────────────

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MIAA_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:imagery_activation", "E1:familiarity_enhancement",
            "E2:a1_modulation",
            "M0:activation_function", "M1:familiarity_effect",
            "P0:melody_retrieval", "P1:continuation_prediction",
            "P2:phrase_structure",
            "F0:melody_continuation_pred", "F1:ac_activation_pred",
            "F2:recognition_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # BA22 / posterior STG — imagery activation hub
            RegionLink("E0:imagery_activation", "STG", 0.80,
                       "Kraemer 2005"),
            RegionLink("E1:familiarity_enhancement", "STG", 0.75,
                       "Kraemer 2005"),
            RegionLink("P0:melody_retrieval", "STG", 0.65,
                       "Halpern 2004"),
            # Primary auditory cortex — A1 modulation
            RegionLink("E2:a1_modulation", "A1_HG", 0.70,
                       "Kraemer 2005"),
            RegionLink("P0:melody_retrieval", "A1_HG", 0.50,
                       "Halpern 2004"),
            # Recognition → STG substrate
            RegionLink("F2:recognition_pred", "STG", 0.40,
                       "Di Liberto 2021"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Familiarity-enhanced imagery → weak dopamine anticipation
            NeuroLink("E1:familiarity_enhancement", 0, "produce", 0.10,
                      "Kraemer 2005"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Kraemer", 2005,
                         "AC active during musical imagery in silence; "
                         "region×music-type F(1,14)=48.92; familiar>unfamiliar "
                         "p<.0001; instrumental>lyrics in A1 p<.0005",
                         "fMRI, n=15"),
                Citation("Halpern", 2004,
                         "Perception-imagery overlap in posterior PT; "
                         "behavioral r=0.84; SMA without subvocalization",
                         "fMRI, n=10 musicians"),
                Citation("Di Liberto", 2021,
                         "Imagery pitch encoding comparable to perception "
                         "(p=0.19 n.s.); sub-1Hz critical F(1,20)=369.8",
                         "EEG, n=21 musicians"),
                Citation("Zatorre", 2005,
                         "Secondary/belt AC reliable for imagery; "
                         "top-down frontal→auditory reactivation",
                         "review"),
                Citation("Bellier", 2023,
                         "Music reconstructed from STG; 68% significant "
                         "electrodes in bilateral STG",
                         "iEEG, n=29, 2668 electrodes"),
                Citation("Bellmann", 2024,
                         "4 timbre processing clusters: bilateral pSTG/HG/SMG "
                         "+ R anterior insula",
                         "ALE meta-analysis, k=18, N=338"),
                Citation("Pantev", 2001,
                         "Timbre-specific cortical enhancement in musicians",
                         "MEG, n=17, F(1,15)=28.55"),
                Citation("Alluri", 2012,
                         "Timbral features map to bilateral STG during "
                         "naturalistic music",
                         "fMRI, n=11, Z=8.13"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Unfamiliar music should produce weaker imagery activation "
                "than familiar music (Kraemer 2005 confirmed, p<.0001)",
                "Broadband noise should NOT produce imagery activation "
                "(low tonalness → low E0)",
                "Lyrics-only imagery should show weaker A1 activation "
                "than instrumental imagery (Kraemer 2005 confirmed, p<.0005)",
            ),
            version="1.0.0",
        )

    # ── Compute ───────────────────────────────────────────────────────

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R³/H³ into 11D imagery representation.

        Delegates to 4 layer functions (extraction → temporal_integration
        → cognitive_present → forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 11)`` — E(3) + M(2) + P(3) + F(3)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(r3_features, h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
