"""MEAMN -- Music-Evoked Autobiographical Memory Network.

Relay nucleus (depth 0) in IMU, Function F4. Models how music evokes
autobiographical memories via the hippocampus-mPFC-PCC hub. Familiar
musical patterns bind to personal history, producing vivid memory retrieval
when acoustic features trigger the MEAMN circuit.

Dependency chain:
    MEAMN is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:              [0]  -> [0]    (A, roughness)
    stumpf_fusion:          [3]  -> [3]    (A, stumpf_fusion)
    sensory_pleasantness:   [4]  -> [4]    (A, sensory_pleasantness)
    amplitude:              [7]  -> [7]    (A, velocity_A)
    loudness:               [10] -> [10]   (B, onset_strength)
    warmth:                 [12] -> [12]   (C, warmth)
    tonalness:              [14] -> [14]   (C, brightness_kuttruff)
    entropy:                [22] -> [22]   (D, unchanged)
    x_l0l5:                 [25:33]        (F, coupling)
    x_l5l7:                 [41:49]        (H, coupling)

Output structure: E(3) + M(2) + P(3) + F(4) = 12D
  E-layer [0:3]   Extraction    (sigmoid)    scope=internal
  M-layer [3:5]   Memory        (sigmoid)    scope=internal
  P-layer [5:8]   Present       (sigmoid)    scope=hybrid
  F-layer [8:12]  Forecast      (sigmoid)    scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/meamn/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Relay
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
    16: "1000ms (beat)",
    20: "5000ms (phrase)",
    24: "36000ms (section)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 4: "max", 8: "velocity",
    18: "trend", 19: "stability",
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


# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0               # A group
_STUMPF_FUSION = 3           # A group
_SENSORY_PLEASANTNESS = 4    # A group
_AMPLITUDE = 7               # A group (velocity_A)
_LOUDNESS = 10               # B group (onset_strength)
_WARMTH = 12                 # C group
_TONALNESS = 14              # C group (brightness_kuttruff)
_ENTROPY = 22                # D group


# -- 19 H3 Demand Specifications ----------------------------------------------
# Multi-scale: H16(1s) -> H20(5s) -> H24(36s)

_MEAMN_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Binding + Warmth + Roughness + Loudness (7 tuples) ===
    _h3(_STUMPF_FUSION, "stumpf_fusion", 16, 1, 2,
        "Binding stability at 1s — memory coherence",
        "Janata 2009"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 20, 1, 0,
        "Binding over 5s consolidation — memory trace",
        "Janata 2009"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 24, 1, 0,
        "Long-term binding context 36s — deep memory",
        "Barrett 2010"),
    _h3(_WARMTH, "warmth", 16, 0, 2,
        "Current timbre warmth — nostalgia trigger",
        "Sakakibara 2025"),
    _h3(_WARMTH, "warmth", 20, 1, 0,
        "Sustained warmth = nostalgia over 5s",
        "Sakakibara 2025"),
    _h3(_ROUGHNESS, "roughness", 16, 0, 2,
        "Current dissonance — valence proxy (inverse)",
        "Context-dependent 2021"),
    _h3(_ROUGHNESS, "roughness", 20, 18, 0,
        "Dissonance trajectory over 5s — affective trend",
        "Context-dependent 2021"),

    # === M-layer: Pleasantness + Loudness + Entropy + Amplitude (6 tuples) ===
    _h3(_LOUDNESS, "loudness", 16, 0, 2,
        "Current arousal level — encoding strength",
        "Janata 2009"),
    _h3(_LOUDNESS, "loudness", 20, 1, 0,
        "Average arousal over 5s — sustained engagement",
        "Derks-Dijkman 2024"),
    _h3(_LOUDNESS, "loudness", 24, 2, 0,
        "Arousal variability over 36s — self-referential buildup",
        "Janata 2009"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Current pleasantness — memory valence",
        "Janata 2009"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 20, 18, 0,
        "Pleasantness trajectory over 5s — reward trend",
        "Janata 2007"),

    # === M-layer continued: Entropy + Amplitude (3 tuples) ===
    _h3(_ENTROPY, "entropy", 16, 0, 2,
        "Current unpredictability — familiarity inverse",
        "Derks-Dijkman 2024"),
    _h3(_ENTROPY, "entropy", 20, 1, 0,
        "Average complexity over 5s — encoding difficulty",
        "Derks-Dijkman 2024"),
    _h3(_ENTROPY, "entropy", 24, 19, 0,
        "Pattern stability over 36s — familiarity trajectory",
        "Tulving 2002"),
    _h3(_AMPLITUDE, "amplitude", 16, 8, 0,
        "Energy change rate — arousal dynamics",
        "Janata 2009"),

    # === P-layer + F-layer: Tonalness + Amplitude max (3 tuples) ===
    _h3(_AMPLITUDE, "amplitude", 20, 4, 0,
        "Peak energy over 5s — vividness trajectory",
        "Janata 2009"),
    _h3(_TONALNESS, "tonalness", 16, 0, 2,
        "Melodic recognition state — tonal clarity",
        "Sakakibara 2025"),
    _h3(_TONALNESS, "tonalness", 20, 1, 0,
        "Tonal stability over 5s — melodic familiarity",
        "Sakakibara 2025"),
)

assert len(_MEAMN_H3_DEMANDS) == 19


class MEAMN(Relay):
    """Music-Evoked Autobiographical Memory Network -- IMU Relay (depth 0, 12D).

    Models how music evokes autobiographical memories via the
    hippocampus-mPFC-PCC hub. Janata 2009: dorsal MPFC (BA 8/9)
    parametrically tracks tonal space movement during autobiographically
    salient songs (fMRI 3T, N=13, t(9)=5.784, p<0.0003). Sakakibara 2025:
    acoustic similarity alone triggers nostalgia (EEG, N=33, eta_p^2=0.636).

    Dependency chain:
        MEAMN is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> familiarity computation (memory_state, nostalgia_link)
        -> reward: emotion component (emotional_color)
        -> F5 Emotion: emotional trajectory (emo_response_fc)
        -> precision engine: pi_pred (self_ref_fc)
        -> MEAMN relay wrapper in scheduler
    """

    NAME = "MEAMN"
    FULL_NAME = "Music-Evoked Autobiographical Memory Network"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:f01_retrieval", "E1:f02_nostalgia",
             "E2:f03_emotion"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:meam_retrieval", "M1:p_recall"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 8,
            ("P0:memory_state", "P1:emotional_color",
             "P2:nostalgia_link"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 12,
            ("F0:mem_vividness_fc", "F1:emo_response_fc",
             "F2:self_ref_fc", "F3:reserved"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MEAMN_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:f01_retrieval", "E1:f02_nostalgia",
            "E2:f03_emotion",
            "M0:meam_retrieval", "M1:p_recall",
            "P0:memory_state", "P1:emotional_color",
            "P2:nostalgia_link",
            "F0:mem_vividness_fc", "F1:emo_response_fc",
            "F2:self_ref_fc", "F3:reserved",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Hippocampus — autobiographical binding hub
            RegionLink("P0:memory_state", "Hippocampus", 0.90,
                       "Janata 2009"),
            # mPFC — self-referential retrieval
            RegionLink("E0:f01_retrieval", "mPFC", 0.85,
                       "Janata 2009"),
            # PCC — episodic recollection
            RegionLink("P1:emotional_color", "PCC", 0.75,
                       "Barrett 2010"),
            # Amygdala — emotional tagging of memories
            RegionLink("E2:f03_emotion", "Amygdala", 0.80,
                       "Sakakibara 2025"),
            # STG — melodic template storage
            RegionLink("P2:nostalgia_link", "STG", 0.75,
                       "Sakakibara 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Janata", 2009,
                         "Dorsal MPFC parametrically tracks autobiographical "
                         "salience during music listening",
                         "fMRI 3T, N=13"),
                Citation("Sakakibara", 2025,
                         "Nostalgia Brain-Music Interface — acoustic "
                         "similarity triggers nostalgia",
                         "EEG, N=33"),
                Citation("Janata", 2007,
                         "30-80% MEAM trigger rate with popular music; "
                         "reminiscence bump ages 10-30",
                         "behavioral, N~300"),
                Citation("Derks-Dijkman", 2024,
                         "28/37 studies show musical mnemonics improve "
                         "memory",
                         "systematic review, 37 studies"),
                Citation("Barrett", 2010,
                         "Music-evoked nostalgia modulated by arousal, "
                         "valence, and personality",
                         "behavioral"),
                Citation("Tulving", 2002,
                         "Episodic memory requires coherent feature binding",
                         "review"),
                Citation("Context-dependent", 2021,
                         "Multimodal integration in STS and hippocampus",
                         "fMRI, N=84"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Music-evoked autobiographical memories require familiar "
                "music (Janata 2009: MPFC tracks only autobiographically "
                "salient songs)",
                "Nostalgia requires acoustic similarity to past exposure "
                "(Sakakibara 2025: eta_p^2=0.636)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 12D autobiographical memory representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 12)`` — E(3) + M(2) + P(3) + F(4)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
