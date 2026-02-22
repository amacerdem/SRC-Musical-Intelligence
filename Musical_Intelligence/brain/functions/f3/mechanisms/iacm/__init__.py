"""IACM — Inharmonicity-Attention Capture Model.

Relay nucleus (depth 0) in ASU, Function F3. Models how inharmonic
spectral content captures attention via automatic deviance detection:
inharmonicity breaks auditory scene regularity, triggering pre-attentive
novelty responses (P3a) and object segregation adjustments.

Dependency chain:
    IACM is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other F3 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:              [0]  -> [0]    (A, unchanged)
    periodicity:            [5]  -> [5]    (A, unchanged)
    amplitude:              [7]  -> [7]    (A, unchanged)
    spectral_flux:          [10] -> [10]   (B, was onset_strength)
    tonalness:              [14] -> [14]   (C, was brightness_kuttruff)
    spectral_flatness:      [16] -> [16]   (C, unchanged)
    spectral_change:        [21] -> [21]   (D, unchanged)
    x_l0l5:                 [25] -> [25]   (F, unchanged)

Output structure: E(3) + M(3) + P(2) + F(3) = 11D
  E-layer [0:3]   Extraction    (sigmoid)     scope=internal
  M-layer [3:6]   Memory        (sigmoid)     scope=internal
  P-layer [6:8]   Present       (sigmoid)     scope=hybrid
  F-layer [8:11]  Forecast      (sigmoid)     scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/iacm/IACM-*.md
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
    1: "50ms (high-beta)",
    3: "100ms (alpha-beta)",
    4: "125ms (theta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value",
    1: "mean",
    2: "std",
    8: "velocity",
    14: "periodicity",
    20: "entropy",
    21: "zero-crossings",
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


# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0            # roughness (A group, unchanged)
_PERIODICITY = 5          # periodicity (A group, unchanged)
_AMPLITUDE = 7            # amplitude (A group, unchanged)
_SPECTRAL_FLUX = 10       # spectral_flux (B group, was onset_strength)
_TONALNESS = 14           # tonalness (C group, was brightness_kuttruff)
_SPECTRAL_FLATNESS = 16   # spectral_flatness (C group, unchanged)
_SPECTRAL_CHANGE = 21     # spectral_change (D group, unchanged)
_X_L0L5_START = 25        # cross-band coupling (F group, unchanged)


# -- 16 H3 Demand Specifications ----------------------------------------------
# Multi-scale: H0(25ms) -> H1(50ms) -> H3(100ms) -> H4(125ms) -> H16(1000ms)

_IACM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Tonalness (5 tuples) ===
    _h3(14, "tonalness", 0, 0, 2,
        "Tonalness value 25ms — instant tonal/noisy",
        "Albouy 2017"),
    _h3(14, "tonalness", 1, 1, 2,
        "Tonalness mean 50ms — smoothed tonal state",
        "Albouy 2017"),
    _h3(14, "tonalness", 3, 0, 2,
        "Tonalness value 100ms — inharmonicity context",
        "Albouy 2017"),
    _h3(14, "tonalness", 4, 14, 2,
        "Tonalness periodicity 125ms — tonal rhythm",
        "Herrmann 2015"),
    _h3(14, "tonalness", 16, 14, 2,
        "Tonalness periodicity 1s — long tonal pattern",
        "Herrmann 2015"),

    # === Spectral Flatness (3 tuples) ===
    _h3(16, "spectral_flatness", 0, 0, 2,
        "Spectral flatness 25ms — noise proxy",
        "Albouy 2017"),
    _h3(16, "spectral_flatness", 3, 20, 2,
        "Flatness entropy 100ms — spectral unpredictability",
        "Koelsch 2019"),

    # === Roughness (2 tuples) ===
    _h3(0, "roughness", 3, 0, 2,
        "Roughness value 100ms — sensory dissonance",
        "Fishman 2001"),
    _h3(0, "roughness", 3, 20, 2,
        "Roughness entropy 100ms — dissonance variability",
        "Koelsch 2019"),

    # === Spectral Flatness long (1 tuple) ===
    _h3(16, "spectral_flatness", 16, 1, 2,
        "Flatness mean 1s — sustained noise level",
        "Albouy 2017"),

    # === Periodicity (2 tuples) ===
    _h3(5, "periodicity", 3, 0, 2,
        "Periodicity value 100ms — scene coherence",
        "Herrmann 2015"),
    _h3(5, "periodicity", 3, 2, 2,
        "Periodicity std 100ms — scene variability",
        "Herrmann 2015"),

    # === Cross-band coupling x_l0l5 (3 tuples) ===
    _h3(25, "x_l0l5", 3, 0, 2,
        "Coupling value 100ms — scene binding",
        "Zatorre 2007"),
    _h3(25, "x_l0l5", 3, 14, 2,
        "Coupling periodicity 100ms — binding rhythm",
        "Zatorre 2007"),
    _h3(25, "x_l0l5", 16, 21, 2,
        "Coupling zero-crossings 1s — phase resets",
        "Zatorre 2007"),

    # === Spectral Change (1 tuple: L0 memory) ===
    _h3(21, "spectral_change", 4, 8, 0,
        "Spectral change velocity 125ms — onset detection",
        "Koelsch 2019"),
)

assert len(_IACM_H3_DEMANDS) == 16


class IACM(Relay):
    """Inharmonicity-Attention Capture Model — ASU Relay (depth 0, 11D).

    Models how inharmonic spectral content captures attention via
    automatic deviance detection. Albouy 2017: pitch-based attention
    relies on temporal fine structure (MEG N=20, amusic vs control);
    Herrmann 2015: auditory steady-state responses index object
    segregation (EEG N=24); Zatorre 2007: spectral-temporal binding
    in auditory cortex (fMRI review).

    Dependency chain:
        IACM is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> AACM (aesthetic attention modulation)
        -> salience network beliefs (F3 Appraisal)
    """

    NAME = "IACM"
    FULL_NAME = "Inharmonicity-Attention Capture Model"
    UNIT = "ASU"
    FUNCTION = "F3"
    OUTPUT_DIM = 11

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:inharmonic_capture", "E1:object_segregation",
             "E2:precision_weighting"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 6,
            ("M0:attention_capture", "M1:approx_entropy",
             "M2:object_perception_or"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 8,
            ("P0:p3a_capture", "P1:spectral_encoding"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:object_segreg_pred", "F1:attention_shift_pred",
             "F2:multiple_objects_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _IACM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:inharmonic_capture", "E1:object_segregation",
            "E2:precision_weighting",
            "M0:attention_capture", "M1:approx_entropy",
            "M2:object_perception_or",
            "P0:p3a_capture", "P1:spectral_encoding",
            "F0:object_segreg_pred", "F1:attention_shift_pred",
            "F2:multiple_objects_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # TPJ — attention capture / reorienting
            RegionLink("E0:inharmonic_capture", "TPJ", 0.80,
                       "Herrmann 2015"),
            # IFG — object segregation / deviance detection
            RegionLink("E1:object_segregation", "IFG", 0.75,
                       "Albouy 2017"),
            # STG — spectral encoding / tonal processing
            RegionLink("P1:spectral_encoding", "STG", 0.80,
                       "Albouy 2017"),
            # AC — primary auditory cortex inharmonicity response
            RegionLink("P0:p3a_capture", "AC", 0.70,
                       "Fishman 2001"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Albouy", 2017,
                         "Pitch-based attention relies on temporal fine "
                         "structure; amusic individuals show impaired "
                         "inharmonicity detection; MEG mismatch negativity "
                         "indexes automatic pitch deviance",
                         "MEG, N=20"),
                Citation("Herrmann", 2015,
                         "Auditory steady-state responses index object "
                         "segregation; 40Hz entrainment modulated by "
                         "spectral regularity; EEG topography maps "
                         "attention capture",
                         "EEG, N=24"),
                Citation("Zatorre", 2007,
                         "Spectral-temporal binding in auditory cortex; "
                         "cross-band coupling underlies scene analysis; "
                         "hierarchical pitch processing from brainstem "
                         "to cortex",
                         "fMRI, review"),
                Citation("Koelsch", 2019,
                         "Predictive coding in auditory cortex; spectral "
                         "unpredictability drives attention capture; "
                         "entropy-based salience computation",
                         "review"),
                Citation("Fishman", 2001,
                         "Phase-locked A1 activity graded by spectral "
                         "regularity; direct cortical response to "
                         "inharmonicity",
                         "intracranial AEP/ECoG"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Inharmonic tones should elicit larger P3a than harmonic "
                "(testable: Albouy 2017 MMN paradigm)",
                "Object segregation should correlate with periodicity "
                "regularity (testable: Herrmann 2015 ASSR)",
                "Cross-band coupling should predict scene analysis "
                "accuracy (testable: Zatorre 2007 binding hypothesis)",
                "Spectral entropy should modulate attention capture "
                "magnitude (testable: Koelsch 2019 predictive coding)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 11D inharmonicity-attention representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 11)`` — E(3) + M(3) + P(2) + F(3)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
