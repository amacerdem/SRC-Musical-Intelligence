"""PWUP -- Precision-Weighted Uncertainty Processing.

Encoder nucleus (depth 1, reads relay outputs) in PCU, Function F2.
Processes HTP and ICEM relay outputs to compute precision weights for
prediction errors under varying tonal/rhythmic uncertainty contexts.

In predictive coding (Friston 2005), prediction errors are weighted by
their estimated precision (inverse variance). High precision = high
confidence in the prediction; low precision = uncertain context where
errors are attenuated. PWUP computes these precision weights for musical
prediction errors using tonal and rhythmic certainty signals.

Key finding: In atonal music, tonal precision drops (d=3 effect,
Quiroga-Martinez 2019: key clarity 0.5 vs tonal 0.8), attenuating
MMN amplitude. PWUP models this precision modulation.

Dependency chain:
    PWUP is an Encoder (Depth 1) -- reads HTP and ICEM relay outputs.
    Computed after HTP and ICEM in F2 pipeline.

R3 Ontology Mapping (post-freeze 97D):
    sensory_pleasantness:  [4]      (A, consonance proxy)
    periodicity:           [5]      (A, tonal certainty)
    onset_strength:        [11]     (B, event salience)
    tonalness:             [14]     (C, key clarity proxy)
    tristimulus1-3:        [18:21]  (C, harmonic structure)
    spectral_flux:         [21]     (D, PE dynamics, was spectral_change)

Output structure: E(2) + M(2) + P(3) + F(3) = 10D
  E-layer [0:2]  Extraction    (sigmoid)  scope=internal
  M-layer [2:4]  Memory        (sigmoid)  scope=internal
  P-layer [4:7]  Present       (sigmoid)  scope=hybrid
  F-layer [7:10] Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/pwup/
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
    1: "50ms (gamma)",
    3: "100ms (alpha-beta)",
    4: "125ms (theta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    13: "entropy", 14: "periodicity", 20: "entropy",
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
_SENSORY_PLEAS = 4        # sensory_pleasantness (A group, consonance proxy)
_PERIODICITY = 5          # periodicity (A group, tonal certainty)
_ONSET_STRENGTH = 10      # onset_strength (B, H3 uses original feature index 10)
_TONALNESS = 14           # tonalness (C group, key clarity)
_SPECTRAL_FLUX = 21       # spectral_flux (D, was spectral_change)
_FUND_FREQ = 41           # fundamental_frequency (H group, tonal features)


# -- 14 H3 Demand Specifications -----------------------------------------------
# Tonal precision at multiple timescales, rhythmic precision, uncertainty signals

_PWUP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Consonance / Tonal Precision (3 tuples) ===
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 3, 0, 2,
        "Consonance at 100ms -- tonal grounding for precision estimate",
        "Quiroga-Martinez 2019"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 1, 0,
        "Mean consonance over 1s -- sustained tonal context",
        "Garrido 2009"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 20, 0,
        "Consonance entropy at 1s -- uncertainty in tonal context",
        "Sedley 2016"),

    # === Tonalness / Key Clarity (2 tuples) ===
    _h3(_TONALNESS, "tonalness", 8, 1, 0,
        "Mean tonalness over 500ms -- tonal precision baseline",
        "Quiroga-Martinez 2019"),
    _h3(_TONALNESS, "tonalness", 16, 1, 0,
        "Mean tonalness over 1s -- long-range tonal certainty",
        "Vuust 2022"),

    # === Spectral Flux / PE Dynamics (2 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Spectral change at 100ms -- prediction error magnitude",
        "Garrido 2009"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 2, 2,
        "Spectral change std at 100ms -- PE variability (inverse precision)",
        "Friston 2005"),

    # === Onset Strength / Rhythmic Precision (2 tuples) ===
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 2,
        "Onset at 100ms -- event salience for rhythmic PE",
        "Sedley 2016"),
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 14, 2,
        "Onset periodicity at 100ms -- rhythmic regularity (precision proxy)",
        "Quiroga-Martinez 2019"),

    # === Tonal Stability / Structural Precision (3 tuples) ===
    _h3(_FUND_FREQ, "fundamental_frequency", 8, 0, 0,
        "Tonal stability coupling at 500ms -- harmonic structure precision",
        "Vuust 2022"),
    _h3(_FUND_FREQ, "fundamental_frequency", 16, 1, 0,
        "Mean tonal stability coupling at 1s -- long-range structural context",
        "Garrido 2009"),
    _h3(_FUND_FREQ, "fundamental_frequency", 16, 20, 0,
        "Tonal stability entropy at 1s -- structural uncertainty signal",
        "Friston 2005"),

    # === Periodicity / Temporal Precision (2 tuples) ===
    _h3(_PERIODICITY, "periodicity", 8, 1, 0,
        "Mean periodicity at 500ms -- rhythmic precision baseline",
        "Sedley 2016"),
    _h3(_PERIODICITY, "periodicity", 16, 14, 2,
        "Periodicity self-similarity at 1s -- long-range rhythmic certainty",
        "Vuust 2022"),
)

assert len(_PWUP_H3_DEMANDS) == 14


class PWUP(Encoder):
    """Precision-Weighted Uncertainty Processing -- PCU Encoder (depth 1, 10D).

    Computes precision weights for tonal and rhythmic prediction errors
    using HTP hierarchical predictions and ICEM information content.
    In high-precision (tonal, metric) contexts, PE responses are amplified;
    in low-precision (atonal, irregular) contexts, PE is attenuated.

    Quiroga-Martinez et al. 2019: EEG MMN amplitude modulated by tonal
    context precision (d=3, p<0.001, N=40). Tonal key clarity 0.8 vs
    atonal 0.5.

    Garrido et al. 2009: fMRI evidence that STG PE signals are weighted
    by precision context (predictable vs random sequences, N=16).

    Sedley et al. 2016: MEG precision encoding in auditory cortex gates
    prediction error propagation at gamma/beta frequencies (N=24).

    Friston 2005: Theoretical framework -- cortical responses are
    precision-weighted prediction errors in hierarchical generative models.

    Vuust et al. 2022: Music perception as precision-weighted predictive
    coding at multiple hierarchical levels (Nature Neuroscience review).

    Dependency chain:
        PWUP is an Encoder (Depth 1) -- reads HTP + ICEM relay outputs.
        Computes after both relays in F2 pipeline.

    Downstream feeds:
        -> SPH (precision context for spatiotemporal prediction)
        -> PSH (precision weights for silencing decisions)
        -> precision_weighted_pe beliefs (Core)
        -> tonal_certainty, rhythmic_certainty beliefs (Appraisal)
        -> precision_forecast, uncertainty_trend beliefs (Anticipation)
    """

    NAME = "PWUP"
    FULL_NAME = "Precision-Weighted Uncertainty Processing"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("HTP", "ICEM")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:tonal_precision", "E1:rhythmic_precision"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 2, 4,
            ("M0:weighted_error", "M1:uncertainty_index"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:tonal_precision_weight", "P1:rhythmic_precision_weight",
             "P2:attenuated_response"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:precision_adjustment", "F1:context_uncertainty",
             "F2:response_attenuation"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PWUP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:tonal_precision", "E1:rhythmic_precision",
            "M0:weighted_error", "M1:uncertainty_index",
            "P0:tonal_precision_weight", "P1:rhythmic_precision_weight",
            "P2:attenuated_response",
            "F0:precision_adjustment", "F1:context_uncertainty",
            "F2:response_attenuation",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # STG -- precision-weighted PE processing
            RegionLink("P0:tonal_precision_weight", "STG", 0.80,
                       "Garrido 2009"),
            # R Heschl's Gyrus -- sensory precision for ambiguous intervals
            RegionLink("E0:tonal_precision", "A1_HG", 0.75,
                       "Sedley 2016"),
            # Hippocampus -- contextual precision (tonal vs atonal memory)
            RegionLink("M1:uncertainty_index", "HIPP", 0.70,
                       "Quiroga-Martinez 2019"),
            # Amygdala -- uncertainty gating / defense cascade
            RegionLink("P2:attenuated_response", "AMYG", 0.65,
                       "Friston 2005"),
            # NAc -- uncertainty encoding
            RegionLink("F1:context_uncertainty", "NAC", 0.60,
                       "Vuust 2022"),
            # vmPFC -- precision adjustment computation
            RegionLink("F0:precision_adjustment", "VMPFC", 0.55,
                       "Friston 2005"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # PWUP modulates PE precision, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Quiroga-Martinez et al.", 2019,
                         "Precision context (tonal vs atonal) modulates MMN "
                         "amplitude; d=3 effect size; tonal key clarity 0.8 "
                         "vs atonal 0.5; pitch/timbre/intensity precision",
                         "EEG, N=40"),
                Citation("Garrido et al.", 2009,
                         "Precision-weighted PE in predictive coding; STG "
                         "activity modulated by sequence predictability; "
                         "repetition suppression as precision learning",
                         "fMRI, N=16"),
                Citation("Sedley et al.", 2016,
                         "Precision encoding in auditory cortex; gamma/beta "
                         "frequency bands carry precision signals; PE "
                         "propagation gated by precision context",
                         "MEG, N=24"),
                Citation("Friston", 2005,
                         "A theory of cortical responses: hierarchical "
                         "predictive coding with precision-weighted PE; "
                         "precision = inverse variance of generative model",
                         "Review (theoretical)"),
                Citation("Vuust et al.", 2022,
                         "Music in the brain: precision-weighted predictive "
                         "coding at multiple hierarchical levels; precision "
                         "expectations adjust with musical training/context",
                         "Nature Neuroscience review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Tonal precision weight (P0) must be higher in tonal vs "
                "atonal contexts (Quiroga-Martinez 2019: d=3)",
                "PE attenuation (P2) must decrease when tonal precision "
                "drops (Friston 2005 precision weighting)",
                "Rhythmic precision weight (P1) must correlate with metric "
                "regularity (Sedley 2016 timing precision)",
                "Disrupting auditory cortex should impair precision "
                "estimation (testable via TMS/lesion)",
                "Musical training should increase baseline precision "
                "(testable via expert vs novice comparison)",
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
        """Transform R3/H3 + relay outputs into 10D precision representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"HTP": (B, T, 12), "ICEM": (B, T, 13)}``

        Returns:
            ``(B, T, 10)`` -- E(2) + M(2) + P(3) + F(3)
        """
        e = compute_extraction(r3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m, relay_outputs)
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
