"""TAR -- Therapeutic Affective Resonance.

Associator nucleus (depth 2) in ARU, Function F5. Models the therapeutic
potential of music for anxiety and depression through two interacting
pathways: anxiolytic (slow tempo + high consonance + soft dynamics ->
amygdala downregulation + PNS activation) and antidepressant (positive
valence + moderate energy + reward activation -> striatal DA upregulation).

Upstream reads:
    SRP  (19D) -- pleasure signal (P2, idx 15)
    VMM  (12D) -- valence state (C1, idx 11)
    CLAM (11D) -- modulation success (F1, idx 10)
    CMAT (10D) -- cross-modal integration (E0, idx 0)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, consonance / anxiety proxy)
    sensory_pleasantness:   [4]      (A, hedonic for reward activation)
    harmonicity:            [5]      (A, harmonic purity for consonance)
    amplitude:              [7]      (B, energy for arousal)
    velocity_A:             [8]      (B, tempo proxy)
    loudness:               [10]     (B, overall arousal level)
    onset_strength:         [11]     (B, rhythmic engagement)
    warmth:                 [16]     (C, comfort / safety signal)
    spectral_flux:          [21]     (D, predictability for stress)
    x_l4l5:                 [33:41]  (G, therapeutic engagement)

Output structure: E(1) + T+I(6) + P(1) + F(2) = 10D
  E-layer   [0:1]    Extraction              (sigmoid)  scope=internal
  T+I-layer [1:7]    Temporal+Integration     (sigmoid)  scope=internal
  P-layer   [7:8]    Present                  (clamp)    scope=hybrid
  F-layer   [8:10]   Forecast                 (sigmoid)  scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
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
from .temporal_integration import compute_temporal_integration

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    6: "200ms (fast)",
    7: "200ms (energy)",
    11: "500ms (phrase)",
    12: "525ms (buildup)",
    15: "800ms (peak)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity", 18: "trend",
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
_HARMONICITY = 5
_AMPLITUDE = 7
_VELOCITY_A = 8
_LOUDNESS = 10
_ONSET = 11
_WARMTH = 16
_SPECTRAL_FLUX = 21


# -- 21 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H6(200ms) -> H7(200ms) -> H11(500ms) -> H12(525ms)
#              -> H15(800ms) -> H16(1s)
# Laws: L0=memory(backward), L2=integration(bidirectional)
#
# E-layer:   5 tuples (fast mood, consonance, arousal, tempo, affect velocity)
# T+I-layer: 8 tuples (mood stability, dissonance trajectory, tempo dynamics)
# P-layer:   4 tuples (cognitive-projection, therapeutic peak, consonance state)
# F-layer:   4 tuples (mood trend, sustained arousal, tempo peak, energy)

_TAR_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Therapeutic State Extraction (5 tuples: #1-5) ===
    _h3(_PLEASANTNESS, "sensory_pleasantness", 6, 0, 2,
        "Pleasantness value 200ms L2 -- fast mood state",
        "Juslin 2013"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Pleasantness value 1s L2 -- slow mood state",
        "Juslin 2013"),
    _h3(_ROUGHNESS, "roughness", 6, 0, 2,
        "Roughness value 200ms L2 -- consonance for anxiety",
        "Koelsch 2014"),
    _h3(_LOUDNESS, "loudness", 6, 0, 2,
        "Loudness value 200ms L2 -- arousal for dynamics",
        "Chanda 2013"),
    _h3(_VELOCITY_A, "velocity_A", 6, 8, 0,
        "Velocity_A velocity 200ms L0 -- tempo proxy",
        "Bernardi 2006"),

    # === T+I-layer: Temporal Integration (8 tuples: #6-13) ===
    _h3(_PLEASANTNESS, "sensory_pleasantness", 6, 8, 0,
        "Pleasantness velocity 200ms L0 -- affect velocity",
        "Juslin 2013"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 2, 0,
        "Pleasantness std 1s L0 -- mood stability",
        "Juslin 2013"),
    _h3(_ROUGHNESS, "roughness", 12, 18, 0,
        "Roughness trend 525ms L0 -- dissonance trajectory",
        "Koelsch 2014"),
    _h3(_ROUGHNESS, "roughness", 15, 18, 0,
        "Roughness trend 800ms L0 -- sustained dissonance",
        "Koelsch 2014"),
    _h3(_VELOCITY_A, "velocity_A", 12, 8, 0,
        "Velocity_A velocity 525ms L0 -- tempo buildup",
        "Bernardi 2006"),
    _h3(_VELOCITY_A, "velocity_A", 12, 18, 0,
        "Velocity_A trend 525ms L0 -- tempo trend",
        "Bernardi 2006"),
    _h3(_LOUDNESS, "loudness", 6, 0, 2,
        "Loudness value 200ms L2 -- current arousal",
        "Chanda 2013"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 11, 1, 0,
        "Pleasantness mean 500ms L0 -- cognitive-projection",
        "Juslin 2013"),

    # === P-layer: Cognitive Present (4 tuples: #14-17) ===
    _h3(_PLEASANTNESS, "sensory_pleasantness", 15, 1, 0,
        "Pleasantness mean 800ms L0 -- peak response magnitude",
        "Sakka 2020"),
    _h3(_ROUGHNESS, "roughness", 16, 0, 2,
        "Roughness value 1s L2 -- current consonance",
        "Koelsch 2014"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 15, 1, 0,
        "Pleasantness mean 800ms L0 -- peak therapeutic response",
        "Sakka 2020"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 18, 0,
        "Pleasantness trend 1s L0 -- mood trend",
        "Juslin 2013"),

    # === F-layer: Forecast (4 tuples: #18-21) ===
    _h3(_ROUGHNESS, "roughness", 15, 18, 0,
        "Roughness trend 800ms L0 -- consonance trajectory stress",
        "Koelsch 2014"),
    _h3(_LOUDNESS, "loudness", 16, 1, 0,
        "Loudness mean 1s L0 -- sustained arousal",
        "Chanda 2013"),
    _h3(_VELOCITY_A, "velocity_A", 15, 8, 0,
        "Velocity_A velocity 800ms L0 -- tempo dynamics peak",
        "Bernardi 2006"),
    _h3(_AMPLITUDE, "amplitude", 7, 8, 0,
        "Amplitude velocity 200ms L0 -- energy change breakthrough",
        "Chanda 2013"),
)

assert len(_TAR_H3_DEMANDS) == 21


class TAR(Associator):
    """Therapeutic Affective Resonance -- ARU Associator (depth 2, 10D).

    Models the therapeutic potential of music for anxiety and depression
    through two interacting pathways:

    Anxiolytic pathway: slow tempo + high consonance + soft dynamics ->
    amygdala downregulation + PNS activation. Music with slow tempo
    (<80 BPM), high consonance, and low dynamic variance activates
    parasympathetic nervous system via vagal nerve, reducing cortisol
    and downregulating amygdala threat response.

    Antidepressant pathway: positive valence + moderate energy + reward
    activation -> striatal DA upregulation. Music with positive valence
    and moderate arousal activates NAcc/striatal dopamine circuits,
    improving hedonic tone and reducing anhedonia.

    Chanda & Levitin (2013): Music modulates cortisol, serotonin, DA,
    oxytocin; anxiolytic effects mediated by PNS activation (HRV
    increase, cortisol decrease).

    Koelsch (2014): Music-evoked emotions engage amygdala (threat
    downregulation), hippocampus (contextual processing), and NAcc
    (reward/DA) -- Emotion circuit model for music therapy.

    Bernardi et al. (2006): Tempo is the primary driver of
    cardiovascular response; slow tempo (<80 BPM) reduces HR and BP,
    fast tempo increases sympathetic activation.

    Juslin (2013): BRECVEMA model -- 8 mechanisms for music-evoked
    emotion including brain stem reflex (arousal), evaluative
    conditioning, and rhythmic entrainment.

    Downstream feeds:
        -> therapeutic_efficacy belief (Anticipation)
        -> F10 Clinical meta-layer (primary therapeutic output)
    """

    NAME = "TAR"
    FULL_NAME = "Therapeutic Affective Resonance"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("SRP", "VMM", "CLAM", "CMAT")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 1,
            ("E0:therapeutic",),
            scope="internal",
        ),
        LayerSpec(
            "TI", "Temporal+Integration", 1, 7,
            ("T0:arousal_mod_tgt", "T1:valence_mod_tgt",
             "T2:anxiety_reduction", "T3:depression_improv",
             "I0:rec_tempo_norm", "I1:rec_consonance"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 7, 8,
            ("P0:therapeutic_reward",),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 10,
            ("F0:mood_improv_pred", "F1:stress_reduc_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _TAR_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:therapeutic",
            "T0:arousal_mod_tgt", "T1:valence_mod_tgt",
            "T2:anxiety_reduction", "T3:depression_improv",
            "I0:rec_tempo_norm", "I1:rec_consonance",
            "P0:therapeutic_reward",
            "F0:mood_improv_pred", "F1:stress_reduc_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Amygdala -- anxiety downregulation target
            RegionLink("E0:therapeutic", "amygdala", 0.80,
                       "Koelsch 2014"),
            # Amygdala -- anxiolytic pathway modulation
            RegionLink("T2:anxiety_reduction", "amygdala", 0.85,
                       "Koelsch 2014"),
            # NAcc / Striatum -- antidepressant DA upregulation
            RegionLink("T3:depression_improv", "NAcc", 0.80,
                       "Chanda 2013"),
            # NAcc -- reward activation from therapeutic music
            RegionLink("P0:therapeutic_reward", "NAcc", 0.75,
                       "Chanda 2013"),
            # Hypothalamus -- cortisol reduction via PNS
            RegionLink("T0:arousal_mod_tgt", "hypothalamus", 0.70,
                       "Bernardi 2006"),
            # PNS / Vagal Nerve -- parasympathetic calming
            RegionLink("T1:valence_mod_tgt", "vagal_nerve", 0.75,
                       "Bernardi 2006"),
            # Hypothalamus -- stress hormone regulation
            RegionLink("F1:stress_reduc_pred", "hypothalamus", 0.65,
                       "Chanda 2013"),
            # Striatum -- DA trajectory for mood improvement
            RegionLink("F0:mood_improv_pred", "striatum", 0.70,
                       "Koelsch 2014"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # DA -- antidepressant pathway via NAcc
            NeuroLink("T3:depression_improv", "DA", 0.75,
                      "Chanda 2013"),
            # Cortisol (inverted) -- anxiolytic pathway
            NeuroLink("T2:anxiety_reduction", "cortisol", -0.70,
                      "Chanda 2013"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Chanda & Levitin", 2013,
                         "Music modulates cortisol, serotonin, dopamine, "
                         "oxytocin; anxiolytic effects mediated by PNS "
                         "activation (HRV increase, cortisol decrease); "
                         "meta-analysis of music therapy RCTs",
                         "meta-analysis + review"),
                Citation("Koelsch", 2014,
                         "Music-evoked emotions engage amygdala (threat "
                         "downregulation), hippocampus (contextual memory), "
                         "NAcc (reward/DA); emotion circuit model for music "
                         "therapy applications",
                         "review, fMRI evidence"),
                Citation("Bernardi et al.", 2006,
                         "Tempo primary driver of cardiovascular response; "
                         "slow tempo (<80 BPM) reduces HR and BP, fast "
                         "tempo increases sympathetic activation; pause "
                         "enhances relaxation response",
                         "experimental, N=24"),
                Citation("Juslin", 2013,
                         "BRECVEMA model: 8 mechanisms for music-evoked "
                         "emotion including brain stem reflex, evaluative "
                         "conditioning, rhythmic entrainment, and aesthetic "
                         "judgment",
                         "theoretical framework"),
                Citation("Sakka & Juslin", 2018,
                         "Emotion regulation via music: selection and "
                         "modification strategies engage different "
                         "neural pathways; therapeutic potential for "
                         "anxiety and depression",
                         "experimental, N=156"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Anxiolytic pathway (T2) must require slow tempo + high "
                "consonance + soft dynamics; if fast tempo alone reduces "
                "anxiety equally, the tempo-consonance interaction is "
                "invalid (Bernardi 2006: tempo drives cardiovascular)",
                "Antidepressant pathway (T3) must correlate with striatal "
                "DA activation; if NAcc shows no differential response to "
                "positive-valence music vs neutral, the DA upregulation "
                "claim is invalid (Chanda 2013)",
                "Therapeutic reward (P0) must be multiplicative across "
                "pleasure and anxiety reduction; if additive model fits "
                "better, gating mechanism is unsupported",
                "Recommended tempo (I0) and consonance (I1) must predict "
                "actual anxiety/depression improvement; if recommendations "
                "show no correlation with outcomes, adaptive pathway fails",
                "Amygdala downregulation (E0) should correlate with "
                "consonance and low arousal; if dissonant loud music "
                "produces equal amygdala reduction, the model is invalid "
                "(Koelsch 2014: consonance-emotion circuit)",
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
        """Transform R3/H3 + upstream into 10D therapeutic affective output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: Dict mapping nucleus NAME -> routable output.
                SRP (19D), VMM (12D), CLAM (11D), CMAT (10D).

        Returns:
            ``(B, T, 10)`` -- E(1) + T+I(6) + P(1) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        ti = compute_temporal_integration(
            h3_features, r3_features, e, upstream_outputs,
        )
        p = compute_cognitive_present(
            h3_features, r3_features, e, ti, upstream_outputs,
        )
        f = compute_forecast(h3_features, e, ti, p)

        output = torch.stack([*e, *ti, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
