"""DMMS -- Developmental Music Memory Scaffold.

Associator nucleus (depth 2) in IMU, Function F4. Models how early musical
exposure during critical developmental periods (prenatal through age 5)
forms lasting memory scaffolds that shape lifelong music perception,
preference, and therapeutic response.

The neonatal auditory system preferentially encodes caregiver voice
(warmth, consonance) and infant-directed singing patterns, forming
hippocampal-amygdala scaffolds that persist into adulthood and can be
therapeutically accessed through familiar musical stimuli.

Reads: ARU.DAP, ARU.NEMAC (F6 cross-function)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, dissonance proxy)
    stumpf_fusion:          [3]      (A, tonal binding coherence)
    sensory_pleasantness:   [4]      (A, comfort/safety)
    warmth:                 [12]     (C, caregiver voice proxy)
    tonalness:              [14]     (B, melodic recognition)
    entropy:                [22]     (D, pattern complexity)
    x_l0l5:                 [25:33]  (F, salience-binding scaffold)
    x_l5l7:                 [41:49]  (G, familiarity template)

Output structure: E(3) + M(2) + P(2) + F(3) = 10D
  E-layer [0:3]   Extraction    (sigmoid)   scope=internal
  M-layer [3:5]   Memory        (sigmoid)   scope=internal
  P-layer [5:7]   Present       (clamp)     scope=hybrid
  F-layer [7:10]  Forecast      (sigmoid)   scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/dmms/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

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
    16: "1000ms (beat)",
    20: "5000ms (phrase)",
    24: "36000ms (section)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 3: "std", 4: "max",
    19: "stability",
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
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 10
_WARMTH = 12
_TONALNESS = 14
_ENTROPY = 22
_X_L0L5 = 25
_X_L5L7 = 41


# -- 15 H3 Demand Specifications -----------------------------------------------
# Developmental music memory scaffold: consonance, warmth, binding,
# tonalness, entropy across multiple temporal horizons (1s, 5s, 36s).

_DMMS_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # -- E-layer: 6 tuples at H16 (1s) L2 (integration) --
    _h3(3, "stumpf_fusion", 16, 1, 2,
        "Binding coherence 1s -- scaffold formation",
        "Partanen 2022"),
    _h3(4, "sensory_pleasantness", 16, 0, 2,
        "Comfort signal 1s -- neonatal pairing",
        "Partanen 2022"),
    _h3(12, "warmth", 16, 0, 2,
        "Voice-warmth 1s -- caregiver proxy",
        "Trehub 2003"),
    _h3(14, "tonalness", 16, 0, 2,
        "Melodic recognition 1s -- imprinting",
        "Trehub 2003"),
    _h3(0, "roughness", 16, 0, 2,
        "Dissonance 1s -- consonance proxy (inverted)",
        "Partanen 2022"),
    _h3(22, "entropy", 16, 0, 2,
        "Pattern complexity 1s -- plasticity gating",
        "Qiu 2025"),
    # -- M-layer: 5 tuples at H20/H24 L0 (memory) --
    _h3(3, "stumpf_fusion", 24, 1, 0,
        "Long-term binding 36s -- scaffold persistence",
        "Strait 2012"),
    _h3(4, "sensory_pleasantness", 20, 1, 0,
        "Sustained pleasantness 5s -- consolidation",
        "Strait 2012"),
    _h3(14, "tonalness", 20, 1, 0,
        "Tonal stability 5s -- template formation",
        "Trainor 2012"),
    _h3(12, "warmth", 20, 1, 0,
        "Sustained warmth 5s -- caregiver signal",
        "Trainor 2012"),
    _h3(0, "roughness", 20, 1, 0,
        "Consonance scaffold 5s -- stability",
        "Strait 2012"),
    # -- P-layer: 1 new tuple --
    _h3(10, "loudness", 16, 0, 2,
        "Arousal level 1s -- scaffold activation",
        "Nguyen 2023"),
    # -- F-layer: 3 new tuples --
    _h3(10, "loudness", 24, 3, 0,
        "Arousal variability 36s -- persistence gating",
        "Qiu 2025"),
    _h3(22, "entropy", 24, 19, 0,
        "Pattern stability 36s -- scaffold persistence",
        "Qiu 2025"),
    _h3(7, "amplitude", 20, 4, 0,
        "Peak energy 5s -- preference formation",
        "Trainor 2012"),
)

assert len(_DMMS_H3_DEMANDS) == 15


class DMMS(Associator):
    """Developmental Music Memory Scaffold -- IMU Associator (depth 2, 10D).

    Models how early musical exposure during critical developmental periods
    forms lasting memory scaffolds through hippocampal-amygdala binding,
    caregiver voice encoding, and melodic template imprinting.

    Partanen et al. 2022: Parental singing enhances auditory processing in
    preterm infants; neonatal scaffold formation via caregiver voice
    (MEG RCT, N=33, eta2=0.229).

    Qiu et al. 2025: Fetal-infant music exposure enhances mPFC/amygdala
    dendritic complexity; dose-dependent plasticity during critical period
    (mouse, N=48, r=0.38).

    Trehub 2003: Developmental origins of musicality; infants prefer
    consonance, show enhanced processing of infant-directed singing.

    Dependency chain:
        MEAMN (Depth 0, Relay) + PNH/MMP (Depth 0/1) --> DMMS (Depth 2)

    Upstream reads:
        None within IMU (Associator reads all depth 0+1 in unit)

    Cross-function feeds:
        -> ARU.DAP: F1:preference_formation for hedonic capacity
        -> ARU.NEMAC: scaffold signals for reward modulation

    Downstream feeds:
        -> F4 Memory (MEAMN): scaffold depth for retrieval
        -> F6 Reward (DAP): preference_formation for hedonic capacity
        -> F10 Clinical (meta-layer): therapeutic_potential
    """

    NAME = "DMMS"
    FULL_NAME = "Developmental Music Memory Scaffold"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("MEAMN", "PNH", "MMP")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:early_binding", "E1:dev_plasticity",
             "E2:melodic_imprint"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:scaffold_strength", "M1:imprinting_depth"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:scaffold_activation", "P1:bonding_warmth"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:scaffold_persistence", "F1:preference_formation",
             "F2:therapeutic_potential"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _DMMS_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:early_binding", "E1:dev_plasticity",
            "E2:melodic_imprint",
            "M0:scaffold_strength", "M1:imprinting_depth",
            "P0:scaffold_activation", "P1:bonding_warmth",
            "F0:scaffold_persistence", "F1:preference_formation",
            "F2:therapeutic_potential",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Hippocampus -- scaffold formation and template consolidation
            RegionLink("E0:early_binding", "hippocampus", 0.85,
                       "Partanen 2022"),
            RegionLink("P0:scaffold_activation", "hippocampus", 0.80,
                       "Nguyen 2023"),
            # Amygdala -- emotional tagging of early scaffolds
            RegionLink("E0:early_binding", "amygdala", 0.80,
                       "Qiu 2025"),
            RegionLink("P1:bonding_warmth", "amygdala", 0.75,
                       "Scholkmann 2024"),
            # Auditory Cortex (A1/STG) -- melodic template formation
            RegionLink("E1:dev_plasticity", "STG", 0.80,
                       "Qiu 2025"),
            RegionLink("E2:melodic_imprint", "STG", 0.85,
                       "Trehub 2003"),
            # mPFC -- critical period synaptic plasticity hub
            RegionLink("E1:dev_plasticity", "mPFC", 0.75,
                       "Qiu 2025"),
            RegionLink("F0:scaffold_persistence", "mPFC", 0.70,
                       "Qiu 2025"),
            # Right Prefrontal Cortex -- caregiver-directed music processing
            RegionLink("P1:bonding_warmth", "rPFC", 0.70,
                       "Scholkmann 2024"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # DMMS is developmental-structural, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Partanen et al.", 2022,
                         "Parental singing enhances auditory processing in "
                         "preterm infants; neonatal scaffold formation via "
                         "caregiver voice; MEG frequency-tagging shows "
                         "enhanced cortical tracking after singing intervention",
                         "MEG RCT, N=33, eta2=0.229"),
                Citation("Qiu et al.", 2025,
                         "Fetal-infant music exposure enhances mPFC/amygdala "
                         "dendritic complexity; dose-dependent plasticity; "
                         "social behavior improvement correlates with "
                         "synaptic density in mPFC",
                         "mouse, N=48, r=0.38"),
                Citation("Trehub", 2003,
                         "Developmental origins of musicality; infants "
                         "prefer consonance over dissonance; enhanced "
                         "processing of infant-directed singing; melodic "
                         "contour sensitivity is innate",
                         "review"),
                Citation("Strait et al.", 2012,
                         "Early musical training enhances subcortical "
                         "speech encoding; dose-dependent encoding gains; "
                         "auditory brainstem response (ABR) precision "
                         "correlates with years of training",
                         "ABR, N=31, r=0.562-0.629"),
                Citation("Trainor & Unrau", 2012,
                         "Musical training before age 7 enhances auditory "
                         "cortex development; experience-dependent sensitive "
                         "period for temporal processing",
                         "review"),
                Citation("Scholkmann et al.", 2024,
                         "Creative music therapy (CMT) induces hemodynamic "
                         "changes in neonatal prefrontal and auditory cortex; "
                         "functional near-infrared spectroscopy evidence for "
                         "scaffold activation during music therapy",
                         "fNIRS, N=17"),
                Citation("Nguyen, Trainor et al.", 2023,
                         "Universal infant-directed singing provides "
                         "ecological mechanism for scaffold formation; "
                         "caregivers communicate with infants via song "
                         "across all cultures",
                         "review"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.45, 0.65),
            falsification_criteria=(
                "Early binding (E0) must be higher for consonant + warm "
                "stimuli vs dissonant + cold; if E0 shows no difference, "
                "the neonatal scaffold model is invalid (Partanen 2022: "
                "singing vs no-singing eta2=0.229)",
                "Developmental plasticity (E1) should show dose-dependent "
                "response: more exposure -> higher plasticity index; if "
                "flat, critical period model is invalid (Qiu 2025: r=0.38 "
                "dose-response)",
                "Scaffold activation (P0) should be higher for music heard "
                "during critical period (0-5y) vs novel music; if no "
                "difference, scaffold persistence is invalid (Trainor 2012: "
                "age-7 boundary for enhanced processing)",
                "Therapeutic potential (F2) must correlate with clinical "
                "music therapy outcomes; if F2 does not predict therapy "
                "responders, clinical utility claim is invalid "
                "(Scholkmann 2024: fNIRS hemodynamic changes)",
                "Bonding warmth (P1) triple product must require all three "
                "conditions (familiar + warm + consonant); if any single "
                "condition drives P1 alone, the specificity claim is "
                "invalid (Trehub 2003: consonance preference is necessary "
                "but not sufficient)",
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
        """Transform R3/H3 into 10D developmental music memory scaffold.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"MEAMN": (B, T, D), ...}``

        Returns:
            ``(B, T, 10)`` -- E(3) + M(2) + P(2) + F(3)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
