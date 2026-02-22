"""TPRD -- Tonotopy-Pitch Representation Dissociation.

Associator nucleus (depth 2) in IMU, Function F4. Models the dual
representation system in Heschl's gyrus where medial regions encode
tonotopic (frequency-map) information while anterolateral regions
encode pitch (F0) chroma, and quantifies their dissociation.

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, tonotopic beating proxy)
    sethares_dissonance:    [1]      (A, spectral dissonance)
    stumpf_fusion:          [3]      (A, pitch fusion quality)
    sensory_pleasantness:   [4]      (A, consonance integration)
    inharmonicity:          [5]      (A, tonotopy-pitch conflict)
    harmonic_deviation:     [6]      (A, harmonic template error)
    amplitude:              [7]      (B, signal energy)
    loudness:               [10]     (B, attention weight)
    tonalness:              [14]     (C, pitch clarity / F0 salience)
    spectral_autocorrelation: [17]   (C, harmonic periodicity)
    entropy:                [22]     (D, spectral complexity)

Output structure: T(3) + M(2) + P(2) + F(3) = 10D
  T-layer [0:3]  Tonotopic     (sigmoid)  scope=internal
  M-layer [3:5]  Memory        (sigmoid)  scope=internal
  P-layer [5:7]  Present       (clamp)    scope=hybrid
  F-layer [7:10] Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/tprd/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

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
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity", 14: "periodicity",
    19: "stability",
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


# -- 18 H3 Demand Specifications -----------------------------------------------
# Fast horizons H0-H18 for brainstem-level pitch processing.
# Tonotopy-pitch dissociation tracks from cochlear (5.8ms) through
# phrase (2s) timescales.

_TPRD_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # -- T-layer (9 tuples) ---------------------------------------------------
    _h3(0, "roughness", 10, 0, 2,
        "Current tonotopic beating at chord level (400ms)",
        "Fishman 2001"),
    _h3(5, "inharmonicity", 10, 0, 2,
        "Current tonotopy-pitch conflict at chord level (400ms)",
        "Basinski 2025"),
    _h3(3, "stumpf_fusion", 0, 0, 2,
        "Immediate pitch fusion (cochlear, 5.8ms)",
        "Bidelman 2013"),
    _h3(3, "stumpf_fusion", 3, 1, 2,
        "Brainstem pitch fusion (23.2ms)",
        "Bidelman 2013"),
    _h3(14, "tonalness", 0, 0, 2,
        "Immediate pitch salience (cochlear, 5.8ms)",
        "Briley 2013"),
    _h3(14, "tonalness", 3, 1, 2,
        "Brainstem pitch salience (23.2ms)",
        "Briley 2013"),
    _h3(17, "spectral_autocorrelation", 3, 14, 2,
        "Harmonic periodicity at brainstem level (23.2ms)",
        "Norman-Haignere 2013"),
    _h3(10, "loudness", 10, 0, 2,
        "Attention weight at chord level (400ms)",
        "Fishman 2001"),
    _h3(6, "harmonic_deviation", 10, 0, 2,
        "Harmonic template mismatch at chord level (400ms)",
        "Basinski 2025"),
    # -- M-layer (6 tuples) ---------------------------------------------------
    _h3(0, "roughness", 14, 1, 0,
        "Average tonotopic load over progression (700ms)",
        "Briley 2013"),
    _h3(5, "inharmonicity", 14, 1, 0,
        "Average tonotopy-pitch conflict over progression (700ms)",
        "Basinski 2025"),
    _h3(3, "stumpf_fusion", 6, 1, 0,
        "Beat-level fusion stability (200ms)",
        "Bidelman 2013"),
    _h3(14, "tonalness", 6, 1, 0,
        "Beat-level pitch clarity (200ms)",
        "Briley 2013"),
    _h3(17, "spectral_autocorrelation", 6, 14, 0,
        "Beat-level harmonic periodicity (200ms)",
        "Norman-Haignere 2013"),
    _h3(22, "entropy", 14, 1, 0,
        "Average spectral complexity over progression (700ms)",
        "Foo 2016"),
    # -- P-layer (1 new tuple, 4 shared with T) --------------------------------
    _h3(22, "entropy", 6, 0, 0,
        "Spectral complexity at beat level (200ms)",
        "Foo 2016"),
    # -- F-layer (2 new tuples, 6 shared with M+P) ----------------------------
    _h3(4, "sensory_pleasantness", 18, 19, 0,
        "Consonance stability over phrase for dissociation forecast (2s)",
        "Cheung 2019"),
    _h3(7, "amplitude", 6, 8, 0,
        "Energy change rate at beat level (200ms)",
        "Briley 2013"),
)

assert len(_TPRD_H3_DEMANDS) == 18


class TPRD(Associator):
    """Tonotopy-Pitch Representation Dissociation -- IMU Associator (depth 2, 10D).

    Models the dual representation system within Heschl's gyrus: medial
    regions encode tonotopic (frequency-map/cochleotopic) information
    while anterolateral regions encode pitch (F0) chroma. The dissociation
    between these systems is quantified and tracked across time.

    Briley et al. (2013): Pure-tone responses on medial HG; pitch chroma
    F(1,28)=29.865, p<0.001 in anterolateral HG; dipole location
    difference L p=0.024, R p=0.047 (EEG, N=8-15).

    Norman-Haignere et al. (2013): Pitch-sensitive regions respond
    primarily to resolved harmonics in anterior auditory cortex
    (fMRI, N=12).

    Basinski et al. (2025): Inharmonic sounds generate stronger P3a
    (cluster p=0.010, 190-353ms) and object-related negativity
    (EEG, N=30).

    Dependency chain:
        (upstream relay/encoder outputs) --> TPRD (Depth 2)

    Downstream feeds:
        -> pitch representation beliefs (Appraisal)
        -> tonotopic encoding assessments
        -> dissociation monitoring
    """

    NAME = "TPRD"
    FULL_NAME = "Tonotopy-Pitch Representation Dissociation"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ()
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "T", "Tonotopic", 0, 3,
            ("T0:tonotopic_encoding", "T1:pitch_representation",
             "T2:dissociation_degree"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:dissociation_index", "M1:spectral_pitch_ratio"),
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

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _TPRD_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "T0:tonotopic_encoding", "T1:pitch_representation",
            "T2:dissociation_degree",
            "M0:dissociation_index", "M1:spectral_pitch_ratio",
            "P0:tonotopic_state", "P1:pitch_state",
            "F0:pitch_percept_fc", "F1:tonotopic_adpt_fc",
            "F2:dissociation_fc",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Heschl's Gyrus (medial) -- tonotopic encoding (primary AC)
            RegionLink("T0:tonotopic_encoding", "HG_medial", 0.90,
                       "Briley 2013"),
            # Anterolateral HG -- pitch chroma representation
            RegionLink("T1:pitch_representation", "HG_anterolateral", 0.90,
                       "Briley 2013"),
            # R-STG -- dissonant-sensitive sites anterior
            RegionLink("T2:dissociation_degree", "R_STG", 0.75,
                       "Foo 2016"),
            # Planum Temporale -- functional differentiation from HG
            RegionLink("P0:tonotopic_state", "PT", 0.70,
                       "Fishman 2001"),
            # HG medial -- tonotopic state readout
            RegionLink("P1:pitch_state", "HG_anterolateral", 0.85,
                       "Norman-Haignere 2013"),
            # Anterolateral HG -- pitch percept forecast
            RegionLink("F0:pitch_percept_fc", "HG_anterolateral", 0.80,
                       "Tabas 2019"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # TPRD is sensory-representational, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Briley et al.", 2013,
                         "Pure-tone responses on medial HG; pitch chroma "
                         "F(1,28)=29.865, p<0.001 in anterolateral HG; "
                         "dipole location difference L p=0.024, R p=0.047; "
                         "medial-lateral tonotopic-to-pitch gradient",
                         "EEG, N=8-15"),
                Citation("Norman-Haignere et al.", 2013,
                         "Pitch-sensitive regions respond primarily to "
                         "resolved harmonics in anterior auditory cortex; "
                         "pitch representation independent of resolvability",
                         "fMRI, N=12"),
                Citation("Fishman et al.", 2001,
                         "Phase-locked oscillatory activity in A1/HG "
                         "correlates with dissonance; PT shows no "
                         "phase-locking; functional differentiation",
                         "intracranial, N=3 macaque + 2 human"),
                Citation("Basinski et al.", 2025,
                         "Inharmonic sounds generate stronger P3a "
                         "(cluster p=0.010, 190-353ms) and object-related "
                         "negativity; inharmonicity drives attentional "
                         "capture through representational conflict",
                         "EEG, N=30"),
                Citation("Foo et al.", 2016,
                         "High-gamma in STG tracks roughness; "
                         "dissonant-sensitive sites anterior in R-STG",
                         "ECoG, N=8, p<0.001 FDR"),
                Citation("Tabas et al.", 2019,
                         "POR latency up to 36ms longer for dissonant "
                         "dyads; consonance processing in anterolateral HG",
                         "MEG, N=37"),
                Citation("Bidelman", 2013,
                         "Brainstem FFR encodes consonance hierarchy; "
                         "subcortical pitch salience predicts perceptual "
                         "consonance (r >= 0.81)",
                         "review"),
                Citation("Cheung et al.", 2019,
                         "Uncertainty and surprise jointly predict "
                         "auditory cortex, amygdala, hippocampus activity; "
                         "uncertainty-surprise interaction modulates "
                         "processing",
                         "fMRI, N=39"),
            ),
            evidence_tier="beta",
            confidence_range=(0.60, 0.80),
            falsification_criteria=(
                "Tonotopic encoding (T0) must localize to medial HG and "
                "pitch representation (T1) to anterolateral HG; if both "
                "activate the same region, dissociation claim is invalid "
                "(Briley 2013: dipole difference p<0.05 bilateral)",
                "Dissociation index (M0) must increase with inharmonicity; "
                "if inharmonic stimuli produce M0 near 0.5 (balanced), the "
                "conflict mechanism is not operating (Basinski 2025: P3a "
                "effect p=0.010)",
                "Pitch representation (T1) should respond to resolved "
                "harmonics more than unresolved; if T1 is equally strong "
                "for both, harmonic resolvability is irrelevant "
                "(Norman-Haignere 2013)",
                "Tonotopic state (P0) should correlate with phase-locked "
                "activity in A1/HG; if P0 is high during non-phase-locked "
                "conditions, the tonotopic readout is invalid "
                "(Fishman 2001)",
                "Pitch percept forecast (F0) should predict pitch clarity "
                "changes; if F0 accuracy does not exceed chance for "
                "consonant vs dissonant transitions, predictive claim is "
                "invalid (Tabas 2019: latency difference up to 36ms)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Transform R3/H3 into 10D tonotopy-pitch dissociation output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"name": (B, T, dim)}`` for upstream nuclei.

        Returns:
            ``(B, T, 10)`` -- T(3) + M(2) + P(2) + F(3)
        """
        t = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, t)
        p = compute_cognitive_present(h3_features, r3_features, t, m)
        f = compute_forecast(h3_features, r3_features, t, m, p)

        output = torch.stack([*t, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
