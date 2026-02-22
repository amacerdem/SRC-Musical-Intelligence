"""BARM -- Brainstem Auditory Response Modulation.

Encoder nucleus (depth 1) in ASU, Function F3. Models how brainstem auditory
responses are modulated by attention and rhythmic context. Musicians show enhanced
brainstem responses (ABR/FFR) to attended stimuli.

Reads: SNEM.entrainment_strength (intra-F3 dependency)

R3 Ontology Mapping (post-freeze 97D):
    amplitude:          [7]      (A, velocity_A)
    spectral_flux:      [10]     (B, onset_strength proxy)
    onset_strength:     [11]     (B, event salience)
    spectral_change:    [21]     (D, spectral_flux)
    energy_change:      [22]     (D, dynamic change)
    x_l0l5:             [25]     (F, sensorimotor coupling)

Output structure: E(3) + M(2) + P(2) + F(3) = 10D
  E-layer [0:3]  Extraction    (sigmoid)  scope=internal
  M-layer [3:5]  Memory        (sigmoid)  scope=internal
  P-layer [5:7]  Present       (sigmoid)  scope=hybrid
  F-layer [7:10] Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/barm/
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
    14: "periodicity", 21: "zero-crossings",
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
_AMPLITUDE = 7            # amplitude / velocity_A (A group)
_SPECTRAL_FLUX = 10       # spectral_flux / onset_strength proxy (B group)
_ONSET_STRENGTH = 11      # onset_strength (B group, event salience)
_SPECTRAL_CHANGE = 21     # spectral_change / spectral_flux (D group)
_ENERGY_CHANGE = 22       # energy_change (D group, dynamic change)
_X_L0L5 = 25             # sensorimotor coupling (F group)


# -- 14 H3 Demand Specifications -----------------------------------------------
# Brainstem response modulation requires periodicity (beat regularity),
# velocity (dynamic tracking), and coupling (sensorimotor integration).

_BARM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Periodicity / Beat Regularity (4 tuples) ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 14, 0,
        "Spectral change periodicity 500ms -- tempo groove",
        "Skoe 2010"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 14, 2,
        "Beat periodicity 1s -- entrainment reference",
        "Skoe 2010"),
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 14, 2,
        "Onset periodicity 1s -- beat regularity",
        "Tierney 2013"),
    _h3(_X_L0L5, "x_l0l5", 16, 14, 2,
        "Coupling periodicity 1s -- metric structure",
        "Tierney 2013"),

    # === Velocity / Dynamic Change (2 tuples) ===
    _h3(_ENERGY_CHANGE, "energy_change", 8, 8, 0,
        "Energy velocity 500ms -- dynamic change",
        "Musacchia 2007"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 8, 0,
        "Spectral change velocity 500ms -- spectral dynamics",
        "Skoe 2010"),

    # === Value / Instantaneous (3 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Flux value 100ms -- onset detection",
        "Skoe 2010"),
    _h3(_AMPLITUDE, "amplitude", 3, 0, 2,
        "Amplitude value 100ms -- beat amplitude",
        "Musacchia 2007"),
    _h3(_X_L0L5, "x_l0l5", 8, 0, 2,
        "Coupling value 500ms -- motor integration",
        "Tierney 2013"),

    # === Mean / Sustained Context (2 tuples) ===
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 1, 2,
        "Onset mean 100ms -- onset context",
        "Skoe 2010"),
    _h3(_AMPLITUDE, "amplitude", 16, 1, 2,
        "Amplitude mean 1s -- sustained level",
        "Musacchia 2007"),

    # === Phase / Coupling Dynamics (3 tuples) ===
    _h3(_X_L0L5, "x_l0l5", 16, 21, 2,
        "Coupling zero-crossings 1s -- phase resets",
        "Tierney 2013"),
    _h3(_X_L0L5, "x_l0l5", 3, 14, 2,
        "Coupling periodicity 100ms -- fast metric cue",
        "Tierney 2013"),
    _h3(_X_L0L5, "x_l0l5", 3, 0, 2,
        "Coupling value 100ms -- immediate motor state",
        "Tierney 2013"),
)

assert len(_BARM_H3_DEMANDS) == 14


class BARM(Encoder):
    """Brainstem Auditory Response Modulation -- ASU Encoder (depth 1, 10D).

    Models how brainstem auditory responses (ABR / FFR) are modulated by
    attention, rhythmic context, and sensorimotor coupling. Musicians show
    enhanced brainstem responses to attended stimuli and metrically strong
    beats, reflecting top-down cortical modulation of subcortical processing.

    Skoe & Kraus 2010: ABR/FFR in musicians shows enhanced temporal encoding
    of speech and music stimuli, especially at beat-aligned time points
    (N=20, ABR latency d=1.2).

    Tierney & Kraus 2013: Musicians with better beat synchronization show
    more consistent brainstem responses to speech, linking motor timing
    precision to auditory subcortical encoding (N=30, r=0.65).

    Musacchia et al. 2007: Musicians show enhanced subcortical representation
    of speech and music in ABR/FFR, with cross-domain transfer effects
    (N=20, ABR amplitude d=0.8).

    Dependency chain:
        BARM is an Encoder (Depth 1) -- reads SNEM relay output.
        Computed after SNEM in F3 pipeline.

    Downstream feeds:
        -> beat_alignment beliefs (Appraisal)
        -> regularization_strength beliefs (Core)
        -> brainstem modulation context for F3 integrators
    """

    NAME = "BARM"
    FULL_NAME = "Brainstem Auditory Response Modulation"
    UNIT = "ASU"
    FUNCTION = "F3"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("SNEM",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:regularization_tendency", "E1:beat_alignment",
             "E2:sync_benefit"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:veridical_perception", "M1:regularization_effect"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:beat_alignment_accuracy", "P1:regularization_strength"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:beat_accuracy_pred", "F1:sync_benefit_pred",
             "F2:individual_diff_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _BARM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:regularization_tendency", "E1:beat_alignment",
            "E2:sync_benefit",
            "M0:veridical_perception", "M1:regularization_effect",
            "P0:beat_alignment_accuracy", "P1:regularization_strength",
            "F0:beat_accuracy_pred", "F1:sync_benefit_pred",
            "F2:individual_diff_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # IC -- brainstem auditory response modulation hub
            RegionLink("E1:beat_alignment", "IC", 0.80,
                       "Skoe 2010"),
            # MGB -- thalamic relay for modulated brainstem signals
            RegionLink("P0:beat_alignment_accuracy", "MGB", 0.75,
                       "Musacchia 2007"),
            # Cochlear Nucleus -- early subcortical encoding
            RegionLink("E0:regularization_tendency", "CN", 0.70,
                       "Skoe 2010"),
            # AC -- cortical top-down modulation of brainstem
            RegionLink("P1:regularization_strength", "AC", 0.65,
                       "Tierney 2013"),
            # STG -- integration of brainstem output with cortical processing
            RegionLink("F0:beat_accuracy_pred", "STG", 0.60,
                       "Tierney 2013"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # BARM modulates subcortical responses, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Skoe & Kraus", 2010,
                         "ABR/FFR in musicians shows enhanced temporal encoding "
                         "of speech and music stimuli at beat-aligned time "
                         "points; brainstem plasticity reflects cortical "
                         "training effects",
                         "ABR, N=20"),
                Citation("Tierney & Kraus", 2013,
                         "Beat synchronization ability predicts brainstem "
                         "response consistency to speech; sensorimotor-auditory "
                         "coupling links motor timing to subcortical encoding "
                         "(r=0.65, p<0.001)",
                         "behavioral+ABR, N=30"),
                Citation("Musacchia et al.", 2007,
                         "Musicians show enhanced subcortical representation "
                         "of speech and music in ABR/FFR with cross-domain "
                         "transfer; amplitude enhancement d=0.8",
                         "ABR, N=20"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Beat alignment accuracy (P0) must be higher for metrically "
                "strong vs weak beats (Skoe 2010: ABR latency d=1.2)",
                "Regularization strength (P1) must correlate with motor "
                "timing precision (Tierney 2013: r=0.65)",
                "Sync benefit (E2) must increase with rhythmic regularity "
                "of stimulus (Musacchia 2007: cross-domain transfer)",
                "Disrupting sensorimotor coupling should reduce brainstem "
                "enhancement (testable via motor suppression paradigm)",
                "Non-musicians should show lower baseline regularization "
                "(testable via expert vs novice ABR comparison)",
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
        """Transform R3/H3 + SNEM relay output into 10D brainstem modulation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"SNEM": (B, T, 12)}``

        Returns:
            ``(B, T, 10)`` -- E(3) + M(2) + P(2) + F(3)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, e, m, relay_outputs)
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
