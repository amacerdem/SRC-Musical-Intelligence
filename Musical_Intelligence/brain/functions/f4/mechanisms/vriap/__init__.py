"""VRIAP -- VR-Integrated Analgesia Paradigm.

Associator nucleus (depth 2) in IMU, Function F4. Models the
VR-integrated analgesic mechanisms whereby active musical engagement
in virtual reality gates pain processing through motor-sensory
coupling, multi-modal binding, and S1 connectivity modulation.

Core finding (Liang 2025): VRMS enhances bilateral PM&SMA FC vs
VRAO (t=3.574, p=0.004 FDR) and S1 FC (t=4.023, p=0.002 FDR,
fNIRS, N=50). Active motor engagement with music generates efference
copies that gate nociceptive input through S1 (Melzack & Wall 1965).

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, dissonance proxy)
    stumpf_fusion:          [3]      (A, multi-modal binding)
    sensory_pleasantness:   [4]      (A, comfort/safety signal)
    amplitude:              [7]      (B, engagement intensity)
    loudness:               [10]     (B, arousal correlate)
    onset_strength:         [11]     (B, motor cueing)
    spectral_flux:          [21]     (D, event salience)
    entropy:                [22]     (D, predictability proxy)
    x_l0l5:                 [25:33]  (F, motor-sensory coupling)
    x_l5l7:                 [41:49]  (G, comfort-familiarity coupling)

Output structure: E(3) + M(2) + P(2) + F(3) = 10D
  E-layer [0:3]   Extraction     (sigmoid)  scope=internal
  M-layer [3:5]   Memory         (sigmoid/product)  scope=internal
  P-layer [5:7]   Present        (clamp)    scope=hybrid
  F-layer [7:10]  Forecast       (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/vriap/
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
    16: "1000ms (beat)",
    20: "5000ms (phrase)",
    24: "36000ms (section)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 3: "std", 4: "max",
    8: "velocity", 18: "trend", 19: "stability",
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
_STUMPF = 3
_PLEASANTNESS = 4
_AMPLITUDE = 7
_LOUDNESS = 10
_ONSET = 11
_SPECTRAL_FLUX = 21
_ENTROPY = 22


# -- 18 H3 Demand Specifications -----------------------------------------------
# Multi-scale: H16(1s) -> H20(5s) -> H24(36s)
# Laws: L0=memory(backward), L2=integration(bidirectional)
#
# E-layer: 7 unique tuples (motor engagement, pain gating, multi-modal binding)
# M-layer: 5 unique tuples (sustained dynamics for analgesia integration)
# P-layer: 1 new tuple (spectral_flux value; 3 shared with E)
# F-layer: 5 new tuples (prediction horizons; 3 shared with M)

_VRIAP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Episodic Engagement (7 tuples) ===
    _h3(_ONSET, "onset_strength", 16, 0, 2,
        "Onset value 1s L2 -- motor cueing signal for active engagement",
        "Liang 2025"),
    _h3(_LOUDNESS, "loudness", 16, 0, 2,
        "Loudness value 1s L2 -- engagement intensity / immersion",
        "Liang 2025"),
    _h3(_AMPLITUDE, "amplitude", 16, 8, 0,
        "Amplitude velocity 1s L0 -- energy change rate for motor coupling",
        "Liang 2025"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Pleasantness value 1s L2 -- comfort level for pain gating",
        "Liang 2025"),
    _h3(_ROUGHNESS, "roughness", 16, 0, 2,
        "Roughness value 1s L2 -- dissonance level (inverted for safety)",
        "Liang 2025"),
    _h3(_ENTROPY, "entropy", 16, 0, 2,
        "Entropy value 1s L2 -- unpredictability for binding modulation",
        "Bushnell 2013"),
    _h3(_STUMPF, "stumpf_fusion", 16, 1, 2,
        "Stumpf fusion mean 1s L2 -- binding stability for multi-modal integration",
        "Bushnell 2013"),

    # === M-layer: Temporal Integration (5 tuples) ===
    _h3(_ONSET, "onset_strength", 20, 1, 0,
        "Onset mean 5s L0 -- sustained motor drive trajectory",
        "Arican 2025"),
    _h3(_LOUDNESS, "loudness", 20, 1, 0,
        "Loudness mean 5s L0 -- sustained immersion level",
        "Arican 2025"),
    _h3(_AMPLITUDE, "amplitude", 20, 4, 0,
        "Amplitude max 5s L0 -- peak energy for engagement ceiling",
        "Liang 2025"),
    _h3(_PLEASANTNESS, "sensory_pleasantness", 20, 18, 0,
        "Pleasantness trend 5s L0 -- comfort trajectory for analgesia build-up",
        "Putkinen 2025"),
    _h3(_ROUGHNESS, "roughness", 20, 18, 0,
        "Roughness trend 5s L0 -- dissonance trajectory for pain modulation",
        "Putkinen 2025"),

    # === P-layer: Cognitive Present (1 new tuple) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 0, 2,
        "Spectral flux value 1s L2 -- event salience for motor-pain state",
        "Liang 2025"),

    # === F-layer: Forecast (5 new tuples) ===
    _h3(_LOUDNESS, "loudness", 24, 3, 0,
        "Loudness std 36s L0 -- engagement variability over section scale",
        "Liang 2025"),
    _h3(_ENTROPY, "entropy", 20, 1, 0,
        "Entropy mean 5s L0 -- complexity context for engagement prediction",
        "Bushnell 2013"),
    _h3(_ENTROPY, "entropy", 24, 19, 0,
        "Entropy stability 36s L0 -- pattern stability for consolidation",
        "Bushnell 2013"),
    _h3(_STUMPF, "stumpf_fusion", 20, 1, 0,
        "Stumpf fusion mean 5s L0 -- binding stability for analgesia prediction",
        "Bushnell 2013"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 20, 1, 0,
        "Spectral flux mean 5s L0 -- sustained change rate for event prediction",
        "Garza-Villarreal 2017"),
)

assert len(_VRIAP_H3_DEMANDS) == 18


class VRIAP(Associator):
    """VR-Integrated Analgesia Paradigm -- IMU Associator (depth 2, 10D).

    Models VR-integrated analgesic mechanisms through three interacting
    pathways: active motor engagement (E0), pain gating via S1
    connectivity reduction (E1), and multi-modal hippocampal binding
    (E2). The multiplicative analgesia index (M0) requires all three
    pathways to co-activate for meaningful pain modulation.

    Liang et al. (2025): VRMS enhances bilateral PM&SMA FC vs VRAO
    (t=3.574, p=0.004 FDR; fNIRS, N=50); S1 FC enhancement (t=4.023,
    p=0.002 FDR). Active motor engagement generates efference copies
    that gate nociceptive input.

    Arican & Soyman (2025): Active task engagement > silence for
    analgesia (W=236.5, p=0.001, r_rb=0.491, N=123); passive music
    alone not significant (p=0.101).

    Putkinen et al. (2025): NAcc opioid release correlates with chills
    (r=-0.52, PET, N=15); pleasure-dependent BOLD in ACC (fMRI, N=30).

    Memory-only pathway (no specific upstream reads required).

    Downstream feeds:
        -> analgesic memory beliefs, motor-pain interaction assessments
        -> S1 connectivity modulation for pain processing
    """

    NAME = "VRIAP"
    FULL_NAME = "VR-Integrated Analgesia Paradigm"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ()
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:motor_engagement", "E1:pain_gate",
             "E2:multimodal_binding"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:analgesia_index", "M1:active_passive_differential"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:motor_pain_state", "P1:s1_connectivity"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:analgesia_fc", "F1:engagement_fc", "F2:reserved"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _VRIAP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:motor_engagement", "E1:pain_gate",
            "E2:multimodal_binding",
            "M0:analgesia_index", "M1:active_passive_differential",
            "P0:motor_pain_state", "P1:s1_connectivity",
            "F0:analgesia_fc", "F1:engagement_fc", "F2:reserved",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # PM&SMA -- motor planning, efference copy generation
            RegionLink("E0:motor_engagement", "PM_SMA", 0.85,
                       "Liang 2025"),
            # S1 -- pain signal propagation, connectivity reduced
            RegionLink("E1:pain_gate", "S1", 0.85,
                       "Liang 2025"),
            # Anterior Insula -- pain awareness, interoceptive gating
            RegionLink("E1:pain_gate", "anterior_insula", 0.75,
                       "Putkinen 2025"),
            # Hippocampus -- multi-modal binding, analgesic memory
            RegionLink("E2:multimodal_binding", "hippocampus", 0.70,
                       "Bushnell 2013"),
            # M1 -- motor execution, VRMS > VRMI activation
            RegionLink("M0:analgesia_index", "M1", 0.80,
                       "Liang 2025"),
            # DLPFC -- cognitive control, VRMS hetero-FC
            RegionLink("P0:motor_pain_state", "DLPFC", 0.75,
                       "Liang 2025"),
            # mPFC -- pain appraisal, therapeutic context
            RegionLink("F0:analgesia_fc", "mPFC", 0.65,
                       "Bushnell 2013"),
            # NAcc -- opioid release, music pleasure
            RegionLink("M1:active_passive_differential", "NAcc", 0.70,
                       "Putkinen 2025"),
            # ACC -- pain-pleasure appraisal, trajectory evaluation
            RegionLink("F0:analgesia_fc", "ACC", 0.65,
                       "Putkinen 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # VRIAP is motor-analgesic, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Liang et al.", 2025,
                         "VRMS enhances bilateral PM&SMA FC vs VRAO "
                         "(t=3.574, p=0.004 FDR); S1 FC enhancement "
                         "(t=4.023, p=0.002 FDR); RDLPFC hetero-FC "
                         "with S1/PM&SMA/M1 (p<0.05 FDR); bilateral "
                         "M1 activation VRMS > VRMI (RM1 z=-2.196, "
                         "p=0.028)",
                         "fNIRS, N=50"),
                Citation("Arican & Soyman", 2025,
                         "Active task engagement > silence for analgesia "
                         "(W=236.5, p=0.001, r_rb=0.491, N=123); "
                         "passive music alone not significant (p=0.101)",
                         "behavioral, N=123"),
                Citation("Putkinen et al.", 2025,
                         "NAcc opioid release correlates with musical "
                         "chills (BPND x chills r=-0.52, PET, N=15); "
                         "pleasure-dependent BOLD in ACC, insula, SMA "
                         "(cluster-level FWE p<0.05, fMRI, N=30)",
                         "PET+fMRI, N=15+30"),
                Citation("Bushnell et al.", 2013,
                         "Cognitive and emotional control of pain through "
                         "mPFC/insula pathways; multi-modal integration "
                         "modulates nociceptive processing",
                         "review"),
                Citation("Melzack & Wall", 1965,
                         "Gate control theory: non-nociceptive input gates "
                         "pain signal transmission at spinal cord level",
                         "theory"),
                Citation("Garza-Villarreal et al.", 2017,
                         "Moderate pooled analgesic effects of music "
                         "across chronic pain conditions",
                         "systematic review + meta-analysis"),
            ),
            evidence_tier="beta",
            confidence_range=(0.60, 0.80),
            falsification_criteria=(
                "Analgesia index (M0) must be multiplicative: removing any "
                "one pathway (motor engagement, pain gating, or multi-modal "
                "binding) should collapse M0 toward zero; if additive model "
                "fits better, multiplicative gating is invalid",
                "Active-passive differential (M1) must show active > passive "
                "for pain reduction; if passive music alone produces equal "
                "analgesia, the motor-engagement pathway is unnecessary "
                "(contradicts Arican & Soyman 2025: passive p=0.101)",
                "S1 connectivity (P1) must decrease during active motor "
                "engagement; if S1 connectivity is unchanged or increases, "
                "gate control mechanism is invalid (Liang 2025: t=4.023)",
                "Motor engagement (E0) must correlate with PM&SMA FC; "
                "if PM&SMA shows no enhancement during active engagement, "
                "efference copy generation claim is invalid",
                "Multi-modal binding (E2) should be stronger when auditory, "
                "visual, and motor streams are all present; unimodal "
                "conditions should show reduced E2 (Bushnell 2013)",
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
        """Transform R3/H3 into 10D VR-integrated analgesia output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: Dict mapping nucleus NAME -> routable output
                              (memory-only pathway, no specific reads).

        Returns:
            ``(B, T, 10)`` -- E(3) + M(2) + P(2) + F(3)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(h3_features, e, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
