"""STAI -- Spectral-Temporal Aesthetic Integration.

Encoder nucleus (depth 1) in SPU, Function F5. Models the 2x2 factorial
interaction between spectral (consonance) and temporal (forward flow)
integrity in aesthetic judgment. Both dimensions must be intact for full
aesthetic response; disrupting either reduces response to ~35%; disrupting
both collapses to ~0%. The interaction locus is vmPFC-IFG connectivity
(Kim 2019).

Reads: R3/H3 directly -- no upstream relay dependencies (UPSTREAM_READS empty).

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, roughness_total)
    sethares_dissonance:    [1]      (A, spectral dissonance)
    helmholtz_kang:         [2]      (A, consonance measure)
    stumpf_fusion:          [3]      (A, harmonic fusion)
    sensory_pleasantness:   [4]      (A, hedonic valence)
    amplitude:              [7]      (B, velocity_A)
    loudness:               [8]      (B, velocity_D)
    onset_strength:         [11]     (B, event salience)
    warmth:                 [12]     (C, spectral warmth)
    tonalness:              [14]     (C, brightness_kuttruff)
    tristimulus1-3:         [18:21]  (C, harmonic energy distribution)
    spectral_change:        [21]     (D, spectral_flux temporal)
    energy_change:          [22]     (D, energy dynamics temporal)
    x_l4l5:                 [33:41]  (G, aesthetic binding signal)

Output structure: E(4) + M(2) + P(3) + F(3) = 12D
  E-layer [0:4]   Extraction           (sigmoid)  scope=internal
  M-layer [4:6]   Temporal Integration (sigmoid)  scope=internal
  P-layer [6:9]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer [9:12]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/stai/
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
    0: "5.8ms (micro)",
    2: "17ms (onset)",
    3: "100ms (integration)",
    5: "46ms (grouping)",
    8: "300ms (phrase)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity", 14: "periodicity",
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
_SETHARES = 1
_HELMHOLTZ = 2
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_LOUDNESS = 8
_ONSET_STRENGTH = 11
_WARMTH = 12
_TONALNESS = 14
_TRISTIMULUS1 = 18
_TRISTIMULUS2 = 19
_TRISTIMULUS3 = 20
_SPECTRAL_CHANGE = 21
_ENERGY_CHANGE = 22


# -- 14 H3 Demand Specifications -----------------------------------------------
# Spectral-temporal aesthetic integration requires very short horizons
# (H0=5.8ms to H8=300ms) capturing micro-timing and spectral integrity.

_STAI_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Spectral + Temporal Integrity (5 tuples) ===
    _h3(_ROUGHNESS, "roughness", 0, 0, 2,
        "Instantaneous dissonance at 5.8ms",
        "Kim 2019"),
    _h3(_ROUGHNESS, "roughness", 3, 1, 2,
        "Mean dissonance over 100ms integration",
        "Kim 2019"),
    _h3(_HELMHOLTZ, "helmholtz_kang", 0, 0, 2,
        "Instantaneous consonance at 5.8ms",
        "Kim 2019"),
    _h3(_HELMHOLTZ, "helmholtz_kang", 3, 1, 2,
        "Mean consonance over 100ms integration",
        "Kim 2019"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 3, 0, 2,
        "Spectral pleasantness at 100ms",
        "Blood & Zatorre 2001"),

    # === E-Layer cont + M-Layer: Temporal dynamics + interaction (4 tuples) ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 1, 0,
        "Mean spectral flux over 300ms",
        "Koelsch 2014"),
    _h3(_ENERGY_CHANGE, "energy_change", 8, 8, 0,
        "Energy change rate at 300ms",
        "Menon & Levitin 2005"),
    _h3(33, "x_l4l5[0]", 8, 0, 2,
        "Aesthetic binding signal at 300ms",
        "Kim 2019"),
    _h3(33, "x_l4l5[0]", 8, 14, 2,
        "Binding periodicity at 300ms",
        "Kim 2019"),

    # === P-Layer: Timbre + quality encoding (5 tuples) ===
    _h3(_WARMTH, "warmth", 2, 0, 2,
        "Spectral warmth at 17ms onset",
        "Koelsch 2014"),
    _h3(_TONALNESS, "tonalness", 5, 1, 0,
        "Mean tonalness at 46ms grouping",
        "Blood & Zatorre 2001"),
    _h3(_TRISTIMULUS1, "tristimulus1", 2, 0, 2,
        "Fundamental energy at 17ms",
        "Menon & Levitin 2005"),
    _h3(_TRISTIMULUS2, "tristimulus2", 2, 0, 2,
        "Mid-harmonic energy at 17ms",
        "Menon & Levitin 2005"),
    _h3(_TRISTIMULUS3, "tristimulus3", 2, 0, 2,
        "High-harmonic energy at 17ms",
        "Menon & Levitin 2005"),
)

assert len(_STAI_H3_DEMANDS) == 14


class STAI(Encoder):
    """Spectral-Temporal Aesthetic Integration -- SPU Encoder (depth 1, 12D).

    Models the 2x2 factorial interaction between spectral integrity
    (consonance quality) and temporal integrity (forward flow) in aesthetic
    judgment. Both dimensions must be intact for full aesthetic response --
    disrupting either reduces neural response to ~35% of maximum; disrupting
    both collapses response to ~0%.

    Kim et al. 2019: 2x2 factorial fMRI design (N=20) -- spectral integrity
    x temporal integrity interaction at vmPFC-IFG connectivity (T=6.852,
    FWE p<.05). Rostral ACC mediates spectral-temporal interaction.

    Blood & Zatorre 2001: PET N=10 -- intensely pleasurable music activates
    vmPFC, NAcc, VTA; pleasure correlates with consonance quality and
    temporal structure.

    Koelsch 2014: Review -- aesthetic processing engages vmPFC/OFC for value
    computation, STG/Heschl's for spectral quality, reward circuit for
    temporal expectation resolution.

    Menon & Levitin 2005: fMRI N=13 -- NAcc, VTA, hypothalamus activated
    by music; functional connectivity between mesolimbic structures
    correlates with pleasantness ratings.

    Dependency chain:
        STAI is an Encoder (Depth 1) -- reads R3/H3 directly.
        No upstream relay dependencies.

    Downstream feeds:
        -> aesthetic_judgment beliefs (Appraisal)
        -> spectral/temporal quality context for F5 integrators
    """

    NAME = "STAI"
    FULL_NAME = "Spectral-Temporal Aesthetic Integration"
    UNIT = "SPU"
    FUNCTION = "F5"
    OUTPUT_DIM = 12
    UPSTREAM_READS = ()  # STAI reads R3/H3 directly, no upstream dependencies

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:spectral_integrity", "E1:temporal_integrity",
             "E2:aesthetic_integration", "E3:vmpfc_ifg_connectivity"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 4, 6,
            ("M0:aesthetic_value", "M1:spectral_temporal_interaction"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 9,
            ("P0:spectral_quality", "P1:temporal_quality",
             "P2:aesthetic_response"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 12,
            ("F0:aesthetic_rating_pred", "F1:reward_response_pred",
             "F2:connectivity_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _STAI_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:spectral_integrity", "E1:temporal_integrity",
            "E2:aesthetic_integration", "E3:vmpfc_ifg_connectivity",
            "M0:aesthetic_value", "M1:spectral_temporal_interaction",
            "P0:spectral_quality", "P1:temporal_quality",
            "P2:aesthetic_response",
            "F0:aesthetic_rating_pred", "F1:reward_response_pred",
            "F2:connectivity_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # vmPFC / IFG -- aesthetic integration hub
            RegionLink("E2:aesthetic_integration", "vmPFC", 0.85,
                       "Kim 2019"),
            RegionLink("E3:vmpfc_ifg_connectivity", "IFG", 0.85,
                       "Kim 2019"),
            # Rostral ACC -- spectral-temporal interaction
            RegionLink("M1:spectral_temporal_interaction", "rACC", 0.80,
                       "Kim 2019"),
            # NAcc / Caudate / Putamen -- reward circuit for temporal integrity
            RegionLink("P2:aesthetic_response", "NAcc", 0.80,
                       "Blood & Zatorre 2001"),
            RegionLink("M0:aesthetic_value", "caudate", 0.75,
                       "Menon & Levitin 2005"),
            # STG / Heschl's Gyrus -- spectral quality encoding
            RegionLink("P0:spectral_quality", "STG", 0.80,
                       "Koelsch 2014"),
            RegionLink("E0:spectral_integrity", "Heschls", 0.75,
                       "Koelsch 2014"),
            # Thalamus -- integration relay
            RegionLink("E1:temporal_integrity", "thalamus", 0.70,
                       "Menon & Levitin 2005"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # STAI aesthetic integration; no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Kim et al.", 2019,
                         "2x2 factorial fMRI: spectral integrity x temporal "
                         "integrity interaction at vmPFC-IFG connectivity "
                         "(T=6.852, FWE p<.05). Disrupting either dimension "
                         "reduces aesthetic response to ~35%",
                         "fMRI, N=20"),
                Citation("Blood & Zatorre", 2001,
                         "PET: intensely pleasurable music activates vmPFC, "
                         "NAcc, VTA; pleasure correlates with consonance "
                         "quality and temporal structure",
                         "PET, N=10"),
                Citation("Koelsch", 2014,
                         "Aesthetic processing: vmPFC/OFC for value, "
                         "STG/Heschl's for spectral quality, reward circuit "
                         "for temporal expectation resolution",
                         "review"),
                Citation("Menon & Levitin", 2005,
                         "NAcc, VTA, hypothalamus activated by music; "
                         "functional connectivity between mesolimbic "
                         "structures correlates with pleasantness ratings",
                         "fMRI, N=13"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Spectral integrity (E0) must be higher for consonant vs "
                "dissonant stimuli (Kim 2019: 2x2 factorial, spectral main "
                "effect)",
                "Temporal integrity (E1) must reflect forward flow quality "
                "(Kim 2019: temporal main effect on aesthetic response)",
                "Aesthetic integration (E2) must show supra-additive "
                "interaction (Kim 2019: interaction T=6.852, neither "
                "dimension alone produces full response)",
                "Disrupting spectral integrity alone should reduce aesthetic "
                "response to ~35% (Kim 2019: spectral disruption condition)",
                "Disrupting temporal integrity alone should reduce aesthetic "
                "response to ~35% (Kim 2019: temporal disruption condition)",
                "vmPFC-IFG connectivity (E3) should correlate with aesthetic "
                "integration (Kim 2019: connectivity as interaction locus)",
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
        """Transform R3/H3 into 12D spectral-temporal aesthetic integration.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{}`` -- STAI has no upstream reads.

        Returns:
            ``(B, T, 12)`` -- E(4) + M(2) + P(3) + F(3)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
