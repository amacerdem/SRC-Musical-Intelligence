"""PMIM -- Predictive Memory Integration Model.

Encoder nucleus (depth 1) in IMU, Function F4. Models how the brain
integrates ERAN (long-term syntax violation) and MMN (short-term deviance
detection) prediction-error signals to drive predictive memory updating.

Reads: PNH.ratio_encoding (intra-F4 dependency via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, sensory dissonance)
    stumpf_fusion:          [3]      (A, tonal coherence)
    sensory_pleasantness:   [4]      (A, consonance)
    inharmonicity:          [5]      (A, ratio deviation)
    onset_strength:         [11]     (B, event salience)
    tonalness:              [14]     (C, harmonic purity)
    spectral_flux:          [21]     (D, change magnitude)
    entropy:                [22]     (D, unpredictability)
    x_l0l5:                 [25:33]  (F, sensory-level coupling)
    x_l5l7:                 [41:49]  (G, high-level syntax coupling)

Output structure: P(3) + M(3) + S(3) + F(2) = 11D
  P-layer [0:3]  Prediction   (sigmoid)  scope=internal
  M-layer [3:6]  Mathematical (sigmoid)  scope=internal
  S-layer [6:9]  State        (sigmoid)  scope=hybrid
  F-layer [9:11] Forecast     (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pmim/
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
    10: "400ms (chord)",
    14: "700ms (progression)",
    18: "2s (phrase)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    13: "entropy", 14: "periodicity", 18: "trend", 19: "stability",
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
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_INHARMONICITY = 5
_LOUDNESS = 10             # loudness proxy (onset_strength)
_ONSET_STRENGTH = 11
_TONALNESS = 14
_SPECTRAL_FLUX = 21
_ENTROPY = 22


# -- 18 H3 Demand Specifications -----------------------------------------------
# Predictive memory integration requires multi-scale prediction error
# (ERAN/MMN), precision estimation, and temporal trajectories.

_PMIM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === P-layer: Prediction Features (8 tuples) ===
    _h3(_ROUGHNESS, "roughness", 10, 0, 2,
        "Current dissonance at chord level (400ms)",
        "Koelsch 2000"),
    _h3(_ROUGHNESS, "roughness", 14, 1, 0,
        "Average dissonance over progression (700ms)",
        "Koelsch 2000"),
    _h3(_INHARMONICITY, "inharmonicity", 10, 0, 2,
        "Current ratio deviation at chord level",
        "Koelsch 2000"),
    _h3(_INHARMONICITY, "inharmonicity", 14, 8, 0,
        "Rate of complexity change over progression",
        "Wagner 2018"),
    _h3(_ENTROPY, "entropy", 10, 0, 2,
        "Current unpredictability at chord level",
        "Bonetti 2024"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 10, 0, 2,
        "Current change magnitude at chord level",
        "Wagner 2018"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 14, 8, 0,
        "Acceleration of change over progression",
        "Wagner 2018"),
    _h3(_ONSET_STRENGTH, "onset_strength", 10, 0, 2,
        "Onset salience for MMN triggering",
        "Bonetti 2024"),

    # === M-layer: Temporal Integration (7 tuples) ===
    _h3(_ENTROPY, "entropy", 14, 1, 0,
        "Average complexity over progression (700ms)",
        "Cheung 2019"),
    _h3(_ENTROPY, "entropy", 18, 13, 0,
        "Higher-order unpredictability over phrase (2s)",
        "Cheung 2019"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 10, 0, 2,
        "Fusion state at chord level for precision",
        "Gold 2019"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 14, 14, 0,
        "Cadential regularity proxy over progression",
        "Gold 2019"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 10, 0, 2,
        "Current consonance for precision",
        "Gold 2019"),
    _h3(_TONALNESS, "tonalness", 10, 0, 2,
        "Harmonic purity for precision",
        "Friston 2005"),
    _h3(_TONALNESS, "tonalness", 14, 18, 0,
        "Tonal trend over progression",
        "Koelsch 2014"),

    # === S-layer: Cognitive Present (3 tuples) ===
    _h3(_ROUGHNESS, "roughness", 18, 18, 0,
        "Dissonance trajectory over phrase (2s) -- syntax context",
        "Koelsch 2009"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 18, 19, 0,
        "Consonance stability over phrase -- syntax stability",
        "Fong 2020"),
    _h3(_LOUDNESS, "loudness", 10, 0, 2,
        "Current intensity for PE weighting at chord level",
        "Bonetti 2024"),

    # Note: F-layer reuses (0,18,18,0), (21,14,8,0), (14,14,18,0)
    # from P/M/S layers -- no additional unique tuples.
)

assert len(_PMIM_H3_DEMANDS) == 18


class PMIM(Encoder):
    """Predictive Memory Integration Model -- IMU Encoder (depth 1, 11D).

    Models how the brain integrates ERAN (early right anterior negativity)
    and MMN (mismatch negativity) prediction-error signals to drive
    predictive memory updating. ERAN detects long-term harmonic syntax
    violations via IFG (Broca's area), while MMN detects short-term
    deviance via STG echoic memory. Their convergence in IFG produces
    hierarchical prediction errors that drive Bayesian model updating
    in hippocampus and ACC.

    Koelsch et al. 2000: ERAN elicited by Neapolitan sixth chords,
    peak 150-180 ms, right-frontal maximum (EEG N=24, p<0.001).

    Wagner et al. 2018: MMN for harmonic interval deviants;
    consonance-dissonance asymmetry (EEG N=15).

    Bonetti et al. 2024: Hierarchical PE from auditory cortex to
    hippocampus to ACC (MEG N=83, p<0.001).

    Dependency chain:
        PMIM is an Encoder (Depth 1) -- reads PNH relay output.
        Computed after PNH in F4 pipeline.

    Downstream feeds:
        -> memory_update beliefs (Core)
        -> prediction_confidence beliefs (Appraisal)
        -> syntax_processing context for F4 integrators
    """

    NAME = "PMIM"
    FULL_NAME = "Predictive Memory Integration Model"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("PNH",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "P", "Prediction", 0, 3,
            ("P0:eran_response", "P1:mmn_response",
             "P2:combined_pred_error"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Mathematical", 3, 6,
            ("M0:hierarchical_pe", "M1:model_precision",
             "M2:from_synthesis"),
            scope="internal",
        ),
        LayerSpec(
            "S", "State", 6, 9,
            ("S0:syntax_state", "S1:deviance_state",
             "S2:memory_update"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:eran_forecast_fc", "F1:mmn_forecast_fc"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PMIM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "P0:eran_response", "P1:mmn_response",
            "P2:combined_pred_error",
            "M0:hierarchical_pe", "M1:model_precision",
            "M2:from_synthesis",
            "S0:syntax_state", "S1:deviance_state",
            "S2:memory_update",
            "F0:eran_forecast_fc", "F1:mmn_forecast_fc",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # IFG (BA44) -- ERAN + MMN shared generator
            RegionLink("P0:eran_response", "IFG", 0.85,
                       "Koelsch 2000"),
            # STG -- echoic mismatch / MMN generator
            RegionLink("P1:mmn_response", "STG", 0.80,
                       "Wagner 2018"),
            # Hippocampus -- memory updating from hierarchical PE
            RegionLink("S2:memory_update", "Hippocampus", 0.75,
                       "Bonetti 2024"),
            # ACC/MCC -- prediction error monitoring
            RegionLink("P2:combined_pred_error", "ACC", 0.70,
                       "Bonetti 2024"),
            # Auditory Cortex -- sensory prediction mismatch
            RegionLink("S1:deviance_state", "AC", 0.65,
                       "Fong 2020"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # PMIM operates on cortical prediction error, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Koelsch et al.", 2000,
                         "ERAN elicited by Neapolitan sixth chords, peak "
                         "150-180 ms, right-frontal maximum; long-term "
                         "harmonic syntax violation signal in IFG",
                         "EEG, N=24"),
                Citation("Wagner et al.", 2018,
                         "MMN for harmonic interval deviants; "
                         "consonance-dissonance asymmetry in echoic "
                         "mismatch detection",
                         "EEG, N=15"),
                Citation("Bonetti et al.", 2024,
                         "Hierarchical PE from auditory cortex to "
                         "hippocampus to ACC/MCC; feedforward prediction "
                         "error drives memory updating",
                         "MEG, N=83"),
                Citation("Cheung et al.", 2019,
                         "Uncertainty x surprise interaction predicts "
                         "musical pleasure; amygdala/hippocampus "
                         "beta=-0.140 (corrected p=0.002)",
                         "fMRI, N=40"),
                Citation("Gold et al.", 2019,
                         "Inverted-U preference for intermediate "
                         "predictive complexity; quadratic IC and "
                         "entropy effects on liking",
                         "behavioral, N=70"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.85),
            falsification_criteria=(
                "ERAN response (P0) must be larger for Neapolitan sixth "
                "chords than in-key chords (Koelsch 2000: p<0.001)",
                "MMN response (P1) must scale with degree of harmonic "
                "deviance (Wagner 2018: consonance-dissonance asymmetry)",
                "Hierarchical PE (M0) must correlate with hippocampal "
                "activation (Bonetti 2024: MEG N=83)",
                "Memory update (S2) should be highest for surprising "
                "events in novel contexts (Bayesian updating rule)",
                "Model precision (M1) should increase with stimulus "
                "regularity and decrease with novel modulations",
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
        """Transform R3/H3 + PNH relay output into 11D predictive memory signal.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"PNH": (B, T, 11)}``

        Returns:
            ``(B, T, 11)`` -- P(3) + M(3) + S(3) + F(2)
        """
        p = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(h3_features, r3_features, p)
        s = compute_cognitive_present(h3_features, r3_features, p, m)
        f = compute_forecast(h3_features, p, s)

        output = torch.stack([*p, *m, *s, *f], dim=-1)
        return output.clamp(0.0, 1.0)
