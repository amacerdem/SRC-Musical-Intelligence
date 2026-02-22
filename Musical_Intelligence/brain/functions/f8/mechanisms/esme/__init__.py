"""ESME -- Error-Signal Modulated Encoding.

Associator nucleus (depth 2) in SPU, Function F8. Models expertise-specific
enhancement of mismatch negativity (MMN) responses. Musical training
selectively enhances pre-attentive deviance detection in a domain-specific
gradient pattern: pitch for singers/violinists, rhythm for drummers/jazz
musicians, timbre for instrumentalists.

Core finding: MMN amplitude is enhanced in a domain-specific manner by
musical training, following a gradient pattern rather than a clean
dissociation (Tervaniemi 2022; Vuust et al. 2012). The ALE meta-analysis
(Criscuolo et al. 2022, k=84, N=3005) confirms bilateral STG + L IFG
activation in musicians, while Martins et al. 2022 constrains against
clean 3-way dissociation.

Reads: EDNR (F8 SPU), TSCP (F8 SPU), CDMR (F8 SPU)
EDNR, TSCP, and CDMR are all F8 SPU mechanisms at lower depths.

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, dissonance baseline)
    helmholtz_kang:         [2]      (A, consonance reference)
    onset_strength:         [11]     (B, temporal alignment)
    warmth:                 [12]     (C, timbral blending)
    tonalness:              [14]     (C, pitch clarity)
    tristimulus1:           [18]     (C, F0 energy)
    tristimulus2:           [19]     (C, mid harmonics)
    tristimulus3:           [20]     (C, high harmonics)
    spectral_flux:          [21]     (D, spectral deviance)
    pitch_change:           [23]     (D, pitch flux)
    timbre_change:          [24]     (D, timbre change)
    x_l4l5:                 [33:41]  (H, temporal-spectral coupling)

Output structure: E(4) + M(1) + P(3) + F(3) = 11D
  E-layer  [0:4]   Extraction           (sigmoid)  scope=internal
  M-layer  [4:5]   Temporal Integration (sqrt)     scope=internal
  P-layer  [5:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer  [8:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/esme/
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

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    0: "25ms (ultra-gamma)",
    2: "17ms (gamma)",
    3: "100ms (alpha)",
    5: "46ms (high-gamma)",
    8: "300ms (delta)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
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


# -- R3 feature indices (post-freeze 97D) ------------------------------------
_HELMHOLTZ = 2
_ONSET_STRENGTH = 11
_WARMTH = 12
_TONALNESS = 14
_TRISTIMULUS1 = 18
_TRISTIMULUS2 = 19
_TRISTIMULUS3 = 20
_SPECTRAL_FLUX = 21
_PITCH_CHANGE = 23
_TIMBRE_CHANGE = 24
_X_L4L5_START = 33

# -- Upstream dimension defaults -----------------------------------------------
_EDNR_DIM = 10
_TSCP_DIM = 10
_CDMR_DIM = 11


# -- 12 H3 Demand Specifications -----------------------------------------------
# ESME spans H0 (25ms) through H8 (300ms), using L0 (forward) and L2
# (bidirectional) laws. E-layer: 10 tuples, P-layer: 2 tuples, total: 12.

_ESME_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Expertise-Specific MMN Extraction (10 tuples) ===
    # f01: Pitch MMN
    _h3(_HELMHOLTZ, "helmholtz_kang", 0, 0, 2,
        "Consonance deviance baseline 25ms L2",
        "Koelsch et al. 1999"),
    _h3(_HELMHOLTZ, "helmholtz_kang", 3, 1, 2,
        "Consonance template 100ms L2",
        "Koelsch et al. 1999"),
    _h3(_PITCH_CHANGE, "pitch_change", 3, 8, 0,
        "Pitch deviant detection velocity 100ms L0",
        "Koelsch et al. 1999"),

    # f02: Rhythm MMN
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 0,
        "Onset strength for rhythm deviance 100ms L0",
        "Vuust et al. 2012"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 8, 0,
        "Spectral deviance velocity 100ms L0",
        "Vuust et al. 2012"),
    _h3(_X_L4L5_START, "x_l4l5", 8, 0, 2,
        "Temporal-spectral coupling 300ms L2",
        "Liao et al. 2024"),

    # f03: Timbre MMN
    _h3(_TRISTIMULUS1, "tristimulus1", 2, 0, 2,
        "Tristimulus1 F0 energy instantaneous 17ms L2",
        "Tervaniemi 2022"),
    _h3(_TRISTIMULUS2, "tristimulus2", 2, 0, 2,
        "Tristimulus2 mid harmonics instantaneous 17ms L2",
        "Tervaniemi 2022"),
    _h3(_TRISTIMULUS3, "tristimulus3", 2, 0, 2,
        "Tristimulus3 high harmonics instantaneous 17ms L2",
        "Tervaniemi 2022"),
    _h3(_TIMBRE_CHANGE, "timbre_change", 8, 2, 0,
        "Timbre change magnitude 300ms L0",
        "Tervaniemi 2022"),

    # === P-Layer: Deviance Detection Context (2 tuples) ===
    _h3(_WARMTH, "warmth", 2, 0, 2,
        "Warmth instantaneous 17ms L2 for timbre context",
        "Tervaniemi 2022"),
    _h3(_TONALNESS, "tonalness", 5, 1, 0,
        "Tonalness template 46ms L0 for pitch clarity",
        "Wagner et al. 2018"),
)

assert len(_ESME_H3_DEMANDS) == 12

# Verify uniqueness of H3 tuples
_ESME_TUPLES = [d.as_tuple() for d in _ESME_H3_DEMANDS]
assert len(_ESME_TUPLES) == len(set(_ESME_TUPLES)), (
    f"Duplicate H3 tuples: {len(_ESME_TUPLES)} vs {len(set(_ESME_TUPLES))}"
)


class ESME(Associator):
    """Error-Signal Modulated Encoding -- SPU Associator (depth 2, 11D).

    Models expertise-specific enhancement of mismatch negativity (MMN)
    responses. Musical training selectively enhances pre-attentive
    deviance detection in a domain-specific gradient: pitch for
    singers/violinists, rhythm for drummers/jazz musicians, timbre for
    instrumentalists.

    Koelsch et al. (1999): Violinists show MMN to 0.75% pitch deviants
    in major chord triads; MMN absent in non-musicians. EEG, N=20.

    Vuust et al. (2012): Genre-specific gradient
    jazz > rock > pop > non-musicians for complex rhythmic deviants.
    EEG, N=40.

    Tervaniemi (2022): "Sound parameters most important in performance
    evoke the largest MMN." Review, multiple studies.

    Criscuolo et al. (2022): ALE meta-analysis (k=84, N=3005): bilateral
    STG + L IFG (BA44) activation in musicians vs non-musicians.

    Dependency chain:
        ESME reads EDNR, TSCP, CDMR (F8 SPU depth 0-1). Computed
        after all three in scheduler.

    Downstream feeds:
        -> expertise_mmn belief (Appraisal)
        -> F3 Attention via deviance detection signals
    """

    NAME = "ESME"
    FULL_NAME = "Error-Signal Modulated Encoding"
    UNIT = "SPU"
    FUNCTION = "F8"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("EDNR", "TSCP", "CDMR")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:pitch_mmn", "f02:rhythm_mmn",
             "f03:timbre_mmn", "f04:expertise_enhancement"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 4, 5,
            ("M0:mmn_expertise_function",),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 5, 8,
            ("P0:pitch_deviance_detection",
             "P1:rhythm_deviance_detection",
             "P2:timbre_deviance_detection"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:feature_enhancement_pred",
             "F1:expertise_transfer_pred",
             "F2:developmental_trajectory"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _ESME_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:pitch_mmn", "f02:rhythm_mmn",
            "f03:timbre_mmn", "f04:expertise_enhancement",
            "M0:mmn_expertise_function",
            "P0:pitch_deviance_detection",
            "P1:rhythm_deviance_detection",
            "P2:timbre_deviance_detection",
            "F0:feature_enhancement_pred",
            "F1:expertise_transfer_pred",
            "F2:developmental_trajectory",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Bilateral STG -- primary locus of MMN enhancement
            RegionLink("f01:pitch_mmn", "bilateral_STG", 0.85,
                       "Koelsch et al. 1999"),
            # Bilateral STG -- rhythm MMN
            RegionLink("f02:rhythm_mmn", "bilateral_STG", 0.80,
                       "Vuust et al. 2012"),
            # Bilateral STG -- timbre MMN
            RegionLink("f03:timbre_mmn", "bilateral_STG", 0.80,
                       "Tervaniemi 2022"),
            # L IFG (BA44) -- expertise-dependent activation
            RegionLink("f04:expertise_enhancement", "L_IFG", 0.75,
                       "Criscuolo et al. 2022"),
            # Heschl's Gyrus -- structural plasticity trajectory
            RegionLink("F2:developmental_trajectory", "HG", 0.80,
                       "Bucher et al. 2023"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Glutamate -- excitatory MMN generation
            NeuroLink("M0:mmn_expertise_function", "glutamate", 0.70,
                      "Yu et al. 2015"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Koelsch et al.", 1999,
                         "Violinists show MMN to 0.75% pitch deviants in "
                         "major chord triads; MMN absent in non-musicians",
                         "EEG, N=20"),
                Citation("Vuust et al.", 2012,
                         "Genre-specific gradient jazz > rock > pop > "
                         "non-musicians for complex rhythmic deviants",
                         "EEG, N=40"),
                Citation("Tervaniemi", 2022,
                         "Sound parameters most important in performance "
                         "evoke the largest MMN — domain-specific gradient "
                         "principle",
                         "Review"),
                Citation("Criscuolo et al.", 2022,
                         "ALE meta-analysis (k=84, N=3005): bilateral STG "
                         "+ L IFG (BA44) activation in musicians. General "
                         "enhancement across domains",
                         "ALE meta-analysis, k=84, N=3005"),
                Citation("Martins et al.", 2022,
                         "No singer vs instrumentalist P2/P3 difference — "
                         "clean 3-way dissociation is an oversimplification; "
                         "the actual pattern is a gradient",
                         "EEG, N=60"),
                Citation("Yu et al.", 2015,
                         "MMN as comprehensive indicator of perception of "
                         "regularities — unified expertise metric",
                         "Review"),
                Citation("Wagner et al.", 2018,
                         "Pre-attentive harmonic interval MMN = -0.34 uV "
                         "at 173ms (p = 0.003)",
                         "EEG"),
                Citation("Bucher et al.", 2023,
                         "Heschl's Gyrus 130% larger in professional "
                         "musicians; OFC co-activation 25-40ms faster",
                         "Structural MRI"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.55, 0.75),
            falsification_criteria=(
                "Pitch MMN (f01) must show larger amplitude for trained "
                "pitch processors (singers, violinists) than for drummers "
                "or non-musicians (Koelsch 1999: 0.75% detection threshold)",
                "Rhythm MMN (f02) must show genre-specific gradient "
                "jazz > rock > pop > non-musicians (Vuust 2012)",
                "Timbre MMN (f03) must be largest for the trained "
                "instrument timbre (Tervaniemi 2022: domain-specific)",
                "Expertise enhancement (f04) must show gradient, NOT clean "
                "3-way dissociation (Martins 2022 constraint)",
                "MMN expertise function must require BOTH deviance AND "
                "expertise to be high (geometric mean property)",
                "Developmental trajectory must correlate with years of "
                "musical training (Bucher 2023: HG size)",
                "Cross-domain transfer must exist but be weaker than "
                "within-domain enhancement (Criscuolo 2022: general STG)",
                "Ablating all three upstream (EDNR, TSCP, CDMR) should "
                "degrade but not eliminate ESME output",
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
        """Transform R3/H3 + upstream into 11D expertise-specific MMN output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"EDNR": (B, T, D), "TSCP": (B, T, D),
                                  "CDMR": (B, T, D)}``

        Returns:
            ``(B, T, 11)`` -- E(4) + M(1) + P(3) + F(3)
        """
        upstream_outputs = upstream_outputs or {}
        B, T = r3_features.shape[0], r3_features.shape[1]
        device = r3_features.device

        # -- Upstream (graceful degradation with zeros) -----------------------
        ednr = upstream_outputs.get(
            "EDNR", torch.zeros(B, T, _EDNR_DIM, device=device),
        )
        tscp = upstream_outputs.get(
            "TSCP", torch.zeros(B, T, _TSCP_DIM, device=device),
        )
        cdmr = upstream_outputs.get(
            "CDMR", torch.zeros(B, T, _CDMR_DIM, device=device),
        )

        e = compute_extraction(h3_features, r3_features, ednr, tscp, cdmr)
        m = compute_temporal_integration(
            h3_features, r3_features, e, ednr, tscp, cdmr,
        )
        p = compute_cognitive_present(
            h3_features, r3_features, e, m, ednr, tscp, cdmr,
        )
        f = compute_forecast(h3_features, e, m, p, ednr, tscp, cdmr)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
