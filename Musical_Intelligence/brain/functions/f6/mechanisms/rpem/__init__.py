"""RPEM -- Reward Prediction Error in Music.

Relay nucleus (depth 0) in RPU, Function F6. Models the reward prediction
error (RPE) crossover interaction in the ventral striatum discovered by
Gold et al. (2023): Surprise x Liked = VS activation (positive RPE),
Surprise x Disliked = VS deactivation (negative RPE). The unsigned RPE
magnitude drives attention and learning regardless of valence.

Dependency chain:
    RPEM is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:              [0]    (A, roughness)
    sensory_pleasantness:   [4]    (A, sensory_pleasantness)
    loudness:               [8]    (B, velocity_D)
    onset_strength:         [10]   (B, onset_strength)
    spectral_change:        [21]   (D, spectral_flux)
    concentration_change:   [24]   (D, concentration_change)
    x_l0l5:                 [25:33] (F, coupling)
    x_l4l5:                 [33:41] (F, coupling)

Output structure: E(4) + M(2) + P(2) = 8D  (NO F-layer)
  E-layer [0:4]   Extraction          (sigmoid)             scope=internal
  M-layer [4:6]   Temporal Integration (max/clamp -- SPECIAL) scope=internal
  P-layer [6:8]   Cognitive Present   (clamp+sigmoid)       scope=hybrid

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/rpem/
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
from .temporal_integration import compute_temporal_integration

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    3: "100ms (gamma)",
    4: "125ms (theta)",
    8: "500ms (sub-beat)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity", 20: "entropy",
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
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 8                    # velocity_D
_ONSET_STRENGTH = 10             # spectral_flux -> onset_strength
_SPECTRAL_CHANGE = 21            # spectral_flux -> spectral_change
_CONCENTRATION_CHANGE = 24
_X_L0L5_START = 25               # F group (coupling)
_X_L4L5_START = 33               # F group (coupling)


# -- 15 H3 Demand Specifications (E:8 + M:5 + P:2) ----------------------------

_RPEM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Extraction (tuples 0-7) ===

    # #0: Spectral entropy at 125ms -- prediction uncertainty
    _h3(_SPECTRAL_CHANGE, "spectral_change", 4, 20, 0,
        "Spectral entropy at 125ms -- prediction uncertainty",
        "Gold 2023"),
    # #1: Spectral change at 100ms -- instantaneous surprise
    _h3(_SPECTRAL_CHANGE, "spectral_change", 3, 0, 2,
        "Spectral change at 100ms -- instantaneous surprise",
        "Gold 2023"),
    # #2: Concentration change at 100ms -- uncertainty signal
    _h3(_CONCENTRATION_CHANGE, "concentration_change", 3, 0, 2,
        "Concentration change at 100ms -- uncertainty signal",
        "Gold 2023"),
    # #3: Mean pleasantness over 1s -- sustained liking
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 1, 2,
        "Mean pleasantness over 1s -- sustained liking",
        "Gold 2023"),
    # #4: Roughness at 100ms -- instantaneous dissonance
    _h3(_ROUGHNESS, "roughness", 3, 0, 2,
        "Roughness at 100ms -- instantaneous dissonance",
        "Gold 2023"),
    # #5: Roughness velocity at 100ms -- tension rate for negative RPE
    _h3(_ROUGHNESS, "roughness", 3, 8, 0,
        "Roughness velocity at 100ms -- tension rate for negative RPE",
        "Gold 2023"),
    # #6: RPE coupling at 100ms -- cross-domain RPE signal
    _h3(_X_L4L5_START, "x_l4l5[0]", 3, 0, 2,
        "RPE coupling at 100ms -- cross-domain RPE signal",
        "Gold 2023"),
    # #7: Prediction entropy at 1s -- model uncertainty
    _h3(_X_L0L5_START, "x_l0l5[0]", 16, 20, 2,
        "Prediction entropy at 1s -- model uncertainty",
        "Cheung 2019"),

    # === M-layer: Temporal Integration (tuples 8-12) ===

    # #8: Spectral velocity at 500ms -- surprise dynamics
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 8, 0,
        "Spectral velocity at 500ms -- surprise dynamics",
        "Gold 2023"),
    # #9: Onset at 100ms -- event boundary detection
    _h3(_ONSET_STRENGTH, "onset_strength", 3, 0, 2,
        "Onset at 100ms -- event boundary detection",
        "Gold 2023"),
    # #10: Onset at 125ms -- event boundary (theta band)
    _h3(_ONSET_STRENGTH, "onset_strength", 4, 0, 2,
        "Onset at 125ms -- event boundary (theta band)",
        "Gold 2023"),
    # #11: Onset variability at 500ms -- event regularity
    _h3(_ONSET_STRENGTH, "onset_strength", 8, 2, 2,
        "Onset variability at 500ms -- event regularity",
        "Gold 2023"),
    # #12: Loudness at 100ms -- salience weighting
    _h3(_LOUDNESS, "loudness", 3, 0, 2,
        "Loudness at 100ms -- salience weighting",
        "Gold 2023"),

    # === P-layer: Cognitive Present (tuples 13-14) ===

    # #13: RPE coupling velocity at 500ms -- RPE dynamics
    _h3(_X_L4L5_START, "x_l4l5[0]", 8, 8, 0,
        "RPE coupling velocity at 500ms -- RPE dynamics",
        "Gold 2023"),
    # #14: Prediction mean at 500ms -- expected reward baseline
    _h3(_X_L0L5_START, "x_l0l5[0]", 8, 1, 2,
        "Prediction mean at 500ms -- expected reward baseline",
        "Cheung 2019"),
)

assert len(_RPEM_H3_DEMANDS) == 15


class RPEM(Relay):
    """Reward Prediction Error in Music -- RPU Relay (depth 0, 8D).

    Models the reward prediction error crossover interaction in the ventral
    striatum. Gold 2023: Surprise x Liked = VS activation (positive RPE,
    d = 1.07); Surprise x Disliked = VS deactivation (negative RPE).
    Cheung 2019: uncertainty x surprise jointly determine musical pleasure.

    SPECIAL: M-layer uses torch.max and torch.clamp instead of sigmoid.
      - rpe_magnitude = max(positive_rpe, negative_rpe)
      - vs_response = clamp(positive_rpe - negative_rpe + 0.5, 0, 1)

    Dependency chain:
        RPEM is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> current_rpe for reward learning signal
        -> vs_activation_state for salience and precision
        -> Cross-relay interaction with DAED (RPE modulates anticipatory DA)
        -> Precision engine (RPE magnitude modulates pi_obs)
    """

    NAME = "RPEM"
    FULL_NAME = "Reward Prediction Error in Music"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 8

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:surprise_signal", "f02:liking_signal",
             "f03:positive_rpe", "f04:negative_rpe"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 4, 6,
            ("rpe_magnitude", "vs_response"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 8,
            ("current_rpe", "vs_activation_state"),
            scope="hybrid",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _RPEM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:surprise_signal", "f02:liking_signal",
            "f03:positive_rpe", "f04:negative_rpe",
            "rpe_magnitude", "vs_response",
            "current_rpe", "vs_activation_state",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # VS (ventral striatum / NAcc) -- RPE crossover locus
            RegionLink("vs_response", "NAcc", 0.90,
                       "Gold 2023"),
            # STG -- surprise signal source
            RegionLink("f01:surprise_signal", "STG", 0.85,
                       "Gold 2023"),
            # VTA -- dopaminergic source for RPE
            RegionLink("vs_activation_state", "VTA", 0.80,
                       "Salimpoor 2011"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- RPE is a dopaminergic signal
            NeuroLink("current_rpe", "dopamine", 0.90,
                      "Gold 2023"),
            NeuroLink("rpe_magnitude", "dopamine", 0.85,
                      "Salimpoor 2011"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Gold", 2023,
                         "VS shows surprise x liking crossover interaction "
                         "for reward prediction error in music",
                         "fMRI, d = 1.07 positive RPE, d = 1.22 surprise"),
                Citation("Cheung", 2019,
                         "Uncertainty and surprise jointly determine musical "
                         "pleasure (Goldilocks effect)",
                         "behavioral + computational, N=39+38"),
                Citation("Salimpoor", 2011,
                         "Caudate DA ramps before peak; NAcc DA bursts at "
                         "peak; PET [11C]raclopride",
                         "PET, N=8, r=0.71 caudate, r=0.84 NAcc"),
                Citation("Salimpoor", 2013,
                         "STG-to-NAcc structural connectivity predicts "
                         "individual reward sensitivity",
                         "DTI + fMRI, N=19"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.92),
            falsification_criteria=(
                "VS BOLD must show surprise x liking crossover interaction "
                "(Gold 2023: d = 1.07 for positive RPE in VS)",
                "Pharmacological blockade of DA should abolish RPE signal "
                "(Ferreri 2019: risperidone diminishes music reward)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 8D reward prediction error representation.

        Delegates to 3 layer functions (extraction -> temporal_integration
        -> cognitive_present) and stacks results. No F-layer.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 8)`` -- E(4) + M(2) + P(2)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)

        output = torch.stack([*e, *m, *p], dim=-1)
        return output.clamp(0.0, 1.0)
