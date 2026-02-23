"""HMCE -- Hierarchical Musical Context Encoding.

Relay nucleus (depth 0) in STU, Function F7. Models how musical context
is encoded at multiple hierarchical timescales -- from local pitch/onset
events to medium-range phrase structure to long-range tonal/formal
organization. The auditory cortex builds hierarchical representations
through forward temporal integration from A1 to STG to MTG.

Dependency chain:
    HMCE is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with PEOM, MSR, GSSM at Phase 0a of the kernel scheduler.

R3 Ontology Mapping (v1 -> 97D freeze):
    amplitude:            [7]   (B group, velocity_A)
    spectral_flux:        [10]  (B group, onset_strength proxy)
    onset_strength:       [11]  (B group, event salience)
    spectral_autocorr:    [17]  (C group)
    spectral_change:      [21]  (D group)
    x_l5l7:               [51]  (H group, contextual coupling)
    x_l0l2l5:             [60]  (J group, hierarchical integration)

Output structure: E(3) + M(3) + P(3) + F(2) = 11D
  E-layer [0:3]   Extraction    (sigmoid activation)       scope=internal
  M-layer [3:6]   Memory        (temporal dynamics)         scope=internal
  P-layer [6:9]   Present       (encoding state)            scope=hybrid
  F-layer [9:11]  Forecast      (structure predictions)     scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hmce/
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
    3: "100ms (alpha-beta)",
    8: "250ms (theta)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 13: "kurtosis",
    14: "periodicity", 18: "trend",
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


# -- R3 feature indices (post-freeze 97D) -------------------------------------
_AMPLITUDE = 7         # amplitude / velocity_A (B group)
_ONSET_STRENGTH = 11   # onset_strength (B group)
_SPECTRAL_AUTO = 17    # spectral_autocorrelation (C group)
_SPECTRAL_CHANGE = 21  # spectral_change (D group)
_X_L5L7 = 51          # x_l5l7 (H group, contextual coupling)
_X_L0L2L5 = 60        # x_l0l2l5 (J group, hierarchical integration)


# -- 17 H3 Demand Specifications -----------------------------------------------
# E-layer: 8 tuples, M-layer: 5 tuples, P-layer: 4 tuples

_HMCE_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Short/Medium/Long Context Encoding (8 tuples) ===
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 3, 14, 0,
        "Spectral periodicity 100ms -- local pitch regularity",
        "Koelsch 2009"),
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 3, 2, 0,
        "Spectral std 100ms -- local pitch variability",
        "Koelsch 2009"),
    _h3(_ONSET_STRENGTH, "onset_strength", 8, 14, 0,
        "Onset periodicity 250ms -- rhythmic regularity at theta",
        "Koelsch 2009"),
    _h3(_AMPLITUDE, "amplitude", 3, 2, 0,
        "Amplitude std 100ms -- dynamic variability at onset scale",
        "Pearce 2018"),
    _h3(_X_L0L2L5, "x_l0l2l5", 8, 1, 0,
        "Hierarchical mean 250ms -- medium-range context integration",
        "Pearce 2018"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 18, 0,
        "Spectral change trend 1s -- long-range spectral trajectory",
        "Pearce 2018"),
    _h3(_X_L0L2L5, "x_l0l2l5", 16, 1, 0,
        "Hierarchical mean 1s -- long-range structure integration",
        "Koelsch 2009"),
    _h3(_X_L5L7, "x_l5l7", 16, 13, 0,
        "Contextual coupling kurtosis 1s -- structural surprise detection",
        "Koelsch 2009"),

    # === M-Layer: Context Depth + Structure Regularity (5 tuples) ===
    _h3(_X_L0L2L5, "x_l0l2l5", 8, 18, 0,
        "Hierarchical trend 250ms -- context depth direction",
        "Pearce 2018"),
    _h3(_X_L0L2L5, "x_l0l2l5", 16, 18, 0,
        "Hierarchical trend 1s -- long-range structure direction",
        "Pearce 2018"),
    _h3(_X_L5L7, "x_l5l7", 8, 1, 0,
        "Contextual coupling mean 250ms -- coupling strength",
        "Koelsch 2009"),
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 16, 1, 0,
        "Spectral autocorrelation mean 1s -- tonal regularity",
        "Tillmann 2003"),
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 14, 0,
        "Onset periodicity 1s -- structural regularity at beat scale",
        "Tillmann 2003"),

    # === P-Layer: Encoding State (4 tuples) ===
    _h3(_AMPLITUDE, "amplitude", 3, 0, 0,
        "Amplitude value 100ms -- instantaneous dynamic level",
        "Koelsch 2009"),
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 0,
        "Onset value 100ms -- current event salience",
        "Koelsch 2009"),
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 8, 14, 0,
        "Spectral periodicity 250ms -- tonal regularity at theta",
        "Tillmann 2003"),
    _h3(_X_L0L2L5, "x_l0l2l5", 3, 0, 0,
        "Hierarchical value 100ms -- instantaneous context state",
        "Pearce 2018"),
)

assert len(_HMCE_H3_DEMANDS) == 17


class HMCE(Relay):
    """Hierarchical Musical Context Encoding -- STU Relay (depth 0, 11D).

    Models how musical context is built hierarchically from local events
    (100ms) through phrase-level structures (250ms) to formal organization
    (1s). Koelsch (2009) showed hierarchical processing in auditory cortex
    for syntactic structure. Pearce (2018) demonstrated that statistical
    learning builds context at multiple timescales. Tillmann et al. (2003)
    showed implicit tonal structure encoding in STG.

    Dependency chain:
        HMCE is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> AMSS, ETAM (F3 cross-function via STU)
        -> context_depth belief (Core, F7)
        -> structure_regularity belief (Appraisal, F7)
    """

    NAME = "HMCE"
    FULL_NAME = "Hierarchical Musical Context Encoding"
    UNIT = "STU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("f01:short_context", "f02:medium_context",
             "f03:long_context"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 6,
            ("M0:context_depth", "M1:structure_regularity",
             "M2:transition_dynamics"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 9,
            ("P0:a1_stg_encoding", "P1:context_predict",
             "P2:phrase_expect"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:phrase_boundary_pred", "F1:structure_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _HMCE_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:short_context", "f02:medium_context",
            "f03:long_context",
            "M0:context_depth", "M1:structure_regularity",
            "M2:transition_dynamics",
            "P0:a1_stg_encoding", "P1:context_predict",
            "P2:phrase_expect",
            "F0:phrase_boundary_pred", "F1:structure_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # A1 / Heschl's Gyrus -- local event encoding
            RegionLink("f01:short_context", "A1_HG", 0.80,
                       "Koelsch 2009"),
            # Superior Temporal Gyrus -- phrase-level context
            RegionLink("P0:a1_stg_encoding", "STG", 0.75,
                       "Koelsch 2009"),
            # Middle Temporal Gyrus -- long-range structure
            RegionLink("f03:long_context", "MTG", 0.60,
                       "Pearce 2018"),
            # Hippocampus -- context memory for structural expectation
            RegionLink("M0:context_depth", "hippocampus", 0.50,
                       "Tillmann 2003"),
            # ACC -- structural surprise detection
            RegionLink("M2:transition_dynamics", "ACC", 0.55,
                       "Koelsch 2009"),
        )

    @property
    def neuro_links(self) -> Tuple:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Koelsch", 2009,
                         "Hierarchical processing in auditory cortex for "
                         "musical syntactic structure; A1-STG-MTG cascade "
                         "builds context from local to global",
                         "fMRI + EEG, review"),
                Citation("Pearce", 2018,
                         "Statistical learning builds musical context at "
                         "multiple timescales; IDyOM model predicts "
                         "information content across temporal hierarchies",
                         "computational modeling + behavioral"),
                Citation("Tillmann", 2003,
                         "Implicit tonal structure encoding in STG; "
                         "harmonic priming even in non-musicians reflects "
                         "automatic context building",
                         "fMRI, N=20"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.85),
            falsification_criteria=(
                "Short context (f01) must respond to local pitch/onset "
                "changes within 100ms window; if insensitive to note-level "
                "events, local encoding is invalid",
                "Context depth (M0) must increase monotonically with "
                "phrase length for tonal music (Pearce 2018: information "
                "content decreases with more context)",
                "Structure regularity (M1) must differentiate tonal from "
                "atonal sequences (Tillmann 2003: priming effect)",
                "Phrase boundary prediction (F0) should correlate with "
                "ERP phrase-boundary responses (CPS component)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 11D hierarchical context encoding.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(3) + F(2)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
