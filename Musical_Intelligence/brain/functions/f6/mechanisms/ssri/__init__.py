"""SSRI -- Social Synchrony Reward Integration.

Encoder nucleus (depth 1) in RPU, Function F6. Models the reward and
bonding signals arising from interpersonal musical synchrony. Social
music-making amplifies hedonic reward by 1.3-1.8x compared to solitary
listening through coordinated timing, shared affect, and group flow.

Reads: DAED, RPEM (intra-circuit via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    onset_strength:             [10]     (B, temporal alignment)
    velocity_A:                 [7]      (A, amplitude / dynamic envelope)
    sensory_pleasantness:       [4]      (A, hedonic quality)
    velocity_D:                 [8]      (B, loudness / arousal)
    warmth:                     [12]     (C, timbral blending)
    distribution_entropy:       [22]     (D, energy change / coordination)
    spectral_flux:              [21]     (D, structural coordination)
    x_l0l5[0]:                  [25]     (F, consonance-energy coupling)

Output structure: E(5) + M(2) + P(2) + F(2) = 11D
  E-layer   [0:5]   Extraction           (sigmoid)  scope=internal
  M-layer   [5:7]   Temporal Integration (mixed)    scope=internal
  P-layer   [7:9]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [9:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ssri/
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
    4: "125ms (beta-fast)",
    8: "500ms (phrase)",
    16: "1s (beat)",
    20: "5s (LTI)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity",
    14: "periodicity", 18: "trend", 20: "entropy",
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
_ONSET_STRENGTH = 10
_AMPLITUDE = 7
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 8
_WARMTH = 12
_ENERGY_CHANGE = 22
_SPECTRAL_CHANGE = 21
_X_L0L5_0 = 25


# -- 16 H3 Demand Specifications -----------------------------------------------
# Social Synchrony Reward Integration requires multi-scale temporal features
# spanning fast micro-timing (100ms) to long-range social bonding dynamics (5s).
# E-layer: 12 tuples, M-layer: 0, P-layer: 2, F-layer: 2.

_SSRI_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Social Synchrony Extraction (12 tuples) ===
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 2,
        "Onset at 100ms alpha — micro-timing alignment",
        "Kokal 2011"),
    _h3(_ONSET_STRENGTH, "onset_strength", 4, 14, 2,
        "Beat periodicity 125ms — rhythmic entrainment",
        "Wohltjen 2023"),
    _h3(_ONSET_STRENGTH, "onset_strength", 8, 14, 2,
        "Onset periodicity 500ms — phrase-level coordination",
        "Kokal 2011"),
    _h3(_AMPLITUDE, "velocity_A", 8, 1, 2,
        "Mean amplitude 500ms — shared dynamic envelope",
        "Williamson 2019"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 8, 1, 2,
        "Mean pleasantness 500ms — shared hedonic quality",
        "Ni 2024"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 1, 2,
        "Mean pleasantness 1s — sustained positive affect",
        "Ni 2024"),
    _h3(_ENERGY_CHANGE, "distribution_entropy", 8, 8, 0,
        "Energy velocity 500ms — dynamic coordination tracking",
        "Wohltjen 2023"),
    _h3(_WARMTH, "warmth", 16, 1, 2,
        "Mean warmth 1s — timbral blending quality",
        "Ni 2024"),
    _h3(_SPECTRAL_CHANGE, "spectral_flux", 8, 20, 2,
        "Spectral entropy 500ms — structural coordination demand",
        "Williamson 2019"),
    _h3(_X_L0L5_0, "x_l0l5[0]", 16, 18, 2,
        "Coupling trend 1s — consonance-energy interaction trajectory",
        "Ni 2024"),
    _h3(_X_L0L5_0, "x_l0l5[0]", 20, 1, 0,
        "Coupling mean 5s LTI — sustained emotional synchrony",
        "Dunbar 2012"),
    _h3(_LOUDNESS, "velocity_D", 20, 18, 0,
        "Loudness trend 5s LTI — long-range dynamic trajectory",
        "Dunbar 2012"),

    # === P-Layer: Neural State Estimation (1 unique tuple) ===
    # Note: P-layer also reuses E#10 (25,20,1,0) and E#11 (8,20,18,0)
    _h3(_X_L0L5_0, "x_l0l5[0]", 8, 0, 2,
        "Coupling at 500ms — current consonance-energy interaction state",
        "Ni 2024"),

    # === F-Layer: reuses E#9 (25,16,18,2) and E#11 (8,20,18,0) ===
    # No unique F-layer tuples — all reused from E-layer.
)

assert len(_SSRI_H3_DEMANDS) == 13


class SSRI(Encoder):
    """Social Synchrony Reward Integration -- RPU Encoder (depth 1, 11D).

    Models the reward and bonding signals from interpersonal musical
    synchrony. Social music-making amplifies hedonic reward by 1.3-1.8x
    through coordinated timing, shared affect, and group flow.

    Five extraction features (synchrony_reward, social_bonding_index,
    group_flow_state, entrainment_quality, collective_pleasure) capture
    the multi-dimensional reward landscape of social music-making. The
    temporal integration layer computes social prediction error (SPE)
    and synchrony amplification. The cognitive present estimates neural
    coupling and endorphin dynamics. Forecasts predict bonding trajectory
    and flow sustainability.

    Kokal et al. 2011: Joint drumming activates caudate nucleus with
    coordination quality (fMRI, N=34).

    Ni et al. 2024: Social bonding increases prefrontal neural
    synchronization during coordinated music-making (fNIRS hyperscanning,
    N=528, d=0.85).

    Williamson & Bonshor 2019: Brass band group music produces flow and
    cognitive engagement (qualitative/quantitative, N=116).

    Wohltjen et al. 2023: Beat entrainment ability is a stable individual
    difference (behavioral, N=210, d=1.37).

    Dunbar 2012: Synchronized music-making increases endorphin release
    (pain threshold proxy, N=multiple, d=0.60-0.80).

    Dependency chain:
        SSRI is an Encoder (Depth 1) -- reads DAED and RPEM relay outputs
        (F6 intra-circuit). Computed after DAED and RPEM in F6 pipeline.

    Downstream feeds:
        -> social_bonding belief (Appraisal)
        -> group_flow belief (Appraisal)
        -> synchrony_reward belief (Appraisal)
        -> RPU reward computation via synchrony_amplification
    """

    NAME = "SSRI"
    FULL_NAME = "Social Synchrony Reward Integration"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("DAED", "RPEM")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="RPU_DAED__RPU_SSRI__reward_signal",
            name="DAED reward signals to SSRI social reward modulation",
            source_unit="RPU",
            source_model="DAED",
            source_dims=("wanting_index", "liking_index"),
            target_unit="RPU",
            target_model="SSRI",
            correlation="r=0.65",
            citation="Kokal 2011",
        ),
        CrossUnitPathway(
            pathway_id="RPU_RPEM__RPU_SSRI__prediction_error",
            name="RPEM prediction error to SSRI social PE baseline",
            source_unit="RPU",
            source_model="RPEM",
            source_dims=("reward_prediction_error",),
            target_unit="RPU",
            target_model="SSRI",
            correlation="r=0.58",
            citation="Cheung 2019",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 5,
            ("f01:synchrony_reward", "f02:social_bonding_index",
             "f03:group_flow_state", "f04:entrainment_quality",
             "f05:collective_pleasure"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 5, 7,
            ("M0:social_prediction_error", "M1:synchrony_amplification"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 7, 9,
            ("P0:prefrontal_coupling", "P1:endorphin_proxy"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:bonding_trajectory_pred", "F1:flow_sustain_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SSRI_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:synchrony_reward", "f02:social_bonding_index",
            "f03:group_flow_state", "f04:entrainment_quality",
            "f05:collective_pleasure",
            "M0:social_prediction_error", "M1:synchrony_amplification",
            "P0:prefrontal_coupling", "P1:endorphin_proxy",
            "F0:bonding_trajectory_pred", "F1:flow_sustain_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Caudate nucleus -- synchrony reward signal
            RegionLink("f01:synchrony_reward", "caudate", 0.80,
                       "Kokal 2011"),
            # NAcc -- social prediction error and collective pleasure
            RegionLink("M0:social_prediction_error", "NAcc", 0.75,
                       "Cheung 2019"),
            # rDLPFC -- prefrontal coupling
            RegionLink("P0:prefrontal_coupling", "rDLPFC", 0.85,
                       "Ni 2024"),
            # rTPJ -- prefrontal coupling (joint with rDLPFC)
            RegionLink("P0:prefrontal_coupling", "rTPJ", 0.75,
                       "Ni 2024"),
            # VTA -- endorphin dynamics
            RegionLink("P1:endorphin_proxy", "VTA", 0.70,
                       "Dunbar 2012"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Beta-endorphin -- endorphin proxy from sustained synchrony
            NeuroLink("P1:endorphin_proxy", "beta-endorphin", 0.80,
                      "Dunbar 2012"),
            # Dopamine -- synchrony reward drives mesolimbic dopamine
            NeuroLink("f01:synchrony_reward", "dopamine", 0.75,
                      "Kokal 2011"),
            # Oxytocin -- social bonding index
            NeuroLink("f02:social_bonding_index", "oxytocin", 0.70,
                      "Ni 2024"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Kokal et al.", 2011,
                         "Joint drumming activates caudate nucleus with "
                         "coordination quality; social reward from synchrony",
                         "fMRI, N=34"),
                Citation("Ni et al.", 2024,
                         "Social bonding increases prefrontal neural "
                         "synchronization during coordinated music-making "
                         "(rDLPFC, rTPJ)",
                         "fNIRS hyperscanning, N=528, d=0.85"),
                Citation("Williamson & Bonshor", 2019,
                         "Brass band group music produces flow and cognitive "
                         "engagement through coordinated performance",
                         "qualitative/quantitative, N=116"),
                Citation("Wohltjen et al.", 2023,
                         "Beat entrainment ability is a stable individual "
                         "difference predicting coordination quality",
                         "behavioral, N=210, d=1.37"),
                Citation("Dunbar", 2012,
                         "Synchronized music-making increases endorphin "
                         "release (pain threshold proxy, social bonding)",
                         "meta-review, d=0.60-0.80"),
                Citation("Cheung et al.", 2019,
                         "Uncertainty x surprise interaction predicts "
                         "musical pleasure and prediction error processing",
                         "fMRI, N=39"),
                Citation("Tarr, Launay & Dunbar", 2014,
                         "Synchronized dancing elevates pain threshold "
                         "via endorphin release, mediating social bonding",
                         "behavioral, d~0.62"),
            ),
            evidence_tier="beta",
            confidence_range=(0.60, 0.85),
            falsification_criteria=(
                "Synchrony reward (f01) must correlate with caudate "
                "activation during coordinated music-making (Kokal 2011)",
                "Social bonding index (f02) must increase with sustained "
                "synchrony duration and predict prefrontal coupling "
                "(Ni 2024: d=0.85)",
                "Group flow (f03) must peak during coordinated passages "
                "and decrease during solo or uncoordinated sections "
                "(Williamson & Bonshor 2019)",
                "Entrainment quality (f04) must predict beat synchrony "
                "accuracy and show stable individual differences "
                "(Wohltjen 2023: d=1.37)",
                "Synchrony amplification must produce 1.3-1.8x reward "
                "boost over solo baseline for coordinated music-making "
                "(Dunbar 2012)",
                "Endorphin proxy must show slow buildup (tau=30s) and "
                "correlate with pain threshold elevation in synchronized "
                "conditions (Tarr et al. 2014: d~0.62)",
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
        """Transform R3/H3 + DAED/RPEM relay outputs into 11D social synchrony.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"DAED": (B, T, D), "RPEM": (B, T, D)}``

        Returns:
            ``(B, T, 11)`` -- E(5) + M(2) + P(2) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(
            h3_features, r3_features, e, relay_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
