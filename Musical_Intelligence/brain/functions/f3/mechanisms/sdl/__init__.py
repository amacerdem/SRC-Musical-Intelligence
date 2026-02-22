"""SDL -- Salience-Dependent Lateralization.

Associator nucleus (depth 2, reads STANM upstream + PWSM cross-function from F2)
in ASU, Function F3. Models how hemispheric lateralization of auditory processing
shifts dynamically as a function of acoustic salience: spectrally complex stimuli
recruit right-lateralized networks while temporally complex stimuli recruit
left-lateralized networks, with the balance modulated by attentional demands
and cross-stream coupling.

Dependency chain:
    SDL is an Associator (Depth 2) -- reads upstream STANM (Encoder, depth 1).
    Cross-unit input: PWSM (F2) provides precision-weighted spectral modulation.

R3 Ontology Mapping (97D freeze):
    loudness:           [8]   (A, velocity_D -- intensity envelope)
    spectral_flux:      [10]  (B, onset_strength -- temporal onset proxy)
    spectral_centroid:  [15]  (C, spectral focus)
    x_l0l5:             [25]  (F, coupling -- cross-band interaction)
    x_l4l5:             [37]  (F, cross-stream interaction)

Output structure: E(3) + M(2) + P(2) + F(2) = 9D
  E-layer [0:3]  Extraction   (tanh/sigmoid)  scope=internal
  M-layer [3:5]  Memory       (tanh/sigmoid)  scope=internal
  P-layer [5:7]  Present      (tanh/sigmoid)  scope=hybrid
  F-layer [7:9]  Forecast     (sigmoid)       scope=external

CRITICAL: E0, M0, P0 use torch.tanh for lateralization dims [-1, 1].
          All other dims use torch.sigmoid [0, 1].
          Final clamp is (-1, 1).

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/sdl/
Poeppel 2003: Asymmetric sampling in time (temporal windows).
Zatorre 2002: Hemispheric specialization for spectral vs temporal processing.
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
    0: "25ms (gamma)",
    1: "50ms (gamma)",
    3: "100ms (alpha-beta)",
    4: "125ms (theta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
    17: "1250ms",
    20: "5000ms (phrase)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    14: "periodicity", 17: "peaks", 18: "trend",
    19: "stability", 20: "entropy", 21: "zero_crossings",
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
_LOUDNESS = 8             # velocity_D (A group)
_SPECTRAL_FLUX = 10       # onset_strength (B group)
_SPECTRAL_CENTROID = 15   # spectral_centroid (C group)
_X_L0L5 = 25             # coupling (F group)
_X_L4L5 = 37             # cross-stream interaction (F group)


# -- 18 H3 Demand Specifications -----------------------------------------------
# Multi-scale lateralization demands: spectral vs temporal asymmetric sampling

_SDL_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Spectral Centroid / spectral focus (2 tuples) ===
    _h3(15, "spectral_centroid", 3, 0, 2,
        "Centroid value 100ms -- spectral focus",
        "Poeppel 2003"),
    _h3(15, "spectral_centroid", 3, 2, 2,
        "Centroid std 100ms -- spectral spread",
        "Zatorre 2002"),

    # === Spectral Flux / temporal onset (4 tuples) ===
    _h3(10, "spectral_flux", 3, 0, 2,
        "Flux value 100ms -- temporal focus",
        "Poeppel 2003"),
    _h3(10, "spectral_flux", 0, 0, 2,
        "Flux instant -- fast onset",
        "Zatorre 2002"),
    _h3(10, "spectral_flux", 1, 1, 2,
        "Flux mean 50ms -- smoothed onset",
        "Zatorre 2002"),
    _h3(10, "spectral_flux", 4, 17, 2,
        "Flux peaks 125ms -- event detection",
        "Poeppel 2003"),

    # === Spectral Flux long (1 tuple) ===
    _h3(10, "spectral_flux", 16, 17, 2,
        "Flux peaks 1s -- periodicity proxy",
        "Poeppel 2003"),

    # === Loudness / intensity context (2 tuples) ===
    _h3(8, "loudness", 16, 20, 2,
        "Loudness entropy 1s -- salience demand",
        "Zatorre 2002"),
    _h3(8, "loudness", 3, 0, 2,
        "Loudness value 100ms -- intensity context",
        "Zatorre 2002"),

    # === Cross-stream x_l4l5 / bilateral processing (5 tuples) ===
    _h3(37, "x_l4l5", 3, 20, 2,
        "Cross-stream entropy 100ms -- bilateral load",
        "Zatorre 2002"),
    _h3(37, "x_l4l5", 16, 17, 2,
        "Cross-stream peaks 1s -- oscillatory marker",
        "Poeppel 2003"),
    _h3(37, "x_l4l5", 3, 0, 2,
        "Cross-stream value 100ms -- bilateral state",
        "Zatorre 2002"),
    _h3(37, "x_l4l5", 3, 2, 2,
        "Cross-stream std 100ms -- bilateral variability",
        "Zatorre 2002"),
    _h3(37, "x_l4l5", 16, 1, 2,
        "Cross-stream mean 1s -- sustained bilateral",
        "Zatorre 2002"),

    # === Cross-band coupling x_l0l5 / hemispheric dynamics (4 tuples) ===
    _h3(25, "x_l0l5", 17, 8, 0,
        "Coupling velocity 1250ms -- hemispheric shift",
        "Poeppel 2003"),
    _h3(25, "x_l0l5", 1, 0, 0,
        "Coupling value 50ms L0 -- fast binding",
        "Poeppel 2003"),
    _h3(25, "x_l0l5", 8, 1, 0,
        "Coupling mean 500ms L0 -- medium binding",
        "Poeppel 2003"),
    _h3(25, "x_l0l5", 20, 18, 0,
        "Coupling trend 5s L0 -- long dynamics",
        "Poeppel 2003"),
)

assert len(_SDL_H3_DEMANDS) == 18


class SDL(Associator):
    """Salience-Dependent Lateralization -- ASU Associator (depth 2, 9D).

    Models how hemispheric lateralization of auditory processing shifts
    dynamically as a function of acoustic salience. Poeppel 2003: asymmetric
    sampling in time -- left hemisphere operates at ~25-50ms temporal windows
    (gamma), right hemisphere at ~150-250ms (theta); spectral complexity
    biases right, temporal complexity biases left.

    Zatorre et al. 2002: hemispheric specialization review -- right AC
    preferentially processes spectral detail (pitch, timbre), left AC
    preferentially processes temporal detail (rhythm, speech rate); salience
    modulates the degree of lateralization.

    Dependency chain:
        STANM (Encoder, Depth 1) -> SDL (Associator, Depth 2)
        Cross-unit: PWSM (F2) -> SDL

    Upstream reads:
        STANM: P0:temporal_alloc [6], P1:spectral_alloc [7]

    Downstream feeds:
        -> lateralization beliefs (Appraisal)
        -> hemispheric_engagement beliefs (Anticipation)
    """

    NAME = "SDL"
    FULL_NAME = "Salience-Dependent Lateralization"
    UNIT = "ASU"
    FUNCTION = "F3"
    OUTPUT_DIM = 9
    UPSTREAM_READS = ("STANM",)
    CROSS_UNIT_READS = ("PWSM",)

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:dynamic_lateral", "E1:local_clustering",
             "E2:hemispheric_osc"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:lateralization_index", "M1:salience_demand"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:dynamic_lateral_p", "P1:hemispheric_engage"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 9,
            ("F0:network_config_pred", "F1:processing_eff_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SDL_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:dynamic_lateral", "E1:local_clustering",
            "E2:hemispheric_osc",
            "M0:lateralization_index", "M1:salience_demand",
            "P0:dynamic_lateral_p", "P1:hemispheric_engage",
            "F0:network_config_pred", "F1:processing_eff_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # left AC -- temporal processing lateralization
            RegionLink("E0:dynamic_lateral", "left_AC", 0.85,
                       "Poeppel 2003"),
            # right AC -- spectral processing lateralization
            RegionLink("E1:local_clustering", "right_AC", 0.85,
                       "Zatorre 2002"),
            # planum temporale -- asymmetric cortical surface
            RegionLink("M0:lateralization_index", "planum_temporale", 0.80,
                       "Zatorre 2002"),
            # posterior STG -- spectrotemporal integration
            RegionLink("P0:dynamic_lateral_p", "posterior_STG", 0.75,
                       "Poeppel 2003"),
            # HG -- primary auditory cortex processing
            RegionLink("E2:hemispheric_osc", "HG", 0.70,
                       "Poeppel 2003"),
            # TPJ -- lateralization switching
            RegionLink("P1:hemispheric_engage", "TPJ", 0.65,
                       "Zatorre 2002"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # SDL is lateralization-processing, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Poeppel", 2003,
                         "Asymmetric sampling in time: left hemisphere "
                         "operates at ~25-50ms temporal windows (gamma), "
                         "right hemisphere at ~150-250ms (theta); spectral "
                         "complexity biases right, temporal complexity biases "
                         "left; dual oscillatory mechanism for speech and music",
                         "Theoretical framework"),
                Citation("Zatorre et al.", 2002,
                         "Hemispheric specialization review: right AC "
                         "preferentially processes spectral detail (pitch, "
                         "timbre), left AC preferentially processes temporal "
                         "detail (rhythm, speech rate); salience modulates "
                         "degree of lateralization",
                         "fMRI/PET review"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Left hemisphere should show stronger activation for "
                "temporally complex stimuli (testable: Poeppel 2003 "
                "AST prediction with gamma-band EEG)",
                "Right hemisphere should show stronger activation for "
                "spectrally complex stimuli (confirmed: Zatorre 2002 "
                "fMRI pitch tasks)",
                "Salience should modulate lateralization magnitude "
                "(testable: attention manipulation + laterality index)",
                "Cross-stream coupling should predict bilateral "
                "recruitment (testable: EEG coherence analysis)",
                "Disrupting left planum temporale should impair temporal "
                "processing more than spectral (testable: TMS)",
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
        """Transform R3/H3 + STANM upstream into 9D lateralization representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        CRITICAL: E0, M0, P0 use torch.tanh ([-1, 1]) for lateralization
        dimensions. All other dimensions use torch.sigmoid ([0, 1]).
        Final clamp is (-1, 1) to accommodate tanh outputs.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"STANM": (B, T, 11)}``

        Returns:
            ``(B, T, 9)`` -- E(3) + M(2) + P(2) + F(2)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, e, m, upstream_outputs)
        f = compute_forecast(h3_features, m, e)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(-1.0, 1.0)
