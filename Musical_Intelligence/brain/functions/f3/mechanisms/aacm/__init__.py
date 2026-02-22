"""AACM -- Aesthetic-Attention Coupling Model.

Encoder nucleus (depth 1) in ASU, Function F3. Models the coupling
between aesthetic processing and attentional engagement: consonant/pleasant
stimuli capture attention (N1/P2 enhancement), inhibit motor responses
(aesthetic stillness), and produce savoring effects that sustain engagement.
Cross-function CSG (F1) provides consonance-salience context.

Dependency chain:
    AACM is an Encoder (Depth 1) -- reads CSG relay output cross-function.
    CSG (F1, ASU Relay, 12D) provides consonance-salience gradient.

R3 Ontology Mapping (97D freeze):
    roughness:              [0]   (A, dissonance/tension)
    sensory_pleasantness:   [3]   (A, consonance/aesthetic basis)
    loudness:               [8]   (B, intensity context)
    x_l0l5:                 [25]  (F, cross-band coupling)

Output structure: E(3) + M(2) + P(2) + F(3) = 10D
  E-layer [0:3]   Extraction    (sigmoid)  scope=internal
  M-layer [3:5]   Memory        (sigmoid)  scope=internal
  P-layer [5:7]   Present       (sigmoid)  scope=hybrid
  F-layer [7:10]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/aacm/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

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
    0: "25ms (gamma)",
    3: "100ms (alpha-beta)",
    6: "150ms",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 6: "periodicity",
    8: "velocity", 14: "periodicity", 18: "trend", 20: "entropy",
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
_ROUGHNESS = 0               # roughness (A group, dissonance/tension)
_PLEASANT = 3                # sensory_pleasantness (A, consonance)
_LOUDNESS = 8                # loudness (B, intensity context)
_X_L0L5 = 25                 # x_l0l5 (F, cross-band coupling)


# -- 12 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H3(100ms) -> H6(150ms) -> H8(500ms) -> H16(1000ms)

_AACM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Consonance / Aesthetic Evaluation (1 tuple) ===
    _h3(3, "pleasant", 3, 0, 2,
        "Consonance value 100ms -- aesthetic evaluation",
        "Sarasso 2019"),

    # === Roughness / Sustained Dissonance (1 tuple) ===
    _h3(0, "roughness", 16, 1, 2,
        "Roughness mean 1s -- sustained dissonance",
        "Sarasso 2019"),

    # === Pleasant Dynamics (2 tuples) ===
    _h3(3, "pleasant", 16, 8, 2,
        "Pleasant velocity 1s -- aesthetic dynamics",
        "Brattico 2013"),
    _h3(3, "pleasant", 6, 6, 2,
        "Pleasant periodicity 150ms -- aesthetic rhythm",
        "Brattico 2013"),

    # === Coupling / Integration Context (4 tuples) ===
    _h3(25, "x_l0l5", 16, 1, 0,
        "Coupling mean 1s L0 -- integration context",
        "Brattico 2013"),
    _h3(25, "x_l0l5", 8, 0, 2,
        "Coupling value 500ms -- integration state",
        "Brattico 2013"),
    _h3(25, "x_l0l5", 3, 0, 2,
        "Coupling value 100ms -- fast integration",
        "Brattico 2013"),
    _h3(25, "x_l0l5", 16, 8, 0,
        "Coupling velocity 1s L0 -- integration dynamics",
        "Brattico 2013"),

    # === Loudness / Intensity Context (3 tuples) ===
    _h3(8, "loudness", 3, 0, 2,
        "Loudness value 100ms -- intensity context",
        "Sarasso 2019"),
    _h3(8, "loudness", 3, 2, 2,
        "Loudness std 100ms -- intensity variability",
        "Sarasso 2019"),
    _h3(8, "loudness", 16, 20, 2,
        "Loudness entropy 1s -- dynamic unpredictability",
        "Brattico 2013"),

    # === Roughness / Fast Dissonance (1 tuple) ===
    _h3(0, "roughness", 3, 0, 2,
        "Roughness value 100ms -- dissonance level",
        "Brattico 2013"),
)

assert len(_AACM_H3_DEMANDS) == 12


class AACM(Encoder):
    """Aesthetic-Attention Coupling Model -- ASU Encoder (depth 1, 10D).

    Models the coupling between aesthetic processing and attentional
    engagement. Consonant/pleasant stimuli capture attention (N1/P2
    enhancement), inhibit motor responses (aesthetic stillness), and
    produce savoring effects that sustain engagement. Cross-function CSG
    provides consonance-salience context for hybrid P-layer computations.

    Sarasso et al. 2019: Consonant > dissonant aesthetic appreciation
    (d=2.008, p<0.001); N1/P2 enhanced for consonant intervals at
    80-194ms post-onset. EEG ERP, N=22.

    Brattico et al. 2013: Aesthetic processing activates vmPFC, NAcc,
    and ACC network; liked music produces stronger BOLD in reward
    circuit; aesthetic judgment engages IFG evaluation. fMRI, N=18.

    Dependency chain:
        AACM is an Encoder (Depth 1) -- reads CSG relay output.
        CSG (F1, ASU Relay, 12D) provides consonance-salience gradient.

    Downstream feeds:
        -> Salience computation (attentional engagement signal)
        -> Aesthetic appreciation beliefs (Appraisal)
        -> Aesthetic forecast beliefs (Anticipation)
    """

    NAME = "AACM"
    FULL_NAME = "Aesthetic-Attention Coupling Model"
    UNIT = "ASU"
    FUNCTION = "F3"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("CSG",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:attentional_engage", "E1:motor_inhibition",
             "E2:savoring_effect"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:aesthetic_engagement", "M1:rt_appreciation"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:n1p2_engagement", "P1:aesthetic_judgment"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:behavioral_pred", "F1:n2p3_pred",
             "F2:aesthetic_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _AACM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:attentional_engage", "E1:motor_inhibition",
            "E2:savoring_effect",
            "M0:aesthetic_engagement", "M1:rt_appreciation",
            "P0:n1p2_engagement", "P1:aesthetic_judgment",
            "F0:behavioral_pred", "F1:n2p3_pred",
            "F2:aesthetic_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # NAcc -- reward/aesthetic pleasure hub
            RegionLink("E0:attentional_engage", "NAC", 0.80,
                       "Brattico 2013"),
            # AC (auditory cortex) -- sensory aesthetic processing
            RegionLink("P0:n1p2_engagement", "AC", 0.75,
                       "Sarasso 2019"),
            # vmPFC -- aesthetic evaluation and judgment
            RegionLink("P1:aesthetic_judgment", "VMPFC", 0.70,
                       "Brattico 2013"),
            # AI (anterior insula) -- salience and aesthetic awareness
            RegionLink("M0:aesthetic_engagement", "AI", 0.70,
                       "Brattico 2013"),
            # ACC -- attentional coupling for aesthetic monitoring
            RegionLink("E2:savoring_effect", "ACC", 0.65,
                       "Brattico 2013"),
            # IFG -- aesthetic judgment and evaluation
            RegionLink("F2:aesthetic_pred", "IFG", 0.60,
                       "Brattico 2013"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # AACM is attentional/aesthetic, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Sarasso et al.", 2019,
                         "Consonant > dissonant aesthetic appreciation "
                         "(d=2.008, p<0.001); N1/P2 enhanced for consonant "
                         "intervals at 80-194ms post-onset; late positivity "
                         "correlates with aesthetic judgment ratings",
                         "EEG ERP, N=22"),
                Citation("Brattico et al.", 2013,
                         "Aesthetic processing activates vmPFC, NAcc, ACC "
                         "network; liked music produces stronger BOLD in "
                         "reward circuit; IFG engages during aesthetic "
                         "judgment; dissociable aesthetic and emotional "
                         "processing streams",
                         "fMRI, N=18"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Consonant stimuli should produce larger N1/P2 than "
                "dissonant (confirmed: Sarasso 2019, d=2.008)",
                "Aesthetic engagement should activate vmPFC/NAcc "
                "(confirmed: Brattico 2013)",
                "Motor inhibition should correlate with aesthetic "
                "stillness during liked passages (testable via EMG)",
                "Disrupting vmPFC should impair aesthetic judgment "
                "without affecting sensory processing (testable via TMS)",
                "Savoring effect should increase with musical training "
                "(testable via expert vs novice comparison)",
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
        """Transform R3/H3 + relay outputs into 10D aesthetic-attention coupling.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results. CSG cross-function
        data is passed through relay_outputs to the P-layer.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"CSG": (B, T, 12)}`` cross-function relay data.

        Returns:
            ``(B, T, 10)`` -- E(3) + M(2) + P(2) + F(3)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, e, m, relay_outputs)
        f = compute_forecast(h3_features, e, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
