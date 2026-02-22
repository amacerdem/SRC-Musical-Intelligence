"""PEOM -- Period Entrainment Optimization Model.

Relay nucleus (depth 0) in MPU, Function F7. Models the period entrainment
optimization mechanism from Thaut et al. (2015, 1998b). The motor system
entrains to auditory period via dP/dt = alpha * (T - P(t)), producing velocity
optimization and variability reduction. Fixed period provides a continuous
time reference (CTR) that reduces jerk and smooths velocity profiles. PEOM is
the F7 relay: it directly bridges R3/H3 features to C3 cognitive-level
motor/timing representations.

Dependency chain:
    PEOM is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    amplitude:              [7]  -> [7]    (B, velocity_A)
    loudness:               [8]  -> [8]    (B, velocity_D)
    spectral_flux:          [10] -> [10]   (B, onset_strength)
    onset_strength:         [11] -> [11]   (B, onset_strength)
    spectral_change:        [21] -> [21]   (D, spectral_flux)
    x_l0l5:                 [25:33]        (F, coupling)

Output structure: E(3) + M(4) + P(2) + F(2) = 11D
  E-layer [0:3]   Extraction          (sigmoid)    scope=internal
  M-layer [3:7]   Temporal Integration (sigmoid)   scope=internal
  P-layer [7:9]   Present             (sigmoid)    scope=hybrid
  F-layer [9:11]  Forecast            (sigmoid)    scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/0_mechanisms-orchestrator.md
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
    3: "100ms (instantaneous)",
    4: "125ms (sub-beat)",
    8: "500ms (beat-fraction)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    14: "periodicity", 21: "zero_crossings",
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
_AMPLITUDE = 7                   # B group (velocity_A)
_LOUDNESS = 8                    # B group (velocity_D)
_SPECTRAL_FLUX = 10              # B group (onset_strength)
_ONSET_STRENGTH = 11             # B group
_SPECTRAL_CHANGE = 21            # D group (spectral_flux)
_X_L0L5_START = 25               # F group (coupling)


# -- 15 H3 Demand Specifications ----------------------------------------------
# E-layer: 9 tuples, M-layer: 4 tuples, P-layer: 2 tuples, F-layer: 0 new

_PEOM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Period entrainment extraction (tuples 0-8) ===

    # #0: Onset at 100ms alpha
    _h3(10, "spectral_flux", 3, 0, 2,
        "Onset at 100ms alpha -- instantaneous beat marker",
        "Thaut 2015"),
    # #1: Beat periodicity at 100ms
    _h3(10, "spectral_flux", 3, 14, 2,
        "Beat periodicity at 100ms -- fast beat tracking",
        "Thaut 1998b"),
    # #2: Beat periodicity at 1000ms
    _h3(10, "spectral_flux", 16, 14, 2,
        "Beat periodicity at 1s -- primary period lock signal",
        "Thaut 2015"),
    # #3: Onset strength at 100ms
    _h3(11, "onset_strength", 3, 0, 2,
        "Onset strength at 100ms -- beat event detection",
        "Thaut 2015"),
    # #4: Onset periodicity at 1s
    _h3(11, "onset_strength", 16, 14, 2,
        "Onset periodicity at 1s -- onset regularity for entrainment",
        "Thaut 1998b"),
    # #5: Beat amplitude at 100ms
    _h3(7, "amplitude", 3, 0, 2,
        "Beat amplitude at 100ms -- temporal intensity proxy",
        "Grahn & Brett 2007"),
    # #6: Amplitude variability 100ms
    _h3(7, "amplitude", 3, 2, 2,
        "Amplitude variability at 100ms -- intensity fluctuation",
        "Yamashita 2025"),
    # #7: Motor-auditory coupling 100ms
    _h3(25, "x_l0l5", 3, 0, 2,
        "Motor-auditory coupling at 100ms -- CTR signal",
        "Thaut 2015"),
    # #8: Coupling periodicity 100ms
    _h3(25, "x_l0l5", 3, 14, 2,
        "Coupling periodicity at 100ms -- motor-auditory sync",
        "Ross & Balasubramaniam 2022"),

    # === M-layer: Temporal integration (tuples 9-12) ===

    # #9: Mean amplitude over 1s -- motor drive baseline
    _h3(7, "amplitude", 16, 1, 2,
        "Mean amplitude over 1s -- motor drive baseline",
        "Grahn & Brett 2007"),
    # #10: Mean loudness over 500ms -- intensity integration
    _h3(8, "loudness", 8, 1, 0,
        "Mean loudness over 500ms -- perceptual intensity integration",
        "Thaut 2015"),
    # #11: Tempo velocity at 125ms -- period rate change
    _h3(21, "spectral_change", 4, 8, 0,
        "Tempo velocity at 125ms -- period rate change detection",
        "Thaut 2015"),
    # #12: Mean tempo change at 1s -- drift tracking
    _h3(21, "spectral_change", 16, 1, 0,
        "Mean tempo change at 1s -- drift tracking for period correction",
        "Repp 2005"),

    # === P-layer: Cognitive present (tuples 13-14) ===

    # #13: Coupling periodicity 1s -- lock stability
    _h3(25, "x_l0l5", 16, 14, 2,
        "Coupling periodicity at 1s -- period lock stability assessment",
        "Fujioka 2012"),
    # #14: Coupling zero-crossings 1s -- lock disruptions
    _h3(25, "x_l0l5", 16, 21, 2,
        "Coupling zero-crossings at 1s -- phase reset / lock disruption",
        "Nozaradan 2011"),
)

assert len(_PEOM_H3_DEMANDS) == 15


class PEOM(Relay):
    """Period Entrainment Optimization Model -- MPU Relay (depth 0, 11D).

    Models the period entrainment optimization mechanism.
    Thaut 2015: motor system entrains to auditory period via
    dP/dt = alpha*(T-P(t)); fixed period provides a continuous time reference
    (CTR) that reduces jerk and smooths velocity profiles.
    Thaut 1998b: motor period entrains even during subliminal 2% tempo
    changes (N=10, synchronized finger tapping).
    Grahn & Brett 2007: putamen Z=5.67, SMA Z=5.03 for beat vs non-beat
    rhythms (fMRI, N=20).

    Dependency chain:
        PEOM is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> period_lock_strength, kinematic_smoothness for kernel scheduler
        -> F3 Attention: salience mixer motor timing signal
        -> F5 Emotion: motor fluency contribution
        -> next_beat_pred_T: temporal prediction for reward computation
        -> PEOM relay wrapper (MPU) in scheduler
    """

    NAME = "PEOM"
    FULL_NAME = "Period Entrainment Optimization Model"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("f01:period_entrainment", "f02:velocity_optimization",
             "f03:variability_reduction"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 7,
            ("motor_period", "velocity", "acceleration", "cv_reduction"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 7, 9,
            ("period_lock_strength", "kinematic_smoothness"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("next_beat_pred_T", "velocity_profile_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PEOM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:period_entrainment", "f02:velocity_optimization",
            "f03:variability_reduction",
            "motor_period", "velocity", "acceleration", "cv_reduction",
            "period_lock_strength", "kinematic_smoothness",
            "next_beat_pred_T", "velocity_profile_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # SMA -- period locking and sequence timing
            RegionLink("f01:period_entrainment", "SMA", 0.90,
                       "Grahn & Brett 2007"),
            # Putamen -- beat period entrainment
            RegionLink("motor_period", "Putamen", 0.90,
                       "Grahn & Brett 2007"),
            # PMd -- velocity planning
            RegionLink("f02:velocity_optimization", "PMd", 0.85,
                       "Thaut 2015"),
            # Cerebellum -- motor timing error correction
            RegionLink("acceleration", "Cerebellum", 0.80,
                       "Thaut 2009b"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Thaut", 2015,
                         "Motor system entrains to auditory period via "
                         "dP/dt = alpha*(T-P(t)); fixed period provides CTR "
                         "that reduces jerk and smooths velocity profiles",
                         "review + computational model"),
                Citation("Thaut", 1998,
                         "Motor period entrains even during subliminal 2% "
                         "tempo changes in synchronized finger tapping",
                         "behavioral, N=10"),
                Citation("Grahn & Brett", 2007,
                         "Putamen Z=5.67, SMA Z=5.03 for beat vs non-beat "
                         "rhythms; basal ganglia beat processing",
                         "fMRI 3T, N=20"),
                Citation("Yamashita", 2025,
                         "CV reduction d=-1.10, stride time CV 4.51 to 2.80 "
                         "with rhythmic cueing; eta_p^2=0.309",
                         "tACS RCT, N=15"),
                Citation("Fujioka", 2012,
                         "Beta oscillations in SMA modulated by rhythmic "
                         "stimulus frequency; period-locked neural activity",
                         "MEG, N=12"),
                Citation("Nozaradan", 2011,
                         "Neural entrainment to beat frequencies; "
                         "frequency-tagged EEG responses to rhythm",
                         "EEG, N=11"),
                Citation("Ross & Balasubramaniam", 2022,
                         "Sensorimotor simulation supports subsecond beat "
                         "timing; motor imagery contributes to beat prediction",
                         "behavioral + TMS, N=24"),
                Citation("Repp", 2005,
                         "Period correction as distinct predictive mechanism; "
                         "separate from phase correction in tapping",
                         "behavioral review"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Period entrainment requires intact basal ganglia timing "
                "circuitry (Grahn & Brett 2007: putamen Z=5.67, SMA Z=5.03)",
                "CV reduction under rhythmic cueing is eliminated by "
                "disruption of SMA/putamen function "
                "(Yamashita 2025: d=-1.10, eta_p^2=0.309)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 11D period entrainment representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(4) + P(2) + F(2)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
