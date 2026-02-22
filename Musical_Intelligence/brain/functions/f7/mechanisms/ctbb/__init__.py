"""CTBB -- Cerebellar Theta-Burst Balance.

Associator nucleus (depth 2) in MPU, Function F7. Models cerebellar theta-
burst stimulation (iTBS) effects on motor timing and postural control.
Cerebellar iTBS reduces postural sway (eta-sq=0.202, F=9.600, p=.004)
with effects sustained >= 30 min. The cerebellar dentate nucleus contains
three functional neuron types for rhythm prediction, timing control, and
error detection (Okada 2022).

CBI null result (eta-sq=0.045 n.s.) suggests the behavioural improvement
may involve alternative circuits (cerebellar-prefrontal, cerebellar-
vestibular) rather than the direct cerebellar-M1 inhibitory pathway.

Reads: PEOM.period_lock_strength + kinematic_smoothness (P-layer, idx 0-1)
       GSSM.phase_lock_strength + gait_stability (P-layer, idx 0-1)
       SPMC.sma_activity + m1_output (P-layer, idx 0-1)

R3 Ontology Mapping (post-freeze 97D):
    amplitude:       [7]      (B, motor output level)
    spectral_flux:   [10]     (B, timing dynamics)
    x_l0l5:          [25:33]  (F, cerebellar-M1 coupling)
    x_l4l5:          [33:41]  (G, balance variability)

Output structure: E(3) + M(3) + P(2) + F(3) = 11D
  E-layer [0:3]   Extraction           (sigmoid)  scope=internal
  M-layer [3:6]   Temporal Integration (sigmoid)  scope=internal
  P-layer [6:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer [8:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ctbb/
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
    3: "100ms (fast)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 14: "periodicity", 19: "stability",
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
_AMPLITUDE = 7
_SPECTRAL_FLUX = 10


# -- 8 H3 Demand Specifications -----------------------------------------------
# E-layer: 5 tuples (coupling stability/periodicity/fast, balance var, motor)
# M-layer: 3 tuples (spectral_flux onset/mean/variability)
# P-layer: 0 tuples
# F-layer: 0 tuples (shares E-layer coupling stability + periodicity)

_CTBB_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Cerebellar Extraction (5 tuples) ===
    _h3(25, "x_l0l5", 16, 19, 0,
        "Coupling stability 1s L0 -- cerebellar timing reliability",
        "Sansare 2025"),
    _h3(25, "x_l0l5", 16, 14, 2,
        "Coupling periodicity 1s L2 -- M1 modulation oscillatory basis",
        "Sansare 2025"),
    _h3(25, "x_l0l5", 3, 0, 2,
        "Cerebellar coupling 100ms L2 -- fast cerebellar timing signal",
        "Okada 2022"),
    _h3(33, "x_l4l5", 16, 2, 0,
        "Balance variability 1s L0 -- postural sway proxy",
        "Sansare 2025"),
    _h3(7, "amplitude", 16, 1, 2,
        "Mean motor output 1s L2 -- amplitude for postural control",
        "Sansare 2025"),

    # === M-layer: Timing Dynamics (3 tuples) ===
    _h3(10, "spectral_flux", 3, 0, 2,
        "Timing onset 100ms L2 -- immediate timing detection",
        "Okada 2022"),
    _h3(10, "spectral_flux", 16, 1, 0,
        "Mean timing 1s L0 -- sustained timing level",
        "Sansare 2025"),
    _h3(10, "spectral_flux", 16, 2, 0,
        "Timing variability 1s L0 -- timing precision inverse",
        "Sansare 2025"),
)

assert len(_CTBB_H3_DEMANDS) == 8


class CTBB(Associator):
    """Cerebellar Theta-Burst Balance -- MPU Associator (depth 2, 11D).

    Models cerebellar theta-burst stimulation (iTBS) effects on motor
    timing and postural control. Cerebellar iTBS reduces postural sway
    with sustained effects >= 30 min. Three functional neuron types in
    cerebellar dentate: rhythm prediction, timing control, error detection.

    Sansare et al. (2025): Cerebellar iTBS reduces postural sway
    (eta-sq=0.202, F=9.600, p=.004) with effects sustained >= 30 min;
    CBI null (eta-sq=0.045 n.s.) suggests alternative circuit mediation
    (iTBS, N=38).

    Okada et al. (2022): Cerebellar dentate nucleus contains 3 functional
    neuron types for rhythm prediction, timing control, and error detection
    (single-neuron recording, primate).

    Ivry (1988): Lateral cerebellum dissociation for timing vs execution;
    cerebellar lesions selectively impair timing but not force control
    (lesion, N=14).

    Shi et al. (2025): Bilateral M1 iTBS enhances gait automaticity
    (F=5.558, p=.026), supporting cerebellar-M1 pathway role in motor
    timing (iTBS, N=20).

    Huang et al. (2005): LTP-like facilitation from iTBS lasts ~20-30 min;
    TAU_DECAY=1800s governs temporal envelope of cerebellar enhancement
    (TMS, N=12).

    Dependency chain:
        CTBB reads PEOM (F7 relay, depth 0), GSSM (F7, depth 0),
        SPMC (F7, depth 1). Computed after all three in C3 scheduler.

    Downstream feeds:
        -> cerebellar_timing belief (Appraisal)
        -> balance_prediction belief (Anticipation)
    """

    NAME = "CTBB"
    FULL_NAME = "Cerebellar Theta-Burst Balance"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("PEOM", "GSSM", "SPMC")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:f25_cerebellar_timing", "E1:f26_m1_modulation",
             "E2:f27_postural_control"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 6,
            ("M0:timing_enhancement", "M1:sway_reduction",
             "M2:cerebellar_m1_coupling"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 8,
            ("P0:timing_precision", "P1:motor_stability"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:timing_pred", "F1:balance_pred", "F2:modulation_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _CTBB_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:f25_cerebellar_timing", "E1:f26_m1_modulation",
            "E2:f27_postural_control",
            "M0:timing_enhancement", "M1:sway_reduction",
            "M2:cerebellar_m1_coupling",
            "P0:timing_precision", "P1:motor_stability",
            "F0:timing_pred", "F1:balance_pred", "F2:modulation_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Cerebellum (Dentate) -- 3 neuron types: rhythm, timing, error
            RegionLink("E0:f25_cerebellar_timing", "cerebellum_dentate", 0.85,
                       "Okada 2022"),
            # Cerebellum (Lateral) -- timing vs execution dissociation
            RegionLink("P0:timing_precision", "cerebellum_lateral", 0.80,
                       "Ivry 1988"),
            # M1 -- cerebellar-M1 pathway (CBI null but still modeled)
            RegionLink("E1:f26_m1_modulation", "M1", 0.65,
                       "Sansare 2025"),
            # M1 -- coupling strength from M-layer
            RegionLink("M2:cerebellar_m1_coupling", "M1", 0.60,
                       "Sansare 2025"),
            # Prefrontal -- alternative cerebellar-prefrontal circuit
            RegionLink("M0:timing_enhancement", "prefrontal", 0.55,
                       "Sansare 2025"),
            # Vestibular -- balance-related cerebellar output
            RegionLink("E2:f27_postural_control", "vestibular", 0.75,
                       "Sansare 2025"),
            # Motor stability -> Vestibular (balance behaviour)
            RegionLink("P1:motor_stability", "vestibular", 0.70,
                       "Sansare 2025"),
            # Sway reduction -> Cerebellum (timing-balance integration)
            RegionLink("M1:sway_reduction", "cerebellum_dentate", 0.70,
                       "Sansare 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # CTBB modulates via iTBS plasticity, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Sansare et al.", 2025,
                         "Cerebellar iTBS reduces postural sway "
                         "(eta-sq=0.202, F=9.600, p=.004) with effects "
                         "sustained >= 30 min; CBI null (eta-sq=0.045 n.s.) "
                         "suggests alternative circuit mediation",
                         "iTBS, N=38"),
                Citation("Okada et al.", 2022,
                         "Cerebellar dentate nucleus contains 3 functional "
                         "neuron types for rhythm prediction, timing control, "
                         "and error detection",
                         "single-neuron recording, primate"),
                Citation("Ivry", 1988,
                         "Lateral cerebellum dissociation for timing vs "
                         "execution; cerebellar lesions selectively impair "
                         "timing but not force control",
                         "lesion, N=14"),
                Citation("Shi et al.", 2025,
                         "Bilateral M1 iTBS enhances gait automaticity "
                         "(F=5.558, p=.026); supports cerebellar-M1 "
                         "pathway role in motor timing",
                         "iTBS, N=20"),
                Citation("Huang et al.", 2005,
                         "LTP-like facilitation from iTBS lasts ~20-30 min; "
                         "theta-burst protocol produces sustained cortical "
                         "excitability changes",
                         "TMS, N=12"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Cerebellar timing (f25) must increase with coupling "
                "stability; if disrupting coupling does not reduce f25, "
                "the cerebellar-timing link is invalid (Sansare 2025)",
                "Postural control (f27) must show f25*f26 interaction "
                "effect; if the interaction term is ablated and f27 "
                "remains unchanged, the timing-modulation synergy is "
                "invalid (Sansare 2025)",
                "Sway reduction (M1) must be higher (less sway) when "
                "balance variability is lower; if inverting balance_var "
                "does not flip M1, the sway-reduction model is invalid",
                "Timing enhancement should decay with TAU_DECAY=1800s; "
                "if enhancement persists indefinitely without decay, "
                "the LTP-like temporal model is invalid (Huang 2005)",
                "Cerebellar-M1 coupling (M2) should show weak behavioral "
                "effect given CBI null; if M2 dominates the output, the "
                "cautious modeling is invalid (Sansare 2025 CBI null)",
                "Timing precision (P0) must be higher when both f25 and "
                "timing_enhancement are elevated; ablation of either "
                "should reduce P0 (Ivry 1988 timing dissociation)",
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
        """Transform R3/H3 + upstream into 11D cerebellar timing output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"PEOM": (B, T, 11), "GSSM": ..., "SPMC": ...}``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(2) + F(3)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        m = compute_temporal_integration(
            h3_features, r3_features, e, upstream_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
