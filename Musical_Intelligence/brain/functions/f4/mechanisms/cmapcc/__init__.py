"""CMAPCC -- Cross-Modal Action-Perception Common Code.

Associator nucleus (depth 2) in IMU, Function F4. Models the unified
perception-action representation in right premotor cortex where dorsal
(fronto-parietal, action) and ventral (fronto-temporal, auditory) streams
converge. Cross-modal transfer allows learned patterns to generalize
across modalities.

Reads: MEAMN (mnemonic circuit), SNEM (beat cross-circuit)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, roughness_total)
    sethares_dissonance:    [1]      (A, sethares_dissonance)
    stumpf_fusion:          [3]      (A, stumpf_fusion)
    sensory_pleasantness:   [4]      (A, sensory_pleasantness)
    periodicity:            [5]      (A, roughness periodicity)
    amplitude:              [7]      (A, velocity_A)
    loudness:               [8]      (A, velocity_D)
    onset_strength:         [10]     (B, onset_strength)
    spectral_flux:          [11]     (B, spectral_flux)
    x_l0l5:                 [25:33]  (F, energy x consonance)
    x_l4l5:                 [33:41]  (F, derivatives x consonance)
    x_l5l7:                 [41:49]  (F, consonance x timbre)

Output structure: E(3) + M(2) + P(2) + F(3) = 10D
  E-layer [0:3]   Extraction    (sigmoid)  scope=internal
  M-layer [3:5]   Memory        (sigmoid)  scope=internal
  P-layer [5:7]   Present       (sigmoid)  scope=hybrid
  F-layer [7:10]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cmapcc/
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
    6: "200ms (beat)",
    11: "500ms",
    16: "1000ms (bar)",
    20: "5000ms (phrase)",
    24: "36000ms (section)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity", 14: "periodicity",
    18: "trend", 19: "stability",
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


# -- 20 H3 Demand Specifications -----------------------------------------------
# Cross-modal common code: perception-action convergence at multiple timescales.
# L0 (memory/backward) and L2 (integration/bidirectional).

_CMAPCC_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Common Code + Cross-Modal Binding (7 tuples) ===
    _h3(3, "stumpf_fusion", 16, 1, 2,
        "Binding coherence at 1s for common code",
        "Bianco 2016"),
    _h3(4, "sensory_pleasantness", 16, 0, 2,
        "Current sequence valence",
        "Bianco 2016"),
    _h3(5, "periodicity", 16, 1, 2,
        "Pitch regularity at 1s for common code",
        "Bianco 2016"),
    _h3(10, "onset_strength", 6, 0, 2,
        "Beat-level note onsets for action dynamics",
        "Bianco 2016"),
    _h3(8, "loudness", 6, 0, 2,
        "Beat-level intensity for action dynamics",
        "Bianco 2016"),
    _h3(0, "roughness", 16, 0, 2,
        "Current dissonance for sequence identity",
        "Bianco 2016"),
    _h3(1, "sethares_dissonance", 16, 1, 2,
        "Interval quality at 1s",
        "Bianco 2016"),

    # === M-Layer: Consolidation + Motor Coupling (6 tuples) ===
    _h3(3, "stumpf_fusion", 20, 1, 0,
        "Binding over 5s consolidation for transfer estimate",
        "Lahav 2007"),
    _h3(5, "periodicity", 20, 19, 0,
        "Sequence stability over 5s for coherence",
        "Lahav 2007"),
    _h3(10, "onset_strength", 11, 14, 0,
        "Onset regularity at 500ms for motor coupling",
        "Tanaka 2021"),
    _h3(8, "loudness", 11, 8, 0,
        "Intensity dynamics at 500ms for motor coupling",
        "Tanaka 2021"),
    _h3(10, "onset_strength", 16, 1, 0,
        "Mean onset over 1s bar",
        "Tanaka 2021"),
    _h3(8, "loudness", 16, 1, 0,
        "Mean intensity over bar",
        "Tanaka 2021"),

    # === P-Layer: PMC Activation + Mirror Coupling (2 new tuples) ===
    _h3(7, "amplitude", 6, 8, 0,
        "Action dynamics at beat level",
        "Ross 2022"),
    _h3(11, "spectral_flux", 6, 0, 2,
        "Spectral change at beat for event detection",
        "Bianco 2016"),

    # === F-Layer: Transfer + Motor + Perceptual Forecasts (5 new tuples) ===
    _h3(4, "sensory_pleasantness", 24, 1, 0,
        "Long-term valence context for consolidation",
        "Paraskevopoulos 2022"),
    _h3(1, "sethares_dissonance", 24, 19, 0,
        "Long-term interval stability for transfer",
        "Paraskevopoulos 2022"),
    _h3(7, "amplitude", 20, 18, 0,
        "Intensity trajectory 5s for transfer context",
        "Paraskevopoulos 2022"),
    _h3(11, "spectral_flux", 11, 1, 0,
        "Mean flux at 500ms for perceptual prediction",
        "Di Liberto 2021"),
    _h3(0, "roughness", 20, 18, 0,
        "Dissonance trajectory for perceptual prediction",
        "Di Liberto 2021"),
)

assert len(_CMAPCC_H3_DEMANDS) == 20


class CMAPCC(Associator):
    """Cross-Modal Action-Perception Common Code -- IMU Associator (depth 2, 10D).

    Models the unified perception-action representation in right premotor
    cortex where dorsal (fronto-parietal, action) and ventral
    (fronto-temporal, auditory) streams converge. Uses x_l4l5
    (derivatives x consonance) as the primary common code signal --
    temporal dynamics coupled with pitch identity reflects the shared
    format for hearing and performing musical sequences.

    Bianco et al. (2016): Dissociable dorsal and ventral networks
    converge on rIFG for harmonic prediction. BA44 Z=4.29 (action-seed),
    BA45 Z=5.12 (audio-seed), fMRI + resting-state FC, N=29 pianists.

    Lahav et al. (2007): Listening to trained melodies activates
    bilateral premotor, IFG, SMA -- motor training creates
    perceptual-action code (fMRI, N=9).

    Di Liberto et al. (2021): Accurate melody decoding from listening
    and imagery; note-onset F(1,20)=80.6, p=1.9e-8 (EEG, N=21).

    Dependency chain:
        CMAPCC is an Associator (Depth 2) -- reads MEAMN (mnemonic
        circuit) and SNEM (beat cross-circuit).

    Upstream reads:
        MEAMN: M1:p_recall [4], P0:memory_state [5]
        SNEM:  E0:beat_entrainment [0], P0:beat_locked_activity [6]

    Downstream feeds:
        -> cross_modal_transfer beliefs (Appraisal)
        -> mirror_coupling beliefs (Appraisal)
        -> F3 integrators via common code strength
    """

    NAME = "CMAPCC"
    FULL_NAME = "Cross-Modal Action-Perception Common Code"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("MEAMN",)
    CROSS_UNIT_READS = ("SNEM",)

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:common_code", "E1:cross_modal_binding",
             "E2:sequence_generalization"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:common_code_strength", "M1:transfer_probability"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:pmc_activation", "P1:mirror_coupling"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:transfer_pred", "F1:motor_seq_pred",
             "F2:perceptual_seq_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _CMAPCC_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:common_code", "E1:cross_modal_binding",
            "E2:sequence_generalization",
            "M0:common_code_strength", "M1:transfer_probability",
            "P0:pmc_activation", "P1:mirror_coupling",
            "F0:transfer_pred", "F1:motor_seq_pred",
            "F2:perceptual_seq_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Right IFG BA44 -- dorsal convergence for action
            RegionLink("E0:common_code", "R-IFG(BA44)", 0.85,
                       "Bianco 2016"),
            # Right IFG BA45 -- ventral convergence for auditory
            RegionLink("E1:cross_modal_binding", "R-IFG(BA45)", 0.85,
                       "Bianco 2016"),
            # SMA -- motor sequence programming
            RegionLink("P0:pmc_activation", "SMA", 0.80,
                       "Bianco 2016"),
            # Left IFOF -- white matter audiovisual integration
            RegionLink("M1:transfer_probability", "L-IFOF", 0.75,
                       "Moller 2021"),
            # Bilateral SPL BA7 -- visuomotor transformation
            RegionLink("F1:motor_seq_pred", "Bilateral SPL(BA7)", 0.70,
                       "Bianco 2016"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # CMAPCC is perception-action structural, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bianco et al.", 2016,
                         "Dissociable dorsal (fronto-parietal) and ventral "
                         "(fronto-temporal) networks converge on rIFG for "
                         "harmonic prediction; BA44 Z=4.29 (action-seed), "
                         "BA45 Z=5.12 (audio-seed); dual-stream architecture",
                         "fMRI + resting-state FC, N=29 pianists"),
                Citation("Lahav et al.", 2007,
                         "Listening to trained melodies activates bilateral "
                         "premotor, IFG, SMA; motor training creates "
                         "perceptual-action code; brief piano training "
                         "sufficient for action representation",
                         "fMRI, N=9"),
                Citation("Di Liberto et al.", 2021,
                         "Accurate melody decoding from listening and imagery; "
                         "note-onset F(1,20)=80.6, p=1.9e-8; shared encoding "
                         "between perceived and imagined melodies",
                         "EEG, N=21"),
                Citation("Moller et al.", 2021,
                         "Left IFOF FA correlates with audiovisual gain; "
                         "t=3.38, p<0.001; white matter structure supports "
                         "cross-modal integration",
                         "DTI, N=45"),
                Citation("Tanaka", 2021,
                         "Mu suppression at FC/Cz/CP during audiovisual opera; "
                         "d=0.72-0.86 (FDR p=0.027); mirror neuron engagement "
                         "requires multimodal input",
                         "EEG, N=21"),
                Citation("Paraskevopoulos et al.", 2022,
                         "Musicians show enhanced compartmentalized connectivity "
                         "during multisensory statistical learning; g=-1.09; "
                         "training drives broader connectivity changes",
                         "MEG+PTE, N=25"),
                Citation("Ross & Balasubramaniam", 2022,
                         "Motor networks causally involved in beat perception "
                         "via covert entrainment; TMS of premotor cortex "
                         "disrupts beat timing",
                         "mini-review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Common code (E0) must be higher for trained than untrained "
                "sequences (Lahav 2007: motor training creates action "
                "representation of sound, fMRI N=9)",
                "Cross-modal binding (E1) must correlate with IFOF FA "
                "(Moller 2021: t=3.38, p<0.001, DTI N=45)",
                "Mirror coupling (P1) must show mu suppression during "
                "audiovisual but not audio-only conditions (Tanaka 2021: "
                "d=0.72-0.86, EEG N=21)",
                "Transfer prediction (F0) must be higher for musicians than "
                "non-musicians (Paraskevopoulos 2022: g=-1.09, MEG N=25)",
                "Motor sequence prediction (F1) must be disrupted by TMS "
                "of premotor cortex (Ross 2022: causal involvement in "
                "beat perception)",
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
        """Transform R3/H3 + MEAMN/SNEM upstream into 10D cross-modal common code.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"MEAMN": (B, T, D), "SNEM": (B, T, D)}``

        Returns:
            ``(B, T, 10)`` -- E(3) + M(2) + P(2) + F(3)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(
            h3_features, r3_features, e, upstream_outputs,
        )
        p = compute_cognitive_present(
            h3_features, r3_features, e, m, upstream_outputs,
        )
        f = compute_forecast(h3_features, e, m, p, upstream_outputs)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
