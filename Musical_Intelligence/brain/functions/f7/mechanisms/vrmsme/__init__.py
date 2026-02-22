"""VRMSME -- VR Music Stimulation Motor Enhancement.

Encoder nucleus (depth 1) in MPU, Function F7. Models the unique motor-
enhancing effect of VR music stimulation (VRMS) compared to VR action
observation (VRAO) and VR motor imagery (VRMI). VRMS produces superior
bilateral PM&SMA connectivity (p<.01 FDR) and bilateral M1 activation
(p<.05 HBT). The PM-DLPFC-M1 heterogeneous connectivity network is
uniquely activated by VRMS with 14 significant ROI pairs.

Reads: PEOM, MSR (intra-circuit via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    loudness:                   [8]      (B, perceptual intensity)
    spectral_flux:              [10]     (B, music onset detection)
    onset_strength:             [11]     (B, beat marker strength)
    x_l0l5:                     [25:33]  (F, VR-audio-motor coupling)
    x_l4l5:                     [33:41]  (G, sensorimotor binding)

Output structure: E(3) + M(3) + P(2) + F(3) = 11D
  E-layer   [0:3]   Extraction           (sigmoid)  scope=internal
  M-layer   [3:6]   Temporal Integration (sigmoid)  scope=internal
  P-layer   [6:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [8:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/vrmsme/
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
    3: "100ms (alpha)",
    8: "500ms (phrase)",
    16: "1s (beat)",
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


# -- R3 feature name constants ------------------------------------------------
_LOUDNESS = 8
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11
_X_L0L5_0 = 25
_X_L4L5_0 = 33


# -- 12 H3 Demand Specifications -----------------------------------------------
# VR Music Stimulation Motor Enhancement requires multi-scale temporal features
# spanning fast detection (100ms) to sustained bilateral activation (1s).
# E-layer: 12 tuples, M-layer: 0, P-layer: 0, F-layer: 0 (reuses E).
# All L2 (bidirectional integration).

_VRMSME_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: VR Music Enhancement Extraction (12 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Music onset at 100ms -- fast auditory detection",
        "Liang 2025"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 14, 2,
        "Music periodicity 1s -- sustained auditory regularity",
        "Liang 2025"),
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 2,
        "Beat strength 100ms -- motor timing marker",
        "Liang 2025"),
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 14, 2,
        "Onset periodicity 1s -- beat regularity",
        "Liang 2025"),
    _h3(_X_L0L5_0, "x_l0l5[0]", 3, 0, 2,
        "VR-motor coupling 100ms -- fast multi-modal link",
        "Liang 2025"),
    _h3(_X_L0L5_0, "x_l0l5[0]", 3, 14, 2,
        "Coupling periodicity 100ms -- fast coupling regularity",
        "Liang 2025"),
    _h3(_X_L0L5_0, "x_l0l5[0]", 16, 14, 2,
        "Coupling periodicity 1s -- sustained coupling regularity",
        "Liang 2025"),
    _h3(_X_L4L5_0, "x_l4l5[0]", 3, 0, 2,
        "Sensorimotor binding 100ms -- fast action-perception link",
        "Liang 2025"),
    _h3(_X_L4L5_0, "x_l4l5[0]", 3, 2, 2,
        "Binding variability 100ms -- sensorimotor stability",
        "Liang 2025"),
    _h3(_X_L4L5_0, "x_l4l5[0]", 8, 14, 2,
        "Sensorimotor period 500ms -- mid-scale binding",
        "Liang 2025"),
    _h3(_X_L4L5_0, "x_l4l5[0]", 16, 14, 2,
        "Sensorimotor period 1s -- sustained binding regularity",
        "Liang 2025"),
    _h3(_LOUDNESS, "velocity_D", 3, 20, 2,
        "Loudness entropy 100ms -- auditory complexity",
        "Liang 2025"),
)

assert len(_VRMSME_H3_DEMANDS) == 12


class VRMSME(Encoder):
    """VR Music Stimulation Motor Enhancement -- MPU Encoder (depth 1, 11D).

    Models the unique motor-enhancing effect of VR music stimulation (VRMS)
    compared to VR action observation (VRAO) and VR motor imagery (VRMI).
    VRMS produces superior bilateral PM&SMA connectivity (p<.01 FDR) and
    bilateral M1 activation (p<.05 HBT). The PM-DLPFC-M1 heterogeneous
    connectivity network (14 ROI pairs, p<.05 FDR) is uniquely activated
    by VRMS.

    Three extraction features (music_enhancement, bilateral_activation,
    network_connectivity) capture the core VR-music-motor enhancement
    effects. Temporal integration produces clinically interpretable VRMS
    advantage, bilateral index, and connectivity strength. Cognitive present
    estimates motor drive and sensorimotor sync state. Forecasts predict
    enhancement, connectivity, and bilateral activation continuation.

    Liang et al. 2025: VRMS > VRAO in bilateral PM&SMA connectivity
    (RS1, LPMSMA, RPMSMA p<.01 FDR); VRMS > VRMI in bilateral M1
    activation (RM1, LM1 p<.05 HBT) (fNIRS, N=20).

    Li et al. 2025: high-groove music increases hip-ankle coordination
    28.7% and muscle synergy complexity (median synergies HG=7 vs LG=6,
    p=.039).

    Blasi et al. 2025: music/dance interventions produce structural +
    functional neuroplasticity (systematic review, 20 RCTs, N=718).

    Dependency chain:
        VRMSME is an Encoder (Depth 1) -- reads PEOM and MSR relay outputs
        (F7 intra-circuit). Computed after PEOM and MSR in F7 pipeline.

    Downstream feeds:
        -> vr_motor_enhancement belief (Appraisal)
        -> SPMC (motor circuit), DDSMI (bilateral social motor)
    """

    NAME = "VRMSME"
    FULL_NAME = "VR Music Stimulation Motor Enhancement"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("PEOM", "MSR")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="MPU_PEOM__MPU_VRMSME__period_entrainment",
            name="PEOM period entrainment to VRMSME motor coupling context",
            source_unit="MPU",
            source_model="PEOM",
            source_dims=("period_lock_strength", "kinematic_smoothness"),
            target_unit="MPU",
            target_model="VRMSME",
            correlation="r=0.68",
            citation="Liang 2025",
        ),
        CrossUnitPathway(
            pathway_id="MPU_MSR__MPU_VRMSME__training_level",
            name="MSR training level to VRMSME sensorimotor expertise context",
            source_unit="MPU",
            source_model="MSR",
            source_dims=("training_level",),
            target_unit="MPU",
            target_model="VRMSME",
            correlation="r=0.55",
            citation="Blasi 2025",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("f16:music_enhancement", "f17:bilateral_activation",
             "f18:network_connectivity"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 6,
            ("M0:vrms_advantage", "M1:bilateral_index",
             "M2:connectivity_strength"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 8,
            ("P0:motor_drive", "P1:sensorimotor_sync"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:enhancement_pred", "F1:connectivity_pred",
             "F2:bilateral_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _VRMSME_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f16:music_enhancement", "f17:bilateral_activation",
            "f18:network_connectivity",
            "M0:vrms_advantage", "M1:bilateral_index",
            "M2:connectivity_strength",
            "P0:motor_drive", "P1:sensorimotor_sync",
            "F0:enhancement_pred", "F1:connectivity_pred",
            "F2:bilateral_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Bilateral PM & SMA -- VRMS > VRAO connectivity
            RegionLink("M0:vrms_advantage", "bilateral_PM_SMA", 0.85,
                       "Liang 2025"),
            # Bilateral M1 -- VRMS > VRMI activation
            RegionLink("M1:bilateral_index", "bilateral_M1", 0.80,
                       "Liang 2025"),
            # DLPFC -- PM-DLPFC-M1 heterogeneous FC network
            RegionLink("M2:connectivity_strength", "DLPFC", 0.80,
                       "Liang 2025"),
            # S1 -- bilateral sensorimotor activation
            RegionLink("P1:sensorimotor_sync", "S1", 0.70,
                       "Liang 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- motor drive from groove-based reward
            NeuroLink("P0:motor_drive", "dopamine", 0.70,
                      "Li 2025"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Liang et al.", 2025,
                         "VRMS > VRAO in bilateral PM&SMA connectivity "
                         "(p<.01 FDR); VRMS > VRMI in bilateral M1 "
                         "activation (p<.05 HBT); 14 ROI pairs with "
                         "significant heterogeneous FC",
                         "fNIRS, N=20"),
                Citation("Li et al.", 2025,
                         "High-groove music increases hip-ankle coordination "
                         "28.7% and muscle synergy complexity (median "
                         "synergies HG=7 vs LG=6, p=.039)",
                         "biomechanics, groove"),
                Citation("Blasi et al.", 2025,
                         "Music/dance interventions produce structural + "
                         "functional neuroplasticity across 20 RCTs",
                         "systematic review, N=718"),
                Citation("Sarasso et al.", 2019,
                         "Appreciated musical intervals enhance N1/P2 and "
                         "modulate bilateral motor cortex activation",
                         "EEG, motor cortex"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "VRMS advantage (M0) must be higher than VRAO and VRMI "
                "baselines when music stimulation is present with VR "
                "(Liang 2025: VRMS > VRAO p<.01 FDR)",
                "Bilateral index (M1) must distinguish VRMS from VRMI: "
                "VRMS should show significantly higher bilateral M1 "
                "activation (Liang 2025: p<.05 HBT)",
                "Network connectivity (M2) must require both music "
                "enhancement AND bilateral activation to be high "
                "(f16 * f17 interaction term)",
                "Motor drive (P0) must increase with groove level and "
                "predict coordination quality (Li 2025: 28.7% increase)",
                "Enhancement and connectivity predictions should correlate "
                "with sustained VR-music stimulation effects "
                "(Blasi 2025: neuroplasticity from music/dance)",
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
        """Transform R3/H3 + PEOM/MSR relay outputs into 11D VRMS enhancement.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"PEOM": (B, T, D), "MSR": (B, T, D)}``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(2) + F(3)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
