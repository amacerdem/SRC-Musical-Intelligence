"""STC -- Singing Training Connectivity.

Associator nucleus (depth 2) in MPU, Function F7. Models the
interoceptive-motor integration underlying singing training
connectivity. Singing uniquely engages respiratory control, vocal
production, and interoceptive monitoring in an integrated circuit.
Training enhances resting-state connectivity between insula and
speech/respiratory sensorimotor areas.

Core finding: Right anterior insula (AIC) shows expertise x anesthesia
dissociation (F = 22.08, Kleber 2013), confirming its role as the
interoceptive hub. Zamorano 2023: accumulated singing training predicts
enhanced resting-state connectivity.

Reads: MSR.training_level (P2, idx 7) -- sensorimotor expertise context
       SPMC.circuit_flow (M0, idx 3) -- hierarchical motor circuit state
Both are intra-unit (F7, MPU).

R3 Ontology Mapping (post-freeze 97D):
    amplitude:         [7]      (B, vocal intensity)
    loudness:          [8]      (B, respiratory amplitude / breath)
    warmth:            [12]     (C, singing resonance quality)
    tristimulus1:      [15]     (C, voice harmonic fundamental)
    x_l0l5:            [25:33]  (F, respiratory timing / breath-phrase)
    x_l4l5:            [33:41]  (G, interoceptive-motor / voice-body)

Output structure: E(3) + M(3) + P(2) + F(3) = 11D
  E-layer [0:3]   Extraction           (sigmoid)  scope=internal
  M-layer [3:6]   Temporal Integration (sigmoid)  scope=internal
  P-layer [6:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer [8:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/stc/
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
    3: "100ms",
    8: "500ms",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 14: "periodicity", 20: "entropy",
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


# -- 12 H3 Demand Specifications ----------------------------------------------
# E-layer: 11 tuples (interoceptive, respiratory, breath, vocal, harmonic)
# M-layer: 1 new tuple (amplitude mean at 500ms)
# P-layer: 0 new
# F-layer: 0 new (shared with E)
# Total unique: 12 tuples, all L2 (bidirectional)

_STC_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Interoceptive-Motor Extraction (11 tuples) ===
    # -- Interoceptive signal (x_l4l5, R3[33]) --
    _h3(33, "x_l4l5", 3, 0, 2,
        "Interoceptive signal 100ms — voice-body interaction value",
        "Kleber 2013"),
    _h3(33, "x_l4l5", 3, 2, 2,
        "Interoceptive variability 100ms — coupling fluctuation",
        "Zamorano 2023"),
    _h3(33, "x_l4l5", 8, 14, 2,
        "Interoceptive period 500ms — mid-scale monitoring rhythm",
        "Zamorano 2023"),
    _h3(33, "x_l4l5", 16, 14, 2,
        "Interoceptive period 1s — long-scale interoceptive regularity",
        "Zamorano 2023"),
    # -- Respiratory signal (x_l0l5, R3[25]) --
    _h3(25, "x_l0l5", 3, 0, 2,
        "Respiratory coupling 100ms — breath-phrase value",
        "Zarate 2008"),
    _h3(25, "x_l0l5", 8, 14, 2,
        "Respiratory period 500ms — mid-scale breath rhythm",
        "Tsunada 2024"),
    _h3(25, "x_l0l5", 16, 14, 2,
        "Respiratory period 1s — breath-phrase coupling regularity",
        "Tsunada 2024"),
    # -- Breath dynamics (loudness, R3[8]) --
    _h3(8, "loudness", 3, 0, 2,
        "Breath amplitude 100ms — respiratory amplitude proxy",
        "Zarate 2008"),
    _h3(8, "loudness", 3, 20, 2,
        "Breath entropy 100ms — breathing pattern uncertainty",
        "Tsunada 2024"),
    # -- Vocal signals --
    _h3(12, "warmth", 3, 0, 2,
        "Vocal warmth 100ms — laryngeal/articulatory motor output",
        "Kleber 2013"),
    _h3(15, "tristimulus1", 3, 0, 2,
        "Voice harmonic 100ms — fundamental energy proxy",
        "Criscuolo 2022"),

    # === M-layer: Temporal Integration (1 new tuple) ===
    _h3(7, "amplitude", 8, 1, 2,
        "Mean vocal intensity 500ms — temporal integration baseline",
        "Zamorano 2023"),
)

assert len(_STC_H3_DEMANDS) == 12


class STC(Associator):
    """Singing Training Connectivity -- MPU Associator (depth 2, 11D).

    Models the interoceptive-motor integration underlying singing training
    connectivity. Singing uniquely engages respiratory control, vocal
    production, and interoceptive monitoring in an integrated circuit.
    Training enhances resting-state connectivity between insula and
    speech/respiratory sensorimotor areas.

    Zamorano et al. (2023): Accumulated singing training hours predict
    enhanced resting-state functional connectivity between bilateral
    anterior insula and speech/respiratory sensorimotor areas, bilateral
    thalamus, and left putamen (rs-fMRI, N=40 singers + 40 controls).

    Kleber et al. (2013): Right anterior insula cortex (AIC) dissociates
    expertise and anesthesia (F = 22.08, MNI: 48, 0, -3). Vocal-fold
    topical anesthesia differentially modulates AIC in trained singers
    vs nonsingers (fMRI, N=18 singers + 18 nonsingers).

    Zarate & Bhatt (2010): Involuntary pitch correction in trained
    singers supports automatic interoceptive-motor loop. Singers show
    more precise and rapid pitch correction than nonsingers.

    Tsunada et al. (2024): Dual vocal suppression (phasic gating + tonic
    prediction) supports separate interoceptive and motor pathways
    during vocal production monitoring.

    Criscuolo et al. (2022): ALE meta-analysis of 84 studies (N=3,005)
    confirms coherent cortico-subcortical network in musicians, including
    enhanced volume in sensorimotor and interoceptive regions.

    Dependency chain:
        STC reads MSR (F7 intra-unit, depth 0) and SPMC (F7, depth 1).
        Computed after MSR and SPMC in the C3 scheduler.

    Downstream feeds:
        -> vocal_integration belief (Appraisal)
        -> singing_connectivity belief (Anticipation)
    """

    NAME = "STC"
    FULL_NAME = "Singing Training Connectivity"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("MSR", "SPMC")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:f28_interoceptive_coupling",
             "E1:f29_respiratory_integration",
             "E2:f30_speech_sensorimotor"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 6,
            ("M0:connectivity_strength",
             "M1:respiratory_index",
             "M2:voice_body_coupling"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 8,
            ("P0:insula_activity",
             "P1:vocal_motor"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:connectivity_pred",
             "F1:respiratory_pred",
             "F2:vocal_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _STC_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:f28_interoceptive_coupling",
            "E1:f29_respiratory_integration",
            "E2:f30_speech_sensorimotor",
            "M0:connectivity_strength",
            "M1:respiratory_index",
            "M2:voice_body_coupling",
            "P0:insula_activity",
            "P1:vocal_motor",
            "F0:connectivity_pred",
            "F1:respiratory_pred",
            "F2:vocal_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Right Anterior Insula — interoceptive hub
            RegionLink("E0:f28_interoceptive_coupling", "right_AIC", 0.90,
                        "Kleber 2013"),
            # ACC — compensatory vocal control network
            RegionLink("E1:f29_respiratory_integration", "ACC", 0.75,
                        "Zarate 2008"),
            # SMA / M1 — speech motor execution
            RegionLink("E2:f30_speech_sensorimotor", "SMA_M1", 0.80,
                        "Kleber 2013"),
            # Right AIC — connectivity dynamics
            RegionLink("M0:connectivity_strength", "right_AIC", 0.85,
                        "Zamorano 2023"),
            # Bilateral Thalamus — insula co-activation
            RegionLink("M2:voice_body_coupling", "bilateral_thalamus", 0.70,
                        "Zamorano 2023"),
            # S1 — somatosensory feedback for vocal control
            RegionLink("P0:insula_activity", "S1", 0.75,
                        "Kleber 2013"),
            # Left Putamen — motor sequencing for singing
            RegionLink("P1:vocal_motor", "left_putamen", 0.70,
                        "Zamorano 2023"),
            # Right AIC — connectivity prediction
            RegionLink("F0:connectivity_pred", "right_AIC", 0.65,
                        "Zamorano 2023"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # STC modulates via connectivity, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Zamorano et al.", 2023,
                         "Accumulated singing training hours predict "
                         "enhanced resting-state functional connectivity "
                         "between bilateral anterior insula and speech/"
                         "respiratory sensorimotor areas",
                         "rs-fMRI, N=40 singers + 40 controls"),
                Citation("Kleber et al.", 2013,
                         "Right anterior insula cortex dissociates "
                         "expertise and anesthesia (F = 22.08); vocal-fold "
                         "topical anesthesia differentially modulates AIC "
                         "in trained singers vs nonsingers",
                         "fMRI, N=18 singers + 18 nonsingers"),
                Citation("Zarate & Bhatt", 2010,
                         "Involuntary pitch correction in trained singers "
                         "supports automatic interoceptive-motor loop; "
                         "singers show more precise and rapid correction",
                         "behavioral + fMRI"),
                Citation("Zarate & Bhatt", 2008,
                         "ACC + pSTS + anterior insula network for "
                         "compensatory vocal control during pitch-shifted "
                         "auditory feedback",
                         "fMRI, N=14"),
                Citation("Tsunada et al.", 2024,
                         "Dual vocal suppression (phasic gating + tonic "
                         "prediction) supports separate interoceptive and "
                         "motor pathways during vocal production monitoring",
                         "electrophysiology, primate"),
                Citation("Criscuolo et al.", 2022,
                         "ALE meta-analysis of 84 studies (N=3,005) "
                         "confirms coherent cortico-subcortical network "
                         "in musicians including sensorimotor and "
                         "interoceptive regions",
                         "ALE meta-analysis, N=3005"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Interoceptive coupling (f28) must increase with "
                "interoceptive periodicity regularity at 1s; if irregular "
                "interoceptive signals produce high f28, the insula-"
                "sensorimotor connectivity model is invalid "
                "(Zamorano 2023: training -> regularity -> connectivity)",
                "Respiratory integration (f29) must reflect both "
                "periodicity and entropy; if removing breath entropy "
                "does not change f29, the dual pathway model is invalid "
                "(Tsunada 2024: phasic + tonic components)",
                "Speech sensorimotor (f30) must track vocal warmth; if "
                "warmth is replaced by non-vocal timbral features and "
                "f30 remains unchanged, the laryngeal motor proxy is "
                "invalid (Kleber 2013: vocal-fold anesthesia modulation)",
                "Connectivity strength (M0) must correlate with training "
                "level (MSR upstream); if MSR ablation does not affect "
                "STC outputs, the training-connectivity link is invalid",
                "Insula activity (P0) should be higher for vocal than "
                "non-vocal music; if the difference is not observed, the "
                "singing-specific connectivity model is falsified "
                "(Kleber 2013: expertise x anesthesia interaction F=22.08)",
                "Vocal prediction (F2) must use fast timescale (100ms) "
                "while connectivity/respiratory predictions use slow (1s); "
                "if exchanging timescales does not degrade predictions, "
                "the timescale separation is not supported",
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
        """Transform R3/H3 + upstream into 11D singing connectivity output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"MSR": (B, T, 11), "SPMC": (B, T, 11)}``

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
