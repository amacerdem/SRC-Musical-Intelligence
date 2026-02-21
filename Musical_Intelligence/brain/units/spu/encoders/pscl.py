"""PSCL — Pitch Salience in Cortical Lateralization.

Encoder nucleus (depth 1) in SPU. Transforms BCH relay output, R³ spectral
features, and H³ temporal morphologies into a 16D pitch-salience representation
following the cortical auditory pathway in anterolateral Heschl's Gyrus (alHG).

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

# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
# A group [0:7]
_PLEAS = 4          # sensory_pleasantness
_INHARM = 5         # inharmonicity
# C group [12:21]
_TONAL = 14         # tonalness (brightness_kuttruff in code)
_CLARITY = 15       # clarity
_SMOOTH = 16        # spectral_smoothness
_AUTOCORR = 17      # spectral_autocorrelation
_TRIST1 = 18        # tristimulus1
# D group [21:25]
_ENTROPY = 22       # distribution_entropy
_FLATNESS = 23      # distribution_flatness
_CONC = 24          # distribution_concentration
# F group [25:41]
_CHROMA_START = 25  # chroma vector start (12D pitch classes)
_CHROMA_END = 37    # chroma vector end (exclusive)
_PITCH_H = 37       # pitch_height
_PITCHSAL = 39      # pitch_salience

# ── BCH relay output indices ─────────────────────────────────────────
_BCH_E0 = 0         # E0:nps (neural pitch salience)
_BCH_E1 = 1         # E1:harmonicity
_BCH_P0 = 8         # P0:consonance_signal
_BCH_F1 = 13        # F1:pitch_forecast

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

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"BCH": (B, T, 16)}``

        Returns:
            ``(B, T, 16)`` — E(4) + M(4) + P(4) + F(4)
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # BCH relay output
        bch = relay_outputs["BCH"]  # (B, T, 16)

        # Helper to read R³ feature
        def r3(idx: int) -> Tensor:
            return r3_features[:, :, idx]

        # Helper to read H³ feature
        def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
            key = (r3_idx, horizon, morph, law)
            if key in h3_features:
                return h3_features[key]
            return torch.zeros(B, T, device=device)

        # === E-LAYER (indices 0-3) — instantaneous R³ ===

        # E0: Pitch Salience Raw
        e0 = 0.90 * (
            0.40 * r3(_PITCHSAL)
            + 0.35 * r3(_TONAL) * r3(_AUTOCORR)
            + 0.25 * r3(_CONC)
        )

        # E1: HG Activation Proxy
        e1 = 0.85 * (1.0 - r3(_INHARM)) * (
            0.50 * r3(_TRIST1)
            + 0.30 * r3(_SMOOTH)
            + 0.20 * r3(_PITCHSAL)
        )

        # E2: Salience Gradient
        e2 = 0.80 * (1.0 - r3(_ENTROPY)) * (1.0 - r3(_FLATNESS)) * r3(_PLEAS)

        # E3: Spectral Focus
        e3 = r3(_CONC) * r3(_CLARITY) * (1.0 - r3(_FLATNESS))

        # === M-LAYER (indices 4-7) — H³ temporal + BCH ===

        # M0: Salience Sustained
        m0 = (
            0.25 * h3(_TONAL, 6, 1, 0)
            + 0.25 * h3(_PITCHSAL, 6, 1, 0)
            + 0.20 * h3(_AUTOCORR, 6, 1, 0)
            + 0.15 * h3(_TRIST1, 6, 1, 0)
            + 0.15 * h3(_CONC, 6, 14, 0)
        )

        # M1: Spectral Coherence
        m1 = (
            0.30 * h3(_AUTOCORR, 3, 0, 2)
            + 0.30 * h3(_TONAL, 3, 0, 2)
            + 0.20 * h3(_TRIST1, 3, 0, 2)
            + 0.20 * (1.0 - h3(_ENTROPY, 6, 1, 0))
        )

        # M2: Tonal Salience Context
        chroma = r3_features[:, :, _CHROMA_START:_CHROMA_END]  # (B, T, 12)
        chroma_peak = chroma.max(dim=-1).values  # (B, T)
        m2 = (
            0.35 * chroma_peak
            + 0.30 * r3(_PITCHSAL)
            + 0.20 * (1.0 - r3(_ENTROPY))
            + 0.15 * r3(_PITCH_H)
        )

        # M3: BCH Integration
        m3 = (
            0.40 * bch[:, :, _BCH_E0]
            + 0.30 * bch[:, :, _BCH_E1]
            + 0.20 * bch[:, :, _BCH_P0]
            + 0.10 * bch[:, :, _BCH_F1]
        )

        # === P-LAYER (indices 8-11) — cognitive present ===

        # P0: Pitch Prominence Signal
        p0 = (
            0.25 * e0
            + 0.25 * m0
            + 0.20 * m3
            + 0.15 * r3(_PITCHSAL)
            + 0.15 * h3(_PITCHSAL, 6, 0, 2)
        )

        # P1: HG Cortical Response
        p1 = (
            0.30 * e1
            + 0.25 * m1
            + 0.20 * h3(_PITCHSAL, 3, 0, 2)
            + 0.15 * (1.0 - h3(_INHARM, 3, 0, 2))
            + 0.10 * h3(_CLARITY, 3, 0, 2)
        )

        # P2: Periodicity Clarity
        p2 = (
            0.30 * e3
            + 0.25 * h3(_CONC, 6, 14, 0)
            + 0.25 * h3(_AUTOCORR, 3, 0, 2)
            + 0.20 * r3(_TONAL)
        )

        # P3: Salience Hierarchy
        p3 = (
            0.35 * e2
            + 0.25 * m2
            + 0.25 * m0
            + 0.15 * e0
        )

        # === F-LAYER (indices 12-15) — trend extrapolation ===

        # F0: Pitch Continuation
        f0 = (
            0.30 * h3(_TONAL, 6, 18, 0)
            + 0.25 * h3(_PITCHSAL, 6, 18, 0)
            + 0.20 * h3(_TONAL, 6, 1, 1)
            + 0.15 * h3(_PITCHSAL, 6, 1, 1)
            + 0.10 * bch[:, :, _BCH_F1]
        )

        # F1: Salience Direction (signed, [-1, 1])
        f1_raw = (
            0.35 * h3(_PITCHSAL, 6, 18, 0)
            + 0.30 * h3(_TONAL, 6, 18, 0)
            + 0.20 * h3(_CONC, 6, 18, 1)
            + 0.15 * h3(_PITCH_H, 6, 8, 0)
        )
        f1 = torch.tanh(f1_raw)

        # F2: Melody Propagation
        f2 = (
            0.30 * p0
            + 0.25 * h3(_PITCH_H, 6, 1, 1)
            + 0.25 * h3(_PITCH_H, 6, 8, 0)
            + 0.20 * m2
        )

        # F3: Register Trajectory
        f3 = (
            0.40 * h3(_PITCH_H, 6, 8, 0)
            + 0.30 * h3(_PITCH_H, 6, 1, 1)
            + 0.30 * r3(_PITCH_H)
        )

        # === Stack into (B, T, 16) ===
        # Clamp [0,1] for all except F1 which is [-1,1]
        output = torch.stack(
            [e0, e1, e2, e3, m0, m1, m2, m3, p0, p1, p2, p3, f0, f1, f2, f3],
            dim=-1,
        )
        # Selective clamping: all dims to [0,1] except dim 13 (F1) to [-1,1]
        output[:, :, :13] = output[:, :, :13].clamp(0.0, 1.0)
        output[:, :, 13] = output[:, :, 13].clamp(-1.0, 1.0)
        output[:, :, 14:] = output[:, :, 14:].clamp(0.0, 1.0)

        return output
