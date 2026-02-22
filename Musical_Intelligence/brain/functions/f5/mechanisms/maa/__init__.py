"""MAA -- Musical Appreciation of Atonality.

Associator nucleus (depth 2) in PCU, Function F5. Models the
multifactorial appreciation of atonal/complex music. The Goldilocks
surface (Cheung 2019) interacts with mere exposure (Gold 2019) and
cognitive framing (Huang 2016) to produce appreciation. Complexity
tolerance x familiarity multiplicatively gate the pleasure response.

Non-standard: PCU unit (Predictive Coding Unit), not ARU. 3-layer
structure (E+P+F), no separate M-layer.

Cheung et al. (2019): Uncertainty and surprise jointly predict musical
pleasure and amygdala, hippocampus, auditory cortex activity. NAcc
BOLD correlates with subjective pleasure (beta=0.242, fMRI, N=39).
Goldilocks surface: intermediate complexity maximises enjoyment.

Gold et al. (2019): Mere exposure increases liking of initially
disliked atonal music. 8 repetitions shift preference by d=0.42 for
atonal excerpts (N=40, behavioral).

Huang et al. (2016): Artistic framing (vs popular framing) increases
aesthetic appreciation of dissonant/complex music. PCC/mPFC/arMFC
show greater activation for artistic framing (fMRI, N=21).

Mencke et al. (2019): Musical training modulates sensitivity to
stylistic uncertainty; musicians show higher complexity tolerance
(N=30, behavioral + EEG).

Bianco et al. (2020): Sensory precision increases along auditory
hierarchy; Right Heschl's Gyrus shows heightened response under
tonal uncertainty (MEG, N=24).

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, atonality indicator)
    sensory_pleasantness:   [4]      (A, consonance proxy)
    periodicity:            [5]      (A, key clarity)
    tonalness:              [14]     (C, atonality index)
    spectral_change:        [21]     (D, structural complexity)
    x_l5l7:                 [41:49]  (H, appreciation pathway)

Output structure: E(4) + P(3) + F(3) = 10D
  E-layer [0:4]   Extraction     (sigmoid)  scope=internal
  P-layer [4:7]   Present        (clamp)    scope=hybrid
  F-layer [7:10]  Forecast       (sigmoid)  scope=external

Upstream reads: PUPF (12D), VMM (12D)
  PUPF.goldilocks_zone = idx 6 (G1)
  VMM.mode_signal = idx 1 (V1)

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/
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
    3: "100ms (event)",
    8: "300ms (beat)",
    16: "1000ms (bar)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 18: "trend", 19: "stability", 20: "entropy",
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


# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_PERIODICITY = 5
_TONALNESS = 14
_SPECTRAL_CHANGE = 21
_ENTROPY = 22


# -- 14 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H3(100ms) -> H8(300ms) -> H16(1s)
# Laws: L0=memory(backward), L2=integration(bidirectional)
#
# E-layer: 8 tuples (complexity, familiarity, framing, appreciation)
# P-layer: 3 tuples (pattern search, context, aesthetic evaluation)
# F-layer: 3 tuples (growth, recognition, development)

_MAA_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Extraction (8 tuples) ===
    # 1: Consonance entropy 1s -- predictability of consonance distribution
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 20, 0,
        "Consonance entropy 1s L0 -- surprise in consonance distribution",
        "Cheung 2019"),
    # 2: Coupling entropy 1s -- unpredictability in appreciation pathway
    _h3(41, "x_l5l7[0]", 16, 20, 0,
        "Coupling entropy 1s L0 -- appreciation pathway uncertainty",
        "Cheung 2019"),
    # 3: Coupling trend 1s -- direction of appreciation pathway
    _h3(41, "x_l5l7[0]", 16, 18, 0,
        "Coupling trend 1s L0 -- appreciation pathway trajectory",
        "Gold 2019"),
    # 4: Mean periodicity 1s -- key clarity for tonality assessment
    _h3(_PERIODICITY, "periodicity", 16, 1, 0,
        "Mean periodicity 1s L0 -- key clarity for atonality grading",
        "Mencke 2019"),
    # 5: Mean tonalness 1s -- running atonality estimate
    _h3(_TONALNESS, "tonalness", 16, 1, 0,
        "Mean tonalness 1s L0 -- atonality level for complexity tolerance",
        "Mencke 2019"),
    # 6: Spectral change 500ms -- structural complexity at beat scale
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 1, 0,
        "Spectral change mean 500ms L0 -- structural complexity signal",
        "Cheung 2019"),
    # 7: Consonance 100ms -- immediate consonance for framing
    _h3(_PLEASANTNESS, "sensory_pleasantness", 3, 0, 2,
        "Consonance value 100ms L2 -- immediate consonance percept",
        "Huang 2016"),
    # 8: Dissonance 100ms -- immediate dissonance for framing
    _h3(_ROUGHNESS, "roughness", 3, 0, 2,
        "Dissonance value 100ms L2 -- immediate roughness percept",
        "Huang 2016"),

    # === P-layer: Cognitive Present (3 tuples) ===
    # 9: Tonalness 500ms -- current tonal clarity for pattern search
    _h3(_TONALNESS, "tonalness", 8, 1, 0,
        "Tonalness mean 500ms L0 -- current tonal clarity",
        "Bianco 2020"),
    # 10: Coupling 500ms -- current appreciation pathway state
    _h3(41, "x_l5l7[0]", 8, 0, 0,
        "Coupling value 500ms L0 -- current appreciation pathway",
        "Gold 2019"),
    # 11: Mean coupling 1s -- sustained appreciation pathway
    _h3(41, "x_l5l7[0]", 16, 1, 0,
        "Mean coupling 1s L0 -- sustained appreciation pathway",
        "Gold 2019"),

    # === F-layer: Forecast (3 tuples) ===
    # 12: Mean dissonance 1s -- roughness trajectory for growth prediction
    _h3(_ROUGHNESS, "roughness", 16, 1, 0,
        "Mean dissonance 1s L0 -- roughness trajectory for growth",
        "Gold 2019"),
    # 13: Mean consonance 1s -- consonance trajectory for recognition
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 1, 0,
        "Mean consonance 1s L0 -- consonance trajectory for recognition",
        "Cheung 2019"),
    # 14: Stability for preference -- distribution stability
    _h3(_ENTROPY, "distribution_entropy", 16, 19, 0,
        "Distribution entropy stability 1s L0 -- preference stability",
        "Mencke 2019"),
)

assert len(_MAA_H3_DEMANDS) == 14


class MAA(Associator):
    """Musical Appreciation of Atonality -- PCU Associator (depth 2, 10D).

    Models multifactorial appreciation of atonal/complex music through
    three interacting pathways: complexity tolerance driven by the
    Goldilocks surface (E0), familiarity through mere exposure (E1),
    and cognitive framing (E2). The appreciation composite (E3) is
    a multiplicative product: tolerance x familiarity gates pleasure.

    Cheung et al. (2019): Uncertainty and surprise jointly predict
    musical pleasure and amygdala/hippocampus/auditory cortex activity.
    NAcc BOLD correlates with subjective pleasure (beta=0.242, fMRI,
    N=39). Goldilocks surface: intermediate complexity maximises
    enjoyment.

    Gold et al. (2019): Mere exposure increases liking of initially
    disliked atonal music. 8 repetitions shift preference by d=0.42
    for atonal excerpts (N=40, behavioral).

    Huang et al. (2016): Artistic framing (vs popular) increases
    aesthetic appreciation of dissonant/complex music. PCC/mPFC/arMFC
    show greater activation for artistic framing (fMRI, N=21).

    Upstream reads:
        PUPF (12D) -- goldilocks_zone at index 6
        VMM  (12D) -- mode_signal at index 1

    Downstream feeds:
        -> atonal_appreciation belief (Anticipation)
    """

    NAME = "MAA"
    FULL_NAME = "Musical Appreciation of Atonality"
    UNIT = "PCU"
    FUNCTION = "F5"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("PUPF", "VMM")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:complexity_tolerance", "E1:familiarity_index",
             "E2:framing_effect", "E3:appreciation_composite"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:pattern_search", "P1:context_assessment",
             "P2:aesthetic_evaluation"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:appreciation_growth", "F1:pattern_recognition",
             "F2:aesthetic_development"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MAA_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:complexity_tolerance", "E1:familiarity_index",
            "E2:framing_effect", "E3:appreciation_composite",
            "P0:pattern_search", "P1:context_assessment",
            "P2:aesthetic_evaluation",
            "F0:appreciation_growth", "F1:pattern_recognition",
            "F2:aesthetic_development",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Right Heschl's Gyrus -- heightened response under uncertainty
            RegionLink("E0:complexity_tolerance", "Right_Heschls_Gyrus", 0.75,
                       "Bianco 2020"),
            # NAcc -- uncertainty encoding, pleasure signal
            RegionLink("E3:appreciation_composite", "NAcc", 0.80,
                       "Cheung 2019"),
            # mPFC -- aesthetic framing (artistic > popular)
            RegionLink("E2:framing_effect", "mPFC", 0.70,
                       "Huang 2016"),
            # PCC -- self-referential aesthetic processing
            RegionLink("P2:aesthetic_evaluation", "PCC", 0.65,
                       "Huang 2016"),
            # arMFC -- artistic framing modulation
            RegionLink("P1:context_assessment", "arMFC", 0.65,
                       "Huang 2016"),
            # Temporal Cortex -- 1/f scaling mediates pleasure
            RegionLink("E1:familiarity_index", "Temporal_Cortex", 0.70,
                       "Gold 2019"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # MAA is predictive-coding based, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Cheung et al.", 2019,
                         "Uncertainty and surprise jointly predict musical "
                         "pleasure and amygdala, hippocampus, auditory cortex "
                         "activity; NAcc BOLD correlates with subjective "
                         "pleasure (beta=0.242); Goldilocks surface: "
                         "intermediate complexity maximises enjoyment",
                         "fMRI, N=39"),
                Citation("Gold et al.", 2019,
                         "Mere exposure increases liking of initially "
                         "disliked atonal music; 8 repetitions shift "
                         "preference by d=0.42 for atonal excerpts",
                         "behavioral, N=40"),
                Citation("Huang et al.", 2016,
                         "Artistic framing (vs popular) increases aesthetic "
                         "appreciation of dissonant/complex music; PCC/mPFC/"
                         "arMFC show greater activation for artistic framing",
                         "fMRI, N=21"),
                Citation("Mencke et al.", 2019,
                         "Musical training modulates sensitivity to stylistic "
                         "uncertainty; musicians show higher complexity "
                         "tolerance",
                         "behavioral + EEG, N=30"),
                Citation("Bianco et al.", 2020,
                         "Sensory precision increases along auditory hierarchy; "
                         "Right Heschl's Gyrus shows heightened response under "
                         "tonal uncertainty",
                         "MEG, N=24"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Appreciation composite (E3) must be multiplicative: if "
                "complexity tolerance (E0) or familiarity (E1) is near zero, "
                "E3 should collapse toward zero; if additive model fits "
                "better, multiplicative gating is invalid",
                "Familiarity index (E1) must increase with repeated exposure "
                "to atonal material; if mere exposure has no effect on liking "
                "of atonal excerpts, the exposure pathway is unnecessary "
                "(contradicts Gold 2019: d=0.42 after 8 repetitions)",
                "Framing effect (E2) must differ between artistic and popular "
                "context; if no framing difference in aesthetic appreciation, "
                "cognitive framing pathway is invalid (Huang 2016: mPFC/PCC "
                "activation difference)",
                "Complexity tolerance (E0) must follow inverted-U shape "
                "(Goldilocks surface); if linear or monotone, the predictive "
                "coding model is invalid (Cheung 2019: beta=0.242 NAcc)",
                "Pattern search (P0) should be elevated for atonal vs tonal "
                "music; if tonal and atonal music produce equal P0, the "
                "uncertainty-driven search mechanism is unnecessary "
                "(Bianco 2020: Right Heschl's heightened response)",
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
        """Transform R3/H3 + upstream into 10D atonal appreciation output.

        Delegates to 3 layer functions (extraction -> cognitive_present
        -> forecast) and stacks results. No M-layer (3-layer structure).

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: Dict mapping nucleus NAME -> routable output.
                              Reads PUPF (12D) and VMM (12D).

        Returns:
            ``(B, T, 10)`` -- E(4) + P(3) + F(3)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        p = compute_cognitive_present(h3_features, r3_features, e,
                                      upstream_outputs)
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
