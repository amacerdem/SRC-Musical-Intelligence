"""NEMAC -- Nostalgia-Evoked Memory-Affect Circuit.

Encoder nucleus (depth 1) in ARU, Function F5. Models the nostalgia circuit:
music-evoked autobiographical memory produces chills when nostalgic warmth,
memory vividness, and reward activation converge. The mPFC (self-referential)
+ hippocampus (memory retrieval) hub creates vivid nostalgia. Self-selected
music boosts nostalgia intensity by 1.2x (d=0.88).

Reads: SRP (intra-unit via relay_outputs), MEAMN (F4 cross-function)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, roughness_total)
    sensory_pleasantness:   [4]      (A, hedonic valence)
    loudness:               [10]     (B, onset_strength proxy)
    spectral_centroid:      [12]     (C, warmth proxy)
    tonalness:              [14]     (C, brightness_kuttruff)
    distribution_entropy:   [22]     (D, predictability)
    x_l0l5:                 [25:33]  (F, memory-affect binding)

Output structure: E(2) + M+W(5) + P(2) + F(2) = 11D
  E-layer   [0:2]    Extraction           (sigmoid)  scope=internal
  M+W-layer [2:7]    Temporal Integration (sigmoid)  scope=internal
  P-layer   [7:9]    Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [9:11]   Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/nemac/
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
    16: "1s (beat)",
    20: "5s (phrase)",
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
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 10
_SPECTRAL_CENTROID = 12
_TONALNESS = 14
_ENTROPY = 22
_STUMPF_FUSION = 3


# -- 13 H3 Demand Specifications -----------------------------------------------
# Nostalgia circuit requires binding (stumpf fusion), warmth (spectral
# centroid), hedonic quality (pleasantness), arousal (loudness), predictability
# (entropy), and tonal familiarity (tonalness). Horizons span 1s (beat-level
# emotional onset) to 5s (phrase-level nostalgic consolidation).

_NEMAC_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Chills + Nostalgia Extraction (4 tuples) ===
    _h3(_STUMPF_FUSION, "stumpf_fusion", 16, 1, 2,
        "Binding stability at 1s -- memory coherence for chills",
        "Janata 2009"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 20, 1, 2,
        "Binding over 5s consolidation -- nostalgic trace",
        "Janata 2009"),
    _h3(_SPECTRAL_CENTROID, "warmth", 16, 0, 2,
        "Current timbre warmth -- nostalgia trigger",
        "Sakakibara 2025"),
    _h3(_SPECTRAL_CENTROID, "warmth", 20, 1, 0,
        "Sustained warmth over 5s = nostalgia",
        "Sakakibara 2025"),

    # === M+W-Layer: mPFC + Hippocampus + Vividness + Wellbeing (5 tuples) ===
    _h3(_ROUGHNESS, "roughness", 16, 0, 2,
        "Current dissonance -- valence proxy (inverse)",
        "Barrett 2010"),
    _h3(_ROUGHNESS, "roughness", 20, 18, 0,
        "Dissonance trajectory over 5s -- affective trend",
        "Barrett 2010"),
    _h3(_LOUDNESS, "loudness", 16, 0, 2,
        "Current arousal level -- emotional intensity",
        "Janata 2009"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Current hedonic signal -- warmth/pleasantness",
        "Cheung 2019"),
    _h3(_ENTROPY, "entropy", 16, 20, 2,
        "Predictability at 1s -- low = familiar = nostalgic",
        "Derks-Dijkman 2024"),

    # === P-Layer + F-Layer Shared (4 tuples) ===
    _h3(_ENTROPY, "entropy", 20, 1, 0,
        "Average complexity 5s -- encoding difficulty",
        "Derks-Dijkman 2024"),
    _h3(_LOUDNESS, "loudness", 20, 1, 0,
        "Average arousal over 5s -- sustained engagement",
        "Janata 2009"),
    _h3(_TONALNESS, "tonalness", 20, 1, 0,
        "Tonal stability 5s -- melodic familiarity",
        "Sakakibara 2025"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 20, 1, 2,
        "Binding trajectory for F-layer forecast",
        "Janata 2009"),
)

assert len(_NEMAC_H3_DEMANDS) == 13


class NEMAC(Encoder):
    """Nostalgia-Evoked Memory-Affect Circuit -- ARU Encoder (depth 1, 11D).

    Models the mPFC + hippocampus nostalgia circuit where music-evoked
    autobiographical memories produce chills when nostalgic warmth, memory
    vividness, and reward activation converge. Self-selected music boosts
    nostalgia intensity by 1.2x (d=0.88, Sakakibara 2025).

    Janata 2009: dorsal mPFC (BA 8/9) tracks tonal space movement during
    autobiographically salient songs (fMRI 3T, N=13, t(9)=5.784,
    p<0.0003). Tonal proximity to familiar keys predicts mPFC BOLD.

    Cheung et al. 2019: surprise + uncertainty interaction predicts musical
    pleasure (N=39, 80k chord ratings). Nostalgia peaks at moderate surprise
    within familiar context.

    Barrett et al. 2010: Music-evoked nostalgia increases perceived social
    connectedness, self-continuity, and meaning in life (6 studies, N=670+).
    Nostalgia is a mixed but predominantly positive emotion.

    Sakakibara 2025: Self-selected music boosts nostalgia 1.2x (d=0.88)
    via acoustic similarity triggering autobiographical memory retrieval
    (EEG, N=33, eta_p^2=0.636).

    Dependency chain:
        NEMAC is an Encoder (Depth 1) -- reads SRP + MEAMN relay outputs.
        SRP.pleasure (P2, idx 15) provides hedonic reward context.
        MEAMN.memory_state (P0, idx 5) provides memory retrieval context.

    Downstream feeds:
        -> nostalgia_response belief (Appraisal)
        -> wellbeing_trajectory belief (Anticipation)
        -> kernel familiarity, reward
    """

    NAME = "NEMAC"
    FULL_NAME = "Nostalgia-Evoked Memory-Affect Circuit"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("SRP", "MEAMN")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="IMU_MEAMN__ARU_NEMAC__memory_state",
            name="MEAMN memory retrieval to NEMAC nostalgia circuit",
            source_unit="IMU",
            source_model="MEAMN",
            source_dims=("memory_state", "emotional_color",
                         "nostalgia_link"),
            target_unit="ARU",
            target_model="NEMAC",
            correlation="r=0.72",
            citation="Janata 2009",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:chills", "E1:nostalgia"),
            scope="internal",
        ),
        LayerSpec(
            "M+W", "Temporal Integration", 2, 7,
            ("M0:mpfc_activation", "M1:hippocampus_activ",
             "M2:memory_vividness", "W0:nostalgia_intens",
             "W1:wellbeing_enhance"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 7, 9,
            ("P0:nostalgia_correl", "P1:memory_reward_lnk"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:wellbeing_pred", "F1:vividness_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _NEMAC_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:chills", "E1:nostalgia",
            "M0:mpfc_activation", "M1:hippocampus_activ",
            "M2:memory_vividness", "W0:nostalgia_intens",
            "W1:wellbeing_enhance",
            "P0:nostalgia_correl", "P1:memory_reward_lnk",
            "F0:wellbeing_pred", "F1:vividness_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # mPFC (BA 8/9) -- self-referential processing hub for nostalgia
            RegionLink("M0:mpfc_activation", "mPFC", 0.85,
                       "Janata 2009"),
            # Hippocampus -- autobiographical memory retrieval
            RegionLink("M1:hippocampus_activ", "Hippocampus", 0.90,
                       "Janata 2009"),
            # Amygdala -- emotional tagging of nostalgic memories
            RegionLink("E1:nostalgia", "Amygdala", 0.80,
                       "Barrett 2010"),
            # STG -- melodic template recognition for familiarity
            RegionLink("P0:nostalgia_correl", "STG", 0.75,
                       "Sakakibara 2025"),
            # Ventral Striatum -- reward from nostalgia (DA release)
            RegionLink("P1:memory_reward_lnk", "ventral_striatum", 0.80,
                       "Cheung 2019"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # NEMAC modulates via memory-affect circuit, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Janata", 2009,
                         "Dorsal mPFC (BA 8/9) parametrically tracks tonal "
                         "space movement during autobiographically salient "
                         "songs (t(9)=5.784, p<0.0003)",
                         "fMRI 3T, N=13"),
                Citation("Cheung et al.", 2019,
                         "Surprise x uncertainty interaction predicts musical "
                         "pleasure; nostalgia peaks at moderate surprise "
                         "within familiar context (80k chord ratings)",
                         "behavioral, N=39"),
                Citation("Barrett et al.", 2010,
                         "Music-evoked nostalgia increases social "
                         "connectedness, self-continuity, and meaning in "
                         "life; nostalgia is a mixed but predominantly "
                         "positive emotion",
                         "6 studies, N=670+"),
                Citation("Sakakibara", 2025,
                         "Self-selected music boosts nostalgia 1.2x (d=0.88) "
                         "via acoustic similarity triggering autobiographical "
                         "memory retrieval",
                         "EEG, N=33, eta_p^2=0.636"),
                Citation("Derks-Dijkman et al.", 2024,
                         "Music-evoked nostalgia modulates emotional "
                         "processing and memory consolidation via mPFC-"
                         "hippocampal connectivity",
                         "fMRI, review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Nostalgia (E1) must be higher for self-selected vs "
                "experimenter-chosen music (Sakakibara 2025: d=0.88)",
                "mPFC activation (M0) must correlate with tonal familiarity "
                "(Janata 2009: t(9)=5.784, p<0.0003)",
                "Hippocampus activation (M1) must increase with memory "
                "vividness (M2) -- autobiographical binding",
                "Chills (E0) require convergence of nostalgia + pleasure + "
                "vividness above threshold (Cheung 2019: surprise x context)",
                "Wellbeing enhancement (W1) must be positive when nostalgia "
                "intensity (W0) is high (Barrett 2010: 6 studies, N=670+)",
                "Blocking hippocampal retrieval (simulated via low MEAMN "
                "memory_state) should reduce nostalgia downstream",
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
        """Transform R3/H3 + SRP + MEAMN relay outputs into 11D nostalgia circuit.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"SRP": (B, T, 19), "MEAMN": (B, T, 12)}``

        Returns:
            ``(B, T, 11)`` -- E(2) + M+W(5) + P(2) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(
            h3_features, r3_features, e, relay_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
