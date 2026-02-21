"""PSCL — Pitch Salience in Cortical Lateralization.

Encoder nucleus (depth 1) in SPU, Function F1. Transforms BCH relay output,
R³ spectral features, and H³ temporal morphologies into a 16D pitch-salience
representation following the cortical auditory pathway in anterolateral
Heschl's Gyrus (alHG).

Output structure: E(4) + M(4) + P(4) + F(4) = 16D
  E-layer [0:4]   Extraction    (instantaneous R³)     scope=internal
  M-layer [4:8]   Memory        (H³ temporal + BCH)     scope=internal
  P-layer [8:12]  Present       (cognitive integration) scope=hybrid
  F-layer [12:16] Forecast      (trend extrapolation)   scope=external

See Building/C³-Brain/F1-Sensory-Processing/mechanisms/PSCL-*.md
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

# ── Horizon labels ────────────────────────────────────────────────────
_H_LABELS = {
    3: "23ms (onset)",
    6: "200ms (beat)",
}

# ── Morph labels ──────────────────────────────────────────────────────
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity", 14: "periodicity", 18: "trend",
}

# ── Law labels ────────────────────────────────────────────────────────
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


# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
_PLEAS = 4
_INHARM = 5
_TONAL = 14
_CLARITY = 15
_SMOOTH = 16
_AUTOCORR = 17
_TRIST1 = 18
_ENTROPY = 22
_FLATNESS = 23
_CONC = 24
_PITCH_H = 37
_PITCHSAL = 39


# ── 20 H³ Demand Specifications ──────────────────────────────────────
# Ordered: L2 (integration, 7) → L0 (memory, 9) → L1 (prediction, 4)

_PSCL_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === L2 Integration (7 tuples) ===
    _h3(_INHARM, "inharmonicity", 3, 0, 2,
        "Inharmonicity at 23ms (cortical onset)", "McDermott 2010"),
    _h3(_TONAL, "tonalness", 3, 0, 2,
        "Tonalness value at 23ms", "Patterson 2002"),
    _h3(_CLARITY, "clarity", 3, 0, 2,
        "Clarity value at 23ms", "Penagos 2004"),
    _h3(_AUTOCORR, "spectral_autocorrelation", 3, 0, 2,
        "Spectral autocorrelation at 23ms", "Patterson 2002"),
    _h3(_TRIST1, "tristimulus1", 3, 0, 2,
        "Fundamental energy at 23ms", "Pollard 1982"),
    _h3(_PITCHSAL, "pitch_salience", 3, 0, 2,
        "Pitch salience at 23ms (onset)", "Bidelman 2009"),
    _h3(_PITCHSAL, "pitch_salience", 6, 0, 2,
        "Pitch salience value at 200ms (beat)", "Patterson 2002"),

    # === L0 Memory (9 tuples) ===
    _h3(_TONAL, "tonalness", 6, 1, 0,
        "Tonalness mean over 200ms", "Patterson 2002"),
    _h3(_AUTOCORR, "spectral_autocorrelation", 6, 1, 0,
        "Spectral autocorrelation mean 200ms", "Patterson 2002"),
    _h3(_TRIST1, "tristimulus1", 6, 1, 0,
        "Tristimulus1 mean 200ms", "Pollard 1982"),
    _h3(_ENTROPY, "distribution_entropy", 6, 1, 0,
        "Spectral entropy mean 200ms (inverted)", "Penagos 2004"),
    _h3(_CONC, "distribution_concentration", 6, 14, 0,
        "Concentration periodicity 200ms", "Penagos 2004"),
    _h3(_PITCH_H, "pitch_height", 6, 8, 0,
        "Pitch height velocity 200ms", "Pressnitzer 2001"),
    _h3(_PITCHSAL, "pitch_salience", 6, 1, 0,
        "Pitch salience mean 200ms", "Bidelman 2009"),
    _h3(_TONAL, "tonalness", 6, 18, 0,
        "Tonalness trend 200ms", "Patterson 2002"),
    _h3(_PITCHSAL, "pitch_salience", 6, 18, 0,
        "Pitch salience trend 200ms", "Bidelman 2009"),

    # === L1 Prediction (4 tuples) ===
    _h3(_TONAL, "tonalness", 6, 1, 1,
        "Expected tonalness 200ms ahead", "Patterson 2002"),
    _h3(_CONC, "distribution_concentration", 6, 18, 1,
        "Concentration trend 200ms ahead", "Penagos 2004"),
    _h3(_PITCH_H, "pitch_height", 6, 1, 1,
        "Expected pitch height 200ms ahead", "Pressnitzer 2001"),
    _h3(_PITCHSAL, "pitch_salience", 6, 1, 1,
        "Expected pitch salience 200ms ahead", "Bidelman 2009"),
)

assert len(_PSCL_H3_DEMANDS) == 20


class PSCL(Encoder):
    """Pitch Salience in Cortical Lateralization — SPU Encoder (depth 1, 16D).

    Processes BCH relay output alongside R³/H³ into cortical pitch-salience
    representations. Models anterolateral Heschl's Gyrus (alHG) response.
    """

    NAME = "PSCL"
    FULL_NAME = "Pitch Salience in Cortical Lateralization"
    UNIT = "SPU"
    FUNCTION = "F1"
    OUTPUT_DIM = 16
    UPSTREAM_READS = ("BCH",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:pitch_salience_raw", "E1:hg_activation_proxy",
             "E2:salience_gradient", "E3:spectral_focus"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 8,
            ("M0:salience_sustained", "M1:spectral_coherence",
             "M2:tonal_salience_ctx", "M3:bch_integration"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 8, 12,
            ("P0:pitch_prominence_sig", "P1:hg_cortical_response",
             "P2:periodicity_clarity", "P3:salience_hierarchy"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 12, 16,
            ("F0:pitch_continuation", "F1:salience_direction",
             "F2:melody_propagation", "F3:register_trajectory"),
            scope="external",
        ),
    )

    # ── Abstract property implementations ─────────────────────────────

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PSCL_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:pitch_salience_raw", "E1:hg_activation_proxy",
            "E2:salience_gradient", "E3:spectral_focus",
            "M0:salience_sustained", "M1:spectral_coherence",
            "M2:tonal_salience_ctx", "M3:bch_integration",
            "P0:pitch_prominence_sig", "P1:hg_cortical_response",
            "P2:periodicity_clarity", "P3:salience_hierarchy",
            "F0:pitch_continuation", "F1:salience_direction",
            "F2:melody_propagation", "F3:register_trajectory",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Anterolateral Heschl's Gyrus — primary pitch center
            RegionLink("P0:pitch_prominence_sig", "A1_HG", 0.85,
                       "Patterson 2002"),
            RegionLink("P1:hg_cortical_response", "A1_HG", 0.90,
                       "Penagos 2004"),
            RegionLink("P2:periodicity_clarity", "A1_HG", 0.60,
                       "Patterson 2002"),
            # Superior Temporal Gyrus — secondary pitch processing
            RegionLink("P0:pitch_prominence_sig", "STG", 0.60,
                       "Patterson 2002"),
            RegionLink("F2:melody_propagation", "STG", 0.40,
                       "Tabas 2019"),
            # STS and IFG — weaker projections
            RegionLink("F0:pitch_continuation", "STS", 0.30,
                       "Griffiths 2010"),
            RegionLink("F2:melody_propagation", "IFG", 0.25,
                       "Zatorre 2002"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Pitch salience → weak NE modulation (attention)
            NeuroLink("P0:pitch_prominence_sig", 1, "amplify", 0.20,
                      "Zatorre 2002"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Patterson", 2002,
                         "alHG pitch center in fMRI",
                         "cluster peak at [-48,-16,8]"),
                Citation("Penagos", 2004,
                         "Pitch salience tracks alHG activation",
                         "r=0.92"),
                Citation("Oxenham", 2012,
                         "Review: pitch encoding at cortical level",
                         "review"),
                Citation("Bidelman", 2009,
                         "FFR pitch salience predicts consonance",
                         "r=0.81"),
                Citation("Tabas", 2019,
                         "POR latency 36ms shorter for consonant in alHG",
                         "N=37, MEG"),
                Citation("Briley", 2013,
                         "IRN sources 7mm lateral/anterior to pure-tone",
                         "fMRI"),
                Citation("Pressnitzer", 2001,
                         "Pitch salience varies with register",
                         "psychophysics"),
                Citation("Griffiths", 2010,
                         "Temporal pitch processing in STS",
                         "fMRI"),
                Citation("Zatorre", 2002,
                         "Pitch processing in right IFG",
                         "meta-analysis"),
                Citation("Schonwiesner", 2008,
                         "Lateral HG pitch onset dissociation",
                         "fMRI double dissociation"),
                Citation("McDermott", 2010,
                         "Harmonicity preference",
                         "r=0.71"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.80, 0.92),
            falsification_criteria=(
                "alHG BOLD signal should correlate >0.60 with pitch_prominence "
                "for resolved-harmonic stimuli; failure = model invalid",
                "Pitch salience ordering (Strong>Weak>Noise) should replicate "
                "the Penagos 2004 parametric gradient",
            ),
            version="1.0.0",
        )

    # ── Compute ───────────────────────────────────────────────────────

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        relay_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Transform R³/H³ + BCH relay into 16D pitch-salience representation.

        Delegates to 4 layer functions (extraction → temporal_integration
        → cognitive_present → forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"BCH": (B, T, 16)}``

        Returns:
            ``(B, T, 16)`` — E(4) + M(4) + P(4) + F(4)
        """
        bch = relay_outputs["BCH"]  # (B, T, 16)

        e = compute_extraction(r3_features)
        m = compute_temporal_integration(r3_features, h3_features, bch)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(r3_features, h3_features, p, m, bch)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        # Selective clamping: all dims to [0,1] except dim 13 (F1) to [-1,1]
        output[:, :, :13] = output[:, :, :13].clamp(0.0, 1.0)
        output[:, :, 13] = output[:, :, 13].clamp(-1.0, 1.0)
        output[:, :, 14:] = output[:, :, 14:].clamp(0.0, 1.0)

        return output
