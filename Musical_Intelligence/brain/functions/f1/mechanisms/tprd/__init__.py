"""TPRD — Tonotopy-Pitch Representation Dissociation.

Relay nucleus (depth 0) in IMU, Function F1. Models the fundamental
distinction between tonotopic (frequency) encoding in primary/medial
Heschl's gyri and pitch (F0) representation in nonprimary/lateral HG.
Resolves the long-standing debate: tonotopy ≠ pitch (Briley et al. 2013).

Dependency chain:
    TPRD is a Relay (Depth 0) — reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with BCH, SDED, SDNPS, PNH, MIAA, MPG, CSG at Phase 0a.

R3 Ontology Mapping (97D freeze):
    roughness:          [0]    (A group)
    stumpf:             [3]    (A group)
    pleasantness:       [4]    (A group)
    inharmonicity:      [5]    (A group)
    harmonic_deviation: [6]    (A group)
    velocity_A:         [7]    (B group — doc says amplitude)
    velocity_D:         [8]    (B group — doc says loudness[10], corrected)
    tonalness:          [14]   (C group)
    spectral_auto:      [17]   (C group)
    entropy:            [22]   (D group)

Note: Model doc references x_l0l5[25:33] and x_l5l7[41:49] — both DISSOLVED.
Replaced x_l0l5 with energy×consonance inline coupling.
Replaced x_l5l7 with spectral_autocorrelation (existing C group feature).
Model doc [10] loudness → [8] velocity_D (97D naming).

Output structure: T(3) + M(2) + P(2) + F(3) = 10D
  T-layer [0:3]   Tonotopic   (tonotopic/pitch/dissoc)    scope=internal
  M-layer [3:5]   Mathematical (dissoc_idx/spectral_ratio) scope=internal
  P-layer [5:7]   Present     (tonotopic/pitch state)      scope=hybrid
  F-layer [7:10]  Forecast    (pitch/tono/dissoc pred)     scope=external

See Docs/C3/Models/IMU-b8-TPRD/TPRD.md (original model specification)
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
    0: "5.8ms (cochlear)",
    3: "23.2ms (brainstem)",
    6: "200ms (beat)",
    10: "400ms (chord)",
    14: "700ms (progression)",
    18: "2s (phrase)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {0: "value", 1: "mean", 8: "velocity", 14: "periodicity",
             19: "stability"}

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


# -- 18 H3 Demand Specifications -----------------------------------------------
_TPRD_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Pitch-processing chain: H0 → H3 → H6 (10 tuples) ===
    _h3(3, "stumpf_fusion", 0, 0, 2,
        "Immediate pitch fusion (cochlear)",
        "Stumpf 1890"),
    _h3(14, "tonalness", 0, 0, 2,
        "Immediate pitch salience",
        "Briley 2013"),
    _h3(3, "stumpf_fusion", 3, 1, 2,
        "Brainstem pitch fusion mean",
        "Bidelman 2013"),
    _h3(14, "tonalness", 3, 1, 2,
        "Brainstem pitch salience mean",
        "Bidelman 2013"),
    _h3(17, "spectral_autocorrelation", 3, 14, 2,
        "Harmonic periodicity at brainstem level",
        "Patterson 2002"),
    _h3(3, "stumpf_fusion", 6, 1, 0,
        "Beat-level fusion stability",
        "Stumpf 1890"),
    _h3(14, "tonalness", 6, 1, 0,
        "Beat-level pitch clarity",
        "Briley 2013"),
    _h3(17, "spectral_autocorrelation", 6, 14, 0,
        "Beat-level harmonic periodicity",
        "Patterson 2002"),
    _h3(22, "entropy", 6, 0, 0,
        "Spectral complexity at beat level",
        "Norman-Haignere 2013"),
    _h3(7, "velocity_A", 6, 8, 0,
        "Energy change rate at beat level",
        "Bellier 2023"),

    # === Mnemonic horizons: H10 → H14 → H18 (8 tuples) ===
    _h3(0, "roughness", 10, 0, 2,
        "Current tonotopic beating at chord level",
        "Plomp & Levelt 1965"),
    _h3(5, "inharmonicity", 10, 0, 2,
        "Current tonotopy-pitch conflict",
        "Basinski 2025"),
    _h3(6, "harmonic_deviation", 10, 0, 2,
        "Harmonic template mismatch at chord level",
        "Tabas 2019"),
    _h3(8, "velocity_D", 10, 0, 2,
        "Loudness attention weight at chord level",
        "Stevens 1957"),
    _h3(0, "roughness", 14, 1, 0,
        "Average tonotopic load over progression",
        "Foo 2016"),
    _h3(5, "inharmonicity", 14, 1, 0,
        "Average conflict over progression",
        "Basinski 2025"),
    _h3(22, "entropy", 14, 1, 0,
        "Average spectral complexity over progression",
        "Norman-Haignere 2013"),
    _h3(4, "sensory_pleasantness", 18, 19, 0,
        "Consonance stability over phrase",
        "Sarasso 2019"),
)

assert len(_TPRD_H3_DEMANDS) == 18


class TPRD(Relay):
    """Tonotopy-Pitch Representation Dissociation — IMU Relay (depth 0, 10D).

    Models the fundamental distinction between tonotopic (frequency)
    encoding in medial Heschl's gyrus and pitch (F0) representation
    in lateral/anterolateral HG. Primary HG is tuned to spectral content
    (cochleotopic map); non-primary HG extracts perceived pitch (F0).

    Briley, Breakey & Krumbholz (2013), Cerebral Cortex 23(11):2601-2610.

    Dependency chain:
        TPRD is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> PNH (ratio encoding in primary vs nonprimary cortex)
        -> PMIM (tonotopy-pitch dissociation → prediction error)
        -> MSPBA (shared syntactic substrate)
    """

    NAME = "TPRD"
    FULL_NAME = "Tonotopy-Pitch Representation Dissociation"
    UNIT = "IMU"
    FUNCTION = "F1"
    OUTPUT_DIM = 10

    LAYERS = (
        LayerSpec(
            "T", "Tonotopic", 0, 3,
            ("T0:tonotopic", "T1:pitch", "T2:dissociation"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Mathematical", 3, 5,
            ("M0:dissociation_idx", "M1:spectral_pitch_r"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:tonotopic_state", "P1:pitch_state"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:pitch_percept_fc", "F1:tonotopic_adpt_fc",
             "F2:dissociation_fc"),
            scope="external",
        ),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _TPRD_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "T0:tonotopic", "T1:pitch", "T2:dissociation",
            "M0:dissociation_idx", "M1:spectral_pitch_r",
            "P0:tonotopic_state", "P1:pitch_state",
            "F0:pitch_percept_fc", "F1:tonotopic_adpt_fc",
            "F2:dissociation_fc",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Medial HG (primary) — tonotopic encoding
            RegionLink("T0:tonotopic", "A1_HG", 0.85,
                       "Briley 2013"),
            RegionLink("P0:tonotopic_state", "A1_HG", 0.70,
                       "Briley 2013"),
            # Anterolateral HG (nonprimary) — pitch representation
            RegionLink("T1:pitch", "A1_HG", 0.80,
                       "Briley 2013"),
            RegionLink("P1:pitch_state", "A1_HG", 0.65,
                       "Norman-Haignere 2013"),
            # Right STG — dissonance-sensitive gradient
            RegionLink("T2:dissociation", "STG", 0.60,
                       "Foo 2016"),
        )

    @property
    def neuro_links(self) -> Tuple:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Briley", 2013,
                         "Pure-tone responses in medial HG (tonotopic); "
                         "IRN pitch-chroma in anterolateral HG (nonprimary); "
                         "pitch chroma F(1,28)=29.865, p<0.001",
                         "EEG adaptation, N=8-15"),
                Citation("Norman-Haignere", 2013,
                         "Pitch-sensitive regions respond to resolved harmonics; "
                         "located in anterior auditory cortex from low-freq primary",
                         "fMRI, N=12"),
                Citation("Fishman", 2001,
                         "Phase-locked activity in A1/HG for dissonance; "
                         "PT does NOT show significant phase-locking",
                         "intracranial, monkey+human"),
                Citation("Basinski", 2025,
                         "Inharmonicity → P3a attentional capture (p=0.010); "
                         "supports dissociation between spectral and pitch",
                         "EEG oddball, N=30"),
                Citation("Bellier", 2023,
                         "Music reconstructed from auditory cortex HFA; "
                         "R-STG dominance; anterior-posterior organization",
                         "iEEG, N=29, 2668 electrodes"),
                Citation("Tabas", 2019,
                         "POR latency consonant < dissonant (up to 36ms); "
                         "decoder+sustainer model in alHG",
                         "MEG+model, N=37"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Primary HG should show stronger tonotopy; nonprimary stronger pitch "
                "(confirmed: Briley 2013 dipole p=0.024/0.047)",
                "Pitch system should respond to missing F0; tonotopic should not "
                "(confirmed: Bendor & Wang 2005, Briley 2013 IRN)",
                "Inharmonic tones should increase dissociation "
                "(confirmed: Basinski 2025 P3a p=0.010)",
            ),
            version="1.0.0",
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 10D tonotopy-pitch dissociation.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 10)`` — T(3) + M(2) + P(2) + F(3)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
