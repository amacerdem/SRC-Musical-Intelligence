"""SPMC -- SMA-Premotor-M1 Motor Circuit.

Encoder nucleus (depth 1) in MPU, Function F7.  Models the hierarchical
SMA-Premotor-M1 motor circuit for musically-cued movement.  SMA encodes
temporal sequences (longest timescale), PMC performs action selection
(medium), and M1 executes motor output (shortest).  The circuit flow
follows a top-down hierarchy where execution depends on both planning
and preparation being active.  Cerebellar timing precision provides
online error correction.

Reads: PEOM (period entrainment), ASAP (beat prediction), VRMSME (motor
       drive) -- via relay_outputs dict.

R3 Ontology Mapping (post-freeze 97D):
    amplitude:         [7]      (B, motor output strength)
    spectral_flux:     [10]     (B, onset detection for SMA)
    onset_strength:    [11]     (B, beat event for motor timing)
    spectral_change:   [21]     (D, tempo rate for SMA)
    x_l0l5:            [25:33]  (F, hierarchical circuit coupling)
    x_l4l5:            [33:41]  (G, sequence regularity)

Output structure: E(3) + M(3) + P(2) + F(3) = 11D
  E-layer   [0:3]   Extraction           (sigmoid)  scope=internal
  M-layer   [3:6]   Temporal Integration (sigmoid)  scope=internal
  P-layer   [6:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [8:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/spmc/
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
    0: "25ms (gamma)",
    1: "50ms (gamma)",
    3: "100ms (alpha)",
    4: "125ms (beta)",
    8: "500ms (half-beat)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    14: "periodicity", 19: "stability", 20: "entropy",
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


# -- R3 feature names (post-freeze 97D) --------------------------------------
_AMPLITUDE = 7
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11
_SPECTRAL_CHANGE = 21


# -- 20 H3 Demand Specifications ----------------------------------------------
# SMA-Premotor-M1 Motor Circuit requires multi-scale onset/beat periodicity,
# circuit coupling, and sequence stability features.  L0 (forward) + L2
# (bidirectional).

_SPMC_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Motor hierarchy extraction (6 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "SMA onset tracking 100ms",
        "Grahn & Brett 2007"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 14, 2,
        "SMA beat periodicity 1s",
        "Grahn & Brett 2007"),
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 2,
        "Motor timing marker 100ms",
        "Kohler 2025"),
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 14, 2,
        "Onset periodicity 1s",
        "Hoddinott & Grahn 2024"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 4, 8, 0,
        "Tempo velocity 125ms",
        "Pierrieau 2025"),
    _h3(_AMPLITUDE, "amplitude", 16, 1, 2,
        "Mean motor output level 1s",
        "Harrison 2025"),

    # === M-Layer: Temporal integration (5 unique tuples) ===
    # Note: M-layer also reuses E#1 (10,16,14,2) — not repeated here
    _h3(25, "x_l0l5", 8, 14, 2,
        "Circuit periodicity 500ms",
        "Zatorre 2007"),
    _h3(25, "x_l0l5", 16, 14, 2,
        "Circuit periodicity 1s",
        "Harrison 2025"),
    _h3(33, "x_l4l5", 8, 1, 0,
        "Mean pattern stability 500ms",
        "Grahn & Brett 2007"),
    _h3(33, "x_l4l5", 16, 2, 0,
        "Sequence variability 1s",
        "Okada 2022"),
    _h3(33, "x_l4l5", 16, 19, 0,
        "Sequence stability 1s",
        "Okada 2022"),

    # === P-Layer: Cognitive present (2 unique tuples) ===
    # Note: P reuses E#0 (10,3,0,2), E#2 (11,3,0,2) — not repeated
    _h3(25, "x_l0l5", 3, 0, 2,
        "Circuit coupling 100ms for SMA present state",
        "Grahn & Brett 2007"),
    _h3(33, "x_l4l5", 3, 0, 2,
        "Sequence regularity 100ms for M1 present state",
        "Kohler 2025"),

    # === F-Layer: Forecast predictions (2 unique tuples) ===
    # Note: F reuses E#1 (10,16,14,2), M#11 (33,16,19,0) — not repeated
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 1, 0,
        "Mean tempo change 1s for execution prediction",
        "Harrison 2025"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 2, 0,
        "Tempo variability 1s for timing prediction",
        "Okada 2022"),
)

assert len(_SPMC_H3_DEMANDS) == 15


class SPMC(Encoder):
    """SMA-Premotor-M1 Motor Circuit -- MPU Encoder (depth 1, 11D).

    Models the hierarchical motor circuit for musically-cued movement:
        - SMA encodes temporal sequences (longest timescale)
        - PMC performs action selection (medium timescale)
        - M1 executes motor output (shortest timescale)
        - Cerebellum provides timing precision via error correction

    The circuit flow follows a top-down hierarchy where execution depends
    on both planning and preparation being active.  The multiplicative
    interaction f19 * f20 in the E-layer captures this hierarchical
    dependency.

    Grahn & Brett 2007: SMA + putamen respond to beat in metric rhythms
    (F(2,38)=20.67, p<.001, Z=5.03/5.67).

    Hoddinott & Grahn 2024: SMA multi-voxel patterns encode beat strength
    via representational similarity analysis (RSA).

    Kohler 2025: M1 shows content-specific action representations via
    multi-voxel pattern analysis (MVPA).

    Okada 2022: Cerebellar dentate nucleus contains 3 neuron types for
    rhythm prediction, timing control, and error detection.

    Pierrieau 2025: Beta oscillations (13-30 Hz) in motor cortex predict
    motor flexibility / action selection.

    Harrison 2025: Both CTC and SPT pathways active during musically-cued
    movements.

    Dependency chain:
        SPMC is an Encoder (Depth 1) -- reads PEOM, ASAP, VRMSME.
        Computed after depth-0 relays in F7 pipeline.

    Downstream feeds:
        -> motor_hierarchy belief (Core, tau=0.4)
        -> motor_timing belief (Anticipation)
    """

    NAME = "SPMC"
    FULL_NAME = "SMA-Premotor-M1 Motor Circuit"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("PEOM", "ASAP", "VRMSME")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="MPU_PEOM__MPU_SPMC__period_entrainment",
            name="PEOM period lock to SPMC sequence planning",
            source_unit="MPU",
            source_model="PEOM",
            source_dims=("period_lock_strength",),
            target_unit="MPU",
            target_model="SPMC",
            correlation="r=0.65",
            citation="Grahn & Brett 2007",
        ),
        CrossUnitPathway(
            pathway_id="MPU_ASAP__MPU_SPMC__action_simulation",
            name="ASAP motor-to-auditory to SPMC circuit flow",
            source_unit="MPU",
            source_model="ASAP",
            source_dims=("motor_to_auditory",),
            target_unit="MPU",
            target_model="SPMC",
            correlation="r=0.55",
            citation="Patel & Iversen 2014",
        ),
        CrossUnitPathway(
            pathway_id="MPU_VRMSME__MPU_SPMC__motor_enhancement",
            name="VRMSME motor drive to SPMC execution output",
            source_unit="MPU",
            source_model="VRMSME",
            source_dims=("motor_drive",),
            target_unit="MPU",
            target_model="SPMC",
            correlation="r=0.50",
            citation="Liang 2025",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:sequence_planning", "E1:motor_preparation",
             "E2:execution_output"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 6,
            ("M0:circuit_flow", "M1:hierarchy_index",
             "M2:timing_precision"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 8,
            ("P0:sma_activity", "P1:m1_output"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:sequence_pred", "F1:execution_pred",
             "F2:timing_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SPMC_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:sequence_planning", "E1:motor_preparation",
            "E2:execution_output",
            "M0:circuit_flow", "M1:hierarchy_index",
            "M2:timing_precision",
            "P0:sma_activity", "P1:m1_output",
            "F0:sequence_pred", "F1:execution_pred",
            "F2:timing_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # SMA / pre-SMA -- sequence planning & temporal structure
            RegionLink("E0:sequence_planning", "SMA", 0.85,
                       "Grahn & Brett 2007"),
            # PMC -- action selection and motor preparation
            RegionLink("E1:motor_preparation", "PMC", 0.80,
                       "Pierrieau 2025"),
            # M1 -- motor execution output
            RegionLink("E2:execution_output", "M1", 0.85,
                       "Kohler 2025"),
            # Cerebellum (dentate) -- timing precision
            RegionLink("M2:timing_precision", "cerebellum", 0.80,
                       "Okada 2022"),
            # Putamen -- beat-metric response
            RegionLink("P0:sma_activity", "putamen", 0.75,
                       "Grahn & Brett 2007"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- putamen beat-metric response
            NeuroLink("M0:circuit_flow", "dopamine", 0.70,
                      "Grahn & Brett 2007"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Grahn & Brett", 2007,
                         "SMA + putamen respond to beat in metric rhythms; "
                         "F(2,38)=20.67, p<.001; SMA Z=5.03, putamen Z=5.67",
                         "fMRI, N=?"),
                Citation("Hoddinott & Grahn", 2024,
                         "SMA multi-voxel patterns encode beat strength "
                         "via representational similarity analysis",
                         "fMRI, RSA"),
                Citation("Kohler et al.", 2025,
                         "M1 content-specific action representations for "
                         "self-produced actions via MVPA",
                         "fMRI, MVPA"),
                Citation("Okada et al.", 2022,
                         "Cerebellar dentate nucleus: 3 neuron types for "
                         "rhythm prediction, timing, and error detection",
                         "electrophysiology"),
                Citation("Pierrieau et al.", 2025,
                         "Beta oscillations (13-30 Hz) predict motor "
                         "flexibility/action selection, not vigor",
                         "EEG"),
                Citation("Harrison et al.", 2025,
                         "CTC and SPT pathways active during musically-cued "
                         "movements; sensorimotor cortex activation",
                         "fMRI"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Circuit flow (M0) must be higher when both SMA planning "
                "and M1 execution are active than when either is alone "
                "(hierarchical dependency from sigma(0.5*f19+0.5*f21))",
                "Hierarchy index (M1) must track top-down planning structure "
                "via sigma(0.5*f19+0.5*f20), not bottom-up reactivity",
                "Timing precision (M2) must correlate with beat periodicity "
                "(Okada 2022: dentate neurons encode timing accuracy)",
                "Execution output (E2) must depend on the f19*f20 product "
                "(multiplicative gate), not on planning or preparation alone",
                "Disrupting SMA (via TMS/lesion) should reduce sequence "
                "planning and circuit flow while sparing M1 output",
                "Disrupting cerebellum should reduce timing precision but "
                "not hierarchy index (Ivry 1988 dissociation)",
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
        """Transform R3/H3 + relay outputs into 11D motor circuit signal.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"PEOM": (B,T,11), "ASAP": (B,T,11),
                              "VRMSME": (B,T,11)}``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(2) + F(3)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(
            h3_features, r3_features, e, relay_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
