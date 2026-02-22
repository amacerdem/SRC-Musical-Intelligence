"""MAD -- Musical Anhedonia Disconnection.

Encoder nucleus (depth 1) in ARU, Function F5. Models the selective
disconnection between auditory cortex (STG) and reward circuitry (NAcc) that
defines musical anhedonia. The uncinate fasciculus white matter tract integrity
(FA) determines whether music signals reach the reward system. General hedonic
capacity is preserved (double dissociation). 90.9% sound-specific.

Reads: SRP (intra-circuit via relay_outputs), AAC (intra-circuit via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, roughness_total)
    harmonic_ratio:         [2]      (A, consonance perception)
    sensory_pleasantness:   [4]      (A, hedonic valence)
    loudness:               [10]     (B, arousal signal)
    onset_strength:         [11]     (B, event detection)
    spectral_centroid:      [12]     (C, brightness)
    tonalness:              [14]     (C, tonal quality)
    spectral_flux:          [21]     (D, change detection)
    distribution_entropy:   [22]     (D, information content)
    x_l4l5:                 [33:41]  (G, disrupted coupling link)

Output structure: E(2) + D+A(5) + P(2) + F(2) = 11D
  E-layer   [0:2]   Extraction           (sigmoid)  scope=internal
  D+A-layer [2:7]   Temporal Integration  (sigmoid)  scope=internal
  P-layer   [7:9]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [9:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/mad/
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
    6: "200ms (beta)",
    11: "500ms (delta)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 2: "std", 8: "velocity", 20: "entropy",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 1: "prediction", 2: "integration"}


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
_HARMONIC_RATIO = 2
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_SPECTRAL_CENTROID = 12
_TONALNESS = 14
_SPECTRAL_FLUX = 21
_DISTRIBUTION_ENTROPY = 22


# -- 9 H3 Demand Specifications -----------------------------------------------
# Musical anhedonia disconnection requires hedonic dynamics (sensory_pleasantness),
# arousal tracking (loudness), and affect entropy (roughness, loudness) to capture
# the STG-NAcc disconnection and reward absence pattern.

_MAD_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Anhedonia + Dissociation (3 tuples) ===
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 0, 0,
        "1s hedonic value -- absent reward coupling in anhedonia",
        "Martinez-Molina 2016"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 6, 8, 0,
        "Hedonic change rate -- flat in anhedonia",
        "Mas-Herrero 2014"),
    _h3(_LOUDNESS, "loudness", 16, 20, 0,
        "1s affect entropy -- low in anhedonia",
        "Loui 2017"),

    # === D+A-Layer: Connectivity + NAcc + BMRQ + Specificity (3 tuples) ===
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 11, 8, 0,
        "Reward dynamics at 500ms",
        "Martinez-Molina 2016"),
    _h3(_LOUDNESS, "loudness", 11, 2, 0,
        "Reward variability at 500ms",
        "Mas-Herrero 2013"),
    _h3(_ROUGHNESS, "roughness", 16, 20, 0,
        "Affect entropy at 1s",
        "Loui 2017"),

    # === P-Layer: Impaired Reward + Preserved Auditory (2 tuples) ===
    _h3(_LOUDNESS, "loudness", 6, 0, 0,
        "Instant arousal -- preserved in anhedonia",
        "Martinez-Molina 2016"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 6, 0, 0,
        "Instant hedonic -- reward system test",
        "Mas-Herrero 2014"),

    # === F-Layer: Recovery + Probability (1 tuple) ===
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 11, 2, 0,
        "Reward variability for recovery potential",
        "Mas-Herrero 2018"),
)

assert len(_MAD_H3_DEMANDS) == 9


class MAD(Encoder):
    """Musical Anhedonia Disconnection -- ARU Encoder (depth 1, 11D).

    Models the selective disconnection between auditory cortex (STG) and
    reward circuitry (NAcc) that defines musical anhedonia. The uncinate
    fasciculus white matter tract integrity (FA) determines whether music
    signals reach the reward system. General hedonic capacity is preserved
    (double dissociation). 90.9% sound-specific.

    Martinez-Molina et al. 2016: STG-NAcc white matter disconnection in
    specific musical anhedonia. Uncinate fasciculus FA deficit d=-5.89.
    fMRI+DTI, N=45. NAcc activation absent for music but preserved for
    monetary rewards.

    Mas-Herrero et al. 2014: Barcelona Music Reward Questionnaire (BMRQ)
    identifies musical anhedonia prevalence 3-5%. N=500. Factor analysis
    reveals music reward as separable from general reward.

    Loui et al. 2017: DTI study, N=22. 90.9% of musical anhedonics show
    sound-specific deficit. White matter connectivity between STG and
    NAcc predicts music reward sensitivity.

    Mas-Herrero et al. 2018: Neural correlates predict BMRQ classification
    accuracy >90%. fMRI, N=40.

    Dependency chain:
        MAD is an Encoder (Depth 1) -- reads SRP + AAC relay outputs.
        Computed after SRP and AAC in F5 pipeline.

    Downstream feeds:
        -> anhedonia_risk belief (Appraisal)
        -> F10 clinical meta-layer diagnostic
    """

    NAME = "MAD"
    FULL_NAME = "Musical Anhedonia Disconnection"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("SRP", "AAC")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="ARU_SRP__ARU_MAD__pleasure",
            name="SRP pleasure to MAD reward assessment",
            source_unit="ARU",
            source_model="SRP",
            source_dims=("P2:pleasure",),
            target_unit="ARU",
            target_model="MAD",
            correlation="r=-0.72",
            citation="Martinez-Molina 2016",
        ),
        CrossUnitPathway(
            pathway_id="ARU_AAC__ARU_MAD__arousal",
            name="AAC emotional arousal to MAD dissociation",
            source_unit="ARU",
            source_model="AAC",
            source_dims=("E0:emotional_arousal",),
            target_unit="ARU",
            target_model="MAD",
            correlation="r=-0.45",
            citation="Loui 2017",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:anhedonia", "E1:dissociation_idx"),
            scope="internal",
        ),
        LayerSpec(
            "D+A", "Temporal Integration", 2, 7,
            ("D0:stg_nacc_connect", "D1:nacc_music_resp",
             "D2:nacc_general_resp", "A0:bmrq_estimate",
             "A1:sound_specificity"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 7, 9,
            ("P0:impaired_reward", "P1:preserved_auditory"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:recovery_potential", "F1:anhedonia_prob"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MAD_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:anhedonia", "E1:dissociation_idx",
            "D0:stg_nacc_connect", "D1:nacc_music_resp",
            "D2:nacc_general_resp", "A0:bmrq_estimate",
            "A1:sound_specificity",
            "P0:impaired_reward", "P1:preserved_auditory",
            "F0:recovery_potential", "F1:anhedonia_prob",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # STG -- auditory processing, preserved in anhedonia
            RegionLink("P1:preserved_auditory", "STG", 0.85,
                       "Martinez-Molina 2016"),
            # NAcc -- music reward, impaired in anhedonia
            RegionLink("D1:nacc_music_resp", "NAcc", 0.90,
                       "Martinez-Molina 2016"),
            # Uncinate fasciculus -- white matter tract (FA deficit d=-5.89)
            RegionLink("D0:stg_nacc_connect", "uncinate_fasciculus", 0.90,
                       "Martinez-Molina 2016"),
            # VTA -- general reward, preserved in anhedonia
            RegionLink("D2:nacc_general_resp", "VTA", 0.75,
                       "Loui 2017"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- reward pathway (impaired for music in anhedonia)
            NeuroLink("D1:nacc_music_resp", "dopamine", 0.80,
                      "Martinez-Molina 2016"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Martinez-Molina et al.", 2016,
                         "STG-NAcc white matter disconnection in specific "
                         "musical anhedonia. Uncinate fasciculus FA deficit "
                         "d=-5.89. NAcc activation absent for music but "
                         "preserved for monetary rewards",
                         "fMRI+DTI, N=45"),
                Citation("Mas-Herrero et al.", 2014,
                         "Barcelona Music Reward Questionnaire identifies "
                         "musical anhedonia prevalence 3-5%. Music reward "
                         "separable from general reward",
                         "behavioral, N=500"),
                Citation("Mas-Herrero et al.", 2013,
                         "BMRQ developed and validated for music reward "
                         "sensitivity. Five-factor structure: musical "
                         "seeking, emotion evocation, mood regulation, "
                         "sensory-motor, social reward",
                         "factor analysis, N=804"),
                Citation("Loui et al.", 2017,
                         "90.9% of musical anhedonics show sound-specific "
                         "deficit. White matter connectivity between STG "
                         "and NAcc predicts music reward sensitivity",
                         "DTI, N=22"),
                Citation("Mas-Herrero et al.", 2018,
                         "Neural correlates predict BMRQ classification "
                         "accuracy >90%. STG-NAcc connectivity as "
                         "biomarker for musical anhedonia",
                         "fMRI, N=40"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Anhedonia (E0) must be higher when SRP.pleasure is low "
                "and sensory features are intact (double dissociation)",
                "STG-NAcc connectivity (D0) must correlate with uncinate "
                "fasciculus FA (Martinez-Molina 2016: d=-5.89)",
                "NAcc music response (D1) must be selectively impaired "
                "while general response (D2) is preserved",
                "Sound specificity (A1) must exceed 0.9 for true musical "
                "anhedonics (Loui 2017: 90.9% sound-specific)",
                "BMRQ estimate (A0) must correlate with actual BMRQ scores "
                "(Mas-Herrero 2013: validated instrument)",
                "Anhedonia probability (F1) must classify at >90% accuracy "
                "(Mas-Herrero 2018: neural biomarker)",
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
        """Transform R3/H3 + SRP/AAC relay outputs into 11D anhedonia state.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"SRP": (B, T, 19), "AAC": (B, T, 14)}``

        Returns:
            ``(B, T, 11)`` -- E(2) + D+A(5) + P(2) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(
            h3_features, r3_features, e, relay_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
