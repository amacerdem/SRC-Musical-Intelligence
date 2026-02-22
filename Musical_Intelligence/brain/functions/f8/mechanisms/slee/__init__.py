"""SLEE -- Synaptic Long-term Encoding Engine.

Encoder nucleus (depth 1) in NDU, Function F8. Models the statistical
learning expertise enhancement system, capturing how repeated exposure to
auditory regularities builds internal distribution representations, how
expertise sharpens irregularity detection, and how multisensory integration
supports cross-modal binding in musical contexts.

Reads: EDNR (intra-circuit via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    velocity_A:                 [7]      (A, amplitude / dynamic envelope)
    velocity_D:                 [8]      (B, loudness / perceptual weight)
    onset_strength:             [10]     (B, spectral change rate)
    brightness_kuttruff:        [14]     (C, tonalness)
    spectral_flux:              [21]     (D, spectral change)
    pitch_change:               [23]     (D, pitch dynamics)
    pitch_stability:            [24]     (D, pitch regularity)
    x_l4l5:                     [33:41]  (G, pattern-feature binding)
    x_l5l6:                     [41:49]  (H, multi-feature coherence)

Output structure: E(4) + M(3) + P(3) + F(3) = 13D
  E-layer   [0:4]   Extraction           (sigmoid)  scope=internal
  M-layer   [4:7]   Temporal Integration (sigmoid)  scope=internal
  P-layer   [7:10]  Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [10:13] Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/slee/
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
    0: "25ms (instant)",
    3: "100ms (alpha)",
    4: "125ms (beta-fast)",
    8: "500ms (phrase)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 5: "range",
    18: "trend", 20: "entropy",
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


# -- R3 feature name constants ------------------------------------------------
_AMPLITUDE = 7           # velocity_A
_LOUDNESS = 8            # velocity_D
_ONSET_STRENGTH = 10     # spectral_flux / onset_strength
_SPECTRAL_FLUX = 21      # spectral_change / spectral_flux
_PITCH_CHANGE = 23
_PITCH_STABILITY = 24
_X_L4L5_0 = 33
_X_L5L6_0 = 41


# -- 18 H3 Demand Specifications -----------------------------------------------
# Statistical Learning Expertise Enhancement requires multi-scale temporal
# features spanning instant (25ms) through 1s for statistical model building,
# irregularity detection, multisensory integration, and expertise-dependent
# enhancement. E(7) + M(3) + P(4) + F(4) = 18 unique tuples.

_SLEE_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Statistical Learning Extraction (7 tuples) ===
    # 0: Mean loudness 100ms -- distribution model building
    _h3(8, "velocity_D", 3, 1, 2,
        "Mean loudness 100ms for statistical model estimation",
        "Paraskevopoulos 2022"),
    # 1: Amplitude entropy 100ms -- variability of acoustic intensity
    _h3(7, "velocity_A", 3, 20, 2,
        "Amplitude entropy 100ms for distribution model",
        "Carbajal & Malmierca 2018"),
    # 2: Spectral flux variability 100ms -- irregularity detection
    _h3(10, "onset_strength", 3, 2, 2,
        "Spectral flux variability 100ms for detection accuracy",
        "Paraskevopoulos 2022"),
    # 3: Mean spectral flux over 1s -- sustained irregularity baseline
    _h3(10, "onset_strength", 16, 1, 2,
        "Mean spectral flux over 1s for irregularity baseline",
        "Bridwell 2017"),
    # 4: Cross-modal binding 100ms -- multisensory integration
    _h3(41, "x_l5l6", 3, 0, 2,
        "Cross-modal binding at 100ms for multisensory integration",
        "Paraskevopoulos 2022"),
    # 5: Mean binding over 1s -- sustained binding strength
    _h3(41, "x_l5l6", 16, 1, 2,
        "Mean binding over 1s for sustained integration",
        "Porfyri 2025"),
    # 6: Instantaneous irregularity 25ms -- rapid detection signal
    _h3(10, "onset_strength", 0, 0, 2,
        "Instantaneous irregularity 25ms for expertise gating",
        "Bridwell 2017"),

    # === M-Layer: Temporal Integration (3 tuples) ===
    # 7: Pitch stability 100ms -- pattern memory input
    _h3(24, "pitch_stability", 3, 0, 2,
        "Pitch stability 100ms for pattern memory accumulation",
        "Billig 2022"),
    # 8: Stability variability 1s -- memory dynamics
    _h3(24, "pitch_stability", 16, 2, 2,
        "Stability variability 1s for memory dynamics",
        "Billig 2022"),
    # 9: Pattern binding trend 1s -- expertise consolidation proxy
    _h3(33, "x_l4l5", 16, 18, 0,
        "Pattern binding trend over 1s for expertise state",
        "Doelling & Poeppel 2015"),

    # === P-Layer: Cognitive Present (4 tuples) ===
    # 10: Spectral change 100ms -- boundary detection
    _h3(21, "spectral_flux", 3, 0, 2,
        "Spectral change 100ms for pattern segmentation",
        "Bridwell 2017"),
    # 11: Spectral trend 125ms -- boundary direction
    _h3(21, "spectral_flux", 4, 18, 0,
        "Spectral trend 125ms for boundary direction detection",
        "Bridwell 2017"),
    # 12: Pitch change 100ms -- segmentation signal
    _h3(23, "pitch_change", 3, 0, 2,
        "Pitch change 100ms for sequence segmentation",
        "Bridwell 2017"),
    # 13: Mean pitch change 1s -- regularity baseline
    _h3(23, "pitch_change", 16, 1, 2,
        "Mean pitch change 1s for regularity baseline",
        "Fong 2020"),

    # === F-Layer: Forecast (4 tuples) ===
    # 14: Amplitude at 100ms -- attention-based prediction scaling
    _h3(7, "velocity_A", 3, 0, 2,
        "Amplitude at 100ms for detection context",
        "Paraskevopoulos 2022"),
    # 15: Loudness range 500ms -- dynamic range prediction
    _h3(8, "velocity_D", 8, 5, 0,
        "Loudness range 500ms for prediction scaling",
        "Bridwell 2017"),
    # 16: Pattern coupling 100ms -- continuation assessment
    _h3(33, "x_l4l5", 3, 0, 2,
        "Pattern coupling 100ms for continuation estimate",
        "Doelling & Poeppel 2015"),
    # 17: Binding variability 100ms -- prediction uncertainty
    _h3(41, "x_l5l6", 3, 2, 2,
        "Binding variability 100ms for prediction uncertainty",
        "Porfyri 2025"),
)

assert len(_SLEE_H3_DEMANDS) == 18


class SLEE(Encoder):
    """Synaptic Long-term Encoding Engine -- NDU Encoder (depth 1, 13D).

    Models the statistical learning expertise enhancement system. Repeated
    exposure to auditory regularities builds internal distribution
    representations (E-layer), expertise sharpens irregularity detection
    (M-layer), and multisensory integration supports cross-modal binding
    (P-layer). Forward predictions anticipate upcoming events and detection
    performance (F-layer).

    Paraskevopoulos et al. 2022: musicians show enhanced statistical learning
    accuracy (Hedges' g = -1.09); network compartmentalization with 106
    within-network edges (M) vs 192 (NM), p < 0.001 FDR. IFG area 47m
    left is the primary supramodal hub across 5/6 network states.

    Carbajal & Malmierca 2018: predictive coding hierarchy from SSA to MMN
    to deviance detection in the auditory system.

    Bridwell et al. 2017: 45% amplitude reduction for patterned vs random
    sequences; cortical sensitivity to guitar note patterns at 4 Hz.

    Billig et al. 2022: hippocampus supports sequence binding and statistical
    learning memory.

    Doelling & Poeppel 2015: years of musical training correlate with
    entrainment strength (phase-locking value, PLV).

    Fong et al. 2020: MMN as prediction error under Bayesian framework
    with hierarchical processing.

    Porfyri et al. 2025: multisensory training improves audiovisual
    incongruency detection (eta-squared = 0.168). Left MFG, IFS, and
    insula show greatest effective connectivity reorganization.

    Dependency chain:
        SLEE is an Encoder (Depth 1) -- reads EDNR relay output
        (F8 intra-circuit). Computed after EDNR in F8 pipeline.

    Downstream feeds:
        -> statistical_model belief (Core/Appraisal)
        -> multisensory_binding belief (Appraisal)
        -> expertise_level belief (Appraisal)
    """

    NAME = "SLEE"
    FULL_NAME = "Synaptic Long-term Encoding Engine"
    UNIT = "NDU"
    FUNCTION = "F8"
    OUTPUT_DIM = 13
    UPSTREAM_READS = ("EDNR",)

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:statistical_model", "f02:detection_accuracy",
             "f03:multisensory_integration", "f04:expertise_advantage"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 4, 7,
            ("M0:exposure_model", "M1:pattern_memory",
             "M2:expertise_state"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 7, 10,
            ("P0:expectation_formation", "P1:cross_modal_binding",
             "P2:pattern_segmentation"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 10, 13,
            ("F0:next_probability", "F1:regularity_continuation",
             "F2:detection_predict"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SLEE_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:statistical_model", "f02:detection_accuracy",
            "f03:multisensory_integration", "f04:expertise_advantage",
            "M0:exposure_model", "M1:pattern_memory",
            "M2:expertise_state",
            "P0:expectation_formation", "P1:cross_modal_binding",
            "P2:pattern_segmentation",
            "F0:next_probability", "F1:regularity_continuation",
            "F2:detection_predict",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # IFG -- supramodal hub for multisensory integration
            RegionLink("f03:multisensory_integration", "IFG", 0.85,
                       "Paraskevopoulos 2022"),
            # Hippocampus -- sequence binding and statistical learning memory
            RegionLink("M1:pattern_memory", "hippocampus", 0.80,
                       "Billig 2022"),
            # A1 -- statistical model and expectation formation
            RegionLink("P0:expectation_formation", "A1", 0.75,
                       "Carbajal & Malmierca 2018"),
            # STG -- irregularity detection and pattern segmentation
            RegionLink("P2:pattern_segmentation", "STG", 0.75,
                       "Bridwell 2017"),
            # MFG -- multisensory effective connectivity reorganization
            RegionLink("P1:cross_modal_binding", "MFG", 0.70,
                       "Porfyri 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Acetylcholine -- attention-dependent statistical learning
            NeuroLink("f02:detection_accuracy", "acetylcholine", 0.70,
                      "Paraskevopoulos 2022"),
            # Dopamine -- expertise-driven prediction accuracy
            NeuroLink("F0:next_probability", "dopamine", 0.65,
                      "Carbajal & Malmierca 2018"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Paraskevopoulos et al.", 2022,
                         "Musicians show enhanced statistical learning "
                         "accuracy (Hedges' g = -1.09). Network "
                         "compartmentalization: 106 within-network edges (M) "
                         "vs 192 (NM), p < 0.001 FDR. IFG area 47m left is "
                         "the primary supramodal hub across 5/6 network states",
                         "fMRI/MEG, N=24+24"),
                Citation("Carbajal & Malmierca", 2018,
                         "Predictive coding hierarchy from SSA to MMN to "
                         "deviance detection in the auditory system",
                         "review"),
                Citation("Bridwell et al.", 2017,
                         "45% amplitude reduction for patterned vs random "
                         "sequences. Cortical sensitivity to guitar note "
                         "patterns at 4 Hz frequency tagging",
                         "EEG, N=20"),
                Citation("Billig et al.", 2022,
                         "Hippocampus supports sequence binding and "
                         "statistical learning memory",
                         "fMRI, N=25"),
                Citation("Doelling & Poeppel", 2015,
                         "Years of musical training correlate with "
                         "entrainment strength (phase-locking value, PLV)",
                         "MEG, N=12+12"),
                Citation("Fong et al.", 2020,
                         "MMN as prediction error under Bayesian framework "
                         "with hierarchical processing",
                         "EEG/theory"),
                Citation("Porfyri et al.", 2025,
                         "Multisensory training improves audiovisual "
                         "incongruency detection (eta-squared = 0.168). "
                         "Left MFG, IFS, insula show greatest effective "
                         "connectivity reorganization",
                         "fMRI, N=30"),
            ),
            evidence_tier="beta",
            confidence_range=(0.60, 0.85),
            falsification_criteria=(
                "Statistical model (f01) must strengthen with repeated "
                "exposure to auditory regularities; if no accumulation "
                "over session, model is invalid "
                "(Carbajal & Malmierca 2018)",
                "Detection accuracy (f02) must be higher for musicians "
                "than non-musicians; if no expertise effect, "
                "Paraskevopoulos 2022 finding (g = -1.09) is not captured",
                "Multisensory integration (f03) must correlate with IFG "
                "BOLD signal; if no IFG activation for cross-modal "
                "binding, Paraskevopoulos 2022 supramodal hub is invalid",
                "Pattern memory (M1) must show hippocampal engagement "
                "during sequence learning; if no hippocampal correlation, "
                "Billig 2022 binding mechanism is unsupported",
                "Pattern segmentation (P2) must distinguish patterned "
                "from random sequences with >45% amplitude difference; "
                "if difference is smaller, Bridwell 2017 is not replicated",
                "Expertise state (M2) must correlate with years of musical "
                "training; if no training-dependent trend, Doelling & "
                "Poeppel 2015 PLV finding is not captured",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        relay_outputs: Dict[str, Tensor] | None = None,
    ) -> Tensor:
        """Transform R3/H3 + EDNR relay output into 13D statistical learning.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"EDNR": (B, T, 10)}``

        Returns:
            ``(B, T, 13)`` -- E(4) + M(3) + P(3) + F(3)
        """
        relay_outputs = relay_outputs or {}
        B, T = r3_features.shape[:2]
        device = r3_features.device
        ednr = relay_outputs.get(
            "EDNR", torch.zeros(B, T, 10, device=device),
        )

        e = compute_extraction(h3_features, r3_features, ednr)
        m = compute_temporal_integration(h3_features, r3_features, e, ednr)
        p = compute_cognitive_present(h3_features, r3_features, e, m, ednr)
        f = compute_forecast(h3_features, e, m, p, ednr)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
