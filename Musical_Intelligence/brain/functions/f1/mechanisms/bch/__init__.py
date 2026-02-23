"""BCH — Brainstem Consonance Hierarchy.

Relay nucleus (depth 0) in SPU, Function F1. Transforms raw R³ spectral
features and H³ temporal morphologies into a 16D consonance representation
following the brainstem's ascending auditory pathway (AN → CN → SOC → IC → MGB).

Output structure: E(4) + M(4) + P(4) + F(4) = 16D
  E-layer [0:4]   Extraction    (instantaneous R³)     scope=internal
  M-layer [4:8]   Memory        (H³ temporal)           scope=internal
  P-layer [8:12]  Present       (cognitive integration) scope=hybrid
  F-layer [12:16] Forecast      (trend extrapolation)   scope=external

See Building/C³-Brain/F1-Sensory-Processing/mechanisms/BCH-*.md
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

# ── Horizon labels ────────────────────────────────────────────────────
_H_LABELS = {
    0: "5.8ms (instant)",
    3: "23ms (onset)",
    6: "200ms (beat)",
    12: "525ms (phrase)",
    16: "1s (measure)",
    18: "2s (long phrase)",
}

# ── Morph labels ──────────────────────────────────────────────────────
_M_LABELS = {0: "value", 1: "mean", 14: "periodicity", 18: "trend"}

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
_ROUGH = 0
_SETH = 1
_HELM = 2
_STUMP = 3
_PLEAS = 4
_INHARM = 5
_HDEV = 6
_TONAL = 14
_AUTOCORR = 17
_TRIST1 = 18
_TRIST2 = 19
_TRIST3 = 20
_PCE = 38
_PITCHSAL = 39
_KEYCLAR = 51
_TONALSTAB = 60
_COUPLING = 41


# ── 48 H³ Demand Specifications ──────────────────────────────────────
# Ordered: L2 (integration, 19) → L0 (memory, 17) → L1 (prediction, 12)

_BCH_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === L2 Integration (21 tuples) ===
    _h3(_ROUGH, "roughness", 0, 0, 2,
        "Roughness value now (bidirectional)", "Plomp & Levelt 1965"),
    _h3(_ROUGH, "roughness", 3, 1, 2,
        "Roughness mean 23ms (sustained)", "Plomp & Levelt 1965"),
    _h3(_HELM, "helmholtz_kang", 0, 0, 2,
        "Helmholtz consonance now", "Helmholtz 1863"),
    _h3(_HELM, "helmholtz_kang", 3, 1, 2,
        "Helmholtz mean 23ms", "Kang 2009"),
    _h3(_STUMP, "stumpf_fusion", 0, 0, 2,
        "Stumpf fusion now", "Stumpf 1890"),
    _h3(_INHARM, "inharmonicity", 0, 0, 2,
        "Inharmonicity value now", "McDermott 2010"),
    _h3(_HDEV, "harmonic_deviation", 0, 0, 2,
        "Harmonic deviation now", "Bidelman 2013"),
    _h3(_TRIST1, "tristimulus1", 0, 0, 2,
        "Fundamental energy now", "Pollard 1982"),
    _h3(_TRIST2, "tristimulus2", 0, 0, 2,
        "2nd-4th harmonic energy now", "Pollard 1982"),
    _h3(_TRIST3, "tristimulus3", 0, 0, 2,
        "5th+ harmonic energy now", "Pollard 1982"),
    _h3(_PCE, "pitch_class_entropy", 0, 0, 2,
        "Pitch class entropy now", "Temperley 2007"),
    _h3(_PCE, "pitch_class_entropy", 3, 1, 2,
        "Pitch class entropy mean 23ms", "Temperley 2007"),
    _h3(_PITCHSAL, "pitch_salience", 0, 0, 2,
        "Pitch salience now", "Parncutt 1989"),
    _h3(_PITCHSAL, "pitch_salience", 3, 0, 2,
        "Pitch salience value 23ms", "Bidelman 2009"),
    _h3(_PITCHSAL, "pitch_salience", 6, 0, 2,
        "Pitch salience value 200ms", "Bidelman 2009"),
    _h3(_KEYCLAR, "key_clarity", 3, 0, 2,
        "Key clarity 23ms", "Krumhansl 1990"),
    _h3(_KEYCLAR, "key_clarity", 3, 1, 2,
        "Key clarity mean 23ms", "Krumhansl 1990"),
    _h3(_KEYCLAR, "key_clarity", 6, 0, 2,
        "Key clarity 200ms", "Krumhansl 1990"),
    _h3(_TONALSTAB, "tonal_stability", 3, 0, 2,
        "Tonal stability 23ms", "Bharucha 1987"),

    # === L0 Memory (17 tuples) ===
    _h3(_ROUGH, "roughness", 6, 18, 0,
        "Roughness trend 200ms (increasing/decreasing?)", "Plomp & Levelt 1965"),
    _h3(_ROUGH, "roughness", 12, 1, 0,
        "Roughness memory mean 525ms", "Sethares 1993"),
    _h3(_ROUGH, "roughness", 16, 1, 0,
        "Roughness memory mean 1s", "Sethares 1993"),
    _h3(_HELM, "helmholtz_kang", 12, 1, 0,
        "Helmholtz memory 525ms", "Helmholtz 1863"),
    _h3(_HELM, "helmholtz_kang", 18, 1, 0,
        "Helmholtz memory 2s", "Kang 2009"),
    _h3(_STUMP, "stumpf_fusion", 6, 1, 0,
        "Stumpf memory 200ms", "Stumpf 1890"),
    _h3(_STUMP, "stumpf_fusion", 16, 1, 0,
        "Stumpf memory 1s", "Stumpf 1890"),
    _h3(_INHARM, "inharmonicity", 3, 18, 0,
        "Inharmonicity trend 23ms", "McDermott 2010"),
    _h3(_INHARM, "inharmonicity", 12, 1, 0,
        "Inharmonicity memory 525ms", "McDermott 2010"),
    _h3(_HDEV, "harmonic_deviation", 3, 1, 0,
        "Harmonic deviation mean 23ms", "Bidelman 2013"),
    _h3(_HDEV, "harmonic_deviation", 12, 1, 0,
        "Harmonic deviation memory 525ms", "Bidelman 2013"),
    _h3(_PITCHSAL, "pitch_salience", 12, 1, 0,
        "Pitch salience memory 525ms", "Parncutt 1989"),
    _h3(_PITCHSAL, "pitch_salience", 18, 1, 0,
        "Pitch salience memory 2s", "Bidelman 2009"),
    _h3(_KEYCLAR, "key_clarity", 12, 1, 0,
        "Key clarity memory 525ms", "Krumhansl 1990"),
    _h3(_KEYCLAR, "key_clarity", 18, 1, 0,
        "Key clarity memory 2s", "Krumhansl 1990"),
    _h3(_TONALSTAB, "tonal_stability", 6, 1, 0,
        "Tonal stability memory 200ms", "Bharucha 1987"),
    _h3(_TONALSTAB, "tonal_stability", 18, 1, 0,
        "Tonal stability memory 2s", "Bharucha 1987"),

    # === L1 Prediction (12 tuples) ===
    _h3(_ROUGH, "roughness", 6, 1, 1,
        "Expected roughness 200ms ahead", "Plomp & Levelt 1965"),
    _h3(_ROUGH, "roughness", 12, 18, 1,
        "Roughness trend forward 525ms", "Sethares 1993"),
    _h3(_HELM, "helmholtz_kang", 6, 1, 1,
        "Expected consonance 200ms ahead", "Helmholtz 1863"),
    _h3(_HELM, "helmholtz_kang", 12, 1, 1,
        "Expected consonance 525ms ahead", "Kang 2009"),
    _h3(_STUMP, "stumpf_fusion", 6, 1, 1,
        "Expected fusion 200ms ahead", "Stumpf 1890"),
    _h3(_INHARM, "inharmonicity", 6, 18, 1,
        "Inharmonicity trend 200ms ahead", "McDermott 2010"),
    _h3(_PITCHSAL, "pitch_salience", 6, 1, 1,
        "Expected pitch salience 200ms", "Parncutt 1989"),
    _h3(_PITCHSAL, "pitch_salience", 12, 1, 1,
        "Expected pitch salience 525ms", "Bidelman 2009"),
    _h3(_KEYCLAR, "key_clarity", 6, 1, 1,
        "Expected key clarity 200ms", "Krumhansl 1990"),
    _h3(_KEYCLAR, "key_clarity", 16, 1, 1,
        "Expected key clarity 1s", "Krumhansl 1990"),
    _h3(_TONALSTAB, "tonal_stability", 6, 1, 1,
        "Expected tonal stability 200ms", "Bharucha 1987"),
    _h3(_TONALSTAB, "tonal_stability", 12, 1, 1,
        "Expected tonal stability 525ms", "Bharucha 1987"),
)

assert len(_BCH_H3_DEMANDS) == 48


class BCH(Relay):
    """Brainstem Consonance Hierarchy — SPU Relay (depth 0, 16D).

    Transforms raw R³/H³ into consonance representations following the
    brainstem auditory pathway.  First nucleus ever implemented.
    """

    NAME = "BCH"
    FULL_NAME = "Brainstem Consonance Hierarchy"
    UNIT = "SPU"
    FUNCTION = "F1"
    OUTPUT_DIM = 16

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:nps", "E1:harmonicity", "E2:hierarchy", "E3:ffr_behavior"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 8,
            ("M0:consonance_memory", "M1:pitch_memory",
             "M2:tonal_memory", "M3:spectral_memory"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 8, 12,
            ("P0:consonance_signal", "P1:template_match",
             "P2:neural_pitch", "P3:tonal_context"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 12, 16,
            ("F0:consonance_forecast", "F1:pitch_forecast",
             "F2:tonal_forecast", "F3:interval_forecast"),
            scope="external",
        ),
    )

    # ── Abstract property implementations ─────────────────────────────

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _BCH_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:nps", "E1:harmonicity", "E2:hierarchy", "E3:ffr_behavior",
            "M0:consonance_memory", "M1:pitch_memory",
            "M2:tonal_memory", "M3:spectral_memory",
            "P0:consonance_signal", "P1:template_match",
            "P2:neural_pitch", "P3:tonal_context",
            "F0:consonance_forecast", "F1:pitch_forecast",
            "F2:tonal_forecast", "F3:interval_forecast",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Brainstem pathway
            RegionLink("E0:nps", "IC", 0.80, "Bidelman 2009"),
            RegionLink("E1:harmonicity", "AN", 0.75, "Bidelman 2013"),
            RegionLink("E2:hierarchy", "AN", 0.70, "Bidelman & Heinz 2011"),
            RegionLink("E2:hierarchy", "IC", 0.65, "Bidelman & Heinz 2011"),
            RegionLink("E3:ffr_behavior", "IC", 0.60, "Bidelman 2009"),
            # Ascending to thalamus/cortex
            RegionLink("P0:consonance_signal", "MGB", 0.70, "Tramo 2001"),
            RegionLink("P0:consonance_signal", "A1_HG", 0.55, "Tramo 2001"),
            RegionLink("P0:consonance_signal", "STG", 0.50, "Tramo 2001"),
            RegionLink("P1:template_match", "IC", 0.65, "Bidelman 2013"),
            RegionLink("P1:template_match", "MGB", 0.55, "Tramo 2001"),
            RegionLink("P2:neural_pitch", "IC", 0.75, "Bidelman 2009"),
            RegionLink("P3:tonal_context", "MGB", 0.45, "Krumhansl 1990"),
            # Forecasts
            RegionLink("F0:consonance_forecast", "IC", 0.40, "Bidelman 2009"),
            RegionLink("F1:pitch_forecast", "IC", 0.40, "Bidelman 2009"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Consonance → serotonin baseline (tonal stability)
            NeuroLink("P0:consonance_signal", 3, "produce", 0.30,
                      "Blood & Zatorre 2001"),
            # Consonance surprise → weak dopamine
            NeuroLink("P0:consonance_signal", 0, "produce", 0.15,
                      "Salimpoor 2011"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Plomp", 1965, "Critical bandwidth roughness model",
                         "foundational"),
                Citation("Sethares", 1993, "Roughness from spectral peaks",
                         "foundational"),
                Citation("Helmholtz", 1863, "Integer ratio consonance theory",
                         "foundational"),
                Citation("Stumpf", 1890, "Tonal fusion theory",
                         "foundational"),
                Citation("Bidelman", 2009,
                         "FFR pitch salience correlates with consonance",
                         "r=0.81"),
                Citation("Bidelman", 2013,
                         "Harmonicity > roughness as consonance predictor",
                         "r=0.84"),
                Citation("Bidelman", 2011,
                         "AN population predicts hierarchy",
                         "6/6 ordering"),
                Citation("McDermott", 2010,
                         "Harmonicity preference = consonance preference",
                         "r=0.71"),
                Citation("Tramo", 2001,
                         "Brainstem-cortex consonance pathway",
                         "lesion study"),
                Citation("Krumhansl", 1990,
                         "Key profiles and tonal hierarchies",
                         "r=0.97"),
                Citation("Parncutt", 1989,
                         "Virtual pitch salience model",
                         "foundational"),
                Citation("Cousineau", 2015,
                         "FFR-behavior drops for natural stimuli",
                         "r=ns for natural"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.95),
            falsification_criteria=(
                "BCH hierarchy P1>P5>P4>M3>m6>TT should hold for synthetic "
                "tones; failure to reproduce = model invalid",
                "Consonance signal should correlate >0.70 with behavioral "
                "consonance ratings for synthetic dyads",
            ),
            version="1.0.0",
        )

    # ── Compute ───────────────────────────────────────────────────────

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R³/H³ into 16D consonance representation.

        Delegates to 4 layer functions (extraction → temporal_integration
        → cognitive_present → forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 16)`` — E(4) + M(4) + P(4) + F(4)
        """
        e = compute_extraction(r3_features)
        m = compute_temporal_integration(r3_features, h3_features)
        p = compute_cognitive_present(r3_features, h3_features, e)
        f = compute_forecast(r3_features, h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
