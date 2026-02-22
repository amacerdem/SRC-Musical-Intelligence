"""ETAM -- Entrainment, Tempo and Attention Modulation.

Encoder nucleus (depth 1, reads relay outputs) in STU, Function F3. Models
how neural entrainment to the tempo envelope modulates selective attention,
enabling preferential processing of events aligned with entrained temporal
expectations. Tempo-locked oscillations in auditory cortex create attentional
windows that gate perceptual processing, enhancing detection of on-beat events
and supporting stream segregation in complex auditory scenes.

Dependency chain:
    ETAM is an Encoder (Depth 1) -- reads HMCE relay output (cross-unit, STU).
    No same-unit upstream reads.

R3 Ontology Mapping (post-freeze 97D):
    amplitude:          [7]      (A, velocity_A)
    loudness:           [8]      (A, velocity_D)
    spectral_flux:      [10]     (B, onset_strength proxy)
    onset_strength:     [11]     (B, event salience)
    spectral_change:    [21]     (D, spectral_flux)
    energy_change:      [22]     (D, dynamic change)
    timbre_change:      [24]     (D, timbral dynamics)
    x_l0l5:             [25]     (F, coupling)
    x_l4l5:             [33]     (F, cross-stream coupling)
    x_l5l7:             [41]     (H, cognitive coupling)

Output structure: E(4) + M(2) + P(2) + F(3) = 11D
  E-layer [0:4]   Extraction    (sigmoid)  scope=internal
  M-layer [4:6]   Memory        (sigmoid)  scope=internal
  P-layer [6:8]   Present       (sigmoid)  scope=hybrid
  F-layer [8:11]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/etam/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

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
    6: "150ms (beta)",
    8: "500ms (delta)",
    11: "750ms (delta)",
    14: "~900ms (beat)",
    16: "1000ms (beat)",
    20: "5000ms (long)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 3: "std", 4: "max", 8: "velocity",
    13: "entropy", 14: "periodicity", 17: "peaks", 18: "trend",
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
_AMPLITUDE = 7               # amplitude / velocity_A (A group)
_LOUDNESS = 8                # loudness / velocity_D (A group)
_SPECTRAL_FLUX = 10          # spectral_flux / onset_strength proxy (B group)
_ONSET_STRENGTH = 11         # onset_strength (B group)
_SPECTRAL_CHANGE = 21        # spectral_change (D group)
_ENERGY_CHANGE = 22          # energy_change (D group)
_TIMBRE_CHANGE = 24          # timbre_change (D group)
_X_L0L5 = 25                 # coupling (F group)
_X_L4L5 = 33                 # cross-stream coupling (F group)
_X_L5L7 = 41                 # cognitive coupling (H group)


# -- 20 H3 Demand Specifications -----------------------------------------------
# Tempo-locked entrainment across timescales: 150ms -> 500ms -> 750ms -> ~900ms -> 1s -> 5s

_ETAM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Amplitude / early temporal window (2 tuples) ===
    _h3(7, "amplitude", 6, 0, 2,
        "Amplitude value 150ms -- early window", "Tierney 2015"),
    _h3(7, "amplitude", 6, 4, 2,
        "Amplitude max 150ms -- peak detection", "Tierney 2015"),

    # === Loudness / perceptual weight (1 tuple) ===
    _h3(8, "loudness", 6, 0, 0,
        "Loudness value 150ms L0 -- perceptual weight", "Tierney 2015"),

    # === Onset Strength / event marker (1 tuple) ===
    _h3(11, "onset_strength", 6, 0, 0,
        "Onset value 150ms L0 -- event marker", "Grahn 2012"),

    # === Spectral Flux / medium context (1 tuple) ===
    _h3(10, "spectral_flux", 11, 0, 0,
        "Flux value 750ms L0 -- medium context", "Grahn 2012"),

    # === Spectral Change / rate of change (2 tuples) ===
    _h3(21, "spectral_change", 8, 1, 0,
        "Spectral change mean 500ms", "Grahn 2012"),
    _h3(21, "spectral_change", 8, 3, 0,
        "Spectral std 500ms -- variability", "Grahn 2012"),

    # === Energy Change / dynamics (2 tuples) ===
    _h3(22, "energy_change", 11, 8, 0,
        "Energy velocity 750ms -- dynamics", "Tierney 2015"),
    _h3(22, "energy_change", 11, 14, 2,
        "Energy periodicity 750ms -- groove", "Grahn 2012"),

    # === X_L0L5 coupling / bar-level (2 tuples) ===
    _h3(25, "x_l0l5", 16, 0, 2,
        "Coupling value 1s -- bar-level", "Grahn 2012"),
    _h3(25, "x_l0l5", 16, 14, 2,
        "Coupling periodicity 1s -- metric period", "Grahn 2012"),

    # === X_L5L7 cognitive coupling / ~900ms (2 tuples) ===
    _h3(41, "x_l5l7", 14, 1, 0,
        "Cognitive coupling mean ~900ms", "London 2012"),
    _h3(41, "x_l5l7", 14, 13, 0,
        "Cognitive coupling entropy ~900ms", "London 2012"),

    # === Timbre Change / asymmetry (2 tuples) ===
    _h3(24, "timbre_change", 14, 3, 0,
        "Timbre std ~900ms -- asymmetry", "Tierney 2015"),
    _h3(24, "timbre_change", 8, 0, 0,
        "Timbre change value 500ms", "Tierney 2015"),

    # === X_L4L5 cross-stream / tracking (2 tuples) ===
    _h3(33, "x_l4l5", 16, 0, 2,
        "Cross-stream value 1s -- tracking", "London 2012"),
    _h3(33, "x_l4l5", 16, 18, 0,
        "Cross-stream trend 1s -- trajectory", "London 2012"),

    # === Loudness / sustained and long dynamics (2 tuples) ===
    _h3(8, "loudness", 14, 1, 0,
        "Loudness mean ~900ms -- sustained level", "Tierney 2015"),
    _h3(8, "loudness", 20, 18, 0,
        "Loudness trend 5s -- long dynamics", "Tierney 2015"),

    # === Spectral Flux / event salience (1 tuple) ===
    _h3(10, "spectral_flux", 11, 17, 0,
        "Flux peaks 750ms -- event salience", "Grahn 2012"),
)

assert len(_ETAM_H3_DEMANDS) == 20


class ETAM(Encoder):
    """Entrainment, Tempo and Attention Modulation -- STU Encoder (depth 1, 11D).

    Models how neural entrainment to the tempo envelope modulates selective
    attention. Tempo-locked oscillations in auditory cortex create attentional
    windows that gate perceptual processing, enhancing detection of on-beat
    events and supporting stream segregation in complex auditory scenes.

    Tierney & Kraus 2015: EEG entrainment to tempo envelope predicts attention
    performance; beat-locked oscillations amplify on-beat processing (N=24).

    Grahn & Rowe 2012: fMRI evidence that basal ganglia and SMA support
    beat-based temporal prediction; STG encodes tempo envelope for entrainment
    (N=20).

    London 2012: Behavioral review of temporal attention in music; metric
    hierarchy creates graded attentional weights across beat subdivisions.

    Dependency chain:
        ETAM is an Encoder (Depth 1) -- cross-unit read from HMCE (STU).
        No same-unit upstream reads.

    Downstream feeds:
        -> Salience system (attention_gain modulates salience mixing)
        -> Stream segregation beliefs (Appraisal)
        -> Entrainment tracking beliefs (Core)
        -> Attention sustain predictions (Anticipation)
    """

    NAME = "ETAM"
    FULL_NAME = "Entrainment, Tempo and Attention Modulation"
    UNIT = "STU"
    FUNCTION = "F3"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ()
    CROSS_UNIT_READS = ("HMCE",)

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:early_window", "E1:middle_window",
             "E2:late_window", "E3:instrument_asymmetry"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 6,
            ("M0:attention_gain", "M1:entrainment_index"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 8,
            ("P0:envelope_tracking", "P1:stream_separation"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:tracking_prediction", "F1:attention_sustain",
             "F2:segregation_predict"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _ETAM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:early_window", "E1:middle_window",
            "E2:late_window", "E3:instrument_asymmetry",
            "M0:attention_gain", "M1:entrainment_index",
            "P0:envelope_tracking", "P1:stream_separation",
            "F0:tracking_prediction", "F1:attention_sustain",
            "F2:segregation_predict",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # STG -- tempo envelope encoding and entrainment hub
            RegionLink("M0:attention_gain", "STG", 0.85,
                       "Grahn 2012"),
            # HG -- early temporal window processing
            RegionLink("E0:early_window", "HG", 0.80,
                       "Tierney 2015"),
            # MTG -- mid-latency temporal integration
            RegionLink("E1:middle_window", "MTG", 0.75,
                       "Grahn 2012"),
            # IFG -- attentional control for stream segregation
            RegionLink("P1:stream_separation", "IFG", 0.70,
                       "London 2012"),
            # SMA -- motor-auditory temporal prediction
            RegionLink("F0:tracking_prediction", "SMA", 0.65,
                       "Grahn 2012"),
            # Cerebellum -- fine-grained timing for entrainment
            RegionLink("M1:entrainment_index", "cerebellum", 0.60,
                       "Tierney 2015"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # ETAM modulates attention via entrainment, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Tierney & Kraus", 2015,
                         "EEG entrainment to tempo envelope predicts attention "
                         "performance; beat-locked oscillations in auditory cortex "
                         "amplify processing at expected time points; temporal "
                         "fine structure encoding correlates with beat tracking",
                         "EEG+behavioral, N=24"),
                Citation("Grahn & Rowe", 2012,
                         "fMRI evidence: basal ganglia and SMA support beat-based "
                         "temporal prediction; STG encodes tempo envelope; beat "
                         "strength parametrically modulates putamen activity; "
                         "metric structure engages premotor cortex",
                         "fMRI, N=20"),
                Citation("London", 2012,
                         "Hearing in Time: metric hierarchy creates graded "
                         "attentional weights across beat subdivisions; temporal "
                         "attention follows metric structure in music; review of "
                         "behavioral evidence for entrainment-based attention",
                         "behavioral review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Attention gain (M0) must be higher for metrically strong "
                "vs weak beats (Grahn 2012: parametric beat strength in STG)",
                "Entrainment index (M1) must correlate with tempo regularity "
                "(Tierney 2015: EEG phase-locking to beat)",
                "Early window (E0) must show earlier peak than late window (E2) "
                "(testable: ERP latency comparison)",
                "Stream separation (P1) must improve with stronger entrainment "
                "(testable: concurrent stream identification paradigm)",
                "Disrupting SMA should impair temporal prediction without "
                "affecting basic entrainment (testable: TMS/lesion)",
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
        """Transform R3/H3 into 11D entrainment-tempo-attention modulation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"HMCE": (B, T, dim)}`` cross-unit relay.

        Returns:
            ``(B, T, 11)`` -- E(4) + M(2) + P(2) + F(3)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, e, m)
        f = compute_forecast(h3_features, e, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
