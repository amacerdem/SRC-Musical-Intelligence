"""MAA — Multifactorial Atonal Appreciation.

Hub nucleus (depth 4, reads all upstream) in PCU, Function F2. Models how
appreciation of atonal music emerges from the interaction of personality
(openness to experience), aesthetic framing, and exposure/familiarity.

Dependency chain:
    PWUP (upstream) ──→ MAA
    UDP  (upstream) ──→ MAA
    IGFE (upstream) ──→ MAA
    MAA is a Hub (Depth 4) — reads R³/H³ + all upstream outputs.

R3 Ontology Mapping (97D freeze):
    roughness:           [0]     (A, dissonance level)
    sensory_pleasantness:[4]     (A, consonance proxy)
    periodicity:         [5]     (A, tonal certainty)
    tonalness:           [14]    (C, key clarity / atonality index)
    tristimulus1-3:      [18:21] (C, harmonic structure)
    spectral_change:     [21]    (D, structural complexity)

Output structure: E(2) + M(2) + P(3) + F(3) = 10D
  E-layer [0:2]  Extraction  (sigmoid)  scope=internal
  M-layer [2:4]  Memory      (sigmoid)  scope=internal
  P-layer [4:7]  Present     (sigmoid)  scope=hybrid
  F-layer [7:10] Forecast    (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/maa/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Hub
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
    3: "100ms (alpha-beta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 18: "trend", 20: "entropy",
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
_ROUGHNESS = 0            # roughness (A group, dissonance level)
_SENSORY_PLEAS = 4        # sensory_pleasantness (A group, consonance proxy)
_PERIODICITY = 5          # periodicity (A group, tonal certainty)
_TONALNESS = 14           # tonalness (C group, key clarity / atonality index)
_H_COUPLING = 41          # H_coupling (H group)
_SPECTRAL_CHANGE = 21     # spectral_change (D group, structural complexity)


# -- 14 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H3(100ms) -> H8(500ms) -> H16(1s)

_MAA_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Sensory Pleasantness / Consonance proxy (3 tuples) ===
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 3, 0, 2,
        "Consonance at 100ms — immediate aesthetic evaluation",
        "McDermott 2010"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 1, 0,
        "Mean consonance over 1s — sustained pleasantness context",
        "Brattico 2013"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 20, 0,
        "Consonance entropy over 1s — harmonic variety in atonal passage",
        "Berlyne 1971"),

    # === Tonalness / Atonality index (2 tuples) ===
    _h3(_TONALNESS, "tonalness", 8, 1, 0,
        "Mean tonalness over 500ms — tonal anchoring strength",
        "Brattico 2013"),
    _h3(_TONALNESS, "tonalness", 16, 1, 0,
        "Mean tonalness over 1s — sustained tonal clarity context",
        "Greenberg 2015"),

    # === Roughness / Dissonance (2 tuples) ===
    _h3(_ROUGHNESS, "roughness", 3, 0, 2,
        "Roughness at 100ms — immediate dissonance level",
        "McDermott 2010"),
    _h3(_ROUGHNESS, "roughness", 16, 1, 0,
        "Mean roughness over 1s — sustained dissonance context",
        "Brattico 2013"),

    # === Spectral Change / Structural complexity (2 tuples) ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 1, 0,
        "Mean spectral change over 500ms — structural complexity rate",
        "Hargreaves 1984"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 20, 0,
        "Spectral change entropy over 1s — distributional complexity",
        "Berlyne 1971"),

    # === Periodicity / Tonal certainty (1 tuple) ===
    _h3(_PERIODICITY, "periodicity", 16, 1, 0,
        "Mean periodicity over 1s — tonal certainty baseline",
        "Greenberg 2015"),

    # === H_coupling / Cross-band integration (4 tuples) ===
    _h3(_H_COUPLING, "H_coupling", 8, 0, 0,
        "H_coupling at 500ms — cross-band integration value",
        "Brattico 2013"),
    _h3(_H_COUPLING, "H_coupling", 16, 1, 0,
        "H_coupling mean over 1s — sustained integration context",
        "Hargreaves 1984"),
    _h3(_H_COUPLING, "H_coupling", 16, 20, 0,
        "H_coupling entropy over 1s — integration variety",
        "Berlyne 1971"),
    _h3(_H_COUPLING, "H_coupling", 16, 18, 0,
        "H_coupling trend over 1s — appreciation trajectory",
        "Greenberg 2015"),
)

assert len(_MAA_H3_DEMANDS) == 14


class MAA(Hub):
    """Multifactorial Atonal Appreciation — PCU Hub (depth 4, 10D).

    Models how appreciation of atonal music emerges from the interaction
    of personality (openness to experience), aesthetic framing, and
    exposure/familiarity. Atonal appreciation follows an inverted-U curve
    for complexity and grows with repeated exposure and cognitive framing.

    Brattico et al. 2013: aesthetic judgments of music engage mPFC, OFC,
    and cingulate differentially for liked vs disliked (fMRI, N=16).
    Greenberg et al. 2015: openness to experience strongly predicts
    preference for complex/atonal music (N=22,252).
    Hargreaves 1984: inverted-U preference as a function of stimulus
    complexity and familiarity.
    Berlyne 1971: arousal potential determines aesthetic preference
    (foundational theory).
    McDermott et al. 2010: consonance perception is partially learned,
    suggesting plasticity for atonal appreciation (N=64).

    Dependency chain:
        MAA is a Hub (Depth 4) — reads all upstream outputs.
        PWUP → UDP → IGFE → MAA

    Downstream feeds:
        -> atonal_appreciation, aesthetic_flexibility beliefs (Core)
        -> complexity_tolerance, framing_sensitivity beliefs (Appraisal)
        -> appreciation_growth, aesthetic_shift beliefs (Anticipation)
    """

    NAME = "MAA"
    FULL_NAME = "Multifactorial Atonal Appreciation"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 10
    PROCESSING_DEPTH = 4  # Override Hub default
    UPSTREAM_READS = ("PWUP", "UDP", "IGFE")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:complexity_tolerance", "E1:familiarity_index"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 2, 4,
            ("M0:framing_effect", "M1:appreciation_composite"),
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
            "M0:framing_effect", "M1:appreciation_composite",
            "P0:pattern_search", "P1:context_assessment",
            "P2:aesthetic_evaluation",
            "F0:appreciation_growth", "F1:pattern_recognition",
            "F2:aesthetic_development",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # STG — complexity processing / atonal structure parsing
            RegionLink("E0:complexity_tolerance", "STG", 0.75,
                       "Brattico 2013"),
            # mPFC — aesthetic judgment (liked vs disliked)
            RegionLink("P2:aesthetic_evaluation", "MPFC", 0.80,
                       "Brattico 2013"),
            # NAc — reward for acquired atonal appreciation
            RegionLink("M1:appreciation_composite", "NAC", 0.65,
                       "Greenberg 2015"),
            # OFC — aesthetic framing and reappraisal
            RegionLink("M0:framing_effect", "OFC", 0.70,
                       "Brattico 2013"),
            # Hippocampus — familiarity / exposure memory
            RegionLink("E1:familiarity_index", "HIPP", 0.70,
                       "Hargreaves 1984"),
            # Amygdala — affective evaluation of atonal stimuli
            RegionLink("P1:context_assessment", "AMYG", 0.60,
                       "Brattico 2013"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # MAA maps to aesthetic cognition, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Brattico et al.", 2013,
                         "Aesthetic judgments of music engage mPFC, OFC, and "
                         "cingulate; liked vs disliked differentially; "
                         "beauty-related activations in OFC/cingulate",
                         "fMRI, N=16"),
                Citation("Greenberg et al.", 2015,
                         "Openness to experience strongly predicts preference "
                         "for complex/sophisticated music including atonal; "
                         "r=0.35, p<0.001",
                         "Behavioral, N=22,252"),
                Citation("Hargreaves", 1984,
                         "Inverted-U preference as function of subjective "
                         "complexity; familiarity shifts peak rightward; "
                         "review of experimental aesthetics",
                         "Behavioral review"),
                Citation("Berlyne", 1971,
                         "Arousal potential determines aesthetic preference; "
                         "collative variables (novelty, complexity, "
                         "surprisingness) modulate hedonic value",
                         "Foundational theory"),
                Citation("McDermott et al.", 2010,
                         "Consonance perception is partially learned; "
                         "roughness aversion is robust but harmonic "
                         "preference shows cultural variation; N=64",
                         "Behavioral, N=64"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Complexity tolerance should correlate with openness "
                "(testable via personality × preference correlation)",
                "Repeated exposure should increase appreciation for "
                "atonal music (testable via mere exposure paradigm)",
                "Aesthetic framing should shift preference curve "
                "(testable via label/context manipulation)",
                "Inverted-U preference curve for complexity should hold "
                "(testable via parametric complexity variation)",
                "mPFC engagement should differ for appreciated vs "
                "non-appreciated atonal passages "
                "(testable via fMRI aesthetic judgment task)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Transform R³/H³ + upstream into 10D atonal appreciation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"PWUP": (B, T, 10), "UDP": (B, T, 10),
                                 "IGFE": (B, T, 9)}``
            cross_unit_inputs: Unused (no cross-unit reads).

        Returns:
            ``(B, T, 10)`` — E(2) + M(2) + P(3) + F(3)
        """
        e = compute_extraction(r3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(
            r3_features, h3_features, e, m, upstream_outputs,
        )
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
