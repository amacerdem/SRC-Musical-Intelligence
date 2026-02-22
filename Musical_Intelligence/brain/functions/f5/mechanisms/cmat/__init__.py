"""CMAT -- Cross-Modal Affective Transfer.

Associator nucleus (depth 2) in ARU, Function F5. Models how affective
information transfers between sensory modalities via supramodal
representations. Auditory pitch maps to visual brightness, tempo maps
to arousal, and mode maps to warmth/color temperature. In audio-only
mode, CMAT estimates cross-modal transfer potential from acoustic
features that systematically correspond to other modalities.

Core findings:
  Spence (2011): pitch-brightness mapping r=0.72 (meta, 15 studies,
      N=1200+). High pitch -> bright visual percepts.
  Collier & Hubbard (2001): tempo-arousal mapping r=0.68 (N=60).
      Fast tempo -> high arousal across modalities.
  Palmer et al. (2013): mode-color mapping (emotion-mediated),
      major -> warm/bright colors, minor -> cool/dark (N=30).

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, inverse consonance for valence)
    sensory_pleasantness:   [4]      (A, direct hedonic signal)
    loudness:               [10]     (B, arousal for salience)
    brightness:             [15]     (C, supramodal brightness)
    warmth:                 [16]     (C, supramodal warmth)
    spectral_flux:          [21]     (D, frame-to-frame change)
    x_l0l5:                 [25:33]  (F, supramodal binding substrate)

Output structure: E(1) + S+T(5) + P(2) + F(2) = 10D
  E-layer [0:1]   Extraction     (sigmoid)  scope=internal
  S+T-layer [1:6] Temporal+Integ (sigmoid)  scope=internal
  P-layer [6:8]   Present        (clamp)    scope=hybrid
  F-layer [8:10]  Forecast       (sigmoid)  scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/cmat/
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
    11: "500ms (integration)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    19: "stability", 20: "entropy",
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
_LOUDNESS = 10
_BRIGHTNESS = 15
_WARMTH = 16
_SPECTRAL_FLUX = 21
_ENTROPY = 22


# -- 9 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H6(200ms) -> H11(500ms) -> H16(1s)
# Laws: L0=memory(backward), L2=integration(bidirectional)
#
# E-layer: 3 tuples (fast affect state, instant dissonance, arousal)
# S+T-layer: 3 tuples (affect velocity, integration state/variability)
# P-layer: 1 tuple (binding precision)
# F-layer: 2 tuples (sustained affect, stability for generalization)

_CMAT_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Cross-Modal Extraction (3 tuples) ===
    _h3(_PLEASANTNESS, "sensory_pleasantness", 6, 0, 2,
        "Pleasantness value 200ms L2 -- fast affect state for cross-modal mapping",
        "Spence 2011"),
    _h3(_ROUGHNESS, "roughness", 6, 0, 2,
        "Roughness value 200ms L2 -- instant dissonance for valence inversion",
        "Spence 2011"),
    _h3(_LOUDNESS, "loudness", 6, 0, 2,
        "Loudness value 200ms L2 -- arousal for cross-modal salience",
        "Collier & Hubbard 2001"),

    # === S+T-layer: Temporal Integration (3 tuples) ===
    _h3(_PLEASANTNESS, "sensory_pleasantness", 6, 8, 0,
        "Pleasantness velocity 200ms L0 -- affect velocity for temporal binding",
        "Spence 2011"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 11, 1, 0,
        "Pleasantness mean 500ms L0 -- integration state for supramodal valence",
        "Palmer et al. 2013"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 11, 2, 0,
        "Pleasantness std 500ms L0 -- integration variability for congruence",
        "Palmer et al. 2013"),

    # === P-layer: Cognitive Present (1 tuple) ===
    _h3(_ENTROPY, "distribution_entropy", 16, 20, 2,
        "Entropy entropy 1s L2 -- binding precision for multi-sensory salience",
        "Spence 2011"),

    # === F-layer: Forecast (2 tuples) ===
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Pleasantness value 1s L2 -- sustained affect for coherence prediction",
        "Palmer et al. 2013"),
    _h3(_ENTROPY, "distribution_entropy", 16, 19, 0,
        "Entropy stability 1s L0 -- pattern stability for generalization",
        "Spence 2011"),
)

assert len(_CMAT_H3_DEMANDS) == 9


class CMAT(Associator):
    """Cross-Modal Affective Transfer -- ARU Associator (depth 2, 10D).

    Models supramodal affect representations that transfer between
    sensory modalities. Pitch maps to visual brightness (Spence 2011:
    r=0.72, meta-analysis, 15 studies, N=1200+), tempo maps to arousal
    (Collier & Hubbard 2001: r=0.68, N=60), and mode maps to
    warmth/color temperature (Palmer et al. 2013: emotion-mediated,
    N=30). In audio-only mode, cross-modal transfer potential is
    estimated from acoustic features with known systematic
    correspondences.

    Upstream reads:
        VMM.valence_state (idx 11 of 12D): overall valence context
        AAC.emotional_arousal (idx 0 of 14D): arousal context

    Downstream feeds:
        -> TAR (multi-modal therapeutic effectiveness)
        -> cross_modal_affect belief (Anticipation)
    """

    NAME = "CMAT"
    FULL_NAME = "Cross-Modal Affective Transfer"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("VMM", "AAC")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 1,
            ("E0:cross_modal",),
            scope="internal",
        ),
        LayerSpec(
            "S+T", "Temporal Integration", 1, 6,
            ("S0:supramodal_valence", "S1:supramodal_arousal",
             "S2:cross_modal_bind", "T0:binding_temporal",
             "T1:congruence_streng"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 8,
            ("P0:multi_sens_salien", "P1:aud_valence_contr"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 10,
            ("F0:coherence_pred", "F1:generalization_pr"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _CMAT_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:cross_modal",
            "S0:supramodal_valence", "S1:supramodal_arousal",
            "S2:cross_modal_bind", "T0:binding_temporal",
            "T1:congruence_streng",
            "P0:multi_sens_salien", "P1:aud_valence_contr",
            "F0:coherence_pred", "F1:generalization_pr",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # vmPFC / mOFC -- supramodal affect integration hub
            RegionLink("S0:supramodal_valence", "vmPFC_mOFC", 0.80,
                       "Spence 2011"),
            RegionLink("E0:cross_modal", "vmPFC_mOFC", 0.75,
                       "Palmer et al. 2013"),
            # STS -- temporal binding between modalities
            RegionLink("T0:binding_temporal", "STS", 0.80,
                       "Spence 2011"),
            RegionLink("S2:cross_modal_bind", "STS", 0.75,
                       "Collier & Hubbard 2001"),
            # Auditory Cortex -- auditory affect source
            RegionLink("P1:aud_valence_contr", "auditory_cortex", 0.75,
                       "Spence 2011"),
            # Visual Cortex -- cross-modal target (estimated in audio-only)
            RegionLink("S1:supramodal_arousal", "visual_cortex", 0.65,
                       "Spence 2011"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # CMAT is a mapping mechanism, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Spence", 2011,
                         "Pitch-brightness cross-modal mapping r=0.72 "
                         "(meta-analysis, 15 studies, N=1200+); systematic "
                         "correspondences between auditory pitch and visual "
                         "brightness across cultures and ages",
                         "meta-analysis, N=1200+"),
                Citation("Collier & Hubbard", 2001,
                         "Tempo-arousal cross-modal correspondence r=0.68 "
                         "(N=60); fast tempo maps to high arousal, slow "
                         "tempo to calm/low arousal across modalities",
                         "behavioral, N=60"),
                Citation("Palmer et al.", 2013,
                         "Music-color associations mediated by emotion: "
                         "major/fast -> warm/saturated colors; minor/slow "
                         "-> cool/dark colors; emotion fully mediates the "
                         "music-color pathway (N=30)",
                         "behavioral, N=30"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Cross-modal mapping (E0) must correlate with pitch-brightness "
                "correspondence: if high-pitch music does not produce elevated "
                "brightness estimates, the supramodal mapping is invalid "
                "(Spence 2011: r=0.72)",
                "Supramodal valence (S0) must track VMM.valence_state: if "
                "valence from auditory features does not generalize to "
                "estimated visual brightness/warmth, supramodal representation "
                "claim is invalid",
                "Tempo-arousal link (S1) must correlate with AAC.emotional_"
                "arousal and loudness dynamics: if tempo/loudness changes do "
                "not drive arousal in predicted cross-modal direction, the "
                "correspondence is invalid (Collier & Hubbard 2001: r=0.68)",
                "Congruence strength (T1) must be higher when pitch-brightness "
                "and mode-warmth are aligned than misaligned: incongruent "
                "stimuli should reduce T1 (Spence 2011)",
                "Generalization prediction (F1) must decrease with high "
                "entropy (unstable patterns): if prediction confidence "
                "does not track pattern stability, the forecast is unreliable",
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
        """Transform R3/H3 + upstream into 10D cross-modal affective output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"VMM": (B, T, 12), "AAC": (B, T, 14)}``.

        Returns:
            ``(B, T, 10)`` -- E(1) + S+T(5) + P(2) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        st = compute_temporal_integration(
            h3_features, r3_features, e, upstream_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, st)
        f = compute_forecast(h3_features, e, st, p)

        output = torch.stack([*e, *st, *p, *f], dim=-1)
        assert output.shape[-1] == 10
        return output.clamp(0.0, 1.0)
