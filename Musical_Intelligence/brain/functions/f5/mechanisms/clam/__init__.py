"""CLAM -- Closed-Loop Affective Modulation.

Encoder nucleus (depth 1) in ARU, Function F5. Models closed-loop BCI
affective modulation where EEG-decoded brain state drives real-time music
generation to steer affect toward a therapeutic target. Arousal tracking
r=0.74; valence tracking r=0.52 (Ehrlich 2019). Loop latency ~1s.
3/5 participant success rate.

Reads: SRP (intra-circuit via relay_outputs), AAC (intra-circuit via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, roughness_total)
    sensory_pleasantness:   [4]      (A, hedonic valence)
    velocity_A:             [8]      (B, arousal dynamics)
    loudness:               [10]     (B, energy-level arousal)
    onset_strength:         [11]     (B, event density)
    spectral_centroid:      [12]     (C, brightness for BCI mapping)
    spectral_flux:          [21]     (D, real-time feedback signal)
    x_l0l5:                 [25:33]  (F, BCI affect mapping space)

Output structure: E(2) + B+C(5) + P(2) + F(2) = 11D
  E-layer   [0:2]   Extraction           (sigmoid)  scope=internal
  B+C-layer [2:7]   Temporal Integration (sigmoid)  scope=internal
  P-layer   [7:9]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [9:11]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
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
    7: "200ms (beta)",
    12: "525ms (theta)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 8: "velocity", 18: "trend", 20: "entropy",
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
_SENSORY_PLEASANTNESS = 4
_VELOCITY_A = 8
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_SPECTRAL_CENTROID = 12
_SPECTRAL_FLUX = 21


# -- 12 H3 Demand Specifications -----------------------------------------------
# Closed-loop affective modulation requires arousal dynamics (loudness velocity),
# valence baseline (roughness), feedback signal rate (spectral_flux velocity),
# and multi-scale integration across BCI loop latency (~1s).

_CLAM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Affective Modulation + Loop Coherence (2 tuples) ===
    _h3(_LOUDNESS, "loudness", 16, 20, 0,
        "1s entropy of arousal — loop stability",
        "Ehrlich 2019"),
    _h3(_LOUDNESS, "loudness", 7, 8, 0,
        "Instantaneous arousal change — E-layer",
        "Ehrlich 2019"),

    # === B+C-Layer: Decoded/Target Affect + Control (6 tuples) ===
    _h3(_ROUGHNESS, "roughness", 16, 0, 0,
        "1s valence baseline for affect decode",
        "Daly 2019"),
    _h3(_LOUDNESS, "loudness", 16, 0, 0,
        "1s integrated arousal for affect decode",
        "Daly 2019"),
    _h3(_LOUDNESS, "loudness", 12, 18, 0,
        "Arousal trajectory error for control",
        "Ehrlich 2019"),
    _h3(_ROUGHNESS, "roughness", 12, 18, 0,
        "Valence trajectory control signal",
        "Daly 2019"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 7, 8, 0,
        "Feedback signal rate for loop coherence",
        "Ehrlich 2019"),
    _h3(_SPECTRAL_CENTROID, "spectral_centroid", 16, 20, 0,
        "Brightness uncertainty for control output",
        "Miranda 2011"),

    # === P-Layer: Arousal Modulation + Valence Tracking (2 tuples) ===
    _h3(_LOUDNESS, "loudness", 7, 8, 0,
        "Arousal velocity — P-layer modulation",
        "Ehrlich 2019"),
    _h3(_VELOCITY_A, "velocity_A", 7, 8, 0,
        "Dynamic rate for arousal modulation",
        "Daly 2019"),

    # === F-Layer: Forecast (2 tuples) ===
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 12, 0, 0,
        "Hedonic state for target affect prediction",
        "Daly 2019"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 18, 0,
        "Feedback trend for modulation success forecast",
        "Ehrlich 2019"),
)

assert len(_CLAM_H3_DEMANDS) == 12


class CLAM(Encoder):
    """Closed-Loop Affective Modulation -- ARU Encoder (depth 1, 11D).

    Models closed-loop BCI affective modulation where EEG-decoded brain
    state drives real-time music generation to steer affect toward a
    therapeutic target. The loop continuously decodes the listener's
    affective state from frontal EEG (FC6 gamma), computes an error
    signal against the therapeutic target, and adjusts music parameters
    (tempo, mode, dynamics) to minimize the error.

    Ehrlich et al. 2019: BCI closed-loop, N=5, arousal tracking r=0.74,
    valence tracking r=0.52. Loop latency ~1s. 3/5 participants showed
    successful affect steering toward target states.

    Daly et al. 2019: Affective BCI using EEG, arousal and valence
    classification from frontal asymmetry and gamma power. Music features
    (tempo, mode, loudness) mapped to affective dimensions.

    Miranda 2011: Brain-computer music interface using EEG for real-time
    music parameter control. Spectral features drive generative music
    adaptation.

    Dependency chain:
        CLAM is an Encoder (Depth 1) -- reads SRP + AAC relay outputs.
        Computed after SRP and AAC in F5 pipeline.

    Downstream feeds:
        -> affective_control beliefs (Appraisal)
        -> TAR therapeutic assessment (Associator)
    """

    NAME = "CLAM"
    FULL_NAME = "Closed-Loop Affective Modulation"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("SRP", "AAC")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="ARU_SRP__ARU_CLAM__pleasure",
            name="SRP pleasure to CLAM affective loop",
            source_unit="ARU",
            source_model="SRP",
            source_dims=("pleasure",),
            target_unit="ARU",
            target_model="CLAM",
            correlation="r=0.74",
            citation="Ehrlich 2019",
        ),
        CrossUnitPathway(
            pathway_id="ARU_AAC__ARU_CLAM__arousal",
            name="AAC emotional arousal to CLAM affective decode",
            source_unit="ARU",
            source_model="AAC",
            source_dims=("emotional_arousal",),
            target_unit="ARU",
            target_model="CLAM",
            correlation="r=0.74",
            citation="Ehrlich 2019",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:affective_mod", "E1:loop_coherence"),
            scope="internal",
        ),
        LayerSpec(
            "B+C", "Temporal Integration", 2, 7,
            ("B0:decoded_affect", "B1:target_affect", "B2:affect_error",
             "C0:control_output", "C1:music_param_delta"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 7, 9,
            ("P0:arousal_modulation", "P1:valence_tracking"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:target_affect_pred", "F1:modulation_success"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _CLAM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:affective_mod", "E1:loop_coherence",
            "B0:decoded_affect", "B1:target_affect", "B2:affect_error",
            "C0:control_output", "C1:music_param_delta",
            "P0:arousal_modulation", "P1:valence_tracking",
            "F0:target_affect_pred", "F1:modulation_success",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Frontal Cortex (FC6) -- EEG gamma affect decode
            RegionLink("E0:affective_mod", "FC6", 0.80,
                       "Ehrlich 2019"),
            # vmPFC / OFC -- affective state integration
            RegionLink("B0:decoded_affect", "vmPFC", 0.75,
                       "Daly 2019"),
            RegionLink("P1:valence_tracking", "OFC", 0.70,
                       "Daly 2019"),
            # NAcc -- reward-system coupling for loop success
            RegionLink("F1:modulation_success", "NAcc", 0.75,
                       "Ehrlich 2019"),
            # Control output -- frontal executive control
            RegionLink("C0:control_output", "FC6", 0.70,
                       "Miranda 2011"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # CLAM modulates via BCI loop, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Ehrlich et al.", 2019,
                         "BCI closed-loop affective modulation: arousal "
                         "tracking r=0.74, valence tracking r=0.52. Loop "
                         "latency ~1s. 3/5 participants successful affect "
                         "steering toward target states",
                         "BCI, N=5"),
                Citation("Daly et al.", 2019,
                         "Affective BCI using EEG: arousal and valence "
                         "classification from frontal asymmetry and gamma "
                         "power. Music features mapped to affective "
                         "dimensions",
                         "EEG, affective BCI"),
                Citation("Miranda", 2011,
                         "Brain-computer music interface using EEG for "
                         "real-time music parameter control. Spectral "
                         "features drive generative music adaptation",
                         "review, BCI music"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "Arousal tracking (P0) must correlate with loudness "
                "dynamics (Ehrlich 2019: r=0.74 arousal tracking)",
                "Valence tracking (P1) must correlate with roughness "
                "and pleasantness (Ehrlich 2019: r=0.52 valence)",
                "Affect error (B2) must decrease over time when loop "
                "is coherent (Ehrlich 2019: 3/5 converge to target)",
                "Control output (C0) must be higher when affect error "
                "is large (closed-loop proportional control)",
                "Modulation success (F1) must predict reward coupling "
                "(NAcc activation when loop converges)",
                "Disrupting feedback (breaking the loop) should "
                "increase affect error and reduce modulation success",
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
        """Transform R3/H3 + SRP/AAC relay outputs into 11D closed-loop affect.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"SRP": (B, T, 19), "AAC": (B, T, 14)}``

        Returns:
            ``(B, T, 11)`` -- E(2) + B+C(5) + P(2) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(
            h3_features, r3_features, e, relay_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
