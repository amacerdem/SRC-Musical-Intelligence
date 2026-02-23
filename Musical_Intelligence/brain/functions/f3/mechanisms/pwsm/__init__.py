"""PWSM -- Precision-Weighted Salience Model.

Associator nucleus (depth 2) in ASU, Function F3. Models how prediction
errors are weighted by precision estimates to determine their salience --
the predictive coding framework where high-precision prediction errors
gain salience while low-precision errors are suppressed, implementing
the mismatch negativity (MMN) and context reliability computations.

Reads: SNEM (entrainment/novelty), IACM (auditory context)

R3 Ontology Mapping (v1 -> 97D freeze):
    spectral_flux:        [10]  (B group, onset_strength proxy)
    onset_strength:       [11]  (B group, event salience)
    spectral_change:      [21]  (D group)
    distribution_entropy: [22]  (D group)
    pitch_height:         [37]  (K group)

Output structure: E(3) + M(2) + P(2) + F(2) = 9D
  E-layer [0:3]   Extraction    (sigmoid activation)       scope=internal
  M-layer [3:5]   Memory        (precision dynamics)        scope=internal
  P-layer [5:7]   Present       (weighted error state)      scope=hybrid
  F-layer [7:9]   Forecast      (precision predictions)     scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/pwsm/
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
    0: "25ms (gamma)",
    1: "38ms (high-gamma)",
    3: "100ms (alpha-beta)",
    4: "125ms (beta-fast)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 17: "peaks",
    20: "contour", 21: "contrast",
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


# -- R3 feature indices (post-freeze 97D) -------------------------------------
_SPECTRAL_FLUX = 10       # spectral_flux / onset_strength proxy (B group)
_ONSET_STRENGTH = 11      # onset_strength (B group)
_SPECTRAL_CHANGE = 21     # spectral_change (D group)
_ENTROPY = 22             # distribution_entropy (D group)
_PITCH_HEIGHT = 37        # pitch_height (K group)


# -- 16 H3 Demand Specifications -----------------------------------------------
# E-layer: 6 tuples, M-layer: 6 tuples, P-layer: 2 tuples, F-layer: 2 tuples

_PWSM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Precision Weighting + Error Suppression (6 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 17, 2,
        "Flux peaks 1s bidi -- salient onset detection for PE weighting",
        "Garrido 2009"),
    _h3(_ENTROPY, "distribution_entropy", 16, 2, 2,
        "Entropy std 1s bidi -- spectral uncertainty for precision",
        "Friston 2005"),
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 2, 2,
        "Onset std 100ms bidi -- onset variability for error detection",
        "Garrido 2009"),
    _h3(_PITCH_HEIGHT, "pitch_height", 3, 20, 2,
        "Pitch contour 100ms bidi -- melodic contour for prediction",
        "Winkler 2009"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 3, 0, 2,
        "Spectral change value 100ms bidi -- instant spectral deviation",
        "Garrido 2009"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 2, 2,
        "Spectral change std 1s bidi -- long-range flux variability",
        "Friston 2005"),

    # === M-Layer: PE Weighted + Precision (6 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Flux value 100ms bidi -- instant onset for PE computation",
        "Garrido 2009"),
    _h3(_ENTROPY, "distribution_entropy", 3, 0, 2,
        "Entropy value 100ms bidi -- instant complexity for precision",
        "Friston 2005"),
    _h3(_PITCH_HEIGHT, "pitch_height", 3, 0, 2,
        "Pitch height value 100ms bidi -- pitch for PE baseline",
        "Winkler 2009"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 0, 0, 2,
        "Flux value 25ms bidi -- fast onset at brainstem for precision",
        "Garrido 2009"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 1, 1, 2,
        "Flux mean 38ms bidi -- sustained fast onset for precision track",
        "Garrido 2009"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 4, 17, 2,
        "Flux peaks 125ms bidi -- beta-rate onset peaks for PE",
        "Friston 2005"),

    # === P-Layer: Weighted Error + Precision Estimate (2 tuples) ===
    _h3(_PITCH_HEIGHT, "pitch_height", 3, 17, 2,
        "Pitch peaks 100ms bidi -- pitch event salience for MMN",
        "Winkler 2009"),
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 2,
        "Onset value 100ms bidi -- event strength for error weighting",
        "Garrido 2009"),

    # === F-Layer: MMN Presence + Context Reliability (2 tuples) ===
    _h3(_PITCH_HEIGHT, "pitch_height", 16, 21, 2,
        "Pitch contrast 1s bidi -- pitch range for MMN prediction",
        "Winkler 2009"),
    _h3(_PITCH_HEIGHT, "pitch_height", 16, 17, 2,
        "Pitch peaks 1s bidi -- pitch event prediction for context",
        "Friston 2005"),
)

assert len(_PWSM_H3_DEMANDS) == 16


class PWSM(Associator):
    """Precision-Weighted Salience Model -- ASU Associator (depth 2, 9D).

    Models precision-weighted prediction error computation for auditory
    salience. High-precision errors (reliable context + large mismatch)
    drive MMN and attentional capture. Low-precision errors (uncertain
    context) are suppressed.

    Garrido et al. (2009) showed that MMN reflects precision-weighted
    PE in a hierarchical predictive coding framework (MEG/EEG + DCM,
    N=16). Friston (2005) formalized precision as inverse variance of
    prediction errors in the free energy principle. Winkler et al.
    (2009) demonstrated that auditory regularity representations track
    statistical structure and generate predictions.

    Dependency chain:
        SNEM (Depth 0, Relay) + IACM (Depth 0, Relay)
        --> [intermediate depth 1] --> PWSM (Depth 2)

    Upstream reads:
        SNEM: entrainment_strength [1], beat_onset_pred [3]
        IACM: context reliability dimensions

    Downstream feeds:
        -> precision_estimate belief (Appraisal, F3)
        -> SDL (salience driving level, depth 2)
        -> salience engine (precision enrichment)
    """

    NAME = "PWSM"
    FULL_NAME = "Precision-Weighted Salience Model"
    UNIT = "ASU"
    FUNCTION = "F3"
    OUTPUT_DIM = 9
    UPSTREAM_READS = ("SNEM", "IACM")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("f19:precision_weighting", "f20:error_suppression",
             "f21:stability_encoding"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:pe_weighted", "M1:precision"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:weighted_error", "P1:precision_estimate"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 9,
            ("F0:mmn_presence_pred", "F1:context_reliability"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PWSM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f19:precision_weighting", "f20:error_suppression",
            "f21:stability_encoding",
            "M0:pe_weighted", "M1:precision",
            "P0:weighted_error", "P1:precision_estimate",
            "F0:mmn_presence_pred", "F1:context_reliability",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Superior Temporal Gyrus -- MMN generation
            RegionLink("P0:weighted_error", "STG", 0.80,
                       "Garrido 2009"),
            # Inferior Frontal Gyrus -- precision estimation
            RegionLink("P1:precision_estimate", "IFG", 0.70,
                       "Garrido 2009"),
            # Anterior Insula -- salience detection
            RegionLink("f19:precision_weighting", "AI", 0.65,
                       "Friston 2005"),
            # ACC -- error monitoring and context reliability
            RegionLink("F1:context_reliability", "ACC", 0.60,
                       "Friston 2005"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Acetylcholine -- precision modulation
            NeuroLink("P1:precision_estimate", "acetylcholine", 0.45,
                      "Friston 2005"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Garrido", 2009,
                         "MMN reflects precision-weighted prediction error "
                         "in hierarchical predictive coding framework; "
                         "Bayesian model comparison favors predictive coding "
                         "over adaptation account",
                         "MEG/EEG + DCM, N=16"),
                Citation("Friston", 2005,
                         "Free energy principle: precision as inverse "
                         "variance of prediction errors; high precision "
                         "= confident predictions = large PE when violated",
                         "theoretical"),
                Citation("Winkler", 2009,
                         "Auditory regularity representations track "
                         "statistical structure and generate predictions; "
                         "MMN indexes violation of regularity model",
                         "review"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.55, 0.75),
            falsification_criteria=(
                "Precision weighting (f19) must amplify PE for regular "
                "contexts and suppress PE for irregular contexts "
                "(Friston 2005: precision = inverse variance)",
                "MMN presence (F0) must be larger for high-precision "
                "violations than low-precision violations (Garrido 2009: "
                "Bayesian model comparison)",
                "Context reliability (F1) must decrease with increasing "
                "stimulus entropy (Winkler 2009: regularity representation); "
                "if reliability stays high for random sequences, model invalid",
                "Error suppression (f20) must increase for repeated stimuli "
                "(adaptation) but decrease for deviant stimuli (surprise); "
                "monotonic behavior in either direction = model invalid",
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
        """Transform R3/H3 + SNEM/IACM upstream into 9D precision-weighted salience.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"SNEM": (B, T, 12), "IACM": (B, T, 11)}``

        Returns:
            ``(B, T, 9)`` -- E(3) + M(2) + P(2) + F(2)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, e, m, upstream_outputs)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
