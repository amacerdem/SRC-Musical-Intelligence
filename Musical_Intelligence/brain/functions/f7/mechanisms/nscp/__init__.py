"""NSCP -- Neural Synchrony Commercial Prediction.

Associator nucleus (depth 2) in MPU, Function F7. Models the pathway
from population-level neural synchrony (inter-subject correlation) to
commercial success prediction. ISC predicts streaming popularity
(R^2=0.619 combined model); 1% ISC increase corresponds to ~2.4M more
Spotify streams. Catchiness (groove/motor entrainment) drives repeated
listening via an inverted-U syncopation-groove relationship.

Core finding: ISC computed from EEG during music listening reliably
predicts commercial success. Neural synchrony captures shared brain
responses that drive population-level engagement. Leeuwis 2021:
R^2=0.619 combined model for predicting Spotify streams from ISC.

Reads: ASAP.motor_to_auditory (P0, idx 5) -- dorsal stream context
       DDSMI.music_entrainment (P1, idx 7) -- social motor integration

R3 Ontology Mapping (post-freeze 97D):
    stumpf:              [3]      (A, harmonic consonance)
    loudness:            [8]      (B, perceptual loudness)
    spectral_flux:       [10]     (B, onset detection)
    x_l0l5:              [25:33]  (F, cross-layer coherence)
    x_l4l5:              [33:41]  (G, multi-feature binding)

Output structure: E(3) + M(3) + P(2) + F(3) = 11D
  E-layer [0:3]   Extraction           (sigmoid)  scope=internal
  M-layer [3:6]   Temporal Integration (sigmoid)  scope=internal
  P-layer [6:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer [8:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/nscp/
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
    0: "25ms (instant)",
    1: "50ms (fast)",
    3: "100ms (local)",
    4: "125ms (short)",
    8: "500ms (phrase)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 14: "periodicity", 20: "entropy",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {2: "integration"}


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


# -- R3 feature names ---------------------------------------------------------
_STUMPF = "stumpf"
_LOUDNESS = "loudness"
_SPECTRAL_FLUX = "spectral_flux"
_X_L0L5 = "x_l0l5"
_X_L4L5 = "x_l4l5"


# -- 19 H3 Demand Specifications (5E + 3M + 6P + 5F) -------------------------
# All L2 (integration/bidirectional) -- ISC pathway operates on integrated
# temporal features across multiple horizons.
#
# E-layer: 5 tuples (coherence, consonance, binding, onset, loudness)
# M-layer: 3 tuples (coherence, binding 1s, binding 500ms)
# P-layer: 6 tuples (onset/coherence at 25ms, 50ms, 100ms)
# F-layer: 5 tuples (coherence, binding, onset at 1s + short-term)

_NSCP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Neural Synchrony Extraction (5 tuples) ===
    _h3(25, _X_L0L5, 16, 14, 2,
        "Coherence periodicity 1s for ISC proxy",
        "Leeuwis 2021"),
    _h3(3, _STUMPF, 3, 0, 2,
        "Consonance at 100ms for synchrony quality",
        "Sarasso 2019"),
    _h3(33, _X_L4L5, 16, 14, 2,
        "Binding periodicity 1s for commercial prediction",
        "Leeuwis 2021"),
    _h3(10, _SPECTRAL_FLUX, 16, 14, 2,
        "Onset periodicity 1s for catchiness",
        "Spiech 2022"),
    _h3(8, _LOUDNESS, 3, 20, 2,
        "Loudness entropy 100ms for engagement",
        "Spiech 2022"),

    # === M-layer: Temporal Integration (1 unique tuple) ===
    # Note: M reuses E#0 (25,16,14,2) and E#2 (33,16,14,2) — not repeated
    _h3(33, _X_L4L5, 8, 14, 2,
        "Binding periodicity 500ms for temporal integration",
        "Leeuwis 2021"),

    # === P-layer: Cognitive Present (6 tuples) ===
    _h3(10, _SPECTRAL_FLUX, 0, 0, 2,
        "Instantaneous onset 25ms for groove present state",
        "Spiech 2022"),
    _h3(10, _SPECTRAL_FLUX, 3, 0, 2,
        "Onset at 100ms for groove present state",
        "Spiech 2022"),
    _h3(25, _X_L0L5, 0, 0, 2,
        "Coherence at 25ms for coherence present state",
        "Hasson 2004"),
    _h3(25, _X_L0L5, 3, 0, 2,
        "Coherence at 100ms for coherence present state",
        "Hasson 2004"),
    _h3(10, _SPECTRAL_FLUX, 1, 1, 2,
        "Mean onset 50ms for groove smoothing",
        "Spiech 2022"),
    _h3(25, _X_L0L5, 1, 1, 2,
        "Mean coherence 50ms for coherence smoothing",
        "Leeuwis 2021"),

    # === F-layer: Forecast (2 unique tuples) ===
    # Note: F reuses E#0 (25,16,14,2), E#2 (33,16,14,2), E#4 (10,16,14,2)
    _h3(25, _X_L0L5, 4, 14, 2,
        "Coherence periodicity 125ms for short-term trend",
        "Leeuwis 2021"),
    _h3(10, _SPECTRAL_FLUX, 4, 2, 2,
        "Onset variability 125ms for catchiness stability",
        "Spiech 2022"),
)

assert len(_NSCP_H3_DEMANDS) == 14


class NSCP(Associator):
    """Neural Synchrony Commercial Prediction -- MPU Associator (depth 2, 11D).

    Models the pathway from population-level neural synchrony (inter-subject
    correlation) to commercial success prediction. ISC reliably predicts
    streaming popularity and catchiness drives repeated listening through
    motor entrainment.

    Leeuwis et al. (2021): Neural synchrony (ISC) predicts commercial
    success of songs. Combined early+late ISC model achieves R^2=0.619
    for predicting Spotify streams. 1% ISC increase ~ 2.4M more streams.
    (EEG, N=recordings).

    Berns et al. (2010): Neural activity in nucleus accumbens (NAcc) during
    music listening predicts future song sales (r=0.33). Adolescent neural
    responses predict population-level commercial outcomes.
    (fMRI, N=27 adolescents).

    Spiech et al. (2022): Pupil drift rate indexes groove perception with
    inverted-U syncopation relationship (F(1,29)=10.515, p=.003). Moderate
    rhythmic complexity maximizes motor entrainment.
    (pupillometry, N=30).

    Sarasso et al. (2019): Musical consonance enhances motor inhibition
    and aesthetic engagement (eta^2=0.685). Consonance modulates
    population-level motor responses.
    (TMS/EMG, N=36).

    Hasson et al. (2004): Inter-subject correlation in cortical responses
    during naturalistic stimuli is reliable and content-driven. ISC
    captures shared perceptual processing.
    (fMRI, N=5).

    Dependency chain:
        NSCP reads ASAP (F7 intra-unit, depth 1) and DDSMI (F7, depth 1).
        Computed after ASAP and DDSMI in the C3 scheduler.

    Downstream feeds:
        -> neural_synchrony belief (Appraisal)
        -> commercial_potential belief (Anticipation)
    """

    NAME = "NSCP"
    FULL_NAME = "Neural Synchrony Commercial Prediction"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("ASAP", "DDSMI")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:f22_neural_synchrony", "E1:f23_commercial_prediction",
             "E2:f24_catchiness_index"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 6,
            ("M0:isc_magnitude", "M1:sync_consistency",
             "M2:popularity_estimate"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 8,
            ("P0:coherence_level", "P1:groove_response"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:synchrony_pred", "F1:popularity_pred",
             "F2:catchiness_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _NSCP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:f22_neural_synchrony", "E1:f23_commercial_prediction",
            "E2:f24_catchiness_index",
            "M0:isc_magnitude", "M1:sync_consistency",
            "M2:popularity_estimate",
            "P0:coherence_level", "P1:groove_response",
            "F0:synchrony_pred", "F1:popularity_pred",
            "F2:catchiness_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Frontocentral cortex -- strongest ISC effects
            RegionLink("E0:f22_neural_synchrony", "frontocentral_cortex",
                       0.85, "Leeuwis 2021"),
            # Temporal cortex -- ISC during naturalistic listening
            RegionLink("P0:coherence_level", "temporal_cortex", 0.80,
                       "Hasson 2004"),
            # NAcc -- predicts future sales
            RegionLink("E1:f23_commercial_prediction", "NAcc", 0.75,
                       "Berns 2010"),
            # Motor cortex -- groove/motor entrainment
            RegionLink("P1:groove_response", "motor_cortex", 0.80,
                       "Sarasso 2019"),
            # Frontocentral -- ISC magnitude
            RegionLink("M0:isc_magnitude", "frontocentral_cortex", 0.80,
                       "Leeuwis 2021"),
            # NAcc -- popularity estimate
            RegionLink("M2:popularity_estimate", "NAcc", 0.70,
                       "Berns 2010"),
            # Motor cortex -- catchiness prediction
            RegionLink("F2:catchiness_pred", "motor_cortex", 0.65,
                       "Spiech 2022"),
            # Frontocentral -- synchrony prediction
            RegionLink("F0:synchrony_pred", "frontocentral_cortex", 0.70,
                       "Leeuwis 2021"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # NSCP operates via ISC pathway, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Leeuwis et al.", 2021,
                         "Neural synchrony (ISC) predicts commercial success "
                         "of songs. Combined early+late ISC model achieves "
                         "R^2=0.619 for predicting Spotify streams. 1% ISC "
                         "increase corresponds to ~2.4M more streams",
                         "EEG, N=recordings"),
                Citation("Berns et al.", 2010,
                         "Neural activity in nucleus accumbens (NAcc) during "
                         "music listening predicts future song sales (r=0.33). "
                         "Adolescent neural responses predict population-level "
                         "commercial outcomes",
                         "fMRI, N=27 adolescents"),
                Citation("Spiech et al.", 2022,
                         "Pupil drift rate indexes groove perception with "
                         "inverted-U syncopation relationship "
                         "(F(1,29)=10.515, p=.003). Moderate rhythmic "
                         "complexity maximizes motor entrainment",
                         "pupillometry, N=30"),
                Citation("Sarasso et al.", 2019,
                         "Musical consonance enhances motor inhibition and "
                         "aesthetic engagement (eta^2=0.685). Consonance "
                         "modulates population-level motor responses",
                         "TMS/EMG, N=36"),
                Citation("Hasson et al.", 2004,
                         "Inter-subject correlation in cortical responses "
                         "during naturalistic stimuli is reliable and "
                         "content-driven. ISC captures shared perceptual "
                         "processing",
                         "fMRI, N=5"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Neural synchrony (E0) must increase with cross-layer "
                "coherence periodicity; if disrupting coherence does not "
                "reduce E0, the ISC proxy model is invalid (Leeuwis 2021)",
                "Commercial prediction (E1) must correlate with ISC magnitude "
                "(E0); if high ISC does not predict high E1, the ISC-to-"
                "streams pathway is invalid (Leeuwis 2021: R^2=0.619)",
                "Catchiness index (E2) should show inverted-U with rhythmic "
                "complexity; extreme regularity or irregularity should both "
                "reduce E2 (Spiech 2022: F(1,29)=10.515)",
                "Sync consistency (M1) must be high when ISC is temporally "
                "stable; transient ISC spikes without consistency should not "
                "predict commercial success (Leeuwis 2021: R^2 drop 0.011)",
                "Groove response (P1) must increase with onset regularity at "
                "short timescales; removing onset tracking should eliminate "
                "groove signal (Spiech 2022: pupil drift rate)",
                "Popularity prediction (F1) must improve with binding "
                "periodicity; if multi-feature binding does not enhance "
                "prediction, the binding-ISC link is invalid (testable via "
                "ablation of x_l4l5 periodicity input)",
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
        """Transform R3/H3 + upstream into 11D ISC-commercial output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"ASAP": (B, T, 11), "DDSMI": (B, T, 11)}``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(2) + F(3)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        m = compute_temporal_integration(
            h3_features, r3_features, e, upstream_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
