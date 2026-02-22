"""CDMR -- Context-Dependent Mismatch Response.

Encoder nucleus (depth 1) in NDU, Function F8. Models context-dependent
mismatch negativity (MMN) and its modulation by musical expertise. The
mechanism captures how melodic context complexity amplifies deviance
detection selectively in experts, while basic mismatch responses are
present in both musicians and non-musicians.

Reads: EDNR (intra-circuit via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    onset_strength:             [10]     (B, spectral flux / deviance)
    onset_strength_alt:         [11]     (B, onset deviance)
    brightness:                 [13]     (C, tonal context)
    spectral_flux:              [21]     (D, spectral change)
    pitch_change:               [23]     (D, melodic context)
    x_l4l5:                     [33:41]  (G, pattern coupling)
    x_l5l6:                     [41:49]  (G, binding strength)

Output structure: E(4) + M(2) + P(3) + F(2) = 11D
  E-layer   [0:4]   Extraction           (sigmoid)  scope=internal
  M-layer   [4:6]   Temporal Integration (sigmoid)  scope=internal
  P-layer   [6:9]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [9:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/cdmr/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Encoder
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
    3: "100ms (alpha)",
    4: "125ms (theta)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    16: "curvature", 18: "trend", 20: "entropy",
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


# -- R3 feature name constants ------------------------------------------------
_SPECTRAL_FLUX = 10       # onset_strength (R3 naming discrepancy)
_ONSET_STRENGTH = 11      # onset_strength (alt)
_BRIGHTNESS = 13
_SPECTRAL_CHANGE = 21     # spectral_flux (R3 naming discrepancy)
_PITCH_CHANGE = 23
_X_L4L5 = 33
_X_L5L6 = 41


# -- 16 H3 Demand Specifications -----------------------------------------------
# Context-Dependent Mismatch Response requires multi-scale temporal features
# spanning fast gamma deviance (25ms) to beat-level context integration (1s).
# E-layer: 8 tuples, M-layer: 4 tuples, P-layer: 3 tuples, F-layer: 1 tuple.
# All 16 are unique.

_CDMR_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Mismatch Detection & Context (8 tuples) ===
    # 0: Instantaneous deviance at 25ms
    _h3(10, "spectral_flux", 0, 0, 2,
        "Instantaneous deviance at 25ms",
        "Crespo-Bojorque 2018"),
    # 1: Deviance variability at 100ms
    _h3(10, "spectral_flux", 3, 2, 2,
        "Deviance variability at 100ms",
        "Wagner 2018"),
    # 2: Onset deviance at 25ms
    _h3(11, "onset_strength", 0, 0, 2,
        "Onset deviance at 25ms",
        "Wagner 2018"),
    # 3: Onset velocity at 100ms
    _h3(11, "onset_strength", 3, 8, 0,
        "Onset velocity at 100ms",
        "Rupp 2022"),
    # 4: Pitch deviance at 100ms
    _h3(23, "pitch_change", 3, 0, 2,
        "Pitch deviance at 100ms",
        "Crespo-Bojorque 2018"),
    # 5: Mean pitch change over 1s
    _h3(23, "pitch_change", 16, 1, 2,
        "Mean pitch change over 1s",
        "Rupp 2022"),
    # 6: Binding strength at 100ms
    _h3(41, "x_l5l6", 3, 0, 2,
        "Binding strength at 100ms",
        "Rupp 2022"),
    # 7: Binding variability at 100ms
    _h3(41, "x_l5l6", 3, 2, 2,
        "Binding variability at 100ms",
        "Crespo-Bojorque 2018"),

    # === M-Layer: Temporal Integration (4 tuples) ===
    # 8: Mean deviance over 1s
    _h3(10, "spectral_flux", 16, 1, 2,
        "Mean deviance over 1s",
        "Fong 2020"),
    # 9: Pitch variability at 125ms
    _h3(23, "pitch_change", 4, 2, 2,
        "Pitch variability at 125ms",
        "Tervaniemi 2022"),
    # 10: Spectral deviance at 100ms
    _h3(21, "spectral_change", 3, 0, 2,
        "Spectral deviance at 100ms",
        "Fong 2020"),
    # 11: Spectral trend at 125ms
    _h3(21, "spectral_change", 4, 18, 0,
        "Spectral trend at 125ms",
        "Tervaniemi 2022"),

    # === P-Layer: Cognitive Present (3 tuples) ===
    # 12: Tonal context at 100ms
    _h3(13, "brightness", 3, 0, 2,
        "Tonal context at 100ms",
        "Rupp 2022"),
    # 13: Tonal entropy at 100ms
    _h3(13, "brightness", 3, 20, 2,
        "Tonal entropy at 100ms",
        "Crespo-Bojorque 2018"),
    # 14: Pattern coupling at 100ms
    _h3(33, "x_l4l5", 3, 0, 2,
        "Pattern coupling at 100ms",
        "Crespo-Bojorque 2018"),

    # === F-Layer: Forecast (1 tuple) ===
    # 15: Binding curvature over 1s
    _h3(41, "x_l5l6", 16, 16, 2,
        "Binding curvature over 1s",
        "Fong 2020"),
)

assert len(_CDMR_H3_DEMANDS) == 16


class CDMR(Encoder):
    """Context-Dependent Mismatch Response -- NDU Encoder (depth 1, 11D).

    Models context-dependent mismatch negativity (MMN) and its modulation
    by musical expertise. Basic mismatch responses (MMN) are present in both
    musicians and non-musicians in simple oddball paradigms, but complex
    melodic contexts amplify deviance detection selectively in experts.

    Four extraction features (mismatch_amplitude, context_modulation,
    subadditivity_index, expertise_effect) characterize context-dependent
    mismatch responses. Temporal integration computes melodic expectation
    and deviance history. The cognitive present estimates mismatch signal,
    context state, and binding state. Forecasts predict next deviance and
    context continuation.

    Crespo-Bojorque et al. 2018: consonance MMN in both musicians and
    non-musicians (172-250ms), p=0.007 (non-mus), p=0.001 (mus).
    Musicians show consonance MMN > dissonance MMN, right-lateralized
    F(1,15)=4.95, p<0.05 (EEG, N=32).

    Wagner et al. 2018: MMN for major third deviant -0.34uV +/- 0.32,
    p=0.003 (EEG).

    Rupp & Hansen 2022: musicians > non-musicians in subadditivity for
    combined melodic deviants. No group difference in classic oddball, but
    musicians > non-musicians in complex melodic paradigm (MEG).

    Tervaniemi 2022: genre-specific MMN modulation by expertise reflects
    accumulated musical syntax knowledge.

    Fong et al. 2020: MMN as prediction error signal under predictive
    coding framework.

    Koelsch: ERAN (150-250ms) reflects long-term music-syntactic
    regularities distinct from on-line MMN memory.

    Dependency chain:
        CDMR is an Encoder (Depth 1) -- reads EDNR relay output
        (F8 intra-circuit). Computed after EDNR in F8 pipeline.

    Downstream feeds:
        -> mismatch_response belief (Appraisal)
        -> context_modulation belief (Appraisal)
        -> expertise_effect belief (Appraisal)
    """

    NAME = "CDMR"
    FULL_NAME = "Context-Dependent Mismatch Response"
    UNIT = "NDU"
    FUNCTION = "F8"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("EDNR",)

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:mismatch_amplitude", "f02:context_modulation",
             "f03:subadditivity_index", "f04:expertise_effect"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 4, 6,
            ("M0:melodic_expectation", "M1:deviance_history"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 9,
            ("P0:mismatch_signal", "P1:context_state",
             "P2:binding_state"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:next_deviance", "F1:context_continuation"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _CDMR_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:mismatch_amplitude", "f02:context_modulation",
            "f03:subadditivity_index", "f04:expertise_effect",
            "M0:melodic_expectation", "M1:deviance_history",
            "P0:mismatch_signal", "P1:context_state",
            "P2:binding_state",
            "F0:next_deviance", "F1:context_continuation",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # A1/STG -- basic mismatch detection (bilateral auditory cortex)
            RegionLink("f01:mismatch_amplitude", "STG", 0.80,
                       "Rupp 2022"),
            # Anterior auditory cortex -- context modulation
            RegionLink("f02:context_modulation", "STG", 0.75,
                       "Rupp 2022"),
            # Fronto-central cortex -- subadditivity / binding
            RegionLink("f03:subadditivity_index", "IFG", 0.75,
                       "Crespo-Bojorque 2018"),
            # Right IFG -- expertise-dependent mismatch enhancement
            RegionLink("f04:expertise_effect", "IFG", 0.80,
                       "Rupp 2022"),
            # A1 -- mismatch signal
            RegionLink("P0:mismatch_signal", "A1", 0.85,
                       "Crespo-Bojorque 2018"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Glutamate -- prediction error signaling
            NeuroLink("P0:mismatch_signal", "glutamate", 0.70,
                      "Fong 2020"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Crespo-Bojorque et al.", 2018,
                         "Consonance MMN in musicians and non-musicians "
                         "(172-250ms), p=0.007 (non-mus), p=0.001 (mus). "
                         "Musicians: consonance MMN > dissonance MMN, "
                         "right-lateralized F(1,15)=4.95, p<0.05",
                         "EEG, N=32"),
                Citation("Wagner et al.", 2018,
                         "MMN for major third deviant -0.34uV +/- 0.32, "
                         "p=0.003. BESA dipole source reconstruction in "
                         "bilateral auditory cortex",
                         "EEG"),
                Citation("Rupp & Hansen", 2022,
                         "Musicians > non-musicians in subadditivity for "
                         "combined melodic deviants. No group difference in "
                         "classic oddball, but musicians > non-musicians in "
                         "complex melodic paradigm",
                         "MEG"),
                Citation("Tervaniemi", 2022,
                         "Genre-specific MMN modulation by expertise reflects "
                         "accumulated musical syntax knowledge",
                         "review"),
                Citation("Fong et al.", 2020,
                         "MMN as prediction error signal under predictive "
                         "coding framework -- deviance history forms the "
                         "prediction baseline",
                         "computational model"),
                Citation("Koelsch", 2014,
                         "ERAN (150-250ms) reflects long-term music-syntactic "
                         "regularities distinct from on-line MMN memory. "
                         "IFG generators for syntactic prediction",
                         "review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.85),
            falsification_criteria=(
                "Mismatch amplitude (f01) must show significant MMN-like "
                "response to deviant tones in both musicians and "
                "non-musicians for simple contexts (Crespo-Bojorque 2018: "
                "p=0.007 non-mus, p=0.001 mus)",
                "Context modulation (f02) must correlate with melodic "
                "context complexity; complex contexts should produce larger "
                "mismatch responses than simple oddball (Rupp 2022: "
                "musicians > non-musicians in melodic paradigm)",
                "Subadditivity index (f03) must show combined-deviant "
                "responses less than sum of individual responses; if linear "
                "summation, the integration model is invalid (Rupp 2022)",
                "Expertise effect (f04) must be near zero in simple oddball "
                "contexts and positive in complex melodic contexts "
                "(Rupp 2022: no group difference in oddball)",
                "Binding state (P2) must correlate with fronto-central "
                "activation (Crespo-Bojorque 2018: Fz electrode)",
                "Context continuation (F1) must predict future context "
                "richness within ERAN latency window (Koelsch: 150-250ms)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        relay_outputs: Dict[str, Tensor] | None = None,
    ) -> Tensor:
        """Transform R3/H3 + EDNR relay output into 11D mismatch response.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"EDNR": (B, T, 10)}`` from depth-0 relay.

        Returns:
            ``(B, T, 11)`` -- E(4) + M(2) + P(3) + F(2)
        """
        relay_outputs = relay_outputs or {}
        B, T = r3_features.shape[:2]
        device = r3_features.device
        ednr = relay_outputs.get(
            "EDNR", torch.zeros(B, T, 10, device=device),
        )

        e = compute_extraction(h3_features, r3_features, ednr)
        m = compute_temporal_integration(h3_features, r3_features, e, ednr)
        p = compute_cognitive_present(h3_features, r3_features, e, m, ednr)
        f = compute_forecast(h3_features, e, m, p, ednr)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
