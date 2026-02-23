"""SRP -- Striatal Reward Prediction.

Relay nucleus (depth 0) in ARU, Function F5. Models the dopaminergic reward
prediction system in the striatum. Caudate DA ramps quasi-hyperbolically toward
expected reward (wanting), while NAcc DA bursts phasically at peak moments
(liking). The mu-opioid system mediates hedonic impact. SRP is the F5 relay:
it directly bridges R3/H3 features to C3 cognitive-level reward representations.

Dependency chain:
    SRP is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:              [0]  -> [0]    (A, roughness)
    sensory_pleasantness:   [4]  -> [4]    (A, sensory_pleasantness)
    amplitude:              [7]  -> [7]    (B, velocity_A)
    onset_strength:         [11] -> [11]   (B, onset_strength)
    spectral_smoothness:    [16] -> [16]   (C, spectral_smoothness)
    spectral_flux:          [21] -> [21]   (D, spectral_flux)
    distribution_entropy:   [22] -> [22]   (D, unchanged)
    x_l0l5:                 [25:33]        (F, coupling)

Output structure: N+C(6) + T+M(7) + P(3) + F(3) = 19D
  N+C-layer [0:6]   Extraction          (sigmoid)    scope=internal
  T+M-layer [6:13]  Temporal Integration (sigmoid)    scope=internal
  P-layer   [13:16] Present             (sigmoid)    scope=hybrid
  F-layer   [16:19] Forecast            (sigmoid)    scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
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
    9: "350ms (sub-beat)",
    16: "1000ms (beat)",
    18: "2000ms (phrase)",
    20: "5000ms (section-short)",
    22: "15000ms (section-long)",
    24: "36000ms (section)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 4: "max", 8: "velocity",
    11: "acceleration", 14: "periodicity", 15: "smoothness",
    18: "trend", 19: "stability", 22: "peaks",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 1: "forward", 2: "integration"}


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
_ROUGHNESS = 0                   # A group
_SENSORY_PLEASANTNESS = 4        # A group
_AMPLITUDE = 7                   # B group (velocity_A)
_ONSET_STRENGTH = 11             # B group
_SPECTRAL_SMOOTHNESS = 16        # C group
_SPECTRAL_FLUX = 21              # D group
_DISTRIBUTION_ENTROPY = 22       # D group
_X_L0L5_START = 25               # F group (coupling)


# -- 31 H3 Demand Specifications ----------------------------------------------
# Multi-scale: H9(350ms) -> H16(1s) -> H18(2s) -> H20(5s) -> H22(15s) -> H24(36s)

_SRP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === N+C layer: Neurochemical extraction (tuples 1-13) ===

    # #1: Energy velocity section -- caudate ramp
    _h3(_AMPLITUDE, "amplitude", 24, 8, 0,
        "Energy velocity section — caudate DA ramp anticipation",
        "Salimpoor 2011"),
    # #2: Harmonic tension trajectory 36s
    _h3(_ROUGHNESS, "roughness", 24, 18, 0,
        "Harmonic tension trajectory 36s — section-level tension",
        "Huron 2006"),
    # #3: Future max energy 5s -- anticipation gap
    _h3(_AMPLITUDE, "amplitude", 20, 4, 1,
        "Future max energy 5s — anticipation gap for wanting",
        "Salimpoor 2011"),
    # #4: Current energy state
    _h3(_AMPLITUDE, "amplitude", 16, 0, 2,
        "Current energy state — caudate activation level",
        "Salimpoor 2011"),
    # #5: Current dissonance phrase-level
    _h3(_ROUGHNESS, "roughness", 18, 0, 2,
        "Current dissonance phrase-level — opioid proxy",
        "Zatorre 2001"),
    # #6: Baseline dissonance phrase
    _h3(_ROUGHNESS, "roughness", 18, 1, 2,
        "Baseline dissonance phrase — consonance reference",
        "Zatorre 2001"),
    # #7: Consonance phrase -- opioid proxy
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 18, 0, 2,
        "Consonance phrase — opioid hedonic proxy",
        "Blood & Zatorre 2001"),
    # #8: Smoothness phrase -- opioid signal
    _h3(_SPECTRAL_SMOOTHNESS, "spectral_smoothness", 18, 15, 2,
        "Smoothness phrase — spectral opioid warmth signal",
        "Menon & Levitin 2005"),
    # #9: Spectral change rate -- RPE trigger
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 8, 0,
        "Spectral change rate — reward prediction error trigger",
        "Cheung 2019"),
    # #10: Entropy change rate -- surprise
    _h3(_DISTRIBUTION_ENTROPY, "distribution_entropy", 16, 8, 0,
        "Entropy change rate — surprise signal for DA burst",
        "Cheung 2019"),
    # #11: Consonance surprise
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 8, 0,
        "Consonance surprise — hedonic prediction error",
        "Salimpoor 2011"),
    # #12: Energy-consonance coupling signal
    _h3(_X_L0L5_START, "x_l0l5[0]", 18, 0, 2,
        "Energy-consonance coupling — STG-NAcc pathway",
        "Salimpoor 2013"),
    # #13: Onset event density 1s
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 22, 2,
        "Onset event density 1s — rhythmic coupling",
        "Martinez-Molina 2016"),

    # === T+M layer: Temporal integration (tuples 14-24) ===

    # #14: Roughness trajectory phrase -- tension
    _h3(_ROUGHNESS, "roughness", 18, 18, 0,
        "Roughness trajectory phrase — harmonic tension buildup",
        "Huron 2006"),
    # #15: Entropy phrase -- uncertainty
    _h3(_DISTRIBUTION_ENTROPY, "distribution_entropy", 18, 0, 2,
        "Entropy phrase — uncertainty context for prediction",
        "Cheung 2019"),
    # #16: Energy buildup rate 5s -- tension
    _h3(_AMPLITUDE, "amplitude", 20, 8, 0,
        "Energy buildup rate 5s — tension accumulation",
        "Salimpoor 2011"),
    # #17: Energy velocity phrase -- dynamic intensity
    _h3(_AMPLITUDE, "amplitude", 18, 8, 0,
        "Energy velocity phrase — dynamic intensity signal",
        "Menon & Levitin 2005"),
    # #18: Energy acceleration phrase -- buildup
    _h3(_AMPLITUDE, "amplitude", 18, 11, 0,
        "Energy acceleration phrase — buildup detection",
        "Salimpoor 2011"),
    # #19: Consonance trajectory -- prediction match
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 18, 8, 0,
        "Consonance trajectory — prediction match signal",
        "Zatorre & Salimpoor 2013"),
    # #20: Spectral stability phrase
    _h3(_SPECTRAL_SMOOTHNESS, "spectral_smoothness", 18, 19, 2,
        "Spectral stability phrase — appraisal reference",
        "Huron 2006"),
    # #21: Onset regularity 1s
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 14, 2,
        "Onset regularity 1s — rhythmic predictability",
        "Martinez-Molina 2016"),
    # #22: Onset velocity -- reaction trigger
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 8, 0,
        "Onset velocity — reaction trigger for appraisal",
        "Huron 2006"),
    # #23: Spectral flux jerk -- reaction
    _h3(10, "onset_strength", 16, 11, 0,
        "Spectral flux jerk — reaction acceleration trigger",
        "Menon & Levitin 2005"),
    # #24: Peak onset phrase -- peak detection
    _h3(_ONSET_STRENGTH, "onset_strength", 18, 4, 2,
        "Peak onset phrase — peak moment detection",
        "Salimpoor 2011"),

    # === P+F layer: Present + Forecast (tuples 25-31) ===

    # #25: Consonance trend -- resolution signal
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 18, 18, 0,
        "Consonance trend — harmonic resolution signal",
        "Blood & Zatorre 2001"),
    # #26: Future peak energy 15s -- reward forecast
    _h3(_AMPLITUDE, "amplitude", 22, 4, 1,
        "Future peak energy 15s — reward forecast anticipation",
        "Salimpoor 2011"),
    # #27: Dissonance trajectory 5s -- resolution
    _h3(_ROUGHNESS, "roughness", 20, 18, 0,
        "Dissonance trajectory 5s — resolution expectation",
        "Huron 2006"),
    # #28: Consonance trend 5s -- resolution
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 20, 18, 0,
        "Consonance trend 5s — resolution expectation",
        "Blood & Zatorre 2001"),
    # #29: Forward energy velocity -- chills
    _h3(_AMPLITUDE, "amplitude", 20, 8, 1,
        "Forward energy velocity — chills proximity detection",
        "Salimpoor 2011"),
    # #30: Harmonic stability phrase
    _h3(_ROUGHNESS, "roughness", 18, 19, 2,
        "Harmonic stability phrase — resolution baseline",
        "Huron 2006"),
    # #31: Consonance trend 5s (F-layer) — forward law for forecast
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 20, 18, 1,
        "Consonance trend 5s — forecast resolution signal",
        "Zatorre & Salimpoor 2013"),
)

assert len(_SRP_H3_DEMANDS) == 31


class SRP(Relay):
    """Striatal Reward Prediction -- ARU Relay (depth 0, 19D).

    Models the dopaminergic reward prediction system in the striatum.
    Salimpoor 2011: caudate DA increases 9-15s before musical peak
    (PET [11C]raclopride, N=8, r=0.71 caudate, r=0.84 NAcc).
    Blood & Zatorre 2001: pleasant music activates NAcc, VTA, hypothalamus,
    anterior insula (PET rCBF, N=10). Zatorre & Salimpoor 2013: striatal DA
    release correlates with subjective pleasure and willingness-to-pay for
    new music (PET + fMRI + behavioral auction, N=19).

    Dependency chain:
        SRP is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> wanting/liking/pleasure for kernel scheduler
        -> F3 Attention: salience mixer tension
        -> F6 Reward: hedonic contribution
        -> precision engine: prediction_error
        -> SRP relay wrapper in scheduler
    """

    NAME = "SRP"
    FULL_NAME = "Striatal Reward Prediction"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 19

    LAYERS = (
        LayerSpec(
            "N+C", "Extraction", 0, 6,
            ("N0:da_caudate", "N1:da_nacc", "N2:opioid_proxy",
             "C0:vta_drive", "C1:stg_nacc_coupling", "C2:prediction_error"),
            scope="internal",
        ),
        LayerSpec(
            "T+M", "Temporal Integration", 6, 13,
            ("T0:tension", "T1:prediction_match", "T2:reaction",
             "T3:appraisal", "M0:harmonic_tension", "M1:dynamic_intensity",
             "M2:peak_detection"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 13, 16,
            ("P0:wanting", "P1:liking", "P2:pleasure"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 16, 19,
            ("F0:reward_forecast", "F1:chills_proximity",
             "F2:resolution_expect"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SRP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "N0:da_caudate", "N1:da_nacc", "N2:opioid_proxy",
            "C0:vta_drive", "C1:stg_nacc_coupling", "C2:prediction_error",
            "T0:tension", "T1:prediction_match", "T2:reaction",
            "T3:appraisal", "M0:harmonic_tension", "M1:dynamic_intensity",
            "M2:peak_detection",
            "P0:wanting", "P1:liking", "P2:pleasure",
            "F0:reward_forecast", "F1:chills_proximity",
            "F2:resolution_expect",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Caudate (dorsal striatum) -- anticipatory DA ramp
            RegionLink("N0:da_caudate", "Caudate", 0.90,
                       "Salimpoor 2011"),
            # NAcc (ventral striatum) -- consummatory DA burst
            RegionLink("N1:da_nacc", "NAcc", 0.90,
                       "Salimpoor 2011"),
            # VTA -- DA neuron source for striatum
            RegionLink("C0:vta_drive", "VTA", 0.85,
                       "Menon & Levitin 2005"),
            # STG -- auditory-reward structural link
            RegionLink("C1:stg_nacc_coupling", "STG", 0.80,
                       "Salimpoor 2013"),
            # OFC / vmPFC -- value computation, appraisal
            RegionLink("T3:appraisal", "OFC", 0.75,
                       "Huron 2006"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Salimpoor", 2011,
                         "Caudate DA ramps quasi-hyperbolically 9-15s before "
                         "musical peak; NAcc DA bursts at peak",
                         "PET [11C]raclopride, N=8, r=0.71/0.84"),
                Citation("Blood & Zatorre", 2001,
                         "Pleasant music activates NAcc, VTA, hypothalamus, "
                         "anterior insula",
                         "PET rCBF, N=10"),
                Citation("Zatorre & Salimpoor", 2013,
                         "Striatal DA correlates with subjective pleasure and "
                         "willingness-to-pay for new music",
                         "PET + fMRI + auction, N=19"),
                Citation("Salimpoor", 2013,
                         "STG-to-NAcc structural connectivity predicts "
                         "individual reward sensitivity",
                         "DTI + fMRI, N=19"),
                Citation("Menon & Levitin", 2005,
                         "VTA and NAcc activate during pleasant music; "
                         "mesolimbic reward pathway",
                         "fMRI 3T, N=13"),
                Citation("Huron", 2006,
                         "ITPRA theory: Imagination-Tension-Prediction-"
                         "Reaction-Appraisal stages of musical reward",
                         "theoretical framework"),
                Citation("Cheung", 2019,
                         "Uncertainty and surprise jointly determine musical "
                         "pleasure (Goldilocks effect)",
                         "behavioral + computational, N=39+38"),
                Citation("Martinez-Molina", 2016,
                         "Musical anhedonia reveals STG-NAcc disconnection; "
                         "white matter tract integrity",
                         "DTI + fMRI, N=45"),
                Citation("Ferreri", 2019,
                         "Levodopa enhances and risperidone diminishes "
                         "music-evoked reward; pharmacological DA causal",
                         "double-blind RCT, N=27"),
                Citation("Mallik", 2017,
                         "Naltrexone blocks music-evoked pleasure; mu-opioid "
                         "system mediates hedonic impact",
                         "double-blind crossover, N=15"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Music-evoked DA release in caudate/NAcc requires intact "
                "striatal reward circuitry (Salimpoor 2011: PET DA binding "
                "r=0.71/0.84)",
                "Pharmacological blockade of DA (risperidone) or opioid "
                "(naltrexone) eliminates music reward "
                "(Ferreri 2019, Mallik 2017)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 19D striatal reward prediction representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 19)`` — N+C(6) + T+M(7) + P(3) + F(3)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
