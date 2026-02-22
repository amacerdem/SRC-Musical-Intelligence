"""MMP -- Musical Mnemonic Preservation.

Relay nucleus (depth 0) in IMU, Function F4. Models how musical memory is
preserved in Alzheimer's disease through cortically-mediated pathways that
are relatively spared from hippocampal atrophy. Assesses recognition,
scaffolding efficacy, and therapeutic potential.

Dependency chain:
    MMP is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:              [0]  -> [0]    (A, roughness_total)
    stumpf_fusion:          [3]  -> [3]    (A, stumpf_fusion)
    sensory_pleasantness:   [4]  -> [4]    (A, sensory_pleasantness)
    warmth:                 [12] -> [12]   (C, warmth)
    tonalness:              [14] -> [14]   (C, brightness_kuttruff)
    tristimulus1-3:         [18:21] -> [18:21] (C, tristimulus)
    entropy:                [22] -> [22]   (D, entropy)
    x_l5l7:                 [41:49] -> [41:49] (F, coupling)

Output structure: R(3) + P(3) + F(3) + C(3) = 12D
  R-layer [0:3]   Recognition/Preservation  (sigmoid)    scope=internal
  P-layer [3:6]   Present Processing        (sigmoid)    scope=hybrid
  F-layer [6:9]   Future Predictions         (sigmoid)    scope=external
  C-layer [9:12]  Clinical Metrics           (sigmoid)    scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mmp/
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
    24: "36000ms (episodic)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 3: "std", 5: "range",
    14: "periodicity", 19: "stability",
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
_ROUGHNESS = 0            # roughness_total (A group)
_STUMPF_FUSION = 3        # stumpf_fusion (A group)
_SENSORY_PLEASANT = 4     # sensory_pleasantness (A group)
_AMPLITUDE = 7            # velocity_A (A group)
_LOUDNESS = 10            # onset_strength (B group) — doc uses idx 10
_ONSET_STRENGTH = 11      # onset_strength (B group)
_WARMTH = 12              # warmth (C group)
_TONALNESS = 14           # brightness_kuttruff (C group)
_SPECTRAL_SMOOTH = 16     # spectral_smoothness (C group)
_TRIST1 = 18              # tristimulus1 (C group)
_ENTROPY = 22             # entropy (D group)


# -- 21 H3 Demand Specifications ----------------------------------------------
# R-layer (7+1): recognition/preservation features at 1s and 5s horizons
# P-layer (5): present processing at 1s, 5s, and 36s horizons
# F-layer (3): predictions at 5s and 36s horizons
# C-layer (5): clinical metrics at 36s horizon

_MMP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === R-layer: Recognition & Preservation (8 tuples) ===
    _h3(_STUMPF_FUSION, "stumpf_fusion", 16, 0, 2,
        "Binding integrity at 1s — cortical fusion state",
        "Jacobsen 2015"),
    _h3(_WARMTH, "warmth", 16, 0, 2,
        "Timbre warmth at 1s — familiar sound character",
        "Jacobsen 2015"),
    _h3(_WARMTH, "warmth", 20, 1, 0,
        "Sustained warmth over 5s — familiarity proxy",
        "Sikka 2015"),
    _h3(_TONALNESS, "tonalness", 16, 0, 2,
        "Melody recognition state at 1s — harmonic-to-noise",
        "Sikka 2015"),
    _h3(_TRIST1, "tristimulus1", 16, 0, 2,
        "Instrument fundamental at 1s — voice/instrument ID",
        "Sikka 2015"),
    _h3(_ENTROPY, "entropy", 16, 0, 2,
        "Pattern complexity at 1s — familiarity inverse",
        "Derks-Dijkman 2024"),
    _h3(_ROUGHNESS, "roughness", 16, 0, 2,
        "Valence proxy at 1s — emotional tag for retrieval",
        "Jacobsen 2015"),
    _h3(_SENSORY_PLEASANT, "sensory_pleasantness", 16, 0, 2,
        "Memory valence at 1s — preserved hedonic response",
        "Jacobsen 2015"),

    # === P-layer: Present Processing (5 tuples) ===
    _h3(_TONALNESS, "tonalness", 20, 1, 0,
        "Tonal stability over 5s — melody consistency",
        "Sikka 2015"),
    _h3(_WARMTH, "warmth", 24, 19, 0,
        "Long-term warmth stability over 36s — familiarity anchor",
        "Scarratt 2025"),
    _h3(_TONALNESS, "tonalness", 24, 19, 0,
        "Long-term tonal stability over 36s — melodic persistence",
        "El Haj 2012"),
    _h3(_LOUDNESS, "loudness", 16, 0, 2,
        "Current arousal at 1s — engagement level",
        "Scarratt 2025"),
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 14, 2,
        "Rhythmic regularity at 1s — temporal structure",
        "Scarratt 2025"),

    # === F-layer: Future Predictions (3 tuples) ===
    _h3(_SENSORY_PLEASANT, "sensory_pleasantness", 24, 1, 0,
        "Long-term pleasantness over 36s — emotional trajectory",
        "Fang 2017"),
    _h3(_ENTROPY, "entropy", 24, 1, 0,
        "Long-term predictability over 36s — scaffold trajectory",
        "Luxton 2025"),
    _h3(_SPECTRAL_SMOOTH, "spectral_smoothness", 20, 1, 0,
        "Timbral quality over 5s — recognition trajectory",
        "Scarratt 2025"),

    # === C-layer: Clinical Metrics (5 tuples) ===
    _h3(_STUMPF_FUSION, "stumpf_fusion", 24, 19, 0,
        "Long-term binding stability over 36s — cortical integrity",
        "Jacobsen 2015"),
    _h3(_TRIST1, "tristimulus1", 24, 1, 0,
        "Long-term timbre stability over 36s — identity persistence",
        "Espinosa 2025"),
    _h3(_LOUDNESS, "loudness", 24, 3, 0,
        "Arousal variability over 36s — engagement stability",
        "Luxton 2025"),
    _h3(_ROUGHNESS, "roughness", 24, 1, 0,
        "Long-term valence over 36s — sustained emotional tone",
        "Jacobsen 2015"),
    _h3(_AMPLITUDE, "amplitude", 24, 5, 0,
        "Dynamic range over 36s — expressive variation",
        "Jin 2024"),
)

assert len(_MMP_H3_DEMANDS) == 21


class MMP(Relay):
    """Musical Mnemonic Preservation -- IMU Relay (depth 0, 12D).

    Models how musical memory is preserved in Alzheimer's disease through
    cortically-mediated pathways. Jacobsen et al. 2015: SMA/pre-SMA and
    ACC show least cortical atrophy in AD (fMRI+VBM, N=32). Sikka et al.
    2015: older adults shift to L-angular + L-superior-frontal gyrus for
    melody recognition (fMRI, N=40). Derks-Dijkman et al. 2024: 28/37
    studies show musical mnemonic benefit (systematic review).

    Dependency chain:
        MMP is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> MEAMN relay (memory_state, emotional_color)
        -> familiarity engine
        -> Clinical output (preservation_index, therapeutic_efficacy)
    """

    NAME = "MMP"
    FULL_NAME = "Musical Mnemonic Preservation"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            "R", "Retrieval/Recognition", 0, 3,
            ("R0:preserved_memory", "R1:melodic_recognition",
             "R2:scaffold_efficacy"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Preserved Processing", 3, 6,
            ("P0:preserved_recognition", "P1:melodic_identification",
             "P2:familiarity"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 6, 9,
            ("F0:recognition_fc", "F1:emotional_fc",
             "F2:scaffold_fc"),
            scope="external",
        ),
        LayerSpec(
            "C", "Clinical", 9, 12,
            ("C0:preservation_index", "C1:therapeutic_efficacy",
             "C2:hippocampal_independence"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MMP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "R0:preserved_memory", "R1:melodic_recognition",
            "R2:scaffold_efficacy",
            "P0:preserved_recognition", "P1:melodic_identification",
            "P2:familiarity",
            "F0:recognition_fc", "F1:emotional_fc",
            "F2:scaffold_fc",
            "C0:preservation_index", "C1:therapeutic_efficacy",
            "C2:hippocampal_independence",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # SMA/pre-SMA -- preserved musical memory
            RegionLink("R0:preserved_memory", "SMA", 0.85,
                       "Jacobsen 2015"),
            # ACC -- preserved memory pathway
            RegionLink("R0:preserved_memory", "ACC", 0.80,
                       "Jacobsen 2015"),
            # Angular Gyrus -- melodic recognition
            RegionLink("R1:melodic_recognition", "Angular_Gyrus", 0.80,
                       "Sikka 2015"),
            # STG -- melodic templates
            RegionLink("R1:melodic_recognition", "STG", 0.75,
                       "Sikka 2015"),
            # Lingual Gyrus -- visual-musical binding
            RegionLink("R0:preserved_memory", "Lingual_Gyrus", 0.65,
                       "Jacobsen 2015"),
            # Hippocampus -- episodic component (vulnerable)
            RegionLink("C2:hippocampal_independence", "Hippocampus", 0.70,
                       "Espinosa 2025"),
            # Amygdala -- emotional memory preservation
            RegionLink("F1:emotional_fc", "Amygdala", 0.70,
                       "El Haj 2012"),
            # L-Planum Temporale -- musician preservation
            RegionLink("P0:preserved_recognition", "L_Planum_Temporale", 0.65,
                       "Espinosa 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Jacobsen", 2015,
                         "SMA/pre-SMA and ACC show least cortical "
                         "atrophy in AD -- musical memory regions spared",
                         "fMRI+VBM, N=32"),
                Citation("Sikka", 2015,
                         "Older adults shift to L-angular + L-superior-"
                         "frontal gyrus for melody recognition",
                         "fMRI sparse-sampling, N=40"),
                Citation("Derks-Dijkman", 2024,
                         "28/37 studies show musical mnemonic benefit; "
                         "familiarity key contributor",
                         "Systematic review, 37 studies"),
                Citation("Scarratt", 2025,
                         "Familiar music activates auditory, motor, "
                         "emotion, and memory areas; calm+familiar = "
                         "max relaxation",
                         "fMRI, N=57, 4 response clusters"),
                Citation("El Haj", 2012,
                         "Music-evoked autobiographical memories more "
                         "specific and vivid than verbal-evoked in AD",
                         "Behavioral, AD patients"),
                Citation("Fang", 2017,
                         "Music therapy reduces cognitive decline in "
                         "autobiographical/episodic memory",
                         "Systematic mini-review, multiple RCTs"),
                Citation("Luxton", 2025,
                         "Level 1 evidence -- cognitive stimulation "
                         "therapy improves QoL (SMD=0.25, p=0.003)",
                         "Systematic review+meta-analysis, 324 studies"),
                Citation("Espinosa", 2025,
                         "Active musicians show increased GM in "
                         "AD-resistant regions (p<0.0001)",
                         "VBM, N=61"),
                Citation("Jin", 2024,
                         "Musicians preserve youth-like lateralization "
                         "vs compensation in non-musicians",
                         "Resting-state fMRI"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.80, 0.90),
            falsification_criteria=(
                "Musical memory regions (SMA, pre-SMA, ACC) should show "
                "least atrophy in AD (confirmed: Jacobsen 2015)",
                "Familiar melody recognition should shift to angular "
                "gyrus in aging (confirmed: Sikka 2015)",
                "Musical mnemonics should improve recall in AD "
                "(confirmed: Derks-Dijkman 2024, 28/37 studies)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 12D mnemonic preservation representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 12)`` -- R(3) + P(3) + F(3) + C(3)
        """
        r = compute_extraction(h3_features, r3_features)
        p = compute_temporal_integration(h3_features, r3_features, r)
        f = compute_cognitive_present(h3_features, r, p)
        c = compute_forecast(h3_features, r3_features, r)

        output = torch.stack([*r, *p, *f, *c], dim=-1)
        return output.clamp(0.0, 1.0)
