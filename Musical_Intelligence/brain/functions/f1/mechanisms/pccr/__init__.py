"""PCCR — Pitch Chroma Cortical Representation.

Associator nucleus (depth 2) in SPU, Function F1. Transforms upstream
BCH relay (16D) and PSCL encoder (16D) outputs alongside R³ chroma features
and H³ temporal morphologies into an 11D octave-invariant chroma representation.

Dependency chain (strict):
    BCH (Depth 0, Relay)  ──→  PSCL (Depth 1, Encoder)  ──→  PCCR (Depth 2, Associator)
    │                           │                              │
    │ E1:harmonicity ──────────>│                    ──────────>│ (0.25 in P1)
    │ E2:hierarchy   ──────────>│                    ──────────>│ (0.20 in P2)
    │                           │ P0:pitch_prominence ────────>│ (0.15/0.25 in P0/P2)
    │                           │ P2:periodicity_clarity ─────>│ (0.10 in P0)
    └───────────────────────────┘                              │
                                                               ▼
                                                         11D chroma output

Without BCH: No harmonicity or hierarchy → P1/P2 degraded
Without PSCL: No pitch prominence gate → P0/P2 degraded
Without both: PCCR falls back to R³-only E-layer (still functional but weak)

Output structure: E(4) + M(1) + P(3) + F(3) = 11D
  E-layer [0:4]   Extraction    (instantaneous R³)     scope=internal
  M-layer [4:5]   Memory        (H³ temporal)           scope=internal
  P-layer [5:8]   Present       (cognitive integration) scope=hybrid
  F-layer [8:11]  Forecast      (trend extrapolation)   scope=external

See Building/C³-Brain/F1-Sensory-Processing/mechanisms/pccr/PCCR-*.md
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

# ── Horizon labels ────────────────────────────────────────────────────
_H_LABELS = {
    3: "23ms (onset)",
    6: "200ms (beat)",
    12: "525ms (phrase)",
}

# ── Morph labels ──────────────────────────────────────────────────────
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity", 14: "periodicity", 18: "trend",
}

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
_INHARM = 5          # inharmonicity
_TONAL = 14          # tonalness
_AUTOCORR = 17       # spectral_autocorrelation
_PITCH_H = 37        # pitch_height
_PCE = 38            # pitch_class_entropy
_PITCHSAL = 39       # pitch_salience


# ── 14 H³ Demand Specifications ──────────────────────────────────────
# Ordered: L2 (integration, 5) → L0 (memory, 5) → L1 (prediction, 4)

_PCCR_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === L2 Integration (5 tuples) ===
    _h3(_PCE, "pitch_class_entropy", 3, 0, 2,
        "PCE value at 23ms (instant chroma concentration)", "Krumhansl 1990"),
    _h3(_PCE, "pitch_class_entropy", 6, 0, 2,
        "PCE value at 200ms (sustained chroma)", "Krumhansl 1990"),
    _h3(_PITCH_H, "pitch_height", 3, 0, 2,
        "Pitch height value at 23ms (register context)", "Pressnitzer 2001"),
    _h3(_PITCH_H, "pitch_height", 6, 0, 2,
        "Pitch height value at 200ms (register sustained)", "Pressnitzer 2001"),
    _h3(_TONAL, "tonalness", 6, 0, 2,
        "Tonalness value at 200ms (tonal quality sustained)", "Patterson 2002"),

    # === L0 Memory (5 tuples) ===
    _h3(_PCE, "pitch_class_entropy", 6, 18, 0,
        "PCE trend 200ms (chroma stability direction)", "Krumhansl 1990"),
    _h3(_PCE, "pitch_class_entropy", 12, 1, 0,
        "PCE mean 525ms (chroma clarity memory)", "Krumhansl 1990"),
    _h3(_PITCH_H, "pitch_height", 6, 8, 0,
        "Pitch height velocity 200ms (register movement rate)", "Pressnitzer 2001"),
    _h3(_TONAL, "tonalness", 12, 14, 0,
        "Tonalness periodicity 525ms (tonal cycling pattern)", "Patterson 2002"),
    _h3(_PITCHSAL, "pitch_salience", 12, 1, 0,
        "Pitch salience mean 525ms (pitch persistence)", "Bidelman 2009"),

    # === L1 Prediction (4 tuples) ===
    _h3(_PCE, "pitch_class_entropy", 6, 1, 1,
        "Expected PCE 200ms ahead (chroma clarity forecast)", "Krumhansl 1990"),
    _h3(_PITCH_H, "pitch_height", 6, 1, 1,
        "Expected pitch height 200ms ahead (register prediction)", "Pressnitzer 2001"),
    _h3(_TONAL, "tonalness", 6, 1, 1,
        "Expected tonalness 200ms ahead (tonal quality prediction)", "Patterson 2002"),
    _h3(_PITCHSAL, "pitch_salience", 6, 1, 1,
        "Expected pitch salience 200ms ahead (pitch presence forecast)", "Bidelman 2009"),
)

assert len(_PCCR_H3_DEMANDS) == 14


class PCCR(Associator):
    """Pitch Chroma Cortical Representation — SPU Associator (depth 2, 11D).

    Transforms upstream BCH + PSCL outputs alongside R³ chroma features
    into an octave-invariant pitch-class representation.

    Dependency chain:
        BCH (Depth 0) → PSCL (Depth 1) → PCCR (Depth 2)

    Upstream reads:
        BCH:  E1:harmonicity [1], E2:hierarchy [2]
        PSCL: P0:pitch_prominence_sig [8], P2:periodicity_clarity [10]

    Cross-unit feeds (downstream, external):
        → IMU (chroma → melodic memory)
        → STU (chroma → temporal structure)
    """

    NAME = "PCCR"
    FULL_NAME = "Pitch Chroma Cortical Representation"
    UNIT = "SPU"
    FUNCTION = "F1"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("BCH", "PSCL")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:chroma_energy", "E1:chroma_clarity",
             "E2:octave_coherence", "E3:pitch_class_confidence"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 5,
            ("M0:chroma_stability",),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 8,
            ("P0:chroma_identity_signal", "P1:octave_equivalence_index",
             "P2:chroma_salience"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:chroma_continuation_signal",
             "F1:chroma_transition_likelihood",
             "F2:chroma_resolution_direction"),
            scope="external",
        ),
    )

    # ── Abstract property implementations ─────────────────────────────

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PCCR_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:chroma_energy", "E1:chroma_clarity",
            "E2:octave_coherence", "E3:pitch_class_confidence",
            "M0:chroma_stability",
            "P0:chroma_identity_signal", "P1:octave_equivalence_index",
            "P2:chroma_salience",
            "F0:chroma_continuation_signal",
            "F1:chroma_transition_likelihood",
            "F2:chroma_resolution_direction",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Anterolateral HG — chroma encoding center
            RegionLink("P0:chroma_identity_signal", "A1_HG", 0.80,
                       "Patterson 2002"),
            RegionLink("P1:octave_equivalence_index", "A1_HG", 0.70,
                       "Briley 2013"),
            RegionLink("P2:chroma_salience", "A1_HG", 0.50,
                       "Penagos 2004"),
            # Superior Temporal Gyrus — octave-invariant pitch
            RegionLink("P0:chroma_identity_signal", "STG", 0.55,
                       "Warren 2003"),
            RegionLink("P2:chroma_salience", "STG", 0.60,
                       "Patterson 2002"),
            # Superior Temporal Sulcus — pitch class processing
            RegionLink("P1:octave_equivalence_index", "STS", 0.50,
                       "Griffiths 2010"),
            RegionLink("F0:chroma_continuation_signal", "STG", 0.35,
                       "Warren 2003"),
            # Inferior Frontal Gyrus — pitch categorization
            RegionLink("F2:chroma_resolution_direction", "IFG", 0.30,
                       "Zatorre 2002"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Chroma identity → weak NE modulation (pitch-class attention)
            NeuroLink("P0:chroma_identity_signal", 1, "amplify", 0.15,
                      "Weinberger 2004"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Shepard", 1964,
                         "Circularity of pitch: octave equivalence",
                         "foundational"),
                Citation("Deutsch", 1973,
                         "Octave generalization in memory",
                         "behavioral"),
                Citation("Warren", 2003,
                         "Octave-invariant pitch representation in auditory cortex",
                         "fMRI, N=12"),
                Citation("Patterson", 2002,
                         "alHG pitch center in fMRI",
                         "cluster peak at [-48,-16,8]"),
                Citation("Briley", 2013,
                         "IRN sources 7mm lateral/anterior to pure-tone",
                         "fMRI"),
                Citation("Penagos", 2004,
                         "Pitch salience tracks alHG activation",
                         "r=0.92"),
                Citation("Krumhansl", 1990,
                         "Pitch class profiles and tonal hierarchies",
                         "r=0.97"),
                Citation("Pressnitzer", 2001,
                         "Pitch salience varies with register",
                         "psychophysics"),
                Citation("Terhardt", 1974,
                         "Virtual pitch from harmonics: spectral pitch",
                         "foundational"),
                Citation("Weinberger", 2004,
                         "Cortical plasticity for pitch-class selectivity",
                         "animal model"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.75, 0.90),
            falsification_criteria=(
                "Chroma identification accuracy should decrease for inharmonic "
                "timbres (bells vs violin) by >20%; failure = model invalid",
                "Octave-invariant representations should replicate "
                "Warren et al. 2003 octave generalization in auditory cortex",
            ),
            version="1.0.0",
        )

    # ── Compute ───────────────────────────────────────────────────────

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Transform R³/H³ + BCH/PSCL upstream into 11D chroma representation.

        Delegates to 4 layer functions (extraction → temporal_integration
        → cognitive_present → forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"BCH": (B, T, 16), "PSCL": (B, T, 16)}``

        Returns:
            ``(B, T, 11)`` — E(4) + M(1) + P(3) + F(3)
        """
        e = compute_extraction(r3_features)
        m = compute_temporal_integration(r3_features, h3_features)
        p = compute_cognitive_present(
            r3_features, h3_features, e, m, upstream_outputs,
        )
        f = compute_forecast(r3_features, h3_features, p, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
