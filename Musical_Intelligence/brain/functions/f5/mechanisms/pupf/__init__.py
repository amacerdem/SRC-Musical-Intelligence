"""PUPF -- Pleasure-Uncertainty Prediction Function.

Encoder nucleus (depth 1) in ARU, Function F5. Models the Goldilocks
function: pleasure = f(uncertainty H, surprise S). Low H + high S = maximal
pleasure (certain context, surprising event). High H + high S = overwhelm.
Low H + low S = boredom. The H x S interaction drives amygdala and
hippocampus activation (Cheung 2019, d=3.8-4.16).

Reads: SRP (intra-circuit via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    spectral_flux:              [21]     (D, surprise signal -- S axis)
    distribution_entropy:       [22]     (D, Shannon entropy -- H axis)
    distribution_flatness:      [23]     (D, noise-level uncertainty)
    distribution_concentration: [24]     (D, spectral focus predictability)
    sensory_pleasantness:       [4]      (A, hedonic for pleasure function)
    harmonic_deviation:         [6]      (A, harmonic prediction accuracy)
    velocity_A:                 [8]      (B, tempo dynamics for temporal PE)
    roughness:                  [0]      (A, inverse pleasantness)
    loudness:                   [10]     (B, arousal level)
    onset_strength:             [11]     (B, event onset timing)
    x_l0l5:                     [25:33]  (F, energy-consonance surprise coupling)
    x_l4l5:                     [33:41]  (G, dynamics-consonance interaction)

Output structure: E(2) + U+G(5) + P(3) + F(2) = 12D
  E-layer   [0:2]   Extraction           (sigmoid)  scope=internal
  U+G-layer [2:7]   Temporal Integration (sigmoid)  scope=internal
  P-layer   [7:10]  Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [10:12] Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/pupf/
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
    12: "525ms (half-beat)",
    15: "800ms (phrase-sub)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 2: "std", 8: "velocity",
    18: "trend", 20: "entropy",
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
_SPECTRAL_FLUX = 21
_DIST_ENTROPY = 22
_DIST_FLATNESS = 23
_DIST_CONCENTRATION = 24
_SENSORY_PLEASANTNESS = 4
_HARMONIC_DEVIATION = 6
_VELOCITY_A = 8
_ROUGHNESS = 0
_LOUDNESS = 10
_ONSET_STRENGTH = 11


# -- 21 H3 Demand Specifications -----------------------------------------------
# Pleasure-uncertainty prediction function requires entropy (H axis), surprise
# (S axis), H x S interaction, hedonic signals, and temporal PE signals.
# All L0 (memory/backward).

_PUPF_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Prediction Error + Uncertainty (6 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 20, 0,
        "1s entropy of spectral change",
        "Cheung 2019"),
    _h3(_DIST_ENTROPY, "distribution_entropy", 16, 20, 0,
        "1s Shannon entropy",
        "Cheung 2019"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 7, 8, 0,
        "Instantaneous surprise rate",
        "Gold 2019"),
    _h3(_DIST_ENTROPY, "distribution_entropy", 7, 8, 0,
        "Uncertainty change rate",
        "Cheung 2019"),
    _h3(_DIST_ENTROPY, "distribution_entropy", 16, 20, 0,
        "Integrated entropy for H axis",
        "Cheung 2019"),
    _h3(_ONSET_STRENGTH, "onset_strength", 7, 8, 0,
        "Beat onset rate",
        "Gold 2019"),

    # === U+G Layer: Entropy, Surprise, Interaction, Pleasure (9 tuples) ===
    _h3(_DIST_ENTROPY, "distribution_entropy", 12, 18, 0,
        "Entropy trajectory 525ms",
        "Cheung 2019"),
    _h3(_DIST_ENTROPY, "distribution_entropy", 15, 2, 0,
        "Entropy variability 800ms",
        "Cheung 2019"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 12, 8, 0,
        "Surprise rate half-beat",
        "Gold 2019"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 15, 8, 0,
        "Surprise rate 800ms",
        "Cheung 2019"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 18, 0,
        "Surprise trajectory 1s",
        "Cheung 2019"),
    _h3(_HARMONIC_DEVIATION, "harmonic_deviation", 12, 8, 0,
        "Harmonic PE rate",
        "Koelsch 2014"),
    _h3(_HARMONIC_DEVIATION, "harmonic_deviation", 16, 2, 0,
        "Harmonic uncertainty 1s",
        "Koelsch 2014"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 0, 0,
        "Hedonic baseline",
        "Salimpoor 2011"),
    _h3(_VELOCITY_A, "velocity_A", 12, 8, 0,
        "Tempo dynamics half-beat",
        "Cheung 2019"),

    # === P-Layer: Surprise-Pleasure Coupling (2 tuples) ===
    _h3(_VELOCITY_A, "velocity_A", 16, 18, 0,
        "Tempo trend 1s",
        "Koelsch 2014"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 12, 18, 0,
        "Hedonic trajectory",
        "Salimpoor 2011"),

    # === F-Layer: Forecast Trajectories (4 tuples) ===
    _h3(_DIST_ENTROPY, "distribution_entropy", 12, 18, 0,
        "Entropy trajectory (F-layer forecast)",
        "Cheung 2019"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 12, 18, 0,
        "Surprise trajectory (F-layer forecast)",
        "Cheung 2019"),
    _h3(_DIST_ENTROPY, "distribution_entropy", 15, 18, 0,
        "Longer entropy trend",
        "Cheung 2019"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 15, 18, 0,
        "Hedonic trajectory (F-layer forecast)",
        "Salimpoor 2011"),
)

assert len(_PUPF_H3_DEMANDS) == 21


class PUPF(Encoder):
    """Pleasure-Uncertainty Prediction Function -- ARU Encoder (depth 1, 12D).

    Models the Goldilocks function: pleasure = f(uncertainty H, surprise S).
    Low H + high S = maximal pleasure (certain context, surprising event).
    High H + high S = overwhelm (too uncertain to enjoy surprise).
    Low H + low S = boredom (predictable and unsurprising).

    The H x S interaction (not H or S alone) drives amygdala and hippocampus
    activation with large effect sizes (Cheung 2019, d=3.8-4.16). PUPF
    computes the Goldilocks zone and surprise-pleasure coupling that feeds
    into SRP wanting/liking modulation.

    Cheung et al. 2019: Uncertainty and surprise jointly determine music-
    evoked brain responses in amygdala, hippocampus, and auditory cortex
    (fMRI, N=39, d=3.8-4.16 for H x S interaction).

    Gold et al. 2019: Predictability and surprise jointly modulate auditory
    cortical processing and aesthetic pleasure (fMRI, N=40).

    Salimpoor et al. 2011: Anatomically distinct dopamine release during
    anticipation and experience of peak emotion to music (PET,
    [11C]raclopride, N=8).

    Koelsch 2014: Brain correlates of music-evoked emotions -- tension,
    surprise, and resolution drive fronto-insular and striatal responses
    (review of multiple studies).

    Dependency chain:
        PUPF is an Encoder (Depth 1) -- reads SRP relay output (F5 intra-circuit).
        Computed after SRP in F5 pipeline.

    Downstream feeds:
        -> prediction_pleasure belief (Core, tau=0.35)
        -> surprise_valence belief (Appraisal)
        -> SRP wanting/liking modulation via goldilocks_zone
    """

    NAME = "PUPF"
    FULL_NAME = "Pleasure-Uncertainty Prediction Function"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 12
    UPSTREAM_READS = ("SRP",)
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="ARU_SRP__ARU_PUPF__prediction_error",
            name="SRP prediction error to PUPF surprise axis",
            source_unit="ARU",
            source_model="SRP",
            source_dims=("prediction_error",),
            target_unit="ARU",
            target_model="PUPF",
            correlation="r=0.72",
            citation="Cheung 2019",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 2,
            ("E0:prediction_err", "E1:uncertainty"),
            scope="internal",
        ),
        LayerSpec(
            "U+G", "Temporal Integration", 2, 7,
            ("U0:entropy_H", "U1:surprise_S", "U2:HS_interaction",
             "G0:pleasure_P", "G1:goldilocks_zone"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 7, 10,
            ("P0:surprise_pleasure", "P1:affective_outcome",
             "P2:tempo_pred_error"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 10, 12,
            ("F0:next_event_prob", "F1:pleasure_forecast"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PUPF_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:prediction_err", "E1:uncertainty",
            "U0:entropy_H", "U1:surprise_S", "U2:HS_interaction",
            "G0:pleasure_P", "G1:goldilocks_zone",
            "P0:surprise_pleasure", "P1:affective_outcome",
            "P2:tempo_pred_error",
            "F0:next_event_prob", "F1:pleasure_forecast",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Amygdala -- H x S interaction, prediction error processing
            RegionLink("U2:HS_interaction", "amygdala", 0.85,
                       "Cheung 2019"),
            # Hippocampus -- H x S interaction, memory updating
            RegionLink("U2:HS_interaction", "hippocampus", 0.80,
                       "Cheung 2019"),
            # Auditory Cortex -- H x S interaction, predictive coding
            RegionLink("E0:prediction_err", "AC", 0.75,
                       "Cheung 2019"),
            # Striatum (NAcc) -- surprise-pleasure coupling
            RegionLink("P0:surprise_pleasure", "NAcc", 0.80,
                       "Salimpoor 2011"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- pleasure signal from Goldilocks zone
            NeuroLink("G0:pleasure_P", "dopamine", 0.75,
                      "Salimpoor 2011"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Cheung et al.", 2019,
                         "Uncertainty and surprise jointly determine music-"
                         "evoked brain responses in amygdala, hippocampus, "
                         "and auditory cortex; H x S interaction d=3.8-4.16",
                         "fMRI, N=39"),
                Citation("Gold et al.", 2019,
                         "Predictability and surprise jointly modulate "
                         "auditory cortical processing and aesthetic pleasure",
                         "fMRI, N=40"),
                Citation("Salimpoor et al.", 2011,
                         "Anatomically distinct dopamine release during "
                         "anticipation (caudate) and experience (NAcc) of "
                         "peak emotion to music",
                         "PET, [11C]raclopride, N=8"),
                Citation("Koelsch", 2014,
                         "Brain correlates of music-evoked emotions: tension, "
                         "surprise, and resolution drive fronto-insular and "
                         "striatal responses",
                         "review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "H x S interaction (U2) must be higher than H or S alone "
                "for predicting amygdala activation (Cheung 2019: d=3.8-4.16 "
                "for interaction vs d<1 for main effects)",
                "Goldilocks zone (G1) must peak when entropy is low and "
                "surprise is high (certain context + surprising event)",
                "Pleasure (G0) must show inverted-U relationship with surprise "
                "when entropy is held constant (Gold 2019)",
                "High entropy + high surprise should produce low pleasure "
                "(overwhelm), not high pleasure",
                "Low entropy + low surprise should produce low pleasure "
                "(boredom), not high pleasure",
                "Disrupting the H x S interaction should reduce amygdala "
                "and hippocampus activation (testable via entropy-matched "
                "surprise manipulation)",
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
        """Transform R3/H3 + SRP relay output into 12D pleasure-uncertainty.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"SRP": (B, T, 19)}``

        Returns:
            ``(B, T, 12)`` -- E(2) + U+G(5) + P(3) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(
            h3_features, r3_features, e, relay_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
