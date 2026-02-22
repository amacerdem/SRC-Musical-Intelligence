"""MCCN -- Musical Chills Cortical Network.

Encoder nucleus (depth 1) in RPU, Function F6. Models the cortical network
underlying musical chills -- the frisson response characterized by goosebumps,
shivers, and intense pleasure during peak musical moments.

Reads: DAED (dopamine anticipation-experience), MORMR (mu-opioid reward)

R3 Ontology Mapping (post-freeze 97D):
    roughness:          [0]      (A, tension -- inverse consonance)
    amplitude:          [7]      (B, crescendo detection)
    loudness:           [8]      (B, perceptual intensity / chills trigger)
    rms_energy:         [9]      (B, physiological arousal correlate)
    spectral_change:    [21]     (D, surprise events)
    energy_change:      [22]     (D, dynamic shift / crescendo-decrescendo)
    x_l0l5:             [25:33]  (F, theta proxy via low-band coupling)

Output structure: E(4) + P(2) + F(1) = 7D
  E-layer  [0:4]  Extraction        (sigmoid)  scope=internal
  P-layer  [4:6]  Cognitive Present (sigmoid)  scope=hybrid
  F-layer  [6:7]  Forecast          (sigmoid)  scope=external

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/mccn/
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

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    3: "100ms (theta)",
    8: "500ms (chills-trigger)",
    16: "1s (sustained)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 4: "max",
    8: "velocity", 14: "periodicity",
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


# -- R3 feature names (post-freeze 97D) --------------------------------------
_ROUGHNESS = 0
_AMPLITUDE = 7
_LOUDNESS = 8
_RMS_ENERGY = 9
_SPECTRAL_CHANGE = 21
_ENERGY_CHANGE = 22


# -- 16 unique H3 Demand Specifications ---------------------------------------
# Musical Chills Cortical Network requires theta oscillation tracking (x_l0l5),
# loudness/amplitude dynamics (chills triggers), RMS energy (arousal),
# roughness (tension), spectral/energy change (surprise). All L2 (bidi).
# P-layer (6 tuples) and F-layer (6 tuples) are subsets of E-layer (16 tuples).

_MCCN_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Theta pathway (x_l0l5 coupling) ===
    _h3(_ROUGHNESS, "roughness", 8, 1, 2,
        "Mean roughness 500ms -- tension tracking",
        "Chabin 2020"),                                    # 0
    _h3(_ROUGHNESS, "roughness", 16, 2, 2,
        "Roughness variability 1s -- tension dynamics",
        "Chabin 2020"),                                    # 1
    _h3(25, "x_l0l5", 3, 0, 2,
        "Low-band coupling at 100ms -- theta proxy",
        "Chabin 2020"),                                    # 2
    _h3(25, "x_l0l5", 3, 14, 2,
        "Theta periodicity at 100ms -- oscillation tracking",
        "Chabin 2020"),                                    # 3
    _h3(25, "x_l0l5", 16, 14, 2,
        "Low-band periodicity at 1s -- sustained theta",
        "Chabin 2020"),                                    # 4
    _h3(25, "x_l0l5", 16, 1, 2,
        "Mean low-band coupling over 1s",
        "Chabin 2020"),                                    # 5

    # === Amplitude / loudness dynamics ===
    _h3(_AMPLITUDE, "amplitude", 8, 8, 2,
        "Amplitude velocity at 500ms -- crescendo rate",
        "Salimpoor 2011"),                                 # 6
    _h3(_AMPLITUDE, "amplitude", 16, 2, 2,
        "Amplitude variability over 1s -- dynamic range",
        "Chabin 2020"),                                    # 7
    _h3(_LOUDNESS, "loudness", 3, 0, 2,
        "Loudness at 100ms -- instantaneous intensity",
        "Chabin 2020"),                                    # 8
    _h3(_LOUDNESS, "loudness", 8, 4, 2,
        "Peak loudness over 500ms -- chills trigger peak",
        "Salimpoor 2011"),                                 # 9
    _h3(_LOUDNESS, "loudness", 16, 1, 2,
        "Mean loudness over 1s -- baseline",
        "Chabin 2020"),                                    # 10

    # === RMS energy (arousal) ===
    _h3(_RMS_ENERGY, "rms_energy", 3, 0, 2,
        "RMS energy at 100ms -- arousal correlate",
        "Chabin 2020"),                                    # 11
    _h3(_RMS_ENERGY, "rms_energy", 8, 8, 2,
        "Energy velocity at 500ms -- arousal buildup",
        "Chabin 2020"),                                    # 12
    _h3(_RMS_ENERGY, "rms_energy", 16, 1, 2,
        "Mean energy over 1s -- sustained activation",
        "Chabin 2020"),                                    # 13

    # === Surprise / spectral dynamics ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 0, 2,
        "Spectral deviation at 500ms -- surprise event",
        "Putkinen 2025"),                                  # 14
    _h3(_ENERGY_CHANGE, "energy_change", 8, 8, 2,
        "Energy change velocity at 500ms -- dynamic shift",
        "Chabin 2020"),                                    # 15
)

assert len(_MCCN_H3_DEMANDS) == 16


class MCCN(Encoder):
    """Musical Chills Cortical Network -- RPU Encoder (depth 1, 7D).

    Models the cortical network underlying musical chills from Chabin et al.
    (2020). The HD-EEG study (N=18) identified a characteristic theta
    oscillation pattern: simultaneous right prefrontal theta increase and
    central/temporal theta decrease during chills. Source localization
    (LAURA) revealed OFC, bilateral insula, SMA, and bilateral STG
    co-activation (all p < 1e-05).

    The model computes three layers:
      E-layer (4D): theta prefrontal/central oscillation contrast,
          physiological arousal, and chills magnitude.
      P-layer (2D): distributed network activation state and theta
          biomarker pattern.
      F-layer (1D): chills onset prediction based on acoustic buildup
          and current network engagement.

    Chabin et al. 2020: theta contrast + source localization during chills
    (HD-EEG, N=18). RPF theta F(2,15)=3.28, beta/alpha F(2,15)=4.77.

    Putkinen et al. 2025: OFC + amygdala MOR during chills (PET, N=15).

    Salimpoor et al. 2011: caudate (anticipatory) and NAcc (consummatory)
    dopamine release during chills (PET, [11C]raclopride, N=8).

    Dependency chain:
        MCCN is an Encoder (Depth 1) -- reads DAED and MORMR relay outputs.
        Computed after DAED and MORMR in F6 pipeline.

    Downstream feeds:
        -> chills_magnitude belief (Core/Appraisal)
        -> DAED anticipatory dopamine modulation via chills prediction
        -> salience computation via network_state
    """

    NAME = "MCCN"
    FULL_NAME = "Musical Chills Cortical Network"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 7
    UPSTREAM_READS = ("DAED", "MORMR")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="RPU_DAED__RPU_MCCN__anticipatory_da",
            name="DAED anticipatory dopamine to MCCN chills prediction",
            source_unit="RPU",
            source_model="DAED",
            source_dims=("anticipatory_da",),
            target_unit="RPU",
            target_model="MCCN",
            correlation="r=0.71",
            citation="Salimpoor 2011",
        ),
        CrossUnitPathway(
            pathway_id="RPU_MORMR__RPU_MCCN__opioid_context",
            name="MORMR opioid reward context to MCCN chills magnitude",
            source_unit="RPU",
            source_model="MORMR",
            source_dims=("opioid_tone",),
            target_unit="RPU",
            target_model="MCCN",
            correlation="r=0.65",
            citation="Putkinen 2025",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:theta_prefrontal", "E1:theta_central",
             "E2:arousal_index", "E3:chills_magnitude"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 4, 6,
            ("P0:network_state", "P1:theta_pattern"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 6, 7,
            ("F0:chills_onset_pred",),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MCCN_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:theta_prefrontal", "E1:theta_central",
            "E2:arousal_index", "E3:chills_magnitude",
            "P0:network_state", "P1:theta_pattern",
            "F0:chills_onset_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # OFC -- theta reward pathway, source localization p < 1e-05
            RegionLink("E0:theta_prefrontal", "OFC", 0.85,
                       "Chabin 2020"),
            # Insula -- bilateral activation during chills, p < 1e-06
            RegionLink("P0:network_state", "insula", 0.80,
                       "Chabin 2020"),
            # SMA -- motor preparation during chills, p < 1e-07
            RegionLink("P0:network_state", "SMA", 0.75,
                       "Chabin 2020"),
            # STG -- auditory processing during chills
            RegionLink("P1:theta_pattern", "STG", 0.80,
                       "Chabin 2020"),
            # Caudate -- anticipatory DA before chills
            RegionLink("F0:chills_onset_pred", "caudate", 0.80,
                       "Salimpoor 2011"),
            # NAcc -- consummatory DA at chills peak
            RegionLink("E3:chills_magnitude", "NAcc", 0.85,
                       "Salimpoor 2011"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- caudate anticipatory DA predicting chills
            NeuroLink("F0:chills_onset_pred", "dopamine", 0.80,
                      "Salimpoor 2011"),
            # Opioid -- MOR binding in OFC during chills
            NeuroLink("E3:chills_magnitude", "opioid", 0.75,
                      "Putkinen 2025"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Chabin et al.", 2020,
                         "Musical chills: theta oscillation contrast "
                         "(prefrontal increase + central decrease) with "
                         "OFC/insula/SMA/STG co-activation (LAURA); "
                         "RPF theta F(2,15)=3.28, beta/alpha F(2,15)=4.77",
                         "HD-EEG, N=18"),
                Citation("Putkinen et al.", 2025,
                         "OFC + amygdala mu-opioid receptor availability "
                         "predicts music-evoked chills; MOR binding "
                         "correlates with chills frequency",
                         "PET, [11C]carfentanil, N=15"),
                Citation("Salimpoor et al.", 2011,
                         "Anatomically distinct dopamine release during "
                         "anticipation (caudate) and experience (NAcc) of "
                         "peak emotion to music; caudate r=0.71",
                         "PET, [11C]raclopride, N=8"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.85),
            falsification_criteria=(
                "Theta prefrontal (f01) must increase during chills while "
                "theta central (f02) must decrease (inverse pattern); "
                "Chabin 2020: RPF up p=0.049, RC down p=0.025",
                "Chills magnitude (f04) requires co-activation of both "
                "theta prefrontal (f01) and arousal (f03); f01*f03 product "
                "must be significantly above chance for high f04 values",
                "Network state (P0) must correlate with OFC + insula + SMA "
                "+ STG BOLD activation (testable with concurrent fMRI-EEG)",
                "Chills onset prediction (F0) must precede actual chills "
                "by 1-3s; anticipatory DA in caudate (Salimpoor 2011, "
                "r=0.71) provides the temporal constraint",
                "Disrupting theta oscillation contrast (e.g., TMS to "
                "right prefrontal cortex) should reduce chills frequency "
                "without affecting arousal (testable with TMS-EEG)",
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
        """Transform R3/H3 + DAED/MORMR relay outputs into 7D chills network.

        Delegates to 3 layer functions (extraction -> cognitive_present ->
        forecast) and stacks results. No M-layer (temporal integration)
        for MCCN.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"DAED": (B, T, D), "MORMR": (B, T, D)}``

        Returns:
            ``(B, T, 7)`` -- E(4) + P(2) + F(1)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        p = compute_cognitive_present(e)
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
