"""MEAMR -- Music-Evoked Autobiographical Memory Reward.

Encoder nucleus (depth 1) in RPU, Function F6. Models the reward pathway
for music-evoked autobiographical memories. Familiarity is prerequisite for
autobiographical salience, which feeds positive affect. The dMPFC tracks
tonal space continuously, integrating familiarity and autobiographical
relevance into a reward signal.

Core finding: dMPFC (BA 8/9) tracks tonal space and correlates with
autobiographical salience (Janata 2009, P < 0.001, FDR P < 0.025).
Familiarity activates pre-SMA (Z = 5.37), IFG (Z = 4.81), STG.
Combined FAV (familiarity + autobio + valence) in MPFC predicts
positive affect from personally significant music.

Reads: DAED (intra-circuit via relay_outputs)
       MEAMN from F4/IMU (cross-function via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    sensory_pleasantness:       [4]      (A, hedonic recognition cue)
    loudness:                   [8]      (B, intensity context)  (NB: velocity_D)
    warmth:                     [12]     (C, timbral familiarity)
    spectral_centroid:          [13]     (C, tonal register / brightness)
    spectral_change:            [21]     (D, structural complexity)
    energy_change:              [22]     (D, temporal patterns)
    x_l5l6:                     [41:49]  (H, memory-structure binding)

Output structure: E(4) + P(1) + F(1) = 6D
  E-layer [0:4]  Extraction         (sigmoid)  scope=internal
  P-layer [4:5]  Cognitive Present  (sigmoid)  scope=hybrid
  F-layer [5:6]  Forecast           (sigmoid)  scope=external

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/meamr/
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

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    8: "500ms (sub-beat)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    1: "mean", 5: "range", 8: "velocity", 18: "trend", 20: "entropy",
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
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 8
_WARMTH = 12
_SPECTRAL_CENTROID = 13
_SPECTRAL_CHANGE = 21
_ENERGY_CHANGE = 22
_X_L5L6_0 = 41


# -- 14 H3 Demand Specifications -----------------------------------------------
# All in E-layer; P and F layers reuse E-layer outputs (no new H3 demands).
# Two horizons: H8 (500ms) and H16 (1s). Mix of L0 (memory) and L2 (bidi).
#
# E-layer: 14 tuples covering familiarity, autobio salience, dMPFC tracking,
# and positive affect extraction.

_MEAMR_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Pleasantness (familiarity cue / tonal recognition) ===
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 8, 1, 2,
        "Mean pleasantness over 500ms -- tonal quality",
        "Janata 2009"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 18, 2,
        "Pleasantness trend over 1s -- recognition ramp",
        "Janata 2009"),

    # === Loudness (intensity context) ===
    _h3(_LOUDNESS, "loudness", 8, 1, 2,
        "Mean loudness over 500ms -- intensity context",
        "Janata 2009"),
    _h3(_LOUDNESS, "loudness", 16, 1, 2,
        "Mean loudness over 1s -- sustained intensity",
        "Janata 2009"),

    # === Warmth (timbral familiarity) ===
    _h3(_WARMTH, "warmth", 16, 1, 2,
        "Mean warmth over 1s -- timbral familiarity cue",
        "Janata 2009"),

    # === Brightness (tonal register) ===
    _h3(_SPECTRAL_CENTROID, "spectral_centroid", 16, 1, 2,
        "Mean brightness over 1s -- tonal register",
        "Janata 2009"),

    # === Structural complexity ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 20, 2,
        "Structural entropy 500ms -- complexity context",
        "Janata 2009"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 1, 2,
        "Mean structural change 1s",
        "Janata 2009"),

    # === Energy dynamics (temporal patterns) ===
    _h3(_ENERGY_CHANGE, "energy_change", 8, 8, 0,
        "Energy velocity at 500ms -- temporal pattern",
        "Salimpoor 2011"),
    _h3(_ENERGY_CHANGE, "energy_change", 16, 18, 0,
        "Energy change trend 1s -- dynamic trajectory",
        "Salimpoor 2011"),

    # === Memory-structure coupling (autobio salience) ===
    _h3(_X_L5L6_0, "x_l5l6", 8, 1, 2,
        "Memory-structure coupling 500ms",
        "Janata 2009"),
    _h3(_X_L5L6_0, "x_l5l6", 16, 1, 2,
        "Mean memory-structure coupling 1s",
        "Janata 2009"),
    _h3(_X_L5L6_0, "x_l5l6", 16, 18, 2,
        "Memory-structure trend 1s -- autobio buildup",
        "Janata 2009"),
    _h3(_X_L5L6_0, "x_l5l6", 16, 5, 0,
        "Memory-structure range 1s -- coupling dynamic range",
        "Janata 2009"),
)

assert len(_MEAMR_H3_DEMANDS) == 14


class MEAMR(Encoder):
    """Music-Evoked Autobiographical Memory Reward -- RPU Encoder (depth 1, 6D).

    Models the reward pathway for music-evoked autobiographical memories.
    Familiarity is prerequisite for autobiographical salience, which feeds
    positive affect. The dMPFC tracks tonal space continuously, integrating
    familiarity and autobiographical relevance into a reward signal.

    Janata (2009): dMPFC (BA 8/9) tracks tonal space and correlates with
    autobiographical salience (P < 0.001, FDR P < 0.025 in MPFC ROI,
    fMRI, N = 13). Familiarity activates pre-SMA (Z = 5.37), IFG
    (Z = 4.81), SFG, thalamus, STG (P < 0.001 uncorr).

    Salimpoor et al. (2011): Anatomically distinct dopamine release during
    anticipation (caudate) and experience (NAcc) of peak emotion to music
    (PET, [11C]raclopride, N = 8, r = 0.71).

    Dependency chain:
        MEAMR is an Encoder (Depth 1) -- reads DAED relay output (F6 intra-circuit).
        Also reads MEAMN from F4/IMU (cross-function via CrossUnitPathway).
        Computed after DAED in F6 pipeline.

    Downstream feeds:
        -> familiarity modulation in kernel
        -> DAED for affect-driven dopamine consummation
        -> IMU for memory retrieval cue
    """

    NAME = "MEAMR"
    FULL_NAME = "Music-Evoked Autobiographical Memory Reward"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 6
    UPSTREAM_READS = ("DAED",)
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="IMU_MEAMN__RPU_MEAMR__memory_state",
            name="MEAMN memory state to MEAMR familiarity pathway",
            source_unit="IMU",
            source_model="MEAMN",
            source_dims=("memory_state",),
            target_unit="RPU",
            target_model="MEAMR",
            correlation="r=0.65",
            citation="Janata 2009",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:familiarity_index", "E1:autobio_salience",
             "E2:dmpfc_tracking", "E3:positive_affect"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 4, 5,
            ("P0:memory_activation_state",),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 5, 6,
            ("F0:nostalgia_response_pred",),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MEAMR_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:familiarity_index", "E1:autobio_salience",
            "E2:dmpfc_tracking", "E3:positive_affect",
            "P0:memory_activation_state",
            "F0:nostalgia_response_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # dMPFC (BA 8/9) -- autobio salience + tonal tracking
            RegionLink("E1:autobio_salience", "dMPFC", 0.85,
                       "Janata 2009"),
            # dMPFC -- tonal space tracking
            RegionLink("E2:dmpfc_tracking", "dMPFC", 0.80,
                       "Janata 2009"),
            # pre-SMA -- familiarity recognition
            RegionLink("E0:familiarity_index", "pre_SMA", 0.80,
                       "Janata 2009"),
            # IFG -- familiarity processing
            RegionLink("E0:familiarity_index", "IFG", 0.75,
                       "Janata 2009"),
            # STG -- bilateral activation for familiarity
            RegionLink("E0:familiarity_index", "STG", 0.75,
                       "Janata 2009"),
            # vACC + SN/VTA -- positive affect integration
            RegionLink("E3:positive_affect", "vACC", 0.80,
                       "Janata 2009"),
            # NAcc -- memory reward
            RegionLink("P0:memory_activation_state", "NAcc", 0.75,
                       "Salimpoor 2011"),
            # Caudate -- anticipatory DA for nostalgia
            RegionLink("F0:nostalgia_response_pred", "caudate", 0.70,
                       "Salimpoor 2011"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- positive affect from autobiographical memory
            NeuroLink("E3:positive_affect", "dopamine", 0.75,
                      "Salimpoor 2011"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Janata", 2009,
                         "dMPFC (BA 8/9) tracks tonal space and correlates "
                         "with autobiographical salience; familiarity "
                         "activates pre-SMA (Z=5.37), IFG (Z=4.81), STG; "
                         "combined FAV in MPFC (FDR P<0.025)",
                         "fMRI, N=13"),
                Citation("Salimpoor et al.", 2011,
                         "Anatomically distinct dopamine release during "
                         "anticipation (caudate) and experience (NAcc) of "
                         "peak emotion to music",
                         "PET, [11C]raclopride, N=8, r=0.71"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.85),
            falsification_criteria=(
                "Familiarity index (E0) must increase with pleasantness "
                "trend and timbral warmth; if unfamiliar music produces "
                "high E0, the familiarity model is invalid (Janata 2009: "
                "pre-SMA Z=5.37 for familiar music)",
                "Autobiographical salience (E1) must require familiarity "
                "(E0) as prerequisite; high E1 without E0 is invalid "
                "(Janata 2009: dMPFC requires familiarity + autobio)",
                "Positive affect (E3) must require both familiarity AND "
                "autobio salience; either alone should not produce full "
                "E3 activation (Janata 2009: FAV in MPFC FDR P<0.025)",
                "Memory activation state (P0) must correlate with dMPFC "
                "activation; if P0 diverges from E0*E1, the model is "
                "invalid (Janata 2009: P<0.001)",
                "Nostalgia prediction (F0) must increase when both positive "
                "affect and autobio salience are high; if F0 activates "
                "without autobiographical specificity, the model is invalid",
                "MEAMN memory input must amplify familiarity; removing "
                "MEAMN should reduce E0 (testable via ablation of "
                "cross-function pathway)",
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
        """Transform R3/H3 + DAED/MEAMN relay output into 6D memory reward.

        Delegates to 3 layer functions (extraction -> cognitive_present ->
        forecast) and stacks results. No M-layer (temporal integration).

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"DAED": (B, T, D), "MEAMN": (B, T, D)}``

        Returns:
            ``(B, T, 6)`` -- E(4) + P(1) + F(1)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        p = compute_cognitive_present(e)
        f = compute_forecast(e, p)

        output = torch.stack([*e, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
