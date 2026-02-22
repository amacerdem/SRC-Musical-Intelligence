"""PNH — Pythagorean Neural Hierarchy.

Relay nucleus (depth 0) in IMU, Function F4. Models how the auditory system
encodes frequency ratios according to the Pythagorean hierarchy, from brainstem
FFR responses through cortical conflict monitoring to aesthetic preference
judgments. Simple integer ratios (octave 2:1, fifth 3:2) produce low-complexity
encodings; complex ratios (tritone 45:32) produce high-complexity encodings
with stronger conflict signals.

Dependency chain:
    PNH is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:                  [0]  -> [0]    (A, roughness_total)
    sethares_dissonance:        [1]  -> [1]    (A, sethares_dissonance)
    inharmonicity:              [5]  -> [5]    (A, inharmonicity)
    harmonic_deviation:         [6]  -> [6]    (A, harmonic_deviation)
    tonalness:                  [14] -> [14]   (C, brightness_kuttruff)
    spectral_autocorrelation:   [17] -> [17]   (C, spectral_autocorrelation)
    x_l0l5:                     [25:33] -> [25:33] (F, coupling)

Output structure: H(3) + M(2) + P(3) + F(3) = 11D
  H-layer [0:3]   Harmonic Encoding  (sigmoid)   scope=internal
  M-layer [3:5]   Temporal Integ.    (sigmoid)   scope=internal
  P-layer [5:8]   Cognitive Present  (sigmoid)   scope=hybrid
  F-layer [8:11]  Forecast           (sigmoid)   scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pnh/
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
    10: "400ms (chord)",
    14: "700ms (progression)",
    18: "2000ms (phrase)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 14: "periodicity",
    18: "trend", 19: "stability",
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
        law_name=_L_LABELS.get(law, f"L{law}"),
        purpose=purpose,
        citation=citation,
    )


# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0               # roughness_total (A group)
_SETHARES = 1                # sethares_dissonance (A group)
_STUMPF_FUSION = 3           # stumpf_fusion (A group)
_SENSORY_PLEASANT = 4        # sensory_pleasantness (A group)
_INHARMONICITY = 5           # inharmonicity (A group)
_HARMONIC_DEV = 6            # harmonic_deviation (A group)
_LOUDNESS = 10               # onset_strength (B group)
_TONALNESS = 14              # brightness_kuttruff (C group)
_SPEC_AUTOCORR = 17          # spectral_autocorrelation (C group)


# -- 15 H3 Demand Specifications -----------------------------------------------
# Organized by layer: H(6) + M(5) + P(3) + F(1) = 15

_PNH_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === H-Layer: Harmonic Encoding (6 tuples) ===
    _h3(_ROUGHNESS, "roughness", 10, 0, 2,
        "Current dissonance at chord level (400ms)",
        "Bidelman 2009"),
    _h3(_ROUGHNESS, "roughness", 14, 1, 0,
        "Average dissonance over progression (700ms)",
        "Bidelman 2009"),
    _h3(_INHARMONICITY, "inharmonicity", 10, 0, 2,
        "Current ratio complexity (400ms)",
        "Bidelman 2009"),
    _h3(_INHARMONICITY, "inharmonicity", 14, 1, 0,
        "Average complexity over progression (700ms)",
        "Bidelman 2009"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 10, 0, 2,
        "Current tonal fusion (400ms)",
        "Crespo-Bojorque 2018"),
    _h3(_LOUDNESS, "loudness", 10, 0, 2,
        "Attention weight (400ms)",
        "Kim 2021"),

    # === M-Layer: Temporal Integration (5 tuples) ===
    _h3(_ROUGHNESS, "roughness", 18, 18, 0,
        "Dissonance trajectory over phrase (2s)",
        "Plomp 1965"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 14, 1, 2,
        "Fusion stability over progression (700ms)",
        "Bidelman 2009"),
    _h3(_SENSORY_PLEASANT, "sensory_pleasantness", 10, 0, 2,
        "Current consonance (400ms)",
        "Sarasso 2019"),
    _h3(_TONALNESS, "tonalness", 14, 2, 0,
        "Purity variation over progression (700ms)",
        "Sarasso 2019"),
    _h3(_HARMONIC_DEV, "harmonic_deviation", 14, 0, 0,
        "Template mismatch over progression (700ms)",
        "Plomp 1965"),

    # === P-Layer: Cognitive Present (3 tuples) ===
    _h3(_SENSORY_PLEASANT, "sensory_pleasantness", 18, 19, 0,
        "Consonance stability over phrase (2s)",
        "Tabas 2019"),
    _h3(_TONALNESS, "tonalness", 10, 0, 2,
        "Ratio purity at chord level (400ms)",
        "Tabas 2019"),
    _h3(_SPEC_AUTOCORR, "spectral_autocorrelation", 10, 14, 2,
        "Harmonic regularity at chord level (400ms)",
        "Kim 2021"),

    # === F-Layer: Forecast (1 tuple) ===
    _h3(_TONALNESS, "tonalness", 14, 18, 0,
        "Purity trajectory over progression (700ms)",
        "Harrison 2020"),
)

assert len(_PNH_H3_DEMANDS) == 15


class PNH(Relay):
    """Pythagorean Neural Hierarchy — IMU Relay (depth 0, 11D).

    Models how the auditory system encodes frequency ratios according to the
    Pythagorean hierarchy. Bidelman & Krishnan 2009: brainstem FFR responses
    follow Pythagorean hierarchy; NPS ordering matches music theory (r >= 0.81).
    Sarasso et al. 2019: consonance drives aesthetic judgment (eta_p^2=0.685).
    Kim et al. 2021: R-IFG to L-IFG connectivity for syntactic irregularity
    (MEG, N=19, p=0.024 FDR).

    Dependency chain:
        PNH is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> F6 Reward (dissonance resolution PE)
        -> F5 Emotion (preference judgment)
        -> F8 Learning (expertise modulation forecast)
        -> MEAMN relay wrapper in scheduler
    """

    NAME = "PNH"
    FULL_NAME = "Pythagorean Neural Hierarchy"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 11

    LAYERS = (
        LayerSpec(
            "H", "Harmonic Encoding", 0, 3,
            ("H0:ratio_complexity", "H1:conflict_monitoring",
             "H2:expertise_modulation"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 5,
            ("M0:ratio_complexity_norm", "M1:neural_activation"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 5, 8,
            ("P0:ratio_encoding", "P1:conflict_monitoring",
             "P2:consonance_preference"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:dissonance_resolution_fc", "F1:preference_judgment_fc",
             "F2:expertise_modulation_fc"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PNH_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "H0:ratio_complexity", "H1:conflict_monitoring",
            "H2:expertise_modulation",
            "M0:ratio_complexity_norm", "M1:neural_activation",
            "P0:ratio_encoding", "P1:conflict_monitoring",
            "P2:consonance_preference",
            "F0:dissonance_resolution_fc", "F1:preference_judgment_fc",
            "F2:expertise_modulation_fc",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # L-IFG — conflict monitoring (syntactic processing)
            RegionLink("P1:conflict_monitoring", "L_IFG", 0.85,
                       "Kim 2021"),
            # R-IFG — conflict monitoring (non-musician baseline)
            RegionLink("H1:conflict_monitoring", "R_IFG", 0.80,
                       "Kim 2021"),
            # L-STG — ratio encoding (harmonic hierarchy)
            RegionLink("P0:ratio_encoding", "L_STG", 0.80,
                       "Bidelman 2009"),
            # R-STG — ratio encoding
            RegionLink("H0:ratio_complexity", "R_STG", 0.75,
                       "Bidelman 2009"),
            # alHG — consonant dyad POR
            RegionLink("P2:consonance_preference", "alHG", 0.85,
                       "Tabas 2019"),
            # L-MFG — expertise modulation (musician-specific)
            RegionLink("H2:expertise_modulation", "L_MFG", 0.70,
                       "Crespo-Bojorque 2018"),
            # L-IPL — expertise modulation (musician-specific)
            RegionLink("F2:expertise_modulation_fc", "L_IPL", 0.65,
                       "Schon 2005"),
            # ACC — conflict monitoring / prediction error
            RegionLink("F0:dissonance_resolution_fc", "ACC", 0.70,
                       "Kim 2021"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bidelman", 2009,
                         "Brainstem FFR responses follow Pythagorean hierarchy; "
                         "NPS correlation r >= 0.81",
                         "brainstem FFR, N=10"),
                Citation("Crespo-Bojorque", 2018,
                         "Consonance-context MMN in all; dissonance-context MMN "
                         "only in musicians",
                         "EEG oddball, N=32"),
                Citation("Kim", 2021,
                         "R-IFG to L-IFG connectivity for syntactic irregularity",
                         "MEG connectivity, N=19, p=0.024 FDR"),
                Citation("Tabas", 2019,
                         "Consonant dyads produce earlier and larger POR in alHG",
                         "MEG+model, N=37, p<0.0001"),
                Citation("Sarasso", 2019,
                         "Consonance drives aesthetic judgment (eta_p^2=0.685) and "
                         "N1 modulation (eta_p^2=0.225)",
                         "EEG+behavioral, N=22"),
                Citation("Harrison", 2020,
                         "3-factor consonance model: interference + harmonicity "
                         "+ cultural familiarity",
                         "Computational model, N=500+ reanalysis"),
                Citation("Schon", 2005,
                         "Musicians N1-P2 (100-200ms) vs non-musicians N2 "
                         "(200-300ms) for consonance processing",
                         "ERP, N=20"),
                Citation("Plomp", 1965,
                         "Critical bandwidth theory: roughness proportional to "
                         "ratio complexity",
                         "Psychoacoustic"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.92),
            falsification_criteria=(
                "Brainstem FFR should follow Pythagorean hierarchy ordering "
                "(confirmed: Bidelman 2009, r >= 0.81)",
                "Consonant dyads should produce earlier POR in alHG "
                "(confirmed: Tabas 2019, p<0.0001)",
                "Dissonance-context MMN should appear only in musicians "
                "(confirmed: Crespo-Bojorque 2018, EEG oddball N=32)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 11D Pythagorean hierarchy representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 11)`` — H(3) + M(2) + P(3) + F(3)
        """
        h = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, h)
        p = compute_cognitive_present(h3_features, r3_features, h, m)
        f = compute_forecast(h3_features, h, m, p)

        output = torch.stack([*h, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
