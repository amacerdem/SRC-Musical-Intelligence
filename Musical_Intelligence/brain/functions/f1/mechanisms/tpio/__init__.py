"""TPIO -- Timbre Perception-Imagery Overlap.

Relay nucleus (depth 0) in SPU, Function F1. Models the overlap between
timbre perception and timbre imagery -- the neural machinery for real-time
timbral encoding shares substrates with internally generated timbral
representations in pSTG and SMA, establishing a perception-imagery
continuum for spectral processing.

Dependency chain:
    TPIO is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with BCH, MIAA, MPG, SDED at Phase 0a of the kernel scheduler.

R3 Ontology Mapping (v1 -> 97D freeze):
    warmth:               [12]  (C group)
    sharpness:            [13]  (C group)
    tonalness:            [14]  (C group)
    clarity:              [15]  (C group)
    spectral_autocorr:    [17]  (C group)
    tristimulus1:         [18]  (C group)
    tristimulus2:         [19]  (C group)
    tristimulus3:         [20]  (C group)
    spectral_change:      [21]  (D group)
    timbre_change:        [24]  (D group)
    amplitude:            [7]   (B group)
    loudness:             [8]   (B group)

Output structure: E(4) + M(1) + P(2) + F(3) = 10D
  E-layer [0:4]   Extraction    (sigmoid activation)       scope=internal
  M-layer [4:5]   Memory        (overlap integration)      scope=internal
  P-layer [5:7]   Present       (cortical activations)     scope=hybrid
  F-layer [7:10]  Forecast      (imagery predictions)      scope=external

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/tpio/
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
    2: "50ms (gamma-fast)",
    5: "150ms (alpha)",
    8: "250ms (theta)",
    14: "600ms (phrase)",
    20: "1.2s (section)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 3: "std", 8: "velocity",
    18: "trend", 22: "autocorrelation",
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
_WARMTH = 12          # warmth (C group)
_SHARPNESS = 13       # sharpness (C group)
_TONALNESS = 14       # tonalness (C group)
_CLARITY = 15         # clarity (C group)
_SPECTRAL_AUTO = 17   # spectral_autocorrelation (C group)
_TRIST1 = 18          # tristimulus1 (C group)
_TRIST2 = 19          # tristimulus2 (C group)
_TRIST3 = 20          # tristimulus3 (C group)
_SPECTRAL_CHANGE = 21 # spectral_change (D group)
_TIMBRE_CHANGE = 24   # timbre_change (D group)
_AMPLITUDE = 7        # amplitude / velocity_A (B group)
_LOUDNESS = 8         # loudness / velocity_D (B group)


# -- 18 H3 Demand Specifications -----------------------------------------------
# E-layer: 12 tuples, P-layer: 6 tuples

_TPIO_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Perception + Imagery Substrates (12 tuples) ===
    _h3(_WARMTH, "warmth", 2, 0, 2,
        "Instant warmth at fast gamma -- timbral quality encoding",
        "Halpern 2004"),
    _h3(_SHARPNESS, "sharpness", 2, 0, 2,
        "Instant sharpness at fast gamma -- spectral edge encoding",
        "Zatorre 2005"),
    _h3(_TONALNESS, "tonalness", 5, 1, 0,
        "Tonalness mean 150ms -- pitch clarity for timbral context",
        "Patterson 2002"),
    _h3(_CLARITY, "clarity", 5, 0, 0,
        "Clarity value 150ms -- spectral resolution baseline",
        "Halpern 2004"),
    _h3(_TRIST1, "tristimulus1", 2, 0, 2,
        "Tristimulus1 at 50ms -- fundamental energy for imagery grounding",
        "Halpern 2004"),
    _h3(_TRIST2, "tristimulus2", 2, 0, 2,
        "Tristimulus2 at 50ms -- mid-partial energy for spectral color",
        "Halpern 2004"),
    _h3(_TRIST3, "tristimulus3", 2, 0, 2,
        "Tristimulus3 at 50ms -- high-partial energy for spectral color",
        "Halpern 2004"),
    _h3(_WARMTH, "warmth", 14, 1, 0,
        "Warmth mean 600ms -- sustained timbral quality in memory",
        "Crowder 1989"),
    _h3(_TONALNESS, "tonalness", 14, 1, 0,
        "Tonalness mean 600ms -- tonal clarity over phrase timescale",
        "Patterson 2002"),
    _h3(_TRIST1, "tristimulus1", 20, 1, 0,
        "Tristimulus1 mean 1.2s -- long-term fundamental stability",
        "McAdams 1999"),
    _h3(_LOUDNESS, "loudness", 20, 1, 0,
        "Loudness mean 1.2s -- sustained loudness for imagery baseline",
        "Halpern 2004"),
    _h3(_AMPLITUDE, "amplitude", 20, 18, 0,
        "Amplitude trend 1.2s -- dynamic envelope trajectory",
        "Zatorre 2005"),

    # === P-Layer: Present Cortical Activations (6 tuples) ===
    _h3(_SPECTRAL_AUTO, "spectral_autocorrelation", 8, 1, 0,
        "Spectral autocorrelation mean 250ms -- periodicity of timbre",
        "Zatorre 2005"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 1, 0,
        "Spectral change mean 250ms -- flux dynamics for timbre state",
        "McAdams 1999"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 8, 0,
        "Spectral change velocity 250ms -- rate of flux change",
        "McAdams 1999"),
    _h3(_TIMBRE_CHANGE, "timbre_change", 8, 1, 0,
        "Timbre change mean 250ms -- composite timbre dynamics",
        "McAdams 1999"),
    _h3(_TONALNESS, "tonalness", 14, 3, 0,
        "Tonalness std 600ms -- tonal variability for prediction uncertainty",
        "Halpern 2004"),
    _h3(_TRIST1, "tristimulus1", 20, 22, 0,
        "Tristimulus1 autocorrelation 1.2s -- recurrence of spectral shape",
        "Crowder 1989"),
)

assert len(_TPIO_H3_DEMANDS) == 18


class TPIO(Relay):
    """Timbre Perception-Imagery Overlap -- SPU Relay (depth 0, 10D).

    Models the shared cortical substrates for real-time timbre perception
    and internally generated timbral imagery. Halpern et al. (2004) showed
    that imagined timbre activates pSTG and SMA in patterns overlapping
    with perceived timbre (fMRI, N=10). Crowder (1989) established that
    timbral imagery preserves spectral detail. McAdams (1999) confirmed
    timbre space dimensionality maps to spectral/temporal acoustic features.

    Dependency chain:
        TPIO is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> timbre_imagery belief (Appraisal)
        -> MIAA (imagery-action loop)
        -> F5 emotional coloring (timbral aesthetics)
    """

    NAME = "TPIO"
    FULL_NAME = "Timbre Perception-Imagery Overlap"
    UNIT = "SPU"
    FUNCTION = "F1"
    OUTPUT_DIM = 10

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:perception_substrate", "f02:imagery_substrate",
             "f03:perc_imag_overlap", "f04:sma_imagery"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 5,
            ("M0:overlap_index",),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:pstg_activation", "P1:sma_activation"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:imagery_stability_pred", "F1:timbre_expectation",
             "F2:overlap_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _TPIO_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:perception_substrate", "f02:imagery_substrate",
            "f03:perc_imag_overlap", "f04:sma_imagery",
            "M0:overlap_index",
            "P0:pstg_activation", "P1:sma_activation",
            "F0:imagery_stability_pred", "F1:timbre_expectation",
            "F2:overlap_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Right posterior STG -- timbre perception + imagery overlap
            RegionLink("P0:pstg_activation", "STG", 0.80,
                       "Halpern 2004"),
            # Planum Temporale -- spectral template matching
            RegionLink("f01:perception_substrate", "PT", 0.65,
                       "Zatorre 2005"),
            # SMA -- motor imagery for timbral production
            RegionLink("P1:sma_activation", "SMA", 0.55,
                       "Halpern 2004"),
            # Heschl's Gyrus -- early spectral encoding
            RegionLink("f01:perception_substrate", "A1_HG", 0.70,
                       "Patterson 2002"),
        )

    @property
    def neuro_links(self) -> Tuple:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Halpern", 2004,
                         "Imagined timbre activates pSTG and SMA in "
                         "patterns overlapping with perceived timbre; "
                         "imagery fidelity varies with musical training",
                         "fMRI, N=10"),
                Citation("Zatorre", 2005,
                         "Auditory cortex mediates both perception and "
                         "imagery of pitch and timbre; right hemisphere "
                         "specialization for spectral processing",
                         "fMRI + PET, review"),
                Citation("Crowder", 1989,
                         "Timbral imagery preserves spectral detail; "
                         "auditory imagery is analog not propositional",
                         "behavioral, N=24"),
                Citation("McAdams", 1999,
                         "Timbre space dimensionality maps to spectral "
                         "and temporal acoustic features; attack, spectral "
                         "centroid, flux are primary axes",
                         "MDS, N=88 tones"),
                Citation("Patterson", 2002,
                         "alHG pitch center processes spectral fine "
                         "structure underlying timbre perception",
                         "fMRI, cluster peak [-48,-16,8]"),
            ),
            evidence_tier="beta",
            confidence_range=(0.60, 0.80),
            falsification_criteria=(
                "pSTG activation should overlap for perceived and imagined "
                "timbre (Halpern 2004); if no overlap, imagery model invalid",
                "SMA imagery signal (f04) should correlate with musical "
                "training level (Halpern 2004: trained > untrained)",
                "Overlap index (M0) should increase for familiar timbres "
                "compared to novel; failure = imagery specificity invalid",
                "Timbre expectation (F1) should be disrupted by spectral "
                "discontinuities (McAdams 1999: flux axis)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 10D timbre perception-imagery representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 10)`` -- E(4) + M(1) + P(2) + F(3)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
