"""HGSIC -- Hierarchical Groove State Integration Circuit.

Encoder nucleus (depth 1) in STU, Function F7. Models how groove state
emerges from the integration of beat-level gamma oscillations, metric
structure, and motor preparation -- the basal ganglia-cortical circuit
that transforms rhythmic regularity into the subjective experience of
groove and the urge to move.

Reads: PEOM (period entrainment for beat context)

R3 Ontology Mapping (v1 -> 97D freeze):
    amplitude:            [7]   (B group, velocity_A)
    loudness:             [8]   (B group, velocity_D)
    roughness_total:      [9]   (B group, periodicity proxy)
    spectral_flux:        [10]  (B group, onset_strength proxy)
    onset_strength:       [11]  (B group, event salience)
    spectral_change:      [21]  (D group)
    distribution_entropy: [22]  (D group)
    flatness:             [23]  (D group)
    timbre_change:        [24]  (D group)

Output structure: E(3) + M(2) + P(3) + F(3) = 11D
  E-layer [0:3]   Extraction    (sigmoid activation)       scope=internal
  M-layer [3:5]   Memory        (groove dynamics)           scope=internal
  P-layer [5:8]   Present       (motor-auditory state)      scope=hybrid
  F-layer [8:11]  Forecast      (groove predictions)        scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hgsic/
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
    6: "200ms (beat)",
    11: "450ms (measure)",
    16: "1s (phrase)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 4: "min", 14: "periodicity",
    15: "skewness", 17: "peaks", 18: "trend",
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
_AMPLITUDE = 7          # amplitude / velocity_A (B group)
_LOUDNESS = 8           # loudness / velocity_D (B group)
_ROUGHNESS_TOTAL = 9    # roughness_total / periodicity proxy (B group)
_SPECTRAL_FLUX = 10     # spectral_flux / onset_strength proxy (B group)
_ONSET_STRENGTH = 11    # onset_strength (B group)
_SPECTRAL_CHANGE = 21   # spectral_change (D group)
_ENTROPY = 22           # distribution_entropy (D group)
_FLATNESS = 23          # flatness (D group)
_TIMBRE_CHANGE = 24     # timbre_change (D group)


# -- 15 H3 Demand Specifications -----------------------------------------------
# E-layer: 6 tuples, M-layer: 4 tuples, F-layer: 5 tuples

_HGSIC_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Beat Gamma + Meter Integration + Motor Groove (6 tuples) ===
    _h3(_AMPLITUDE, "amplitude", 6, 0, 0,
        "Amplitude value 200ms -- beat-level dynamic envelope",
        "Janata 2012"),
    _h3(_AMPLITUDE, "amplitude", 6, 4, 0,
        "Amplitude min 200ms -- dynamic floor for groove contrast",
        "Madison 2011"),
    _h3(_LOUDNESS, "loudness", 6, 0, 0,
        "Loudness value 200ms -- perceptual intensity at beat",
        "Janata 2012"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 6, 0, 0,
        "Spectral flux value 200ms -- onset energy at beat timescale",
        "Madison 2011"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 6, 17, 0,
        "Spectral flux peaks 200ms -- onset peak detection for groove",
        "Witek 2014"),
    _h3(_ONSET_STRENGTH, "onset_strength", 6, 0, 0,
        "Onset strength value 200ms -- event salience at beat",
        "Janata 2012"),

    # === M-Layer: Groove Index + Coupling Strength (4 tuples) ===
    _h3(_ENTROPY, "distribution_entropy", 11, 1, 0,
        "Entropy mean 450ms -- spectral complexity at measure",
        "Madison 2011"),
    _h3(_ENTROPY, "distribution_entropy", 11, 14, 2,
        "Entropy periodicity 450ms bidi -- complexity cycling",
        "Witek 2014"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 11, 1, 0,
        "Spectral change mean 450ms -- flux dynamics at measure",
        "Madison 2011"),
    _h3(_LOUDNESS, "loudness", 11, 1, 0,
        "Loudness mean 450ms -- sustained loudness for groove baseline",
        "Janata 2012"),

    # === F-Layer: Groove Predictions (5 tuples) ===
    _h3(_ROUGHNESS_TOTAL, "roughness_total", 16, 14, 2,
        "Roughness periodicity 1s bidi -- beat-level roughness cycling",
        "Witek 2014"),
    _h3(_AMPLITUDE, "amplitude", 16, 15, 0,
        "Amplitude skewness 1s -- dynamic asymmetry for groove",
        "Madison 2011"),
    _h3(_AMPLITUDE, "amplitude", 16, 18, 0,
        "Amplitude trend 1s -- dynamic trajectory prediction",
        "Janata 2012"),
    _h3(_FLATNESS, "flatness", 16, 14, 2,
        "Flatness periodicity 1s bidi -- spectral regularity cycling",
        "Madison 2011"),
    _h3(_TIMBRE_CHANGE, "timbre_change", 16, 1, 0,
        "Timbre change mean 1s -- timbral dynamics for motor drive",
        "Witek 2014"),
)

assert len(_HGSIC_H3_DEMANDS) == 15


class HGSIC(Encoder):
    """Hierarchical Groove State Integration Circuit -- STU Encoder (depth 1, 11D).

    Models how groove state emerges from beat-level oscillations, metric
    structure, and motor preparation in the basal ganglia-cortical circuit.

    Janata et al. (2012) showed that groove ratings correlate with motor
    cortex activation and desire to move (fMRI, N=18). Madison et al.
    (2011) demonstrated that medium syncopation maximizes groove via
    inverted-U relationship. Witek et al. (2014) confirmed the inverted-U
    groove-syncopation function (behavioral, N=66).

    Dependency chain:
        HGSIC is an Encoder (Depth 1) -- reads PEOM relay output for
        period entrainment context. Computed after PEOM in F7 pipeline.

    Upstream reads:
        PEOM: period_lock_strength, kinematic_smoothness, next_beat_pred

    Downstream feeds:
        -> groove belief (Core, F7)
        -> motor_coupling belief (Appraisal, F7)
        -> ASAP (motor simulation context)
    """

    NAME = "HGSIC"
    FULL_NAME = "Hierarchical Groove State Integration Circuit"
    UNIT = "STU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("PEOM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("f01:beat_gamma", "f02:meter_integration",
             "f03:motor_groove"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:groove_index", "M1:coupling_strength"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 8,
            ("P0:pstg_activation", "P1:motor_preparation",
             "P2:onset_sync"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:groove_prediction", "F1:beat_expectation",
             "F2:motor_anticipation"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _HGSIC_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:beat_gamma", "f02:meter_integration",
            "f03:motor_groove",
            "M0:groove_index", "M1:coupling_strength",
            "P0:pstg_activation", "P1:motor_preparation",
            "P2:onset_sync",
            "F0:groove_prediction", "F1:beat_expectation",
            "F2:motor_anticipation",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Superior Temporal Gyrus (pSTG) -- auditory groove processing
            RegionLink("P0:pstg_activation", "STG", 0.85,
                       "Janata 2012"),
            # Premotor Cortex -- motor preparation for groove
            RegionLink("P1:motor_preparation", "PMC", 0.75,
                       "Janata 2012"),
            # SMA -- motor planning for beat-locked movement
            RegionLink("f03:motor_groove", "SMA", 0.70,
                       "Grahn 2007"),
            # Putamen -- beat metric processing in basal ganglia
            RegionLink("M0:groove_index", "putamen", 0.60,
                       "Grahn 2007"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- groove pleasure and movement motivation
            NeuroLink("M0:groove_index", "dopamine", 0.55,
                      "Janata 2012"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Janata", 2012,
                         "Groove ratings correlate with motor cortex "
                         "activation and desire to move; basal ganglia "
                         "involvement in groove perception",
                         "fMRI, N=18"),
                Citation("Madison", 2011,
                         "Medium syncopation maximizes groove via inverted-U "
                         "relationship; low and high syncopation reduce groove; "
                         "event density and dynamic range contribute",
                         "behavioral, N=34"),
                Citation("Witek", 2014,
                         "Confirmed inverted-U groove-syncopation function; "
                         "medium complexity grooves most pleasurable; "
                         "desire to move peaks at medium syncopation",
                         "behavioral, N=66"),
                Citation("Grahn", 2007,
                         "Beat-inducing rhythms activate putamen + SMA; "
                         "metric structure drives basal ganglia response",
                         "fMRI, N=20"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.85),
            falsification_criteria=(
                "Groove index (M0) must show inverted-U relationship with "
                "syncopation level (Madison 2011, Witek 2014); monotonic "
                "increase or decrease = model invalid",
                "Motor preparation (P1) must correlate with PMC/SMA "
                "activation during groove perception (Janata 2012: fMRI)",
                "Beat gamma (f01) must be disrupted by non-isochronous "
                "timing; groove requires regularity substrate",
                "Coupling strength (M1) should increase with PEOM period "
                "lock; if decoupled from beat entrainment, integration "
                "mechanism is invalid",
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
        """Transform R3/H3 + PEOM relay output into 11D groove state.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"PEOM": (B, T, 11)}``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(2) + P(3) + F(3)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m,
                                      relay_outputs)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
