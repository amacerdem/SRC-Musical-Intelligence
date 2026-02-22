"""NEWMD -- Neural Entrainment-Working Memory Dissociation.

Associator nucleus (depth 2) in STU, Function F3. Models the dissociation
between neural entrainment to rhythmic stimuli and working memory capacity
for rhythm processing. Tierney 2014 showed that beat synchronization ability
relates to auditory-motor coupling but is partially dissociable from WM
measures. Grahn 2009 demonstrated that SMA, putamen, and cerebellum are
differentially engaged by beat-based vs memory-based rhythm processing.

Dependency chain:
    NEWMD is an Associator (Depth 2) -- reads HMCE cross-unit relay output.
    Computed after HMCE in F3 pipeline.

R3 Ontology Mapping (post-freeze 97D):
    amplitude:          [7]      (A, velocity_A)
    loudness:           [8]      (A, velocity_D)
    spectral_centroid:  [9]      (B, spectral_centroid)
    spectral_flux:      [10]     (B, onset_strength)
    onset_strength:     [11]     (B, event salience)
    spectral_change:    [21]     (D, spectral_flux)
    energy_change:      [22]     (D, dynamic change)
    pitch_change:       [23]     (D, pitch change)
    x_l0l5:             [25]     (F, sensorimotor coupling)
    x_l4l5:             [33]     (F, cross-stream interaction)

Output structure: E(4) + M(2) + P(2) + F(2) = 10D
  E-layer [0:4]   Extraction    (sigmoid)  scope=internal
  M-layer [4:6]   Memory        (sigmoid)  scope=internal
  P-layer [6:8]   Present       (sigmoid)  scope=hybrid
  F-layer [8:10]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/newmd/
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
    6: "150ms (beta)",
    8: "500ms (delta)",
    11: "750ms",
    14: "~900ms",
    16: "1000ms (beat)",
    20: "5000ms (phrase)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 3: "std", 4: "max",
    8: "velocity", 13: "entropy", 14: "periodicity",
    15: "smoothness", 17: "peaks", 19: "stability",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory"}


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
_AMPLITUDE = 7            # amplitude / velocity_A (A group)
_LOUDNESS = 8             # loudness / velocity_D (A group)
_SPECTRAL_CENTROID = 9    # spectral_centroid (B group)
_SPECTRAL_FLUX = 10       # spectral_flux / onset_strength (B group)
_ONSET_STRENGTH = 11      # onset_strength (B group, event salience)
_SPECTRAL_CHANGE = 21     # spectral_change / spectral_flux (D group)
_ENERGY_CHANGE = 22       # energy_change (D group, dynamic change)
_PITCH_CHANGE = 23        # pitch_change (D group)
_X_L0L5 = 25             # sensorimotor coupling (F group)
_X_L4L5 = 33             # cross-stream interaction (F group)


# -- 14 H3 Demand Specifications -----------------------------------------------
# Entrainment-WM dissociation at multiple timescales.
# All L0 (memory/backward) -- causal processing only.

_NEWMD_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Entrainment Route: onset/flux/amplitude (4 tuples) ===
    _h3(11, "onset_strength", 6, 0, 0,
        "Onset value 150ms -- event detection",
        "Tierney 2014"),
    _h3(10, "spectral_flux", 6, 4, 0,
        "Flux max 150ms -- peak detection",
        "Tierney 2014"),
    _h3(11, "onset_strength", 11, 14, 0,
        "Onset periodicity 750ms -- beat regularity",
        "Grahn 2009"),
    _h3(7, "amplitude", 6, 0, 0,
        "Amplitude value 150ms -- beat amplitude",
        "Tierney 2014"),

    # === WM Route: energy/pitch/spectral complexity (4 tuples) ===
    _h3(22, "energy_change", 8, 1, 0,
        "Energy mean 500ms -- dynamic level",
        "Grahn 2009"),
    _h3(23, "pitch_change", 8, 3, 0,
        "Pitch std 500ms -- melodic complexity",
        "Tierney 2014"),
    _h3(21, "spectral_change", 11, 8, 0,
        "Spectral velocity 750ms -- change rate",
        "Grahn 2009"),
    _h3(22, "energy_change", 14, 13, 0,
        "Energy entropy ~900ms -- complexity",
        "Tierney 2014"),

    # === Context / Sustained Level (3 tuples) ===
    _h3(8, "loudness", 16, 1, 0,
        "Loudness mean 1s -- sustained level",
        "Grahn 2009"),
    _h3(9, "spectral_centroid", 16, 15, 0,
        "Centroid smoothness 1s -- timbral stability",
        "Tierney 2014"),
    _h3(23, "pitch_change", 14, 1, 0,
        "Pitch mean ~900ms -- melodic context",
        "Tierney 2014"),

    # === Salience / Event Detection (2 tuples) ===
    _h3(21, "spectral_change", 11, 17, 0,
        "Spectral peaks 750ms -- event salience",
        "Grahn 2009"),
    _h3(25, "x_l0l5", 20, 13, 0,
        "Coupling entropy 5s L0 -- long-term load",
        "Grahn 2009"),

    # === Cross-Stream Stability (1 tuple) ===
    _h3(33, "x_l4l5", 20, 19, 0,
        "Cross-stream stability 5s L0 -- long stability",
        "Grahn 2009"),
)

assert len(_NEWMD_H3_DEMANDS) == 14


class NEWMD(Associator):
    """Neural Entrainment-Working Memory Dissociation -- STU Associator (depth 2, 10D).

    Models the dissociation between neural entrainment to rhythmic stimuli
    and working memory capacity for rhythm processing. Two partially
    dissociable routes process rhythmic information:
      Route 1 (Entrainment): onset periodicity -> motor coupling
      Route 2 (WM): complexity metrics -> cognitive load

    Tierney & Kraus 2014: Beat synchronization ability relates to
    auditory-motor coupling and frequency-following response consistency
    (behavioral+EEG, N=30). Individual differences in beat tapping
    accuracy predicted by neural entrainment but partially dissociable
    from WM capacity measures.

    Grahn & Brett 2009: Beat-based timing engages SMA, putamen, and
    cerebellum differentially from memory-based timing (fMRI, N=18).
    Simple beat detection is automatic (putamen), while complex rhythms
    require WM-supported SMA engagement.

    Dependency chain:
        NEWMD is an Associator (Depth 2) -- reads HMCE cross-unit relay.
        Computed after HMCE in F3 pipeline.

    Downstream feeds:
        -> entrainment_strength beliefs (Appraisal)
        -> wm_capacity beliefs (Appraisal)
        -> dissociation context for F3 integrators
    """

    NAME = "NEWMD"
    FULL_NAME = "Neural Entrainment-Working Memory Dissociation"
    UNIT = "STU"
    FUNCTION = "F3"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ()
    CROSS_UNIT_READS = ("HMCE",)

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:entrainment_strength", "E1:wm_capacity",
             "E2:flexibility_cost", "E3:dissociation_index"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 6,
            ("M0:paradox_magnitude", "M1:dual_route_balance"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 8,
            ("P0:current_entrain", "P1:current_wm_load"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 10,
            ("F0:performance_pred", "F1:adaptation_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _NEWMD_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:entrainment_strength", "E1:wm_capacity",
            "E2:flexibility_cost", "E3:dissociation_index",
            "M0:paradox_magnitude", "M1:dual_route_balance",
            "P0:current_entrain", "P1:current_wm_load",
            "F0:performance_pred", "F1:adaptation_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # AC -- auditory cortex entrainment tracking
            RegionLink("E0:entrainment_strength", "AC", 0.80,
                       "Tierney 2014"),
            # SMA -- motor timing and beat prediction
            RegionLink("P0:current_entrain", "SMA", 0.75,
                       "Grahn 2009"),
            # Putamen -- automatic beat detection
            RegionLink("M0:paradox_magnitude", "putamen", 0.75,
                       "Grahn 2009"),
            # SPL -- superior parietal lobule, WM engagement
            RegionLink("P1:current_wm_load", "SPL", 0.70,
                       "Tierney 2014"),
            # Cerebellum -- rhythmic synchronization
            RegionLink("F1:adaptation_pred", "cerebellum", 0.65,
                       "Grahn 2009"),
            # DLPFC -- working memory capacity and cognitive control
            RegionLink("E1:wm_capacity", "DLPFC", 0.65,
                       "Tierney 2014"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # NEWMD models entrainment-WM dissociation, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Tierney & Kraus", 2014,
                         "Beat synchronization ability relates to auditory-motor "
                         "coupling and frequency-following response consistency; "
                         "individual differences in beat tapping accuracy predicted "
                         "by neural entrainment but partially dissociable from WM",
                         "behavioral+EEG, N=30"),
                Citation("Grahn & Brett", 2009,
                         "Beat-based timing engages SMA, putamen, and cerebellum "
                         "differentially from memory-based timing; simple beat "
                         "detection is automatic (putamen), complex rhythms require "
                         "WM-supported SMA engagement",
                         "fMRI, N=18"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Entrainment strength (E0) must correlate with beat tapping "
                "accuracy for simple rhythms (Tierney 2014: r>0.4)",
                "WM capacity (E1) must predict performance for complex rhythms "
                "but not simple rhythms (Grahn 2009: SMA activation difference)",
                "Dissociation index (E3) must be larger for complex than simple "
                "rhythms (testable via rhythm complexity manipulation)",
                "Paradox magnitude (M0) should be high when entrainment is "
                "strong but flexibility is low (Tierney 2014: individual diffs)",
                "Putamen lesion patients should show reduced E0 but intact E1 "
                "(Grahn 2009: automatic vs controlled beat processing)",
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
        """Transform R3/H3 + HMCE cross-unit into 10D entrainment-WM dissociation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"HMCE": (B, T, D)}``

        Returns:
            ``(B, T, 10)`` -- E(4) + M(2) + P(2) + F(2)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(e)
        p = compute_cognitive_present(h3_features, e, m)
        f = compute_forecast(h3_features, e, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
