"""MMP — Musical Mnemonic Preservation.

Relay nucleus for the Implicit Memory Unit (IMU).

Neural Circuit:
    Audio → A1/STG (melodic recognition)
                ↓
              Angular Gyrus (familiar melody recognition)
                ↓
              SMA/pre-SMA (preserved procedural musical memory)
                ↓
              ACC (musical memory consolidation)
                ↓
              Hippocampus (episodic memory — AD-vulnerable)
                ↓
              Amygdala (emotional tagging of musical memories)

Key Findings:
    - Musical memory regions (SMA, ACC, angular gyrus) are structurally
      preserved in Alzheimer's disease (Jacobsen et al. 2015, Brain)
    - Music therapy improves cognitive function in dementia patients
      (Fang et al. 2017; Luxton et al. 2025)
    - Music-evoked autobiographical memories are enhanced compared to
      verbal cues (El Haj et al. 2012, Memory)
    - Musicians show brain structure protection in aging
      (Espinosa et al. 2025, GeroScience)

Temporal Architecture:
    MMP uses long-horizon H³ demands (H16, H20, H24) to detect
    preserved musical patterns.  Familiarity accumulates over seconds:
    - H16 (1s):  Current recognition state
    - H20 (~4s): Sustained familiarity over phrases
    - H24 (~36s): Long-term preservation signal

R³ Remapping (Ontology Freeze v1.0.0):
    - Doc [25:33] "x_l0l5" → Code [42] beat_strength (dissolved)
    - Doc [41:49] "x_l5l7" → Code [60] tonal_stability (dissolved)
    - v2 [87,88] → Not available (>97D); replaced with existing features
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

# Musical memory preservation in AD — structural sparing
# Source: Jacobsen et al. 2015, Brain 138:2438
# SMA and cingulate cortex regions that encode musical memories
# show less atrophy and less amyloid deposition in AD
PRESERVATION_FACTOR: float = 0.85

# Music therapy cognitive improvement effect
# Source: Fang et al. 2017, meta-analysis
THERAPY_EFFECT: float = 0.60

# Hippocampal independence — proportion of musical memory
# that survives hippocampal damage via cortical routes
# Source: Jacobsen et al. 2015 (preserved recognition without HPC)
HIPPOCAMPAL_INDEPENDENCE: float = 0.70


class MMP(Relay):
    """Musical Mnemonic Preservation — IMU Relay (Depth 0, 12D).

    Models the preservation of musical memory in neurodegenerative
    disease, based on the structural sparing of SMA, ACC, and angular
    gyrus in Alzheimer's disease (Jacobsen et al. 2015).

    Output Structure (12D):
        R-layer (3D) [0:3]:  Recognition — preserved, melodic, scaffold
        P-layer (3D) [3:6]:  Present — recognition, identity, familiarity
        F-layer (3D) [6:9]:  Future — recognition, emotional, scaffold
        C-layer (3D) [9:12]: Clinical — preservation, therapeutic, independence
    """

    NAME = "MMP"
    FULL_NAME = "Musical Mnemonic Preservation"
    UNIT = "IMU"

    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            code="R", name="Recognition", start=0, end=3,
            dim_names=(
                "preserved_recognition",  # Overall preservation strength
                "melodic_recognition",    # Melody-specific recognition
                "scaffold_recognition",   # Structural scaffold intact
            ),
            scope="internal",
        ),
        LayerSpec(
            code="P", name="Present", start=3, end=6,
            dim_names=(
                "recognition_state",    # Current recognition level
                "melodic_identity",     # Current melodic match
                "familiarity_level",    # Current familiarity
            ),
            scope="external",
        ),
        LayerSpec(
            code="F", name="Future", start=6, end=9,
            dim_names=(
                "recognition_forecast",  # Predicted recognition trajectory
                "emotional_forecast",    # Predicted emotional response
                "scaffold_forecast",     # Predicted structural integrity
            ),
            scope="hybrid",
        ),
        LayerSpec(
            code="C", name="Clinical", start=9, end=12,
            dim_names=(
                "preservation_index",     # Relative sparing measure
                "therapeutic_efficacy",   # Music therapy response
                "hippocampal_independence",  # Cortical vs HPC pathway
            ),
            scope="external",
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
    _R3_SPECTRAL_SMOOTHNESS = 16
    _R3_TRISTIMULUS1 = 18
    _R3_DISTRIBUTION_ENTROPY = 22
    _R3_TONAL_STABILITY = 60

    _EPS: float = 1e-8

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """18 temporal demands at long horizons for memory preservation."""
        return (
            # --- Stumpf fusion: binding integrity ---
            H3DemandSpec(r3_idx=3, r3_name="stumpf_fusion",
                         horizon=16, horizon_label="1s measure",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current binding integrity",
                         citation="Jacobsen et al. 2015"),
            H3DemandSpec(r3_idx=3, r3_name="stumpf_fusion",
                         horizon=24, horizon_label="36s section",
                         morph=2, morph_name="std", law=0, law_name="memory",
                         purpose="Long-term binding stability",
                         citation="Jacobsen et al. 2015"),
            # --- Sensory pleasantness: emotional tagging ---
            H3DemandSpec(r3_idx=4, r3_name="sensory_pleasantness",
                         horizon=16, horizon_label="1s measure",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current pleasantness for emotional tagging",
                         citation="Scarratt et al. 2025"),
            H3DemandSpec(r3_idx=4, r3_name="sensory_pleasantness",
                         horizon=24, horizon_label="36s section",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Long-term emotional valence",
                         citation="El Haj et al. 2012"),
            # --- Warmth: timbre familiarity ---
            H3DemandSpec(r3_idx=12, r3_name="warmth",
                         horizon=16, horizon_label="1s measure",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current timbre warmth — instrument identity",
                         citation="Sikka et al. 2015"),
            H3DemandSpec(r3_idx=12, r3_name="warmth",
                         horizon=20, horizon_label="H20 phrase",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Sustained warmth — timbre familiarity",
                         citation="Sikka et al. 2015"),
            H3DemandSpec(r3_idx=12, r3_name="warmth",
                         horizon=24, horizon_label="36s section",
                         morph=2, morph_name="std", law=0, law_name="memory",
                         purpose="Long-term warmth stability",
                         citation="Espinosa et al. 2025"),
            # --- Tonalness: melody recognition ---
            H3DemandSpec(r3_idx=14, r3_name="tonalness",
                         horizon=16, horizon_label="1s measure",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current tonal clarity — melody detection",
                         citation="Sikka et al. 2015"),
            H3DemandSpec(r3_idx=14, r3_name="tonalness",
                         horizon=20, horizon_label="H20 phrase",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Tonal stability over phrases",
                         citation="Jacobsen et al. 2015"),
            H3DemandSpec(r3_idx=14, r3_name="tonalness",
                         horizon=24, horizon_label="36s section",
                         morph=2, morph_name="std", law=0, law_name="memory",
                         purpose="Long-term tonal stability",
                         citation="Derks-Dijkman et al. 2024"),
            # --- Tristimulus1: instrument fundamental ---
            H3DemandSpec(r3_idx=18, r3_name="tristimulus1",
                         horizon=16, horizon_label="1s measure",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Instrument fundamental energy",
                         citation="Sikka et al. 2015"),
            H3DemandSpec(r3_idx=18, r3_name="tristimulus1",
                         horizon=24, horizon_label="36s section",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Long-term timbre identity",
                         citation="Espinosa et al. 2025"),
            # --- Distribution entropy: pattern complexity ---
            H3DemandSpec(r3_idx=22, r3_name="distribution_entropy",
                         horizon=16, horizon_label="1s measure",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current pattern complexity",
                         citation="Baird & Samson 2015"),
            H3DemandSpec(r3_idx=22, r3_name="distribution_entropy",
                         horizon=24, horizon_label="36s section",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Long-term predictability (low = familiar)",
                         citation="Derks-Dijkman et al. 2024"),
            # --- Loudness: arousal context ---
            H3DemandSpec(r3_idx=10, r3_name="loudness",
                         horizon=16, horizon_label="1s measure",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current arousal from loudness",
                         citation="Scarratt et al. 2025"),
            H3DemandSpec(r3_idx=10, r3_name="loudness",
                         horizon=24, horizon_label="36s section",
                         morph=2, morph_name="std", law=0, law_name="memory",
                         purpose="Dynamic range over long section",
                         citation="Fang et al. 2017"),
            # --- Roughness: valence context ---
            H3DemandSpec(r3_idx=0, r3_name="roughness",
                         horizon=16, horizon_label="1s measure",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current dissonance — valence proxy",
                         citation="Scarratt et al. 2025"),
            # --- Onset strength: rhythmic regularity ---
            H3DemandSpec(r3_idx=11, r3_name="onset_strength",
                         horizon=16, horizon_label="1s measure",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Rhythmic regularity — procedural scaffold",
                         citation="Jacobsen et al. 2015"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "preserved_recognition", "melodic_recognition", "scaffold_recognition",
            "recognition_state", "melodic_identity", "familiarity_level",
            "recognition_forecast", "emotional_forecast", "scaffold_forecast",
            "preservation_index", "therapeutic_efficacy", "hippocampal_independence",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            RegionLink(dim_name="preserved_recognition", region="SMA",
                       weight=0.9, citation="Jacobsen et al. 2015"),
            RegionLink(dim_name="scaffold_recognition", region="ACC",
                       weight=0.8, citation="Jacobsen et al. 2015"),
            RegionLink(dim_name="melodic_recognition", region="Angular_Gyrus",
                       weight=0.85, citation="Sikka et al. 2015"),
            RegionLink(dim_name="melodic_identity", region="STG",
                       weight=0.7, citation="Scarratt et al. 2025"),
            RegionLink(dim_name="emotional_forecast", region="Amygdala",
                       weight=0.6, citation="El Haj et al. 2012"),
            RegionLink(dim_name="hippocampal_independence", region="Hippocampus",
                       weight=0.5, citation="Jacobsen et al. 2015"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            NeuroLink(dim_name="familiarity_level", channel=0, effect="produce",
                      weight=0.3, citation="Scarratt et al. 2025"),
            NeuroLink(dim_name="emotional_forecast", channel=2, effect="amplify",
                      weight=0.4, citation="El Haj et al. 2012"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Jacobsen", 2015,
                         "Musical memory regions (SMA, ACC, angular gyrus) "
                         "structurally preserved in AD; less atrophy and amyloid",
                         "structural MRI, AD cohort"),
                Citation("Fang", 2017,
                         "Music therapy improves cognitive function in dementia; "
                         "meta-analysis of interventional studies",
                         "meta-analysis, dementia MT"),
                Citation("El Haj", 2012,
                         "Music-evoked autobiographical memories enhanced vs "
                         "verbal cues in AD; emotional tagging preserved",
                         "behavioral, AD patients"),
                Citation("Derks-Dijkman", 2024,
                         "Musical mnemonics systematic review; preservation of "
                         "procedural and semantic musical memory in dementia",
                         "systematic review"),
                Citation("Stramba-Badiale", 2025,
                         "Autobiographical memory selectively preserved through "
                         "musical triggers in AD",
                         "behavioral, AD cohort"),
                Citation("Sikka", 2015,
                         "fMRI melody recognition: angular gyrus, STG, and SMA "
                         "activation for familiar melodies",
                         "fMRI, familiar melody recognition"),
                Citation("Espinosa", 2025,
                         "Musicians show brain structure protection in aging; "
                         "preserved cortical thickness in auditory/motor areas",
                         "structural MRI, musicians vs controls"),
                Citation("Scarratt", 2025,
                         "Familiar music activates reward and memory networks "
                         "more strongly than unfamiliar in older adults",
                         "fMRI, familiar > unfamiliar"),
                Citation("Luxton", 2025,
                         "Cognitive intervention efficacy through music: "
                         "significant improvement in executive function",
                         "RCT, BJPsych"),
                Citation("Jin", 2024,
                         "Musical preservation of hemispheric lateralization "
                         "patterns in aging and early dementia",
                         "EEG, lateralization preservation"),
                Citation("Baird", 2015,
                         "Music and dementia review: preserved implicit musical "
                         "memory despite severe explicit memory loss",
                         "review, Prog Brain Res"),
                Citation("Domingues", 2025,
                         "Episodic vs semantic musical memory distinction; "
                         "semantic preserved longer in neurodegenerative disease",
                         "behavioral, semantic vs episodic"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.82, 0.90),
            falsification_criteria=(
                "Angular gyrus preservation vs hippocampal atrophy in AD "
                "(CONFIRMED: Jacobsen 2015)",
                "Familiar music recognition preserved in moderate AD "
                "(CONFIRMED: El Haj 2012, Baird 2015)",
                "Music therapy efficacy for cognitive decline "
                "(CONFIRMED: Fang 2017, Luxton 2025)",
                "Emotional response preservation outlasting verbal memory "
                "(CONFIRMED: Stramba-Badiale 2025)",
            ),
            version="3.0.0",
            paper_count=12,
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Musical memory preservation: recognition + preservation + clinical.

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
        onset_str      = r3_features[:, :, self._R3_ONSET_STRENGTH]
        warmth         = r3_features[:, :, self._R3_WARMTH]
        tonalness      = r3_features[:, :, self._R3_TONALNESS]
        smoothness     = r3_features[:, :, self._R3_SPECTRAL_SMOOTHNESS]
        trist1         = r3_features[:, :, self._R3_TRISTIMULUS1]
        dist_ent       = r3_features[:, :, self._R3_DISTRIBUTION_ENTROPY]
        tonal_stab     = r3_features[:, :, self._R3_TONAL_STABILITY]

        _zeros = torch.zeros(B, T, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else _zeros

        # H³ features (18 tuples)
        h3_stumpf_h16       = _h3((3, 16, 0, 2), stumpf)
        h3_stumpf_std_h24   = _h3((3, 24, 2, 0))
        h3_pleas_h16        = _h3((4, 16, 0, 2), pleasant)
        h3_pleas_mean_h24   = _h3((4, 24, 1, 0))
        h3_warmth_h16       = _h3((12, 16, 0, 2), warmth)
        h3_warmth_mean_h20  = _h3((12, 20, 1, 0))
        h3_warmth_std_h24   = _h3((12, 24, 2, 0))
        h3_tonal_h16        = _h3((14, 16, 0, 2), tonalness)
        h3_tonal_mean_h20   = _h3((14, 20, 1, 0))
        h3_tonal_std_h24    = _h3((14, 24, 2, 0))
        h3_trist_h16        = _h3((18, 16, 0, 2), trist1)
        h3_trist_mean_h24   = _h3((18, 24, 1, 0))
        h3_ent_h16          = _h3((22, 16, 0, 2), dist_ent)
        h3_ent_mean_h24     = _h3((22, 24, 1, 0))
        h3_loud_h16         = _h3((10, 16, 0, 2), loudness)
        h3_loud_std_h24     = _h3((10, 24, 2, 0))
        h3_rough_h16        = _h3((0, 16, 0, 2), roughness)
        h3_onset_period_h16 = _h3((11, 16, 14, 2))

        # === R-LAYER (3D) — Recognition ===

        # Binding integrity × warmth × preservation
        preserved_recognition = (
            0.30 * h3_stumpf_h16
            + 0.25 * h3_warmth_h16
            + 0.20 * (1.0 - h3_stumpf_std_h24)    # stability = preservation
            + 0.15 * h3_trist_h16
            + 0.10 * smoothness
        ).clamp(0.0, 1.0)

        # Melodic recognition: tonalness × timbre
        melodic_recognition = (
            0.30 * h3_tonal_h16
            + 0.25 * h3_tonal_mean_h20
            + 0.20 * h3_trist_h16
            + 0.15 * (1.0 - h3_tonal_std_h24)      # tonal stability
            + 0.10 * tonal_stab
        ).clamp(0.0, 1.0)

        # Structural scaffold: rhythm + predictability
        scaffold_recognition = (
            0.30 * h3_onset_period_h16
            + 0.25 * (1.0 - h3_ent_h16)             # low entropy = predictable
            + 0.25 * (1.0 - h3_ent_mean_h24)         # long-term predictability
            + 0.20 * onset_str
        ).clamp(0.0, 1.0)

        # === P-LAYER (3D) — Present ===
        recognition_state = (
            0.40 * preserved_recognition
            + 0.35 * melodic_recognition
            + 0.25 * scaffold_recognition
        ).clamp(0.0, 1.0)

        melodic_identity = (
            0.40 * h3_tonal_h16
            + 0.30 * h3_warmth_h16
            + 0.30 * h3_trist_h16
        ).clamp(0.0, 1.0)

        familiarity_level = (
            0.25 * h3_warmth_mean_h20
            + 0.25 * h3_tonal_mean_h20
            + 0.20 * h3_trist_mean_h24
            + 0.15 * h3_pleas_mean_h24
            + 0.15 * (1.0 - h3_warmth_std_h24)
        ).clamp(0.0, 1.0)

        # === F-LAYER (3D) — Forecast ===
        recognition_forecast = (
            0.50 * recognition_state
            + 0.30 * familiarity_level
            + 0.20 * h3_tonal_mean_h20
        ).clamp(0.0, 1.0)

        emotional_forecast = (
            0.30 * h3_pleas_h16
            + 0.25 * h3_pleas_mean_h24
            + 0.25 * (1.0 - h3_rough_h16)
            + 0.20 * h3_loud_h16
        ).clamp(0.0, 1.0)

        scaffold_forecast = (
            0.50 * scaffold_recognition
            + 0.50 * HIPPOCAMPAL_INDEPENDENCE
        ).clamp(0.0, 1.0)

        # === C-LAYER (3D) — Clinical ===
        preservation_index = (
            PRESERVATION_FACTOR * recognition_state
        ).clamp(0.0, 1.0)

        therapeutic_efficacy = (
            preserved_recognition + melodic_recognition + scaffold_recognition
        ) / 3.0

        hippocampal_indep = (
            HIPPOCAMPAL_INDEPENDENCE * (
                0.50 * preserved_recognition
                + 0.30 * scaffold_recognition
                + 0.20 * amplitude
            )
        ).clamp(0.0, 1.0)

        return torch.stack([
            preserved_recognition, melodic_recognition, scaffold_recognition,
            recognition_state, melodic_identity, familiarity_level,
            recognition_forecast, emotional_forecast, scaffold_forecast,
            preservation_index, therapeutic_efficacy, hippocampal_indep,
        ], dim=-1)
