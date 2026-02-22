"""DDSMI -- Dyadic Dance Social Motor Integration.

Encoder nucleus (depth 1) in MPU, Function F7. Models the four parallel neural
tracking processes during dyadic dance (social coordination, music tracking,
self-movement, partner tracking), compressed into three computationally distinct
signals. Resource competition between auditory and social processing is the key
mechanism: visual contact shifts resources from music tracking to social
coordination (Bigand 2025: F(1,57)=7.48, p=.033). Self-movement tracking is
autonomous from social context (all ps>.224).

Reads: PEOM (period entrainment), ASAP (beat prediction)

R3 Ontology Mapping (post-freeze 97D):
    loudness:          [8]      (B, perceptual intensity)
    onset_strength:    [10]     (B, music onset detection)
    x_l0l5:            [25:33]  (F, music-motor coupling)
    x_l4l5:            [33:41]  (G, social coupling)

Output structure: E(3) + M(3) + P(2) + F(3) = 11D
  E-layer  [0:3]   Extraction           (sigmoid)  scope=internal
  M-layer  [3:6]   Temporal Integration (sigmoid)  scope=internal
  P-layer  [6:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer  [8:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ddsmi/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Encoder
from Musical_Intelligence.contracts.dataclasses import (
    Citation,
    CrossUnitPathway,
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
    3: "100ms (fast)",
    8: "500ms (mid)",
    16: "1s (sustained)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 2: "std", 14: "periodicity", 20: "entropy",
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


# -- R3 feature names (post-freeze 97D) --------------------------------------
_LOUDNESS = 8
_ONSET_STRENGTH = 10


# -- 11 H3 Demand Specifications -----------------------------------------------
# DDSMI requires multi-scale social and music coupling periodicity, plus
# loudness entropy for resource competition modulation. All L2 (integration).

_DDSMI_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Social + Music Multi-Scale Tracking (11 tuples) ===
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 2,
        "Music onset 100ms -- fast auditory tracking",
        "Bigand 2025"),
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 14, 2,
        "Music periodicity 1s -- sustained auditory entrainment",
        "Bigand 2025"),
    _h3(25, "x_l0l5[0]", 3, 0, 2,
        "Music coupling 100ms -- fast motor-auditory link",
        "Bigand 2025"),
    _h3(25, "x_l0l5[0]", 3, 14, 2,
        "Music coupling period 100ms -- fast coupling regularity",
        "Bigand 2025"),
    _h3(25, "x_l0l5[0]", 8, 14, 2,
        "Music coupling period 500ms -- mid-scale regularity",
        "Bigand 2025"),
    _h3(25, "x_l0l5[0]", 16, 14, 2,
        "Music coupling period 1s -- sustained coupling regularity",
        "Bigand 2025"),
    _h3(33, "x_l4l5[0]", 3, 0, 2,
        "Social coupling 100ms -- fast partner tracking",
        "Bigand 2025"),
    _h3(33, "x_l4l5[0]", 3, 2, 2,
        "Social variability 100ms -- partner tracking stability",
        "Bigand 2025"),
    _h3(33, "x_l4l5[0]", 8, 14, 2,
        "Social period 500ms -- mid-scale social coordination",
        "Bigand 2025"),
    _h3(33, "x_l4l5[0]", 16, 14, 2,
        "Social period 1s -- sustained social coordination",
        "Bigand 2025"),
    _h3(_LOUDNESS, "loudness", 3, 20, 2,
        "Loudness entropy 100ms -- auditory complexity",
        "Bigand 2025"),
)

assert len(_DDSMI_H3_DEMANDS) == 11


class DDSMI(Encoder):
    """Dyadic Dance Social Motor Integration -- MPU Encoder (depth 1, 11D).

    Models four parallel neural tracking processes during dyadic dance,
    compressed into three computationally distinct signals. Resource
    competition between auditory and social processing is the key mechanism:
    visual contact shifts resources from music tracking to social coordination.

    The mTRF (multivariate temporal response function) framework disentangles
    four concurrent processes: social coordination tracking, music tracking,
    self-movement tracking, and partner tracking. Self-movement is autonomous
    from social context (all ps>.224). Social coordination is dominant with
    visual contact (F(1,57)=249.75). Visual contact reduces music tracking
    (F(1,57)=7.48, p=.033) while increasing social coordination.

    Bigand et al. 2025: mTRF disentangles four parallel processes in dyadic
    dance (EEG, N=58); social coordination mTRF F(1,57)=249.75; music tracking
    F(1,57)=30.22; visual contact x music F(1,57)=50.10.

    Wohltjen et al. 2023: Beat entrainment predicts social synchrony during
    musical interaction (EEG hyperscanning, d=1.37).

    Kohler et al. 2025: Self-produced actions in left M1, other-produced in
    right PMC (MVPA, content-specific motor representations).

    Sabharwal et al. 2024: Granger causality directional coupling predicts
    leader/follower dynamics in interpersonal coordination.

    Yoneta et al. 2022: Leader/follower roles modulate inter-brain coupling
    dynamics in cooperative music performance.

    Dependency chain:
        DDSMI is an Encoder (Depth 1) -- reads PEOM relay + ASAP encoder.
        Computed in Phase 1 (F7 motor models).

    Downstream feeds:
        -> social_motor_sync belief (Core, tau=0.45)
        -> social_coordination belief (Anticipation)
        -> ARU (social reward via partner_sync)
        -> VRMSME (multi-modal coordination)
    """

    NAME = "DDSMI"
    FULL_NAME = "Dyadic Dance Social Motor Integration"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("PEOM", "ASAP")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="MPU_PEOM__MPU_DDSMI__period_entrainment",
            name="PEOM period entrainment to DDSMI beat anchor",
            source_unit="MPU",
            source_model="PEOM",
            source_dims=("period_lock_strength", "kinematic_smoothness"),
            target_unit="MPU",
            target_model="DDSMI",
            correlation="r=0.65",
            citation="Bigand 2025",
        ),
        CrossUnitPathway(
            pathway_id="MPU_ASAP__MPU_DDSMI__beat_prediction",
            name="ASAP beat prediction to DDSMI auditory anchor",
            source_unit="MPU",
            source_model="ASAP",
            source_dims=("beat_prediction", "motor_simulation"),
            target_unit="MPU",
            target_model="DDSMI",
            correlation="r=0.58",
            citation="Patel & Iversen 2014",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:f13_social_coordination", "E1:f14_music_tracking",
             "E2:f15_visual_modulation"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 6,
            ("M0:mTRF_social", "M1:mTRF_auditory", "M2:mTRF_balance"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 8,
            ("P0:partner_sync", "P1:music_entrainment"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:coordination_pred", "F1:music_pred", "F2:social_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _DDSMI_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:f13_social_coordination", "E1:f14_music_tracking",
            "E2:f15_visual_modulation",
            "M0:mTRF_social", "M1:mTRF_auditory", "M2:mTRF_balance",
            "P0:partner_sync", "P1:music_entrainment",
            "F0:coordination_pred", "F1:music_pred", "F2:social_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Left M1 -- self-produced motor actions
            RegionLink("P0:partner_sync", "left_M1", 0.75,
                       "Kohler 2025"),
            # Right PMC -- other-produced (partner) motor actions
            RegionLink("P0:partner_sync", "right_PMC", 0.80,
                       "Kohler 2025"),
            # Bilateral STG -- auditory tracking during dance
            RegionLink("P1:music_entrainment", "bilateral_STG", 0.70,
                       "Bigand 2025"),
            # Prefrontal -- social coordination mTRF
            RegionLink("M0:mTRF_social", "prefrontal", 0.75,
                       "Bigand 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Oxytocin -- social synchrony and partner bonding
            NeuroLink("P0:partner_sync", "oxytocin", 0.60,
                      "Wohltjen 2023"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bigand et al.", 2025,
                         "mTRF disentangles four parallel neural tracking "
                         "processes during dyadic dance; social coordination "
                         "F(1,57)=249.75, music tracking F(1,57)=30.22, "
                         "visual contact x music F(1,57)=50.10",
                         "EEG, N=58"),
                Citation("Wohltjen et al.", 2023,
                         "Beat entrainment predicts social synchrony during "
                         "musical interaction (d=1.37)",
                         "EEG hyperscanning"),
                Citation("Kohler et al.", 2025,
                         "Self-produced actions in left M1, other-produced "
                         "in right PMC (MVPA content-specific)",
                         "fMRI, MVPA"),
                Citation("Sabharwal et al.", 2024,
                         "Granger causality directional coupling predicts "
                         "leader/follower dynamics in interpersonal "
                         "coordination",
                         "EEG hyperscanning"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Social coordination mTRF (M0) must increase with visual "
                "contact condition (Bigand 2025: F(1,57)=249.75)",
                "Music tracking mTRF (M1) must decrease with visual contact "
                "(Bigand 2025: F(1,57)=7.48, p=.033)",
                "mTRF balance (M2) must exceed 0.5 in visual contact "
                "condition (social > music)",
                "Self-movement tracking must be autonomous from social "
                "context (Bigand 2025: all ps>.224)",
                "Partner synchronization (P0) must predict social reward "
                "downstream (Wohltjen 2023: d=1.37)",
                "Resource competition: increasing partner_sync demands "
                "must decrease music_entrainment (cross-inhibition)",
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
        """Transform R3/H3 + PEOM/ASAP relay output into 11D social motor.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"PEOM": (B, T, 11), "ASAP": (B, T, 11)}``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(2) + F(3)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(e)
        p = compute_cognitive_present(e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
