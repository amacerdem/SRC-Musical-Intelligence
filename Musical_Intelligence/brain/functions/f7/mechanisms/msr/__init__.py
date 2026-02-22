"""MSR -- Musician Sensorimotor Reorganization.

Relay nucleus (depth 0) in MPU, Function F7. Models the dual sensorimotor
reorganization pattern in musicians: enhanced bottom-up precision (40-60 Hz PLV
increase, d=1.13) and increased top-down inhibition (P2 vertex suppression,
d=1.16). Net sensorimotor efficiency emerges from the PLV-P2 dissociation.
L. Zhang et al. (2015) demonstrated this dual reorganization with EEG in a
sample of 24 participants (12 musicians, 12 nonmusicians). Musicians showed
enhanced 40-60 Hz phase-locking (PLV = 0.40-0.44 vs 0.28-0.31) and suppressed
P2 vertex potentials (1.46-3.29 uV vs 4.65-5.91 uV). The low-frequency
time-frequency decomposition confirmed overall efficiency improvement (d=1.28).

Dependency chain:
    MSR is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays (PEOM, GSSM) at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    amplitude:              [7]  -> [7]    (B, velocity_A)
    loudness:               [8]  -> [8]    (B, velocity_D)
    spectral_flux:          [10] -> [10]   (B, onset_strength)
    spectral_change:        [21] -> [21]   (D, spectral_flux)
    x_l0l5:                 [25:33]        (F, coupling)
    x_l4l5:                 [33:41]        (G, interactions)

Output structure: E(3) + M(3) + P(3) + F(2) = 11D
  E-layer [0:3]   Extraction          (sigmoid)    scope=internal
  M-layer [3:6]   Temporal Integration (sigmoid)    scope=internal
  P-layer [6:9]   Present             (sigmoid)    scope=hybrid
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
    0: "25ms (gamma-fast)",
    1: "50ms (gamma)",
    3: "100ms (alpha)",
    4: "125ms (theta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    14: "periodicity", 20: "entropy", 21: "zero_crossings",
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
_ONSET_STRENGTH = 10             # B group (onset_strength)
_SPECTRAL_CHANGE = 21            # D group (spectral_flux)
_X_L0L5_START = 25               # F group (coupling)
_X_L4L5_START = 33               # G group (interactions)


# -- 22 H3 Demand Specifications -----------------------------------------------
# E-layer: 11 tuples, M-layer: 5 tuples, P-layer: 3 tuples, F-layer: 3 tuples
# All L2 (bidirectional integration) per L. Zhang 2015 dual reorganization

_MSR_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Dual reorganization extraction (tuples 0-10) ===

    # #0: Coupling at 25ms gamma -- high-freq tracking
    _h3(25, "x_l0l5", 0, 0, 2,
        "Coupling at 25ms gamma -- high-freq tracking",
        "L. Zhang 2015"),
    # #1: Coupling at 50ms gamma -- PLV source
    _h3(25, "x_l0l5", 1, 0, 2,
        "Coupling at 50ms gamma -- PLV source",
        "L. Zhang 2015"),
    # #2: Mean coupling 50ms -- gamma baseline
    _h3(25, "x_l0l5", 1, 1, 2,
        "Mean coupling 50ms -- gamma baseline",
        "L. Zhang 2015"),
    # #3: Coupling at 100ms alpha -- PLV integration
    _h3(25, "x_l0l5", 3, 0, 2,
        "Coupling at 100ms alpha -- PLV integration",
        "L. Zhang 2015"),
    # #4: Coupling variability 100ms -- precision
    _h3(25, "x_l0l5", 3, 2, 2,
        "Coupling variability 100ms -- precision measure",
        "L. Zhang 2015"),
    # #5: Coupling periodicity 100ms -- oscillation
    _h3(25, "x_l0l5", 3, 14, 2,
        "Coupling periodicity 100ms -- oscillation tracking",
        "L. Zhang 2015"),
    # #6: Sensorimotor coupling 100ms -- training
    _h3(33, "x_l4l5", 3, 0, 2,
        "Sensorimotor coupling 100ms -- training-enhanced binding",
        "Alpheis 2025"),
    # #7: Coupling stability 100ms -- precision
    _h3(33, "x_l4l5", 3, 2, 2,
        "Coupling stability 100ms -- precision measure",
        "Alpheis 2025"),
    # #8: Coupling entropy 100ms -- complexity
    _h3(33, "x_l4l5", 3, 20, 2,
        "Coupling entropy 100ms -- complexity measure",
        "Alpheis 2025"),
    # #9: Loudness entropy 100ms -- P2 proxy
    _h3(8, "loudness", 3, 20, 2,
        "Loudness entropy 100ms -- P2 amplitude proxy",
        "L. Zhang 2015"),
    # #10: Onset periodicity 1s -- P2 suppression
    _h3(10, "onset_strength", 16, 14, 2,
        "Onset periodicity 1s -- P2 suppression indicator",
        "L. Zhang 2015"),

    # === M-layer: Continuous PLV/P2 estimates (tuples 11-15) ===

    # #11: Coupling periodicity 125ms -- theta oscillation
    _h3(25, "x_l0l5", 4, 14, 2,
        "Coupling periodicity 125ms -- theta oscillation",
        "L. Zhang 2015"),
    # #12: Mean coupling over 1s -- long-term PLV baseline
    _h3(25, "x_l0l5", 16, 1, 2,
        "Mean coupling over 1s -- long-term PLV baseline",
        "L. Zhang 2015"),
    # #13: Coupling periodicity 1s -- beat-level PLV
    _h3(25, "x_l0l5", 16, 14, 2,
        "Coupling periodicity 1s -- beat-level PLV",
        "Grahn & Brett 2007"),
    # #14: Loudness at 100ms -- P2 amplitude input
    _h3(8, "loudness", 3, 0, 2,
        "Loudness at 100ms -- P2 amplitude input",
        "L. Zhang 2015"),
    # #15: Loudness variability 100ms -- P2 modulation
    _h3(8, "loudness", 3, 2, 2,
        "Loudness variability 100ms -- P2 modulation",
        "L. Zhang 2015"),

    # === P-layer: Present-state assessment (tuples 16-18) ===

    # #16: Coupling phase resets 1s -- synchrony stability
    _h3(25, "x_l0l5", 16, 21, 2,
        "Coupling phase resets 1s -- synchrony stability",
        "L. Zhang 2015"),
    # #17: Onset at 100ms -- bottom-up input
    _h3(10, "onset_strength", 3, 0, 2,
        "Onset at 100ms -- bottom-up input",
        "Grahn & Brett 2007"),
    # #18: Onset periodicity 100ms -- processing regularity
    _h3(10, "onset_strength", 3, 14, 2,
        "Onset periodicity 100ms -- processing regularity",
        "Grahn & Brett 2007"),

    # === F-layer: Future predictions (tuples 19-21) ===

    # #19: Amplitude at 100ms -- motor drive for prediction
    _h3(7, "amplitude", 3, 0, 2,
        "Amplitude at 100ms -- motor drive for prediction",
        "Grahn & Brett 2007"),
    # #20: Mean amplitude 1s -- sustained motor state
    _h3(7, "amplitude", 16, 1, 2,
        "Mean amplitude 1s -- sustained motor state",
        "Blasi 2025"),
    # #21: Tempo velocity at 125ms -- rate dynamics for prediction
    _h3(21, "spectral_change", 4, 8, 2,
        "Tempo velocity at 125ms -- rate dynamics for prediction",
        "Fujioka 2012"),
)

assert len(_MSR_H3_DEMANDS) == 22


class MSR(Relay):
    """Musician Sensorimotor Reorganization -- MPU Relay (depth 0, 11D).

    Models the dual sensorimotor reorganization pattern in musicians:
    enhanced bottom-up precision (40-60 Hz PLV increase, d=1.13) and
    increased top-down inhibition (P2 vertex suppression, d=1.16).
    L. Zhang 2015: EEG, N=24 (12 musicians, 12 nonmusicians).
    Musicians PLV = 0.40-0.44 vs nonmusicians 0.28-0.31 (d=1.13, p=0.009).
    Musicians P2 = 1.46-3.29 uV vs nonmusicians 4.65-5.91 uV (d=1.16, p=0.005).
    Net sensorimotor efficiency: low-freq TFD d=1.28 (p=0.002).

    Dependency chain:
        MSR is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> training_level + bottom_up_precision for 'sensorimotor_expertise' (Appraisal belief)
        -> ASAP, VRMSME, STC (depth-1/2 models read MSR outputs)
    """

    NAME = "MSR"
    FULL_NAME = "Musician Sensorimotor Reorganization"
    UNIT = "MPU"
    FUNCTION = "F7"
    OUTPUT_DIM = 11

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("f04:high_freq_plv", "f05:p2_suppression",
             "f06:sensorimotor_efficiency"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 6,
            ("plv_high_freq", "p2_amplitude", "efficiency_index"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 9,
            ("bottom_up_precision", "top_down_modulation", "training_level"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("performance_efficiency", "processing_automaticity"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MSR_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f04:high_freq_plv", "f05:p2_suppression",
            "f06:sensorimotor_efficiency",
            "plv_high_freq", "p2_amplitude", "efficiency_index",
            "bottom_up_precision", "top_down_modulation", "training_level",
            "performance_efficiency", "processing_automaticity",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Auditory Cortex -- 40-60 Hz PLV enhancement
            RegionLink("f04:high_freq_plv", "Auditory Cortex", 0.85,
                       "L. Zhang 2015"),
            # ACC -- P2 suppression / top-down cortical gating
            RegionLink("f05:p2_suppression", "ACC", 0.85,
                       "L. Zhang 2015"),
            # PMC / SMA -- motor-area activation across rhythm types
            RegionLink("bottom_up_precision", "PMC", 0.80,
                       "Grahn & Brett 2007"),
            # dlPFC-Putamen -- enhanced FC in musicians
            RegionLink("training_level", "dlPFC", 0.80,
                       "Alpheis 2025"),
            # Cerebellum -- structural neuroplasticity
            RegionLink("processing_automaticity", "Cerebellum", 0.75,
                       "Blasi 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("L. Zhang", 2015,
                         "Dual sensorimotor reorganization in musicians: "
                         "enhanced 40-60 Hz PLV (d=1.13) and P2 vertex "
                         "suppression (d=1.16). Low-freq TFD efficiency "
                         "d=1.28",
                         "EEG, N=24 (12 musicians, 12 nonmusicians)"),
                Citation("Grahn & Brett", 2007,
                         "Musicians activate PMC, cerebellum, SMA during "
                         "all rhythm types; putamen for metric rhythms "
                         "(Z=5.67)",
                         "fMRI 3T, N=20"),
                Citation("Alpheis", 2025,
                         "Enhanced FC of dlPFC-putamen (t=4.46) in musician "
                         "brains during music listening",
                         "fMRI, musicians vs nonmusicians"),
                Citation("Blasi", 2025,
                         "Structural neuroplasticity from music/dance "
                         "training: GMV increases in IFG, cerebellum",
                         "meta-analysis, 20 RCTs, N=718"),
                Citation("Liang", 2025,
                         "VR music stimulation enhances PM-SMA, dlPFC, M1 "
                         "connectivity bilaterally (p<.01 FDR)",
                         "fNIRS, N=20"),
                Citation("Fujioka", 2012,
                         "Internalized timing in beta oscillations (SMA) "
                         "during auditory rhythm perception",
                         "MEG, N=12"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.92),
            falsification_criteria=(
                "Musicians show enhanced 40-60 Hz PLV relative to "
                "nonmusicians (L. Zhang 2015: d=1.13, p=0.009). "
                "Abolishing this PLV difference would falsify the model.",
                "Musicians show suppressed P2 vertex potentials relative "
                "to nonmusicians (L. Zhang 2015: d=1.16, p=0.005). "
                "Equivalent P2 amplitudes would falsify the model.",
                "The dual reorganization pattern (enhanced PLV + suppressed "
                "P2) must co-occur (L. Zhang 2015: TFD d=1.28). "
                "A single-mechanism pattern would falsify the dual model.",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 11D sensorimotor reorganization representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(3) + F(2)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
