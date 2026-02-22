"""SSPS -- Saddle-Shaped Preference Surface.

Associator nucleus (depth 2) in RPU, Function F6. Models how musical
preference follows a saddle-shaped surface in IC (information content) x
entropy space, with two distinct optimal zones producing pleasure.

Core finding: Musical preference is not a simple inverted-U of complexity.
It follows a saddle-shaped surface where two zones produce high preference:
  Zone 1: High entropy + low IC (predictable events in uncertain contexts)
  Zone 2: Low entropy + medium IC (moderate surprise in stable contexts)

Cheung et al. (2019): IC x entropy interaction beta = -0.124, p = 0.000246.
Gold et al. (2023): R^2 = 0.496 for full saddle model.

Reads: IUCP (intra-unit, depth 1) -- inverted-U preference baseline
       RPEM (intra-unit, depth 1) -- reward prediction error for IC level

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, harmonic complexity)
    sensory_pleasantness:   [4]      (A, hedonic quality)
    loudness:               [8]      (B, perceptual salience)
    spectral_change:        [21]     (D, temporal surprise / IC proxy)
    concentration_change:   [24]     (D, spectral complexity / entropy proxy)
    x_l0l5:                 [25:33]  (F, context integration)
    x_l4l5:                 [33:41]  (F, IC-perceptual coupling)

Output structure: E(4) + P(1) + F(1) = 6D   (no M-layer)
  E-layer [0:4]  Extraction        (sigmoid)  scope=internal
  P-layer [4:5]  Cognitive Present (sigmoid)  scope=hybrid
  F-layer [5:6]  Forecast          (sigmoid)  scope=external

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ssps/
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

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    2: "75ms (fast)",
    8: "500ms (phrase)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    15: "smoothness", 20: "entropy",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "forward", 2: "integration"}


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


# -- 14 H3 Demand Specifications (all consumed by E-layer) --------------------
# Spans H2 (75ms) through H16 (1s).  Mix of L0 (forward) and L2
# (bidirectional).  Fast IC features (H2, L0) capture immediate surprise;
# entropy features require longer windows (H16, L2) for stable estimation.

_SSPS_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === IC axis features ===
    _h3(21, "spectral_change", 2, 0, 0,
        "IC at 75ms (fast surprise) -- x-axis of saddle surface",
        "Cheung 2019"),
    _h3(21, "spectral_change", 8, 8, 0,
        "IC velocity at 500ms -- rate of surprise change",
        "Cheung 2019"),
    _h3(21, "spectral_change", 16, 20, 2,
        "IC entropy over 1s -- surprise uncertainty",
        "Cheung 2019"),

    # === Entropy axis features ===
    _h3(24, "concentration_change", 8, 2, 2,
        "Concentration std at 500ms -- spectral complexity variability",
        "Cheung 2019"),
    _h3(24, "concentration_change", 16, 20, 2,
        "Concentration entropy at 1s -- spectral uncertainty",
        "Cheung 2019"),
    _h3(0, "roughness", 8, 1, 2,
        "Mean roughness at 500ms -- harmonic complexity baseline",
        "Mencke 2019"),
    _h3(0, "roughness", 16, 2, 2,
        "Roughness variability at 1s -- harmonic uncertainty",
        "Mencke 2019"),

    # === Hedonic features ===
    _h3(4, "sensory_pleasantness", 8, 1, 2,
        "Mean pleasantness at 500ms -- hedonic quality baseline",
        "Gold 2023"),
    _h3(4, "sensory_pleasantness", 16, 15, 0,
        "Pleasantness smoothness at 1s -- hedonic quality variation",
        "Gold 2023"),

    # === Perceptual features ===
    _h3(8, "loudness", 16, 1, 2,
        "Mean loudness at 1s -- perceptual salience for preference eval",
        "Cheung 2019"),

    # === Coupling / context features ===
    _h3(33, "x_l4l5", 8, 1, 2,
        "IC-perceptual coupling at 500ms -- saddle interaction feature",
        "Cheung 2019"),
    _h3(33, "x_l4l5", 16, 20, 2,
        "Coupling entropy at 1s -- interaction strength uncertainty",
        "Cheung 2019"),
    _h3(25, "x_l0l5", 8, 2, 2,
        "Context variability at 500ms -- environmental unpredictability",
        "Mencke 2019"),
    _h3(25, "x_l0l5", 16, 1, 2,
        "Mean context at 1s -- context integration baseline",
        "Mencke 2019"),
)

assert len(_SSPS_H3_DEMANDS) == 14


class SSPS(Associator):
    """Saddle-Shaped Preference Surface -- RPU Associator (depth 2, 6D).

    Models how musical preference follows a saddle-shaped surface in
    IC (information content) x entropy space.  Two optimal zones produce
    pleasure: (1) high entropy + low IC, (2) low entropy + medium IC.

    Cheung et al. (2019): IC x entropy interaction beta = -0.124,
    p = 0.000246. Saddle surface explains bilateral amygdala/hippocampus
    and auditory cortex activation patterns (fMRI, N=39).

    Gold et al. (2023): Full saddle model R^2 = 0.496.  VS shows
    RPE-like surprise x liking interaction consistent with predictive
    preference evaluation (fMRI, N=40).

    Mencke et al. (2019): Predictable events in uncertain contexts
    (Zone 1) produce pleasure via uncertainty resolution (behavioral,
    N=60).

    Berlyne (1971): Inverted-U preference for moderate complexity in
    stable contexts (Zone 2) -- foundational aesthetic theory.

    Dependency chain:
        SSPS reads IUCP (F6 intra-unit, depth 1) and RPEM (F6 intra-unit).
        Computed after IUCP and RPEM in the C3 scheduler.

    Downstream feeds:
        -> DAED (dopaminergic anticipation via peak proximity)
        -> LDAC (sensory gating via entropy value)
        -> IMU learning (optimal complexity target)
        -> Precision engine (pi_pred for prediction confidence)
    """

    NAME = "SSPS"
    FULL_NAME = "Saddle-Shaped Preference Surface"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 6
    UPSTREAM_READS = ("IUCP", "RPEM")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:ic_value", "f02:entropy_value",
             "f03:saddle_position", "f04:peak_proximity"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 4, 5,
            ("surface_position_state",),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 5, 6,
            ("optimal_zone_pred",),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SSPS_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:ic_value", "f02:entropy_value",
            "f03:saddle_position", "f04:peak_proximity",
            "surface_position_state",
            "optimal_zone_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Auditory cortex -- IC x entropy interaction encoding
            RegionLink("f01:ic_value", "A1_STG", 0.80,
                       "Cheung 2019"),
            # Auditory cortex -- entropy estimation in auditory stream
            RegionLink("f02:entropy_value", "A1_STG", 0.75,
                       "Cheung 2019"),
            # Amygdala -- saddle interaction reflects hedonic evaluation
            RegionLink("f03:saddle_position", "amygdala", 0.80,
                       "Cheung 2019"),
            # Hippocampus -- context-dependent preference memory
            RegionLink("f04:peak_proximity", "hippocampus", 0.75,
                       "Gold 2023"),
            # Amygdala/hippocampus -- bilateral IC x entropy interaction
            RegionLink("surface_position_state", "amygdala", 0.80,
                       "Cheung 2019"),
            # VS (ventral striatum) -- RPE-like surprise x liking
            RegionLink("optimal_zone_pred", "VS", 0.75,
                       "Gold 2023"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- peak proximity modulates anticipatory DA
            NeuroLink("f04:peak_proximity", "dopamine", 0.70,
                      "Gold 2023"),
            # Dopamine -- optimal zone prediction drives DA anticipation
            NeuroLink("optimal_zone_pred", "dopamine", 0.65,
                      "Gold 2023"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Cheung et al.", 2019,
                         "Uncertainty and surprise jointly predict musical "
                         "pleasure and amygdala/hippocampus/auditory cortex "
                         "activity; IC x entropy interaction beta = -0.124",
                         "fMRI, N=39"),
                Citation("Gold et al.", 2023,
                         "Full saddle model R^2 = 0.496; VS shows RPE-like "
                         "surprise x liking interaction consistent with "
                         "predictive preference evaluation",
                         "fMRI, N=40"),
                Citation("Mencke et al.", 2019,
                         "Predictable events in uncertain contexts produce "
                         "pleasure via uncertainty resolution (Zone 1 of "
                         "the saddle surface)",
                         "behavioral, N=60"),
                Citation("Berlyne", 1971,
                         "Inverted-U preference for moderate complexity in "
                         "stable contexts (Zone 2) -- foundational aesthetic "
                         "arousal theory",
                         "theory + behavioral review"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.55, 0.75),
            falsification_criteria=(
                "IC value (f01) must correlate positively with note-level "
                "information content; if f01 does not track IC from IDyOM "
                "or similar models, the IC axis is invalid (Cheung 2019)",
                "Entropy value (f02) must correlate positively with "
                "perceptual uncertainty measures; if f02 does not track "
                "spectral entropy or roughness variability, the entropy "
                "axis is invalid (Cheung 2019)",
                "Saddle position (f03) must show non-monotonic preference: "
                "both very high and very low f03 should occur at preference "
                "peaks; if f03 shows monotonic preference, the saddle "
                "topology is invalid (Cheung 2019: interaction p=0.000246)",
                "Peak proximity (f04) must predict pleasure ratings better "
                "than IC or entropy alone; if single-axis model matches "
                "f04 predictive power, the saddle model adds no value "
                "(Gold 2023: R^2 = 0.496 for full model)",
                "Zone 1 (high entropy + low IC) and Zone 2 (low entropy + "
                "medium IC) must independently correlate with pleasure; if "
                "only one zone shows preference, the dual-zone model "
                "collapses to inverted-U (Mencke 2019 vs Berlyne 1971)",
                "IUCP upstream must provide baseline inverted-U that SSPS "
                "refines; removing IUCP should reduce SSPS saddle contrast "
                "(testable via ablation of IUCP pathway)",
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
        """Transform R3/H3 + upstream into 6D saddle-surface output.

        Delegates to 3 layer functions (extraction -> cognitive_present
        -> forecast; no temporal_integration) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"IUCP": (B, T, D), "RPEM": (B, T, D)}``

        Returns:
            ``(B, T, 6)`` -- E(4) + P(1) + F(1)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        # e is (f01, f02, f03, f04, saddle_value) -- 5 tensors
        p = compute_cognitive_present(h3_features, r3_features, e)
        f = compute_forecast(h3_features, e, p)

        # Stack: 4 E-layer dims + 1 P-layer dim + 1 F-layer dim = 6D
        output = torch.stack([e[0], e[1], e[2], e[3], *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
