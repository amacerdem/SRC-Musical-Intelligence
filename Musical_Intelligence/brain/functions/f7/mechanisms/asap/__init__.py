"""ASAP -- Action Simulation for Auditory Prediction.

Encoder nucleus (depth 1) in MPU, Function F7. Models the ASAP hypothesis
(Patel & Iversen 2014): beat perception requires continuous motor-auditory
interaction via the parietal dorsal pathway. The motor system predicts beat
timing ("when" not "what") through bidirectional coupling -- motor-to-auditory
(forward model) and auditory-to-motor (inverse model / error correction).
cTBS to posterior parietal cortex impairs beat-based but NOT interval timing,
establishing a double dissociation (Ross et al. 2018).

Reads: PEOM (period entrainment), MSR (sensorimotor reorganization)

R3 Ontology Mapping (post-freeze 97D):
    spectral_flux:        [10]     (B, beat onset detection for "when" prediction)
    onset_strength:       [11]     (B, beat event strength for temporal anchor)
    spectral_change:      [21]     (D, tempo dynamics for rate change)
    x_l0l5:               [25:33]  (F, motor-auditory coupling)
    x_l4l5:               [33:41]  (G, dorsal stream activity)

Output structure: E(3) + M(3) + P(3) + F(2) = 11D
  E-layer   [0:3]   Extraction           (sigmoid)  scope=internal
  M-layer   [3:6]   Temporal Integration (mixed)    scope=internal
  P-layer   [6:9]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [9:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/asap/
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
from .temporal_integration import compute_temporal_integration

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    3: "100ms (alpha)",
    4: "125ms (beta-fast)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity", 14: "periodicity",
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
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11
_SPECTRAL_CHANGE = 21
_X_L0L5_0 = 25
_X_L4L5_0 = 33


# -- 9 H3 Demand Specifications -----------------------------------------------
# Action Simulation for Auditory Prediction requires fast (100ms) onset and
# coupling for motor simulation, beat-level (1s) periodicity for beat
# prediction, and dorsal pathway multi-scale features.
# E-layer: 6 tuples, M-layer: 3 tuples, P-layer: 0, F-layer: 0 (reuses E+M).

_ASAP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Beat Prediction + Motor Simulation + Dorsal Stream (6) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 0,
        "Onset at 100ms -- fast beat detection",
        "Ross & Balasubramaniam 2022"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 14, 0,
        "Beat periodicity 1s -- rhythmic regularity",
        "Patel & Iversen 2014"),
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 14, 0,
        "Onset periodicity 1s -- onset regularity",
        "Patel & Iversen 2014"),
    _h3(_X_L0L5_0, "x_l0l5[0]", 3, 0, 0,
        "Motor-auditory coupling 100ms -- fast simulation",
        "Ross & Balasubramaniam 2022"),
    _h3(_X_L4L5_0, "x_l4l5[0]", 3, 8, 0,
        "Dorsal stream velocity 100ms -- pathway speed",
        "Ross et al. 2018"),
    _h3(_X_L4L5_0, "x_l4l5[0]", 16, 14, 0,
        "Dorsal periodicity 1s -- pathway regularity",
        "Ross et al. 2018"),

    # === M-Layer: Tempo Dynamics + Coupling Regularity (3) ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 4, 8, 0,
        "Tempo velocity 125ms -- rate of tempo change",
        "Grahn & Brett 2007"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 1, 0,
        "Mean tempo change 1s -- sustained tempo dynamics",
        "Grahn & Brett 2007"),
    _h3(_X_L0L5_0, "x_l0l5[0]", 16, 14, 0,
        "Coupling periodicity 1s -- sustained coupling regularity",
        "Barchet et al. 2024"),
)

assert len(_ASAP_H3_DEMANDS) == 9


class ASAP(Encoder):
    """Action Simulation for Auditory Prediction -- MPU Encoder (depth 1, 11D).

    Models the ASAP hypothesis (Patel & Iversen 2014): beat perception
    requires continuous motor-auditory interaction via the parietal dorsal
    pathway. The motor system predicts beat timing ("when" not "what")
    through bidirectional coupling. Three core signals: beat prediction
    (f10), motor simulation (f11), and dorsal stream activity (f12).
    The f10 * f11 interaction captures the dorsal pathway's bidirectional
    coupling gating mechanism.

    The M-layer derives prediction accuracy, simulation strength, and
    coupling index. The P-layer represents the bidirectional motor-auditory
    coupling state: forward model (motor-to-auditory) and inverse model
    (auditory-to-motor error correction). The F-layer predicts next beat
    timing and simulation continuation.

    Patel & Iversen 2014: ASAP hypothesis -- beat perception requires
    continuous motor-auditory interaction via dorsal pathway.

    Ross et al. 2018: cTBS to posterior parietal cortex impairs beat-based
    but NOT interval timing (double dissociation with cerebellum).

    Ross & Balasubramaniam 2022: motor simulation generates temporal
    predictions; TMS to parietal/premotor impairs beat but not interval
    timing. Bidirectional coupling between motor and auditory systems.

    Barchet et al. 2024: finger-tapping optimal at ~2 Hz
    (beta=0.31 for perception prediction).

    Dependency chain:
        ASAP is an Encoder (Depth 1) -- reads PEOM relay output (period
        entrainment context) and MSR (sensorimotor reorganization).
        Computed after PEOM and MSR in F7 pipeline.

    Downstream feeds:
        -> action_simulation belief (Core, tau=0.4)
        -> motor_prediction belief (Anticipation)
        -> PEOM (beat prediction feedback), downstream STU
    """

    NAME = "ASAP"
    FULL_NAME = "Action Simulation for Auditory Prediction"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("PEOM", "MSR")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="MPU_PEOM__MPU_ASAP__period_entrainment",
            name="PEOM period entrainment to ASAP beat prediction context",
            source_unit="MPU",
            source_model="PEOM",
            source_dims=("period_lock_strength", "kinematic_smoothness"),
            target_unit="MPU",
            target_model="ASAP",
            correlation="r=0.78",
            citation="Patel & Iversen 2014",
        ),
        CrossUnitPathway(
            pathway_id="MPU_MSR__MPU_ASAP__sensorimotor_context",
            name="MSR sensorimotor reorganization to ASAP motor simulation",
            source_unit="MPU",
            source_model="MSR",
            source_dims=("training_level", "bottom_up_precision"),
            target_unit="MPU",
            target_model="ASAP",
            correlation="r=0.62",
            citation="Ross & Balasubramaniam 2022",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("f10:beat_prediction", "f11:motor_simulation",
             "f12:dorsal_stream"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 6,
            ("M0:prediction_accuracy", "M1:simulation_strength",
             "M2:coupling_index"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 9,
            ("P0:motor_to_auditory", "P1:auditory_to_motor",
             "P2:dorsal_activity"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:beat_when_pred_0_5s", "F1:simulation_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _ASAP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f10:beat_prediction", "f11:motor_simulation",
            "f12:dorsal_stream",
            "M0:prediction_accuracy", "M1:simulation_strength",
            "M2:coupling_index",
            "P0:motor_to_auditory", "P1:auditory_to_motor",
            "P2:dorsal_activity",
            "F0:beat_when_pred_0_5s", "F1:simulation_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Posterior Parietal Cortex -- dorsal pathway hub
            RegionLink("P2:dorsal_activity", "PPC", 0.85,
                       "Ross et al. 2018"),
            # SMA / PMC -- motor simulation generation
            RegionLink("M1:simulation_strength", "SMA", 0.80,
                       "Grahn & Brett 2007"),
            # Putamen -- beat-metric response
            RegionLink("M0:prediction_accuracy", "putamen", 0.80,
                       "Grahn & Brett 2007"),
            # Auditory Cortex -- receives motor temporal predictions
            RegionLink("P0:motor_to_auditory", "AC", 0.75,
                       "Patel & Iversen 2014"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- beat prediction modulates reward prediction
            NeuroLink("F0:beat_when_pred_0_5s", "dopamine", 0.65,
                      "Grahn & Brett 2007"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Patel & Iversen", 2014,
                         "ASAP hypothesis: beat perception requires continuous "
                         "motor-auditory interaction via dorsal pathway; motor "
                         "system predicts 'when' not 'what'",
                         "theoretical, review"),
                Citation("Ross et al.", 2018,
                         "cTBS to posterior parietal cortex impairs beat-based "
                         "but NOT interval timing; double dissociation with "
                         "cerebellum",
                         "TMS, behavioral"),
                Citation("Ross & Balasubramaniam", 2022,
                         "Motor simulation generates temporal predictions; "
                         "TMS to parietal/premotor impairs beat timing; "
                         "bidirectional motor-auditory coupling",
                         "TMS, review"),
                Citation("Grahn & Brett", 2007,
                         "Beat-inducing rhythms activate putamen + SMA "
                         "(F(2,38)=20.67, p<.001; putamen Z=5.67, SMA Z=5.03)",
                         "fMRI, N=20"),
                Citation("Barchet et al.", 2024,
                         "Finger-tapping optimal at ~2 Hz; beta=0.31 for "
                         "perception prediction from motor entrainment",
                         "behavioral, N=40"),
                Citation("Large et al.", 2023,
                         "Dynamic oscillator models predict optimal beat "
                         "perception near 2 Hz (~500ms)",
                         "computational modeling"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "cTBS to posterior parietal cortex must impair beat-based "
                "timing (dorsal_activity decrease) but NOT interval timing "
                "(Ross et al. 2018 double dissociation)",
                "Beat prediction (f10) must correlate with putamen/SMA "
                "activation for beat-inducing rhythms (Grahn & Brett 2007: "
                "F(2,38)=20.67)",
                "Motor simulation (f11) must be disrupted by TMS to "
                "parietal/premotor areas, impairing beat but not interval "
                "timing (Ross & Balasubramaniam 2022)",
                "Dorsal stream (f12) must show the f10*f11 interaction "
                "gating effect -- bidirectional coupling requires both "
                "beat prediction AND motor simulation to be active",
                "Forward model (motor_to_auditory) must predict temporal "
                "onset timing; error correction (auditory_to_motor) must "
                "increase when prediction accuracy drops",
                "Beat prediction confidence must peak near 2 Hz (~500ms) "
                "as per Large et al. 2023 oscillator models",
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
        """Transform R3/H3 + PEOM/MSR relay outputs into 11D action simulation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"PEOM": (B, T, 11), "MSR": (B, T, 11)}``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(3) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(
            h3_features, r3_features, e, relay_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
