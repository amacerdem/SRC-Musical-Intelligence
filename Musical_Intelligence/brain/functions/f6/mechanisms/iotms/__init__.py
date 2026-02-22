"""IOTMS -- Individual Opioid Tone Music Sensitivity.

Associator nucleus (depth 2) in RPU, Function F6. Models how individual
differences in mu-opioid receptor (MOR) availability shape trait-level
music reward sensitivity. The smallest model in the entire C3 system
(5D total output, 12 H3 tuples).

Core finding: Baseline MOR binding potential (BPND) predicts the slope
of the pleasure-to-BOLD response in insula, ACC, SMA, STG, NAcc, and
thalamus. Higher opioid tone = steeper music pleasure coupling.
Putkinen et al. 2025.

Reads: MORMR (intra-unit, F6 RPU) -- MOR-mediated opioid release scaling
       DAED  (intra-unit, F6 RPU) -- DA coupling strength

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, consonance quality)
    sensory_pleasantness:   [4]      (A, hedonic quality)
    loudness:               [8]      (B, perceptual intensity)
    tristimulus1:           [14]     (C, harmonic richness)
    x_l4l5:                 [33:41]  (G, sustained coupling)

Output structure: E(4) + P(1) = 5D
  E-layer [0:4]   Extraction        (sigmoid)  scope=internal
  P-layer [4:5]   Cognitive Present (sigmoid)  scope=hybrid

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/iotms/
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

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    8: "500ms (sub-beat)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "mean", 2: "std", 6: "skew", 18: "trend",
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


# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_LOUDNESS = 8
_TRISTIMULUS1 = 14
_X_L4L5_0 = 33


# -- 12 H3 Demand Specifications -----------------------------------------------
# All E-layer tuples. Concentrated at H8 (500ms) and H16 (1s) with L2
# (bidirectional) law, reflecting the trait-level nature of opioid tone --
# short timescales are irrelevant for stable individual differences.

_IOTMS_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === f01: MOR baseline proxy (5 tuples) ===
    _h3(_PLEASANTNESS, "sensory_pleasantness", 8, 0, 2,
        "Mean hedonic quality at 500ms -- short-term pleasure anchor",
        "Putkinen 2025"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Mean hedonic quality at 1s -- sustained pleasure for MOR estimate",
        "Putkinen 2025"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 2, 2,
        "Hedonic variability at 1s -- pleasure stability indicator",
        "Putkinen 2025"),
    _h3(_ROUGHNESS, "roughness", 8, 0, 2,
        "Mean roughness at 500ms -- consonance quality anchor",
        "Putkinen 2025"),
    _h3(_ROUGHNESS, "roughness", 16, 6, 2,
        "Roughness skewness at 1s -- consonance distribution shape",
        "Putkinen 2025"),

    # === f02: pleasure-BOLD slope (2 tuples) ===
    _h3(_LOUDNESS, "loudness", 8, 0, 2,
        "Mean loudness at 500ms -- short-term intensity anchor",
        "Putkinen 2025"),
    _h3(_LOUDNESS, "loudness", 16, 0, 2,
        "Mean loudness at 1s -- sustained intensity for BOLD slope",
        "Putkinen 2025"),

    # === f03: reward propensity (2 tuples) ===
    _h3(_X_L4L5_0, "x_l4l5_0", 8, 0, 2,
        "Sustained coupling at 500ms -- opioid-perceptual interaction",
        "Mas-Herrero 2014"),
    _h3(_X_L4L5_0, "x_l4l5_0", 16, 0, 2,
        "Sustained coupling at 1s -- prolonged opioid interaction",
        "Mas-Herrero 2014"),

    # === f04: music reward index (3 tuples) ===
    _h3(_X_L4L5_0, "x_l4l5_0", 16, 18, 2,
        "Coupling trend at 1s -- temporal direction of interaction",
        "Martinez-Molina 2016"),
    _h3(_TRISTIMULUS1, "tristimulus1", 16, 0, 2,
        "Mean tristimulus1 at 1s -- harmonic richness for reward index",
        "Martinez-Molina 2016"),
    _h3(_TRISTIMULUS1, "tristimulus1", 16, 2, 2,
        "Tristimulus1 variability at 1s -- harmonic stability indicator",
        "Martinez-Molina 2016"),
)

assert len(_IOTMS_H3_DEMANDS) == 12


class IOTMS(Associator):
    """Individual Opioid Tone Music Sensitivity -- RPU Associator (depth 2, 5D).

    The smallest model in the entire C3 system. Models how individual
    differences in mu-opioid receptor (MOR) availability create stable
    trait-level differences in music reward sensitivity.

    Putkinen et al. (2025): Baseline MOR binding potential (BPND)
    predicted the slope of pleasure-to-BOLD coupling in insula, ACC,
    SMA, STG, NAcc, and thalamus. Effect size d=1.16. PET+fMRI, N=36.

    Mas-Herrero et al. (2014): Barcelona Music Reward Questionnaire
    (BMRQ) captures individual differences in music reward sensitivity.
    BMRQ predicted music pleasure ratings (R^2=0.30). Behavioral, N=500.

    Martinez-Molina et al. (2016): BMRQ scores predicted pleasure
    ratings for music (R^2=0.40). Individual reward sensitivity
    modulates neural response to musical features. fMRI, N=45.

    Dependency chain:
        IOTMS reads MORMR (intra-unit relay, depth 0) and
        DAED (intra-unit encoder, depth 1). Computed after both.

    Downstream feeds:
        -> MORMR: mor_baseline modulates opioid release scaling
        -> DAED: pleasure_bold_slope feeds DA coupling anticipation
        -> RPEM: reward_propensity scales prediction error magnitude
        -> MCCN: music_reward_index modulates chills threshold
        -> ARU: individual_sensitivity modulates affect gain
    """

    NAME = "IOTMS"
    FULL_NAME = "Individual Opioid Tone Music Sensitivity"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 5
    UPSTREAM_READS = ("MORMR", "DAED")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:mor_baseline_proxy", "E1:pleasure_bold_slope",
             "E2:reward_propensity", "E3:music_reward_index"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 4, 5,
            ("P0:individual_sensitivity_state",),
            scope="hybrid",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _IOTMS_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:mor_baseline_proxy",
            "E1:pleasure_bold_slope",
            "E2:reward_propensity",
            "E3:music_reward_index",
            "P0:individual_sensitivity_state",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Insula -- MOR binding hub, pleasure-BOLD coupling
            RegionLink("E0:mor_baseline_proxy", "insula", 0.85,
                       "Putkinen 2025"),
            # NAcc -- reward circuit, pleasure-BOLD slope
            RegionLink("E1:pleasure_bold_slope", "NAcc", 0.85,
                       "Putkinen 2025"),
            # ACC -- anterior cingulate, opioid-reward integration
            RegionLink("E2:reward_propensity", "ACC", 0.80,
                       "Mas-Herrero 2014"),
            # STG -- auditory cortex, music reward sensitivity
            RegionLink("E3:music_reward_index", "STG", 0.75,
                       "Martinez-Molina 2016"),
            # Thalamus -- MOR binding, individual sensitivity gate
            RegionLink("P0:individual_sensitivity_state", "thalamus", 0.70,
                       "Putkinen 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Endogenous opioids -- MOR tone determines reward capacity
            NeuroLink("E0:mor_baseline_proxy", "endorphin", 0.90,
                      "Putkinen 2025"),
            # Dopamine -- reward propensity modulates DA release
            NeuroLink("E2:reward_propensity", "dopamine", 0.75,
                      "Mas-Herrero 2014"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Putkinen et al.", 2025,
                         "Baseline MOR binding potential (BPND) predicted "
                         "pleasure-BOLD slope in insula, ACC, SMA, STG, "
                         "NAcc, and thalamus. Effect size d=1.16. Higher "
                         "opioid tone = steeper music pleasure coupling",
                         "PET+fMRI, N=36"),
                Citation("Mas-Herrero et al.", 2014,
                         "Barcelona Music Reward Questionnaire captures "
                         "individual differences in music reward sensitivity. "
                         "BMRQ predicted music pleasure (R^2=0.30)",
                         "behavioral, N=500"),
                Citation("Martinez-Molina et al.", 2016,
                         "BMRQ scores predicted pleasure ratings for music "
                         "(R^2=0.40). Individual reward sensitivity modulates "
                         "neural response to musical features",
                         "fMRI, N=45"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "MOR baseline proxy (E0) must correlate positively with "
                "sustained hedonic quality; if mean pleasantness does not "
                "predict E0, the opioid-pleasure link is invalid "
                "(Putkinen 2025: MOR BPND -> pleasure-BOLD)",
                "Pleasure-BOLD slope (E1) must increase with E0; if "
                "higher MOR baseline does not produce steeper coupling, "
                "the cascaded dependency is invalid (d=1.16)",
                "Reward propensity (E2) must correlate with sustained "
                "opioid-perceptual coupling; if x_l4l5 interaction does "
                "not predict E2, the BMRQ analog is invalid "
                "(Mas-Herrero 2014: R^2=0.30)",
                "Music reward index (E3) must be the broadest measure; "
                "if E3 does not integrate trend + harmonic richness, "
                "the composite is incomplete (Martinez-Molina 2016: R^2=0.40)",
                "Individual sensitivity (P0) must be trait-stable; "
                "frame-to-frame variance of P0 should be lower than "
                "event-level features in other mechanisms",
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
        """Transform R3/H3 + upstream into 5D opioid-reward sensitivity.

        Delegates to E-layer (4D cascaded extraction) then P-layer (1D
        summary), skipping M and F layers (not present for IOTMS).

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"MORMR": (B, T, D), "DAED": (B, T, D)}``

        Returns:
            ``(B, T, 5)`` -- E(4) + P(1)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        p = compute_cognitive_present(e)

        output = torch.stack([*e, *p], dim=-1)
        return output.clamp(0.0, 1.0)
