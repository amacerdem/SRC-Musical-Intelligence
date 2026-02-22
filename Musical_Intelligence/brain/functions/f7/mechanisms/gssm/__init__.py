"""GSSM -- Gait-Synchronized Stimulation Model.

Relay nucleus (depth 0) in MPU, Function F7. Models gait-synchronized
dual-site stimulation (tDCS to SMA + gait-phase-locked tACS to M1). Phase
synchronization between stimulation rhythm and gait cycle produces stride
variability reduction (CV d=-1.10) and balance improvement (Mini-BESTest
d=1.05). The CV-balance correlation (r=0.62) demonstrates the
variability-balance coupling.

Dependency chain:
    GSSM is a Relay (Depth 0) -- reads R3/H3 directly, no upstream
    dependencies. Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    amplitude:          [7]  -> [7]    (B, velocity_A)
    spectral_flux:      [10] -> [10]   (B, onset_strength)
    onset_strength:     [11] -> [11]   (B, onset_strength)
    energy_change:      [22] -> [22]   (D, distribution_entropy)
    x_l0l5:             [25:33]        (F, coupling)

Output structure: E(3) + M(4) + P(2) + F(2) = 11D
  E-layer [0:3]   Extraction          (sigmoid)    scope=internal
  M-layer [3:7]   Temporal Integration (sigmoid)    scope=internal
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
    3: "100ms (sub-beat)",
    8: "500ms (half-stride)",
    16: "1000ms (beat/stride)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity",
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
_AMPLITUDE = 7               # B group (velocity_A)
_SPECTRAL_FLUX = 10          # B group (onset_strength)
_ONSET_STRENGTH = 11         # B group
_ENERGY_CHANGE = 22          # D group
_X_L0L5_START = 25           # F group (coupling)


# -- 12 H3 Demand Specifications ----------------------------------------------
# E-layer: 7 tuples, M-layer: 3 tuples, P-layer: 2 tuples, F-layer: 0 unique

_GSSM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Extraction (tuples 0-6) ===

    # #0: Step onset value at 100ms -- step detection
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Step onset 100ms -- gait phase detection",
        "Yamashita 2025"),
    # #1: Step periodicity at 100ms -- gait rhythm
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 14, 2,
        "Step periodicity 100ms -- gait rhythm",
        "Yamashita 2025"),
    # #2: Step periodicity at 1s -- stride cycle
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 14, 2,
        "Step periodicity 1s -- stride cycle",
        "Yamashita 2025"),
    # #3: Heel strike value at 100ms
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 2,
        "Heel strike onset 100ms -- phase locking anchor",
        "Yamashita 2025"),
    # #4: Gait periodicity at 500ms -- half-stride
    _h3(_ONSET_STRENGTH, "onset_strength", 8, 14, 2,
        "Gait periodicity 500ms -- half-stride detection",
        "Yamashita 2025"),
    # #5: SMA-M1 coupling value at 100ms -- dual-site sync
    _h3(_X_L0L5_START, "x_l0l5[0]", 3, 0, 2,
        "SMA-M1 coupling 100ms -- dual-site synchronization",
        "Yamashita 2025"),
    # #6: Coupling periodicity at 100ms -- phase lock
    _h3(_X_L0L5_START, "x_l0l5[0]", 3, 14, 2,
        "Coupling periodicity 100ms -- stimulation phase lock",
        "Yamashita 2025"),

    # === M-layer: Temporal Integration (tuples 7-9) ===

    # #7: Step amplitude at 100ms -- stride force
    _h3(_AMPLITUDE, "amplitude", 3, 0, 2,
        "Step amplitude 100ms -- stride force proxy",
        "Yamashita 2025"),
    # #8: Mean amplitude at 1s -- gait energy baseline
    _h3(_AMPLITUDE, "amplitude", 16, 1, 2,
        "Mean amplitude 1s -- gait energy baseline",
        "Yamashita 2025"),
    # #9: Coupling periodicity at 1s -- stride-level SMA-M1 sync
    _h3(_X_L0L5_START, "x_l0l5[0]", 16, 14, 2,
        "Coupling periodicity 1s -- stride-level SMA-M1 sync",
        "Yamashita 2025"),

    # === P-layer: Cognitive Present (tuples 10-11) ===

    # #10: Coupling phase resets at 1s -- lock disruptions
    _h3(_X_L0L5_START, "x_l0l5[0]", 16, 21, 2,
        "Coupling phase resets 1s -- phase lock disruption detection",
        "Grahn & Brett 2007"),
    # #11: Energy dynamics at 500ms -- gait energy fluctuation
    _h3(_ENERGY_CHANGE, "energy_change", 8, 8, 0,
        "Energy dynamics 500ms -- gait energy velocity fluctuation",
        "Yamashita 2025"),
)

assert len(_GSSM_H3_DEMANDS) == 12


class GSSM(Relay):
    """Gait-Synchronized Stimulation Model -- MPU Relay (depth 0, 11D).

    Models gait-synchronized dual-site stimulation from Yamashita et al. (2025).
    Phase synchronization between stimulation rhythm and gait cycle produces
    stride variability reduction (CV d=-1.10) and balance improvement
    (Mini-BESTest d=1.05).

    Dependency chain:
        GSSM is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> phase_lock_strength + gait_stability for 'gait_entrainment' belief
        -> CTBB (depth 2): gait timing signals
    """

    NAME = "GSSM"
    FULL_NAME = "Gait-Synchronized Stimulation Model"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:phase_synchronization", "E1:cv_reduction",
             "E2:balance_improvement"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 7,
            ("M0:stride_cv", "M1:sma_m1_coupling",
             "M2:balance_score", "M3:gait_stability"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 7, 9,
            ("P0:phase_lock_strength", "P1:variability_level"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:cv_pred_30min", "F1:balance_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _GSSM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:phase_synchronization", "E1:cv_reduction",
            "E2:balance_improvement",
            "M0:stride_cv", "M1:sma_m1_coupling",
            "M2:balance_score", "M3:gait_stability",
            "P0:phase_lock_strength", "P1:variability_level",
            "F0:cv_pred_30min", "F1:balance_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # SMA (Fz) -- tDCS target; sequence timing
            RegionLink("M1:sma_m1_coupling", "SMA", 0.85,
                       "Yamashita 2025"),
            # M1 (Cz lateral) -- tACS target; gait-phase-locked execution
            RegionLink("P0:phase_lock_strength", "M1", 0.85,
                       "Yamashita 2025"),
            # Putamen -- beat period entrainment for gait
            RegionLink("E0:phase_synchronization", "Putamen", 0.80,
                       "Grahn & Brett 2007"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Yamashita", 2025,
                         "Gait-synchronized tACS to M1 + tDCS to SMA; "
                         "stride time CV d=-1.10, Mini-BESTest d=1.05, "
                         "CV-balance r=0.62",
                         "tACS+tDCS, N=15, eta_p^2=0.309"),
                Citation("Sansare", 2025,
                         "Cerebellar iTBS reduced postural sway with "
                         "effects sustained >= 30 min in healthy older adults",
                         "iTBS, N=38, eta-sq=0.202"),
                Citation("Grahn & Brett", 2007,
                         "Putamen Z=5.67 for beat period locking; "
                         "SMA Z=5.03 for sequence timing",
                         "fMRI, N=20"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Phase synchronization between stimulation and gait cycle "
                "is necessary for therapeutic effect (Yamashita 2025: "
                "sham d=0.24 n.s. vs real d=-1.10)",
                "Dual-site stimulation (SMA+M1) required; single-site "
                "insufficient for full CV-balance coupling (r=0.62)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 11D gait-synchronized stimulation representation.

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
