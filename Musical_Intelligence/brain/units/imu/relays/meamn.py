"""MEAMN — Music-Evoked Autobiographical Memory Network.

Gold standard Relay nucleus for the Implicit Memory Unit (IMU).

Neural Circuit:
    Audio → STG/A1 (spectrotemporal pattern recognition)
                ↓
              mPFC (BA 8/9, self-referential, tonal space tracking)
                ↓
              Amygdala (emotional tagging, arousal × valence)
                ↓
              Hippocampus + PCC (episodic encoding / retrieval)
                ↓
              Autobiographical Memory + Emotional Coloring

Key Findings:
    - Dorsal MPFC tracks tonal space during autobiographically salient
      songs (Janata 2009, fMRI, t(9)=5.784, p<0.0003)
    - Nostalgia Brain-Music Interface enhances nostalgic feelings
      (Sakakibara 2025, EEG, ηp²=0.636)
    - Musical mnemonics benefit working and episodic memory; AD
      patients retain advantage (Derks-Dijkman 2024, systematic review)
    - Familiar music activates auditory, motor, emotion, and memory
      areas (Scarratt 2025, fMRI, N=57)

Temporal Architecture:
    MEAMN uses long-horizon H³ demands matching memory timescales:
    - H16 (1s):   Encoding — working memory binding
    - H20 (~5s):  Consolidation — hippocampal binding window
    - H24 (~36s): Retrieval — long-term episodic chunk

R³ Remapping (Ontology Freeze v1.0.0):
    - Doc [25:33] "x_l0l5" → Code [42] beat_strength (dissolved)
    - Doc [41:49] "x_l5l7" → Code [60] tonal_stability (dissolved)
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

# ======================================================================
# Scientific constants
# ======================================================================

# Attention weight — autobiographical retrieval strength
# Source: Janata 2009, t(9)=5.784, p<0.0003 (imagery vividness)
ALPHA_ATTENTION: float = 0.80

# Familiarity weight — nostalgia response
# Source: Sakakibara 2025, ηp²=0.636 (nostalgia condition)
BETA_FAMILIARITY: float = 0.70

# Emotional weight — affective coloring
# Source: Janata 2009, t(9)=3.442, p<0.008 (emotional evocation)
GAMMA_EMOTIONAL: float = 0.60


class MEAMN(Relay):
    """Music-Evoked Autobiographical Memory Network — IMU Relay (Depth 0, 12D).

    Models how music uniquely activates autobiographical memory networks,
    engaging hippocampus, medial prefrontal cortex, and temporal regions
    to retrieve personal memories with strong emotional coloring.

    Three components:
        1. RETRIEVAL: Hippocampus + PCC pattern completion
        2. NOSTALGIA: Melodic template match via timbre warmth + contour
        3. EMOTIONAL COLORING: Amygdala affective tagging

    Output Structure (12D):
        E-layer (3D) [0:3]:  Retrieval, nostalgia, emotional coloring
        M-layer (2D) [3:5]:  MEAM retrieval function, recall probability
        P-layer (3D) [5:8]:  Memory state, emotional color, nostalgia link
        F-layer (4D) [8:12]: Vividness, emotional, self-referential, reserved
    """

    NAME = "MEAMN"
    FULL_NAME = "Music-Evoked Autobiographical Memory Network"
    UNIT = "IMU"

    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            code="E", name="Episodic", start=0, end=3,
            dim_names=(
                "retrieval_activation",   # Autobiographical retrieval
                "nostalgia_response",     # Nostalgia intensity
                "emotional_coloring",     # Affective tag strength
            ),
            scope="internal",
        ),
        LayerSpec(
            code="M", name="Model", start=3, end=5,
            dim_names=(
                "meam_retrieval",         # MEAM retrieval function
                "recall_probability",     # P(recall | music)
            ),
            scope="external",
        ),
        LayerSpec(
            code="P", name="Present", start=5, end=8,
            dim_names=(
                "memory_state",           # Current retrieval activation
                "emotional_color",        # Current affective tag
                "nostalgia_link",         # Nostalgia-familiarity warmth
            ),
            scope="external",
        ),
        LayerSpec(
            code="F", name="Future", start=8, end=12,
            dim_names=(
                "mem_vividness_pred",     # Memory vividness 2-5s ahead
                "emo_response_pred",      # Emotional response 1-3s ahead
                "self_referential_pred",  # Self-referential 5-10s ahead
                "reserved",              # Future expansion
            ),
            scope="hybrid",
        ),
    )

    # R³ features (12)
    _R3_ROUGHNESS = 0
    _R3_STUMPF_FUSION = 3
    _R3_SENSORY_PLEASANT = 4
    _R3_AMPLITUDE = 7
    _R3_LOUDNESS = 10
    _R3_ONSET_STRENGTH = 11
    _R3_WARMTH = 12
    _R3_TONALNESS = 14
    _R3_TRISTIMULUS1 = 18
    _R3_DISTRIBUTION_ENTROPY = 22
    _R3_BEAT_STRENGTH = 42         # Replaces dissolved x_l0l5
    _R3_TONAL_STABILITY = 60       # Replaces dissolved x_l5l7

    _EPS: float = 1e-8

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """19 temporal demands at memory-scale horizons."""
        return (
            # --- Stumpf fusion: binding integrity ---
            H3DemandSpec(r3_idx=3, r3_name="stumpf_fusion",
                         horizon=16, horizon_label="1s encoding",
                         morph=1, morph_name="mean", law=2, law_name="integration",
                         purpose="Binding stability at 1s — working memory",
                         citation="Tulving 2002"),
            H3DemandSpec(r3_idx=3, r3_name="stumpf_fusion",
                         horizon=20, horizon_label="5s consolidation",
                         morph=1, morph_name="mean", law=2, law_name="integration",
                         purpose="Binding over 5s — hippocampal consolidation",
                         citation="Janata 2009"),
            H3DemandSpec(r3_idx=3, r3_name="stumpf_fusion",
                         horizon=24, horizon_label="36s retrieval",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Long-term binding context — episodic chunk",
                         citation="Janata 2007"),
            # --- Sensory pleasantness: emotional tagging ---
            H3DemandSpec(r3_idx=4, r3_name="sensory_pleasantness",
                         horizon=16, horizon_label="1s encoding",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current pleasantness for emotional tagging",
                         citation="Scarratt et al. 2025"),
            H3DemandSpec(r3_idx=4, r3_name="sensory_pleasantness",
                         horizon=20, horizon_label="5s consolidation",
                         morph=18, morph_name="trend", law=0, law_name="memory",
                         purpose="Pleasantness trajectory — emotional momentum",
                         citation="Barrett et al. 2010"),
            # --- Loudness: arousal context ---
            H3DemandSpec(r3_idx=10, r3_name="loudness",
                         horizon=16, horizon_label="1s encoding",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current arousal from loudness",
                         citation="Janata 2009"),
            H3DemandSpec(r3_idx=10, r3_name="loudness",
                         horizon=20, horizon_label="5s consolidation",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Average arousal over consolidation window",
                         citation="Scarratt et al. 2025"),
            H3DemandSpec(r3_idx=10, r3_name="loudness",
                         horizon=24, horizon_label="36s retrieval",
                         morph=2, morph_name="std", law=0, law_name="memory",
                         purpose="Arousal variability over episodic chunk",
                         citation="Sakakibara et al. 2025"),
            # --- Warmth: nostalgia trigger ---
            H3DemandSpec(r3_idx=12, r3_name="warmth",
                         horizon=16, horizon_label="1s encoding",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current timbre warmth — nostalgia trigger",
                         citation="Sakakibara et al. 2025"),
            H3DemandSpec(r3_idx=12, r3_name="warmth",
                         horizon=20, horizon_label="5s consolidation",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Sustained warmth — nostalgia maintenance",
                         citation="Sakakibara et al. 2025"),
            # --- Tonalness: melodic recognition ---
            H3DemandSpec(r3_idx=14, r3_name="tonalness",
                         horizon=16, horizon_label="1s encoding",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Melodic recognition state — tonal clarity",
                         citation="Janata 2009"),
            H3DemandSpec(r3_idx=14, r3_name="tonalness",
                         horizon=20, horizon_label="5s consolidation",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Tonal stability over consolidation",
                         citation="Janata 2009"),
            # --- Distribution entropy: pattern complexity ---
            H3DemandSpec(r3_idx=22, r3_name="distribution_entropy",
                         horizon=16, horizon_label="1s encoding",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current pattern complexity — encoding difficulty",
                         citation="Derks-Dijkman et al. 2024"),
            H3DemandSpec(r3_idx=22, r3_name="distribution_entropy",
                         horizon=20, horizon_label="5s consolidation",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Average complexity — familiarity proxy",
                         citation="Derks-Dijkman et al. 2024"),
            H3DemandSpec(r3_idx=22, r3_name="distribution_entropy",
                         horizon=24, horizon_label="36s retrieval",
                         morph=19, morph_name="stability", law=0, law_name="memory",
                         purpose="Pattern stability — low = familiar",
                         citation="Janata 2007"),
            # --- Roughness: valence context ---
            H3DemandSpec(r3_idx=0, r3_name="roughness",
                         horizon=16, horizon_label="1s encoding",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current dissonance — valence proxy",
                         citation="Janata 2009"),
            H3DemandSpec(r3_idx=0, r3_name="roughness",
                         horizon=20, horizon_label="5s consolidation",
                         morph=18, morph_name="trend", law=0, law_name="memory",
                         purpose="Dissonance trajectory — emotional direction",
                         citation="Barrett et al. 2010"),
            # --- Amplitude: energy dynamics ---
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=16, horizon_label="1s encoding",
                         morph=8, morph_name="velocity", law=0, law_name="memory",
                         purpose="Energy change rate — emotional intensity",
                         citation="Scarratt et al. 2025"),
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=20, horizon_label="5s consolidation",
                         morph=4, morph_name="max", law=0, law_name="memory",
                         purpose="Peak energy over consolidation — peak memory",
                         citation="Janata 2009"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "retrieval_activation", "nostalgia_response", "emotional_coloring",
            "meam_retrieval", "recall_probability",
            "memory_state", "emotional_color", "nostalgia_link",
            "mem_vividness_pred", "emo_response_pred",
            "self_referential_pred", "reserved",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            RegionLink(dim_name="retrieval_activation", region="Hippocampus",
                       weight=0.9, citation="Janata 2009"),
            RegionLink(dim_name="self_referential_pred", region="mPFC",
                       weight=0.85, citation="Janata 2009"),
            RegionLink(dim_name="nostalgia_response", region="STG",
                       weight=0.8, citation="Sakakibara et al. 2025"),
            RegionLink(dim_name="emotional_coloring", region="Amygdala",
                       weight=0.8, citation="Janata 2009"),
            RegionLink(dim_name="memory_state", region="PCC",
                       weight=0.7, citation="Janata 2009"),
            RegionLink(dim_name="nostalgia_link", region="Angular_Gyrus",
                       weight=0.6, citation="Scarratt et al. 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            NeuroLink(dim_name="nostalgia_link", channel=0, effect="produce",
                      weight=0.3, citation="Sakakibara et al. 2025"),
            NeuroLink(dim_name="emotional_coloring", channel=2, effect="amplify",
                      weight=0.4, citation="Janata 2009"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Janata", 2009,
                         "Dorsal MPFC tracks tonal space during autobiographically "
                         "salient songs; hub binding music, memories, emotions",
                         "fMRI 3T, N=13, t(9)=5.784"),
                Citation("Sakakibara", 2025,
                         "Nostalgia Brain-Music Interface enhances nostalgic feelings, "
                         "well-being, memory vividness; acoustic similarity triggers nostalgia",
                         "EEG+behavioral, N=33, ηp²=0.636"),
                Citation("Derks-Dijkman", 2024,
                         "Musical mnemonics benefit working and episodic memory; "
                         "familiarity contributes; AD patients retain advantage",
                         "systematic review, 28/37 studies"),
                Citation("Scarratt", 2025,
                         "Familiar music activates auditory, motor, emotion, and "
                         "memory areas; calm music strongest relaxation predictor",
                         "fMRI, N=57, FWE p<0.05"),
                Citation("Janata", 2007,
                         "Music-evoked autobiographical memories: reminiscence bump "
                         "ages 10-30; 30%+ trigger rate with popular music",
                         "behavioral, N≈300"),
                Citation("Barrett", 2010,
                         "Music-evoked nostalgia: affect, memory, personality "
                         "modulate nostalgia intensity",
                         "behavioral"),
                Citation("Tulving", 2002,
                         "Episodic memory requires coherent feature binding; "
                         "theoretical basis for consonance-memory link",
                         "review, Annual Rev Psychology"),
                Citation("Freitas", 2018,
                         "Musical familiarity activates ventral lateral thalamus "
                         "and left medial SFG; motor-memory co-activation",
                         "meta-analysis, ALE"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.92),
            falsification_criteria=(
                "Novel music should NOT trigger autobiographical memories "
                "(CONFIRMED: experimental studies)",
                "Familiar music should enhance recall "
                "(CONFIRMED: behavioral studies)",
                "Emotional intensity should correlate with memory vividness "
                "(CONFIRMED: Janata 2009)",
                "10-30 year encoding period should show strongest recall "
                "(CONFIRMED: reminiscence bump, Janata 2007)",
            ),
            version="3.0.0",
            paper_count=8,
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Music-evoked autobiographical memory: retrieval + nostalgia + affect.

        Args:
            h3_features: H³ dict {(r3_idx, h, m, l): (B, T)}.
            r3_features: (B, T, 97) R³ features.

        Returns:
            (B, T, 12) output.
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # R³ features (12)
        roughness      = r3_features[:, :, self._R3_ROUGHNESS]
        stumpf         = r3_features[:, :, self._R3_STUMPF_FUSION]
        pleasant       = r3_features[:, :, self._R3_SENSORY_PLEASANT]
        amplitude      = r3_features[:, :, self._R3_AMPLITUDE]
        loudness       = r3_features[:, :, self._R3_LOUDNESS]
        warmth         = r3_features[:, :, self._R3_WARMTH]
        tonalness      = r3_features[:, :, self._R3_TONALNESS]
        trist1         = r3_features[:, :, self._R3_TRISTIMULUS1]
        dist_ent       = r3_features[:, :, self._R3_DISTRIBUTION_ENTROPY]
        beat_strength  = r3_features[:, :, self._R3_BEAT_STRENGTH]
        tonal_stab     = r3_features[:, :, self._R3_TONAL_STABILITY]

        _zeros = torch.zeros(B, T, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else _zeros

        # H³ features (19 tuples)
        h3_stumpf_mean_h16   = _h3((3, 16, 1, 2), stumpf)
        h3_stumpf_mean_h20   = _h3((3, 20, 1, 2))
        h3_stumpf_mean_h24   = _h3((3, 24, 1, 0))
        h3_pleas_h16         = _h3((4, 16, 0, 2), pleasant)
        h3_pleas_trend_h20   = _h3((4, 20, 18, 0))
        h3_loud_h16          = _h3((10, 16, 0, 2), loudness)
        h3_loud_mean_h20     = _h3((10, 20, 1, 0))
        h3_loud_std_h24      = _h3((10, 24, 2, 0))
        h3_warmth_h16        = _h3((12, 16, 0, 2), warmth)
        h3_warmth_mean_h20   = _h3((12, 20, 1, 0))
        h3_tonal_h16         = _h3((14, 16, 0, 2), tonalness)
        h3_tonal_mean_h20    = _h3((14, 20, 1, 0))
        h3_ent_h16           = _h3((22, 16, 0, 2), dist_ent)
        h3_ent_mean_h20      = _h3((22, 20, 1, 0))
        h3_ent_stab_h24      = _h3((22, 24, 19, 0))
        h3_rough_h16         = _h3((0, 16, 0, 2), roughness)
        h3_rough_trend_h20   = _h3((0, 20, 18, 0))
        h3_amp_vel_h16       = _h3((7, 16, 8, 0))
        h3_amp_max_h20       = _h3((7, 20, 4, 0))

        # Derived: valence proxy (inverse roughness)
        valence = (1.0 - h3_rough_h16).clamp(0.0, 1.0)

        # Derived: familiarity proxy (low entropy + stable pattern)
        familiarity = (
            0.40 * (1.0 - h3_ent_h16)        # low current entropy
            + 0.30 * h3_ent_stab_h24          # stable over time
            + 0.30 * h3_tonal_mean_h20        # tonal consistency
        ).clamp(0.0, 1.0)

        # === E-LAYER (3D) — Episodic Memory Features ===

        # Retrieval: binding × beat_strength × stumpf (pattern-emotion coupling)
        retrieval_activation = (
            ALPHA_ATTENTION * (
                0.30 * beat_strength          # energy-consonance coupling proxy
                + 0.25 * h3_stumpf_mean_h16   # binding integrity
                + 0.25 * h3_stumpf_mean_h24   # long-term binding
                + 0.20 * stumpf               # current fusion
            )
        ).clamp(0.0, 1.0)

        # Nostalgia: warmth × tonal_stability × familiarity
        nostalgia_response = (
            BETA_FAMILIARITY * (
                0.30 * tonal_stab             # consonance-timbre proxy
                + 0.25 * h3_warmth_mean_h20   # sustained warmth
                + 0.25 * familiarity          # familiarity signal
                + 0.20 * h3_warmth_h16        # current warmth
            )
        ).clamp(0.0, 1.0)

        # Emotional coloring: valence × arousal
        emotional_coloring = (
            GAMMA_EMOTIONAL * (
                0.30 * valence                # pleasantness
                + 0.25 * h3_loud_h16          # arousal
                + 0.25 * h3_pleas_h16         # direct pleasantness
                + 0.20 * h3_amp_vel_h16       # energy dynamics
            )
        ).clamp(0.0, 1.0)

        # === M-LAYER (2D) — Mathematical Model Outputs ===

        # MEAM retrieval function: familiarity × emotional × retrieval
        meam_retrieval = (
            0.40 * retrieval_activation * familiarity
            + 0.30 * familiarity * emotional_coloring
            + 0.30 * nostalgia_response
        ).clamp(0.0, 1.0)

        # Recall probability: familiarity + arousal + valence
        recall_probability = (
            0.35 * familiarity
            + 0.25 * h3_loud_mean_h20
            + 0.25 * valence
            + 0.15 * h3_stumpf_mean_h20
        ).clamp(0.0, 1.0)

        # === P-LAYER (3D) — Present Processing ===

        memory_state = (
            0.40 * retrieval_activation
            + 0.35 * meam_retrieval
            + 0.25 * recall_probability
        ).clamp(0.0, 1.0)

        emotional_color = (
            0.35 * emotional_coloring
            + 0.30 * valence
            + 0.20 * h3_loud_h16
            + 0.15 * h3_pleas_trend_h20
        ).clamp(0.0, 1.0)

        nostalgia_link = (
            0.40 * nostalgia_response
            + 0.30 * familiarity
            + 0.30 * tonal_stab
        ).clamp(0.0, 1.0)

        # === F-LAYER (4D) — Future Predictions ===

        mem_vividness_pred = (
            0.40 * memory_state
            + 0.30 * h3_amp_max_h20
            + 0.30 * recall_probability
        ).clamp(0.0, 1.0)

        emo_response_pred = (
            0.40 * emotional_color
            + 0.30 * h3_pleas_trend_h20
            + 0.30 * h3_rough_trend_h20.abs()
        ).clamp(0.0, 1.0)

        self_referential_pred = (
            0.40 * familiarity
            + 0.30 * nostalgia_link
            + 0.30 * h3_stumpf_mean_h24
        ).clamp(0.0, 1.0)

        reserved = _zeros

        return torch.stack([
            retrieval_activation, nostalgia_response, emotional_coloring,
            meam_retrieval, recall_probability,
            memory_state, emotional_color, nostalgia_link,
            mem_vividness_pred, emo_response_pred,
            self_referential_pred, reserved,
        ], dim=-1)
