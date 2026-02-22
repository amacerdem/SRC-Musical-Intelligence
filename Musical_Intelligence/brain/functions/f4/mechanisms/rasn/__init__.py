"""RASN -- Rhythmic Auditory Stimulation Neuroplasticity.

Encoder nucleus (depth 1) in IMU, Function F4. Models how rhythmic auditory
stimulation drives neuroplasticity through entrainment, motor facilitation,
and long-term synaptic reorganization. RAS is a clinical intervention that
leverages the brain's tendency to synchronize neural oscillations with
external rhythms, producing measurable structural and functional changes.

Reads: SNEM (intra-circuit via relay_outputs), beat-entrainment (F3 cross-circuit)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, roughness_total)
    stumpf_fusion:          [3]      (A, harmonic fusion)
    sensory_pleasantness:   [4]      (A, hedonic valence)
    periodicity_strength:   [5]      (A, rhythmic regularity)
    amplitude:              [7]      (A, velocity_A)
    loudness:               [8]      (A, velocity_D)
    spectral_flux:          [10]     (B, onset_strength proxy)
    onset_strength:         [11]     (B, event salience)
    entropy:                [23]     (D, pattern complexity)
    x_l0l5:                 [25:33]  (F, motor-auditory coupling)
    x_l4l5:                 [33:41]  (F, sensorimotor integration)

Output structure: E(3) + M(2) + P(3) + F(3) = 11D
  E-layer [0:3]   Extraction           (sigmoid)  scope=internal
  M-layer [3:5]   Temporal Integration (sigmoid)  scope=internal
  P-layer [5:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer [8:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/rasn/
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
    6: "200ms (beta)",
    11: "500ms (delta)",
    16: "1s (beat)",
    20: "5s (phrase)",
    24: "36s (plasticity)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 3: "std", 4: "max",
    8: "velocity", 14: "periodicity", 17: "peaks",
    18: "trend", 19: "stability",
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
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_PERIODICITY = 5
_AMPLITUDE = 7
_LOUDNESS = 8
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11
_ENTROPY = 23


# -- 28 H3 Demand Specifications -----------------------------------------------
# Rhythmic auditory stimulation neuroplasticity requires beat entrainment
# (periodicity), motor coupling (energy dynamics), complexity (entropy),
# binding (stumpf fusion), and long-horizon plasticity tracking.

_RASN_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Entrainment + Motor + Plasticity (12 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 6, 0, 2,
        "Current beat onset at 200ms",
        "Grahn 2007"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 11, 4, 0,
        "Peak onset over 500ms",
        "Grahn 2007"),
    _h3(_ONSET_STRENGTH, "onset_strength", 6, 0, 2,
        "Current onset sharpness at 200ms",
        "Nozaradan 2012"),
    _h3(_ONSET_STRENGTH, "onset_strength", 11, 14, 0,
        "Beat regularity at 500ms",
        "Nozaradan 2012"),
    _h3(_AMPLITUDE, "amplitude", 6, 0, 2,
        "Current beat energy at 200ms",
        "Harrison 2025"),
    _h3(_AMPLITUDE, "amplitude", 11, 8, 0,
        "Energy dynamics over 500ms",
        "Harrison 2025"),
    _h3(_AMPLITUDE, "amplitude", 16, 1, 0,
        "Average energy over 1s",
        "Harrison 2025"),
    _h3(_LOUDNESS, "loudness", 6, 0, 2,
        "Current accent strength at 200ms",
        "Grahn 2007"),
    _h3(_LOUDNESS, "loudness", 11, 17, 0,
        "Beat count per 500ms",
        "Noboa 2025"),
    _h3(_LOUDNESS, "loudness", 16, 1, 0,
        "Average loudness over 1s",
        "Noboa 2025"),
    _h3(_PERIODICITY, "periodicity_strength", 6, 0, 2,
        "Current rhythmic regularity at 200ms",
        "Nozaradan 2012"),
    _h3(_PERIODICITY, "periodicity_strength", 11, 14, 0,
        "Entrainment stability at 500ms",
        "Nozaradan 2012"),

    # === M-Layer: Complexity + Binding Integration (7 tuples) ===
    _h3(_ENTROPY, "entropy", 11, 0, 2,
        "Current complexity at 500ms",
        "Zhao 2025"),
    _h3(_ENTROPY, "entropy", 16, 1, 0,
        "Average complexity over 1s",
        "Zhao 2025"),
    _h3(_ENTROPY, "entropy", 20, 1, 0,
        "Complexity over 5s consolidation",
        "Blasi 2025"),
    _h3(_ENTROPY, "entropy", 24, 19, 0,
        "Pattern stability over 36s",
        "Blasi 2025"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 16, 1, 2,
        "Binding stability at 1s",
        "Zhao 2025"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 20, 1, 0,
        "Binding over 5s consolidation window",
        "Blasi 2025"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 24, 1, 0,
        "Long-term binding context 36s",
        "Blasi 2025"),

    # === P-Layer: Entrainment State + Precision (1 new tuple) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 14, 0,
        "Beat regularity at 1s bar level",
        "Ding 2025"),
    # (5,6,0,2), (5,11,14,0), (7,16,1,0) shared with E-layer

    # === F-Layer: Forecast Trajectories (8 tuples) ===
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Current engagement for trajectory",
        "Thaut 2015"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 20, 18, 0,
        "Engagement trajectory over 5s",
        "Thaut 2015"),
    _h3(_ROUGHNESS, "roughness", 16, 0, 2,
        "Current dissonance for challenge level",
        "Blasi 2025"),
    _h3(_ROUGHNESS, "roughness", 20, 18, 0,
        "Dissonance trajectory over 5s",
        "Blasi 2025"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 20, 1, 0,
        "Average onset over 5s consolidation",
        "Grahn 2007"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 24, 19, 0,
        "Onset stability over 36s plasticity",
        "Blasi 2025"),
    _h3(_AMPLITUDE, "amplitude", 20, 4, 0,
        "Peak energy over 5s",
        "Wang 2022"),
    _h3(_AMPLITUDE, "amplitude", 24, 3, 0,
        "Energy variability over 36s",
        "Wang 2022"),
)

assert len(_RASN_H3_DEMANDS) == 28


class RASN(Encoder):
    """Rhythmic Auditory Stimulation Neuroplasticity -- IMU Encoder (depth 1, 11D).

    Models how rhythmic auditory stimulation (RAS) drives neuroplasticity
    through three coupled mechanisms: (1) entrainment of neural oscillations
    to beat frequency via SMA + auditory cortex phase-locking, (2) motor
    facilitation through premotor cortex + cerebellum activation, and
    (3) long-term synaptic reorganization via hippocampal-corticospinal
    connectivity changes.

    Grahn & Brett 2007: fMRI N=27, SMA + putamen respond preferentially to
    beat-inducing rhythms (Z=5.67, FDR p<.05). Beat perception engages
    motor circuitry even during passive listening.

    Blasi et al. 2025: Systematic review 20 RCTs N=718, structural
    neuroplasticity from rhythm interventions -- hippocampal volume increases,
    grey matter changes, white matter integrity improvements after >= 4 weeks.

    Wang 2022: Meta-analysis, 22 studies -- RAS improves walking function
    (gait velocity, stride length, cadence) across neurological conditions.

    Harrison et al. 2025: fMRI N=55, PD + HC cued movement -- SMA, putamen,
    cerebellum activated (FWE-corrected clusters).

    Dependency chain:
        RASN is an Encoder (Depth 1) -- reads SNEM relay output (F3 cross-circuit).
        Computed after SNEM in F3 pipeline.

    Downstream feeds:
        -> memory_binding beliefs (Core)
        -> neuroplasticity_assessment beliefs (Appraisal)
        -> motor_memory context for F4 integrators
    """

    NAME = "RASN"
    FULL_NAME = "Rhythmic Auditory Stimulation Neuroplasticity"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("SNEM",)
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="ASU_SNEM__IMU_RASN__entrainment",
            name="SNEM entrainment to RASN rhythmic processing",
            source_unit="ASU",
            source_model="SNEM",
            source_dims=("beat_entrainment", "meter_entrainment",
                         "entrainment_strength"),
            target_unit="IMU",
            target_model="RASN",
            correlation="r=0.65",
            citation="Tierney & Kraus 2013",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:entrainment_strength", "E1:motor_facilitation",
             "E2:neuroplasticity_index"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 5,
            ("M0:neuroplasticity_composite", "M1:motor_recovery"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 5, 8,
            ("P0:entrainment_state", "P1:temporal_precision",
             "P2:motor_facilitation_level"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:movement_timing_pred", "F1:neuroplastic_change_pred",
             "F2:gait_improvement_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _RASN_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:entrainment_strength", "E1:motor_facilitation",
            "E2:neuroplasticity_index",
            "M0:neuroplasticity_composite", "M1:motor_recovery",
            "P0:entrainment_state", "P1:temporal_precision",
            "P2:motor_facilitation_level",
            "F0:movement_timing_pred", "F1:neuroplastic_change_pred",
            "F2:gait_improvement_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # SMA -- entrainment hub, phase-locking to beat
            RegionLink("E0:entrainment_strength", "SMA", 0.85,
                       "Grahn 2007"),
            # Putamen -- beat induction and timing
            RegionLink("P0:entrainment_state", "putamen", 0.80,
                       "Grahn 2007"),
            # Cerebellum -- temporal precision and motor coordination
            RegionLink("P1:temporal_precision", "cerebellum", 0.80,
                       "Harrison 2025"),
            # Premotor cortex -- motor facilitation
            RegionLink("E1:motor_facilitation", "premotor", 0.75,
                       "Harrison 2025"),
            # Auditory cortex -- rhythmic pattern encoding
            RegionLink("P2:motor_facilitation_level", "AC", 0.70,
                       "Nozaradan 2012"),
            # Hippocampus -- neuroplasticity and memory binding
            RegionLink("E2:neuroplasticity_index", "hippocampus", 0.75,
                       "Blasi 2025"),
            # M1 -- motor output for gait improvement
            RegionLink("F2:gait_improvement_pred", "M1", 0.70,
                       "Wang 2022"),
            # Corticospinal tract -- motor recovery pathway
            RegionLink("M1:motor_recovery", "CST", 0.65,
                       "Blasi 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # RASN modulates via entrainment, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Grahn & Brett", 2007,
                         "SMA + putamen respond preferentially to beat-inducing "
                         "rhythms; beat perception engages motor circuitry even "
                         "during passive listening (Z=5.67, FDR p<.05)",
                         "fMRI, N=27"),
                Citation("Blasi et al.", 2025,
                         "Structural neuroplasticity from rhythm interventions: "
                         "hippocampal volume increases, grey matter changes, "
                         "white matter integrity improvements after >= 4 weeks",
                         "systematic review, 20 RCTs, N=718"),
                Citation("Wang", 2022,
                         "RAS improves walking function: gait velocity, stride "
                         "length, cadence across stroke and neurological "
                         "conditions",
                         "meta-analysis, 22 studies"),
                Citation("Harrison et al.", 2025,
                         "External and internal cues activate sensorimotor "
                         "cortex, SMA, putamen, cerebellum in PD and HC "
                         "(FWE-corrected clusters)",
                         "fMRI, N=55"),
                Citation("Nozaradan", 2012,
                         "Steady-state evoked potentials at beat-related "
                         "frequencies demonstrate neural entrainment to "
                         "rhythmic stimuli",
                         "EEG, frequency-tagging"),
                Citation("Thaut et al.", 2015,
                         "Auditory-motor entrainment via reticulospinal "
                         "pathways; beta oscillations modulated in SMA",
                         "review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.85),
            falsification_criteria=(
                "Entrainment strength (E0) must be higher for regular vs "
                "irregular rhythms (Grahn 2007: Z=5.67 regular > irregular)",
                "Motor facilitation (E1) must increase with beat salience "
                "(Harrison 2025: FWE-corrected sensorimotor activation)",
                "Neuroplasticity index (E2) must show inverted-U with "
                "complexity (Blasi 2025: optimal complexity for plasticity)",
                "Temporal precision (P1) must correlate with periodicity "
                "(Ding 2025: ITPC eta-sq=0.14, all 12 rates entrain)",
                "Gait improvement prediction (F2) must be positive when "
                "entrainment is strong (Wang 2022: positive gait velocity)",
                "Disrupting beat regularity should reduce entrainment and "
                "downstream plasticity (testable via jittered beat paradigm)",
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
        """Transform R3/H3 + SNEM relay output into 11D RAS neuroplasticity.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"SNEM": (B, T, 12)}``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(2) + P(3) + F(3)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(
            h3_features, r3_features, e, m, relay_outputs,
        )
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
