"""RIRI -- RAS-Intelligent Rehabilitation Integration.

Encoder nucleus (depth 1) in IMU, Function F4.  Models how multi-modal
rhythmic auditory stimulation (RAS) drives motor optimization through
convergent temporal input across auditory, visual-VR, and haptic-robotic
modalities.  Integration synergy (multi > unimodal) is captured via
geometric mean gating across E-layer pathways.

Reads: RASN, MEAMN, MMP, HCMC (4 intra-unit deps via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    sensory_pleasantness:  [4]       (A, motor valence proxy)
    amplitude:             [7]       (A, velocity_A)
    loudness:              [8]       (A, velocity_D)
    spectral_flux:         [10]      (B, onset_strength proxy)
    onset_strength:        [11]      (B, event salience)
    warmth:                [12]      (C, therapeutic comfort)
    tonalness:             [14]      (C, brightness_kuttruff)
    spectral_change:       [21]      (D, spectral_flux)
    energy_change:         [22]      (D, dynamic change)
    pitch_change:          [23]      (D, melodic guidance)
    x_l0l5:                [25:33]   (F, auditory-motor coupling / RAS)
    x_l4l5:                [33:41]   (F, sensorimotor integration)
    x_l5l7:                [41:49]   (G, connectivity coupling)

Output structure: E(3) + M(2) + P(2) + F(3) = 10D
  E-layer [0:3]  Extraction    (sigmoid)  scope=internal
  M-layer [3:5]  Model         (geomean/sigmoid)  scope=internal
  P-layer [5:7]  Present       (sigmoid)  scope=hybrid
  F-layer [7:10] Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/riri/
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
    11: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity", 14: "periodicity",
    17: "peaks", 18: "trend", 19: "stability",
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
_SENSORY_PLEASANT = 4     # sensory_pleasantness (A group)
_AMPLITUDE = 7             # amplitude / velocity_A (A group)
_LOUDNESS = 8              # loudness / velocity_D (A group)
_SPECTRAL_FLUX = 10        # spectral_flux (B group)
_ONSET_STRENGTH = 11       # onset_strength (B group)
_WARMTH = 12               # warmth (C group)
_TONALNESS = 14            # tonalness / brightness_kuttruff (C group)
_SPECTRAL_CHANGE = 21      # spectral_change (D group)
_ENERGY_CHANGE = 22        # energy_change (D group)
_PITCH_CHANGE = 23         # pitch_change (D group)
_X_L0L5_START = 25         # x_l0l5 start (F group, 8D)
_X_L4L5_START = 33         # x_l4l5 start (F group, 8D)
_X_L5L7_START = 41         # x_l5l7 start (G group, 8D)


# -- 16 H3 Demand Specifications -----------------------------------------------
# Multi-modal rehabilitation integration requires entrainment coupling (beat),
# sensorimotor coupling (motor window), and connectivity (long horizon).
# Tuples ordered by layer: E(11) + M(2 new, 1 shared) + P(4, 3 shared) + F(4, 2 shared) = 16 unique.

_RIRI_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Multi-modal Entrainment & Integration (11 tuples) ===

    # Beat-level entrainment (H6 = 200ms)
    _h3(_SPECTRAL_FLUX, "spectral_flux", 6, 0, 0,
        "Onset detection at beat level -- RAS trigger",
        "Thaut 2015"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 6, 17, 0,
        "Beat count per 200ms window -- rhythmic density",
        "Thaut 2015"),
    _h3(_ONSET_STRENGTH, "onset_strength", 6, 0, 0,
        "Event onset precision -- beat salience",
        "Harrison 2025"),
    _h3(_ONSET_STRENGTH, "onset_strength", 6, 14, 2,
        "Rhythmic regularity at beat level -- entrainment quality",
        "Ross 2022"),
    _h3(_X_L0L5_START, "x_l0l5", 6, 0, 2,
        "Entrainment coupling signal at beat level",
        "Thaut 2015"),

    # Motor window (H11 = 500ms)
    _h3(_LOUDNESS, "loudness", 11, 1, 0,
        "Mean loudness over motor window -- drive intensity",
        "Harrison 2025"),
    _h3(_X_L4L5_START, "x_l4l5", 11, 0, 2,
        "Sensorimotor coupling signal -- cerebellum/IPL",
        "Harrison 2025"),
    _h3(_X_L4L5_START, "x_l4l5", 11, 17, 0,
        "Sensorimotor peak events -- motor spikes",
        "Yamashita 2025"),
    _h3(_ENERGY_CHANGE, "energy_change", 11, 14, 2,
        "Intensity regularity -- motor effort periodicity",
        "Liang 2025"),

    # Long horizon (H16 = 1s)
    _h3(_X_L5L7_START, "x_l5l7", 16, 1, 0,
        "Mean connectivity coupling -- sustained network",
        "Blasi 2025"),
    _h3(_SENSORY_PLEASANT, "sensory_pleasantness", 16, 1, 0,
        "Sustained pleasantness -- motor valence proxy",
        "Provias 2025"),

    # === M-layer: Integration & Coherence (1 new tuple) ===
    _h3(_X_L0L5_START, "x_l0l5", 16, 19, 0,
        "Entrainment stability over 1s -- coherence anchor",
        "Ross 2022"),

    # === P-layer: Present State (2 new tuples) ===
    _h3(_AMPLITUDE, "amplitude", 11, 0, 2,
        "Current motor drive -- amplitude at motor window",
        "Harrison 2025"),
    _h3(_AMPLITUDE, "amplitude", 11, 8, 0,
        "Intensity change rate -- motor adaptation cue",
        "Yamashita 2025"),

    # === F-layer: Forecast (2 new tuples) ===
    _h3(_X_L5L7_START, "x_l5l7", 16, 18, 0,
        "Connectivity trajectory -- recovery forecast",
        "Blasi 2025"),
    _h3(_X_L5L7_START, "x_l5l7", 16, 14, 2,
        "Connectivity regularity -- restoration prediction",
        "Blasi 2025"),
)

assert len(_RIRI_H3_DEMANDS) == 16


class RIRI(Encoder):
    """RAS-Intelligent Rehabilitation Integration -- IMU Encoder (depth 1, 10D).

    Models how multi-modal rhythmic auditory stimulation (RAS) combined
    with visual-VR and haptic-robotic feedback drives motor optimization
    through convergent temporal entrainment.  Integration synergy is
    captured via geometric mean gating: if any modality pathway fails,
    overall synergy collapses.

    Thaut, McIntosh & Hoemberg 2015: period entrainment drives motor
    optimization via reticulospinal pathways (review, >50 studies).

    Harrison et al. 2025: SMA + putamen + sensorimotor cortex activation
    during musically-cued movement in PD (fMRI, N=20).

    Blasi et al. 2025: structural + functional neuroplasticity from
    music/dance rehabilitation (meta-analysis, 20 RCTs, N=718).

    Dependency chain:
        RIRI is an Encoder (Depth 1) -- reads RASN, MEAMN, MMP, HCMC
        relay outputs (intra-IMU dependencies).
        Computed after all four upstream mechanisms in F4 pipeline.

    Downstream feeds:
        -> beat_entrainment beliefs (Core)
        -> motor adaptation beliefs (Appraisal)
        -> F8 Learning: adaptive difficulty from recovery trajectory
        -> F6 Reward: session success from consolidation prediction
    """

    NAME = "RIRI"
    FULL_NAME = "RAS-Intelligent Rehabilitation Integration"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("RASN", "MEAMN", "MMP", "HCMC")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:multimodal_entrainment", "E1:sensorimotor_integration",
             "E2:enhanced_recovery"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Model", 3, 5,
            ("M0:integration_synergy", "M1:temporal_coherence"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:entrainment_state", "P1:motor_adaptation"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:recovery_trajectory", "F1:connectivity_pred",
             "F2:consolidation_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _RIRI_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:multimodal_entrainment", "E1:sensorimotor_integration",
            "E2:enhanced_recovery",
            "M0:integration_synergy", "M1:temporal_coherence",
            "P0:entrainment_state", "P1:motor_adaptation",
            "F0:recovery_trajectory", "F1:connectivity_pred",
            "F2:consolidation_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # SMA -- multi-modal entrainment hub
            RegionLink("E0:multimodal_entrainment", "SMA", 0.85,
                       "Thaut 2015"),
            # Premotor cortex -- motor preparation from entrainment
            RegionLink("P0:entrainment_state", "PMC", 0.80,
                       "Harrison 2025"),
            # Cerebellum -- sensorimotor prediction error
            RegionLink("E1:sensorimotor_integration", "Cerebellum", 0.80,
                       "Ross 2022"),
            # Putamen -- basal ganglia timing for entrainment
            RegionLink("P0:entrainment_state", "Putamen", 0.75,
                       "Harrison 2025"),
            # M1 -- motor execution from adaptation
            RegionLink("P1:motor_adaptation", "M1", 0.75,
                       "Yamashita 2025"),
            # Hippocampus -- session consolidation
            RegionLink("F2:consolidation_pred", "Hippocampus", 0.70,
                       "Fang 2017"),
            # mPFC -- recovery trajectory monitoring
            RegionLink("F0:recovery_trajectory", "mPFC", 0.65,
                       "Blasi 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # RIRI modulates via entrainment, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Thaut, McIntosh & Hoemberg", 2015,
                         "Period entrainment drives motor optimization via "
                         "reticulospinal pathways; RAS is the dominant "
                         "mechanism for gait rehabilitation in neurological "
                         "disorders",
                         "review, >50 studies"),
                Citation("Harrison et al.", 2025,
                         "SMA + putamen + sensorimotor cortex activation "
                         "during musically-cued movement in Parkinson's; "
                         "cerebellum activated during internal cueing",
                         "fMRI, N=20"),
                Citation("Blasi et al.", 2025,
                         "Structural and functional neuroplasticity from "
                         "music/dance rehabilitation; enhanced FC within "
                         "language and motor networks post-intervention",
                         "meta-analysis, 20 RCTs, N=718"),
                Citation("Liang et al.", 2025,
                         "Music + VR produces greater SMA/premotor "
                         "activation than VR alone; convergent multi-modal "
                         "benefit for motor rehabilitation",
                         "fNIRS, N=26"),
                Citation("Yamashita et al.", 2025,
                         "Gait-synchronized M1+SMA tACS reduces step "
                         "variability; phase-locked stimulation enhances "
                         "motor adaptation",
                         "pilot RCT, N=15"),
                Citation("Fang et al.", 2017,
                         "Music therapy preserves encoding in "
                         "neurodegeneration; hippocampal-cortical "
                         "consolidation supports motor memory",
                         "review, AD patients"),
                Citation("Ross & Balasubramaniam", 2022,
                         "Cerebellar forward models for predictive timing; "
                         "sensorimotor simulation during rhythm perception",
                         "review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.80),
            falsification_criteria=(
                "Multi-modal entrainment (E0) must exceed unimodal RAS "
                "alone (Liang 2025: music+VR > VR, fNIRS SMA activation)",
                "Integration synergy (M0) must collapse when any single "
                "modality is removed (geometric mean property)",
                "Entrainment state (P0) must correlate with gait "
                "variability reduction (Thaut 2015: RAS effect on CV)",
                "Motor adaptation (P1) must increase with phase-locked "
                "stimulation (Yamashita 2025: tACS reduces step variability)",
                "Recovery trajectory (F0) must predict session-to-session "
                "FC changes (Blasi 2025: FC enhancement post-intervention)",
                "Consolidation prediction (F2) must decrease with "
                "hippocampal impairment (Fang 2017: AD encoding deficit)",
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
        """Transform R3/H3 + upstream relay outputs into 10D rehabilitation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.  Upstream
        relay reads (RASN, MEAMN, MMP, HCMC) provide intra-unit context
        with graceful fallback if any are missing.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"RASN": ..., "MEAMN": ..., "MMP": ..., "HCMC": ...}``

        Returns:
            ``(B, T, 10)`` -- E(3) + M(2) + P(2) + F(3)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, e, m, relay_outputs)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
