"""UDP -- Uncertainty-Driven Pleasure.

Integrator nucleus (depth 3, reads all upstream) in PCU, Function F2.
Models how in high-uncertainty contexts (atonal), correct predictions
become more rewarding -- reward inversion when uncertainty exceeds
threshold. Correct predictions in high-uncertainty contexts signal model
improvement and reduced uncertainty, generating pleasure.

Dependency chain (strict):
    HTP  (Depth 0, Relay)   --+
    SPH  (Depth 0, Relay)   --+--> PWUP (Depth 1) --+--> UDP (Depth 3)
    ICEM (Depth 0, Relay)   --+                      |
                               +--> WMED (Depth 2) --+

Upstream reads:
    PWUP: M1:uncertainty_index [idx 3]
    WMED: E1:wm_contribution   [idx 1]

R3 Ontology Mapping (97D freeze):
    sensory_pleasantness:  [4]     (A, unchanged)
    periodicity:           [5]     (A, tonal certainty)
    onset_strength:        [11]    (B, was spectral_flux at old [10])
    tonalness:             [14]    (C, key clarity proxy)
    tristimulus1-3:        [18:21] (C, R3 direct)
    spectral_change:       [21]    (D, spectral_flux)

Output structure: E(2) + M(2) + P(3) + F(3) = 10D
  E-layer [0:2]   Extraction    (sigmoid)  scope=internal
  M-layer [2:4]   Memory        (sigmoid)  scope=internal
  P-layer [4:7]   Present       (sigmoid)  scope=hybrid
  F-layer [7:10]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/udp/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Integrator
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
    1: "50ms (gamma)",
    3: "100ms (alpha-beta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 4: "max", 6: "skew",
    8: "velocity", 18: "trend", 20: "entropy",
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
_SENSORY_PLEAS = 4        # sensory_pleasantness (A group)
_PERIODICITY = 5          # periodicity (A, tonal certainty)
_ONSET = 11               # onset_strength (B, was spectral_flux at old [10])
_TONALNESS = 14           # tonalness (C, key clarity proxy)
_TRISTIMULUS_START = 18   # tristimulus1 (C, R3 direct)
_TRISTIMULUS_END = 21     # tristimulus3 end (exclusive)
_SPECTRAL_CHANGE = 21     # spectral_change (D, spectral_flux)
_H_COUPLING = 41          # H_coupling (H group)


# -- 16 H3 Demand Specifications -----------------------------------------------
# Uncertainty tracking + reward computation across timescales

_UDP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Sensory Pleasantness / hedonic baseline (3 tuples) ===
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 3, 0, 2,
        "Sensory pleasantness at 100ms -- hedonic value integration",
        "Cheung 2019"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 1, 0,
        "Sensory pleasantness at 1s -- mean hedonic memory",
        "Gold 2019"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 16, 20, 0,
        "Sensory pleasantness at 1s -- entropy hedonic memory",
        "Cheung 2019"),

    # === Tonalness / tonal certainty (2 tuples) ===
    _h3(_TONALNESS, "tonalness", 8, 1, 0,
        "Tonalness at 500ms -- mean tonal certainty memory",
        "Pearce 2005"),
    _h3(_TONALNESS, "tonalness", 16, 1, 0,
        "Tonalness at 1s -- mean tonal certainty long-range",
        "Koelsch 2019"),

    # === Periodicity / tonal cycling (2 tuples) ===
    _h3(_PERIODICITY, "periodicity", 8, 1, 0,
        "Periodicity at 500ms -- mean tonal cycling memory",
        "Pearce 2005"),
    _h3(_PERIODICITY, "periodicity", 16, 18, 0,
        "Periodicity at 1s -- trend tonal cycling memory",
        "Koelsch 2019"),

    # === Spectral Change / surprise trigger (3 tuples) ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 1, 0, 2,
        "Spectral change at 50ms -- fast surprise value integration",
        "Cheung 2019"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 3, 0, 2,
        "Spectral change at 100ms -- surprise value integration",
        "Cheung 2019"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 3, 4, 2,
        "Spectral change at 100ms -- max surprise integration",
        "Gold 2019"),

    # === Onset Strength / event detection (2 tuples) ===
    _h3(_ONSET, "onset_strength", 3, 0, 2,
        "Onset strength at 100ms -- event detection value integration",
        "Salimpoor 2011"),
    _h3(_ONSET, "onset_strength", 3, 8, 2,
        "Onset strength at 100ms -- event velocity integration",
        "Salimpoor 2011"),

    # === H_coupling / harmonic coupling context (4 tuples) ===
    _h3(_H_COUPLING, "H_coupling", 8, 0, 0,
        "H_coupling at 500ms -- harmonic coupling value memory",
        "Koelsch 2019"),
    _h3(_H_COUPLING, "H_coupling", 16, 1, 0,
        "H_coupling at 1s -- mean harmonic coupling memory",
        "Pearce 2005"),
    _h3(_H_COUPLING, "H_coupling", 16, 20, 0,
        "H_coupling at 1s -- entropy harmonic coupling memory",
        "Cheung 2019"),
    _h3(_H_COUPLING, "H_coupling", 16, 6, 0,
        "H_coupling at 1s -- skew harmonic coupling memory",
        "Gold 2019"),
)

assert len(_UDP_H3_DEMANDS) == 16


class UDP(Integrator):
    """Uncertainty-Driven Pleasure -- PCU Integrator (depth 3, 10D).

    Models how correct predictions in high-uncertainty contexts become
    more rewarding because they signal model improvement and reduced
    uncertainty. Reward inversion occurs when uncertainty exceeds threshold.

    Gold et al. 2019: pleasure from prediction confirmation in uncertain
    contexts; inverted-U for IC on liking (N=100, p<0.001).
    Cheung et al. 2019: uncertainty x surprise interaction in NAc/amygdala;
    R^2=0.654 (fMRI, N=79).
    Koelsch 2019: musical syntax expectations and emotion; review.
    Salimpoor et al. 2011: dopamine release during music anticipation
    (PET, N=8).
    Pearce 2005: IDyOM information content model; computational.

    Dependency chain:
        PWUP (Depth 1) + WMED (Depth 2) --> UDP (Depth 3)
        UDP reads all upstream R/E/A outputs in PCU.

    Downstream feeds:
        -> ARU (reward signal for wanting/liking)
        -> reward system (hedonic value from uncertainty resolution)
        -> uncertainty_pleasure belief (Core)
        -> reward_inversion, model_improvement beliefs (Appraisal)
        -> pleasure_anticipation, reward_expectation beliefs (Anticipation)
    """

    NAME = "UDP"
    FULL_NAME = "Uncertainty-Driven Pleasure"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("PWUP", "WMED")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:uncertainty_level", "E1:confirmation_reward"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 2, 4,
            ("M0:error_reward", "M1:pleasure_index"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:context_assessment", "P1:prediction_accuracy",
             "P2:reward_computation"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:reward_expectation", "F1:model_improvement",
             "F2:pleasure_anticipation"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _UDP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:uncertainty_level", "E1:confirmation_reward",
            "M0:error_reward", "M1:pleasure_index",
            "P0:context_assessment", "P1:prediction_accuracy",
            "P2:reward_computation",
            "F0:reward_expectation", "F1:model_improvement",
            "F2:pleasure_anticipation",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # STG -- uncertainty x surprise interaction
            RegionLink("E0:uncertainty_level", "STG", 0.80,
                       "Cheung 2019"),
            # NAc -- reward from uncertainty resolution
            RegionLink("P2:reward_computation", "NAC", 0.85,
                       "Cheung 2019"),
            # Caudate -- anticipatory reward during uncertainty
            RegionLink("F0:reward_expectation", "CAUD", 0.75,
                       "Salimpoor 2011"),
            # Amygdala/Hippocampus -- uncertainty x surprise
            RegionLink("E1:confirmation_reward", "AMYG", 0.70,
                       "Cheung 2019"),
            RegionLink("M0:error_reward", "HIPP", 0.65,
                       "Cheung 2019"),
            # vmPFC/OFC -- hedonic evaluation
            RegionLink("M1:pleasure_index", "VMPFC", 0.70,
                       "Gold 2019"),
            RegionLink("P2:reward_computation", "OFC", 0.65,
                       "Gold 2019"),
            # pre-SMA -- uncertainty tracking
            RegionLink("P0:context_assessment", "PRE_SMA", 0.60,
                       "Koelsch 2019"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # UDP maps to reward signals, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Gold et al.", 2019,
                         "Pleasure from prediction confirmation in uncertain "
                         "contexts; inverted-U for IC on liking; IC x entropy "
                         "interaction; p<0.001",
                         "Behavioral, N=100"),
                Citation("Koelsch", 2019,
                         "Musical syntax expectations and emotion; prediction "
                         "violation triggers emotional response; syntax-based "
                         "uncertainty modulates reward",
                         "Review"),
                Citation("Cheung et al.", 2019,
                         "Uncertainty x surprise interaction in NAc/amygdala; "
                         "saddle-shaped pleasure surface; R^2=0.654; low "
                         "uncertainty + high surprise = pleasure",
                         "fMRI, N=79"),
                Citation("Salimpoor et al.", 2011,
                         "Dopamine release: caudate during anticipation, "
                         "NAc during peak pleasure to music; PET p<0.05",
                         "PET, N=8"),
                Citation("Pearce", 2005,
                         "IDyOM information content model; entropy and IC "
                         "predict melodic expectation; computational model "
                         "of auditory prediction",
                         "Computational"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "High-uncertainty contexts must increase reward for correct "
                "predictions (testable: atonal vs tonal paradigm)",
                "Reward inversion must occur above uncertainty threshold "
                "(testable: parametric uncertainty manipulation)",
                "NAc activity should correlate with uncertainty-modulated "
                "prediction confirmation (testable: fMRI replication)",
                "Disrupting dopaminergic pathways should abolish "
                "uncertainty-driven pleasure (testable: pharmacology)",
                "IDyOM entropy should predict pleasure ratings in "
                "high-uncertainty contexts (testable: behavioral)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Transform R3/H3 + PWUP/WMED into 10D uncertainty-driven pleasure.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"PWUP": (B, T, 10), "WMED": (B, T, 11)}``
            cross_unit_inputs: Unused (no cross-unit reads).

        Returns:
            ``(B, T, 10)`` -- E(2) + M(2) + P(3) + F(3)
        """
        e = compute_extraction(r3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(
            r3_features, h3_features, e, m, upstream_outputs,
        )
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
