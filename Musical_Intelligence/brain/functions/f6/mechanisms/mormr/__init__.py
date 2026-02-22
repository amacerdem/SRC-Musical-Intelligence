"""MORMR -- mu-Opioid Receptor Music Reward.

Relay nucleus (depth 0) in RPU, Function F6. Models the endogenous mu-opioid
receptor system mediating hedonic impact during music listening. Based on
Putkinen et al. (2025) PET evidence showing [11C]carfentanil binding changes
in VS, OFC, amygdala, thalamus, and temporal pole during pleasant music.

MORMR is the only F6 relay with an F-layer (forecast). The F-layer reuses
E/M/P outputs and requires 0 new H3 tuples.

Dependency chain:
    MORMR is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:              [0]    (A, roughness)
    sensory_pleasantness:   [4]    (A, sensory_pleasantness)
    amplitude:              [7]    (B, velocity_A)
    loudness:               [8]    (B, velocity_D)
    warmth:                 [12]   (C, warmth)
    brightness:             [13]   (C, brightness_kuttruff)
    energy_change:          [22]   (D, distribution_entropy)
    x_l4l5:                 [33:41] (F, coupling)
    x_l5l7:                 [41:49] (F, coupling)

Output structure: E(4) + M(1) + P(1) + F(1) = 7D
  E-layer [0:4]  Extraction          (sigmoid)    scope=internal
  M-layer [4:5]  Temporal Integration (sigmoid)    scope=internal
  P-layer [5:6]  Present             (sigmoid)    scope=hybrid
  F-layer [6:7]  Forecast            (sigmoid)    scope=external

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/mormr/
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
    3: "100ms (instant)",
    8: "500ms (sub-beat)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity", 18: "trend", 20: "entropy",
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
_ROUGHNESS = 0                   # A group
_SENSORY_PLEASANTNESS = 4        # A group
_AMPLITUDE = 7                   # B group (velocity_A)
_LOUDNESS = 8                    # B group (velocity_D)
_WARMTH = 12                     # C group
_BRIGHTNESS = 13                 # C group (brightness_kuttruff)
_ENERGY_CHANGE = 22              # D group (distribution_entropy)
_X_L4L5_START = 33               # F group (coupling)
_X_L5L7_START = 41               # F group (coupling)


# -- 15 H3 Demand Specifications (E:7 + M:5 + P:3 + F:0) ---------------------

_MORMR_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Extraction (tuples 0-6) ===

    # #0: Mean pleasantness over 1s -- primary hedonic signal
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 1, 2,
        "Mean pleasantness over 1s -- primary hedonic signal",
        "Putkinen 2025"),
    # #1: Mean roughness over 1s -- consonance context (inverted)
    _h3(_ROUGHNESS, "roughness", 16, 1, 2,
        "Mean roughness over 1s -- consonance context (inverted)",
        "Putkinen 2025"),
    # #2: Mean warmth at 500ms -- timbral richness
    _h3(_WARMTH, "warmth", 8, 1, 2,
        "Mean warmth at 500ms -- timbral richness",
        "Putkinen 2025"),
    # #3: Amplitude at 500ms -- peak magnitude for chills
    _h3(_AMPLITUDE, "amplitude", 8, 0, 2,
        "Amplitude at 500ms -- peak magnitude for chills",
        "Putkinen 2025"),
    # #4: Beauty coupling at 500ms -- aesthetic quality
    _h3(_X_L5L7_START, "x_l5l7[0]", 8, 0, 2,
        "Beauty coupling at 500ms -- aesthetic quality",
        "Putkinen 2025"),
    # #5: Pleasantness velocity over 1s -- hedonic change rate
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 8, 0,
        "Pleasantness velocity over 1s -- hedonic change rate",
        "Putkinen 2025"),
    # #6: Beauty entropy at 1s -- aesthetic complexity
    _h3(_X_L5L7_START, "x_l5l7[0]", 16, 20, 2,
        "Beauty entropy at 1s -- aesthetic complexity",
        "Putkinen 2025"),

    # === M-layer: Temporal Integration (tuples 7-11) ===

    # #7: Loudness at 100ms -- instantaneous intensity
    _h3(_LOUDNESS, "loudness", 3, 0, 2,
        "Loudness at 100ms -- instantaneous intensity",
        "Putkinen 2025"),
    # #8: Mean loudness at 500ms -- medium-term intensity
    _h3(_LOUDNESS, "loudness", 8, 1, 2,
        "Mean loudness at 500ms -- medium-term intensity",
        "Putkinen 2025"),
    # #9: Mean loudness at 1s -- sustained intensity context
    _h3(_LOUDNESS, "loudness", 16, 1, 2,
        "Mean loudness at 1s -- sustained intensity context",
        "Putkinen 2025"),
    # #10: Roughness at 100ms -- instantaneous consonance
    _h3(_ROUGHNESS, "roughness", 3, 0, 2,
        "Roughness at 100ms -- instantaneous consonance",
        "Putkinen 2025"),
    # #11: Pleasantness at 100ms -- instantaneous hedonic
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 3, 0, 2,
        "Pleasantness at 100ms -- instantaneous hedonic",
        "Putkinen 2025"),

    # === P-layer: Cognitive Present (tuples 12-14) ===

    # #12: Energy velocity at 500ms -- dynamic modulation rate
    _h3(_ENERGY_CHANGE, "energy_change", 8, 8, 0,
        "Energy velocity at 500ms -- dynamic modulation rate",
        "Putkinen 2025"),
    # #13: Sustained pleasure mean at 500ms -- opioid persistence
    _h3(_X_L4L5_START, "x_l4l5[0]", 8, 1, 2,
        "Sustained pleasure mean at 500ms -- opioid persistence",
        "Putkinen 2025"),
    # #14: Pleasure trend over 1s -- hedonic trajectory
    _h3(_X_L4L5_START, "x_l4l5[0]", 16, 18, 0,
        "Pleasure trend over 1s -- hedonic trajectory",
        "Putkinen 2025"),

    # === F-layer: Forecast -- 0 new H3 tuples (reuses E/M/P) ===
)

assert len(_MORMR_H3_DEMANDS) == 15


class MORMR(Relay):
    """mu-Opioid Receptor Music Reward -- RPU Relay (depth 0, 7D).

    Models the endogenous mu-opioid receptor system mediating hedonic impact
    during music listening. Putkinen 2025: [11C]carfentanil PET shows
    music-induced opioid release in VS, OFC, amygdala (d = 4.8, N = 15).
    Chills count correlates with NAcc BPND (r = -0.52). Baseline MOR tone
    modulates pleasure-BOLD coupling (d = 1.16).

    Dependency chain:
        MORMR is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> opioid_release/chills_count for kernel scheduler
        -> F6 Reward: hedonic opioid contribution
        -> Cross-relay interaction with DAED (dopamine + opioid convergence)
        -> ARU pleasure/arousal signals
        -> Precision engine: chills_onset_pred
    """

    NAME = "MORMR"
    FULL_NAME = "mu-Opioid Receptor Music Reward"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 7

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:opioid_release", "f02:chills_count",
             "f03:nacc_binding", "f04:reward_sensitivity"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 4, 5,
            ("opioid_tone",),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 6,
            ("current_opioid_state",),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 6, 7,
            ("chills_onset_pred",),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MORMR_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:opioid_release", "f02:chills_count",
            "f03:nacc_binding", "f04:reward_sensitivity",
            "opioid_tone",
            "current_opioid_state",
            "chills_onset_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # VS (ventral striatum / NAcc) -- primary opioid release site
            RegionLink("f01:opioid_release", "NAcc", 0.90,
                       "Putkinen 2025"),
            # OFC -- opioid-mediated hedonic evaluation
            RegionLink("f01:opioid_release", "OFC", 0.85,
                       "Putkinen 2025"),
            # Amygdala -- emotional opioid response
            RegionLink("f02:chills_count", "Amygdala", 0.80,
                       "Putkinen 2025"),
            # NAcc hedonic hotspot -- specific MOR binding
            RegionLink("f03:nacc_binding", "NAcc", 0.90,
                       "Putkinen 2025"),
            # Thalamus -- opioid relay
            RegionLink("current_opioid_state", "Thalamus", 0.75,
                       "Putkinen 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Endorphin (mu-opioid) -- primary neuromodulator
            NeuroLink("f01:opioid_release", "endorphin", 0.95,
                      "Putkinen 2025"),
            # Endorphin -- chills-related opioid burst
            NeuroLink("f02:chills_count", "endorphin", 0.85,
                      "Mallik 2017"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Putkinen", 2025,
                         "[11C]carfentanil PET shows music-induced opioid "
                         "release in VS, OFC, amygdala; chills correlate "
                         "with NAcc BPND",
                         "PET [11C]carfentanil, N=15, d=4.8"),
                Citation("Mallik", 2017,
                         "Naltrexone blocks music-evoked pleasure; mu-opioid "
                         "system mediates hedonic impact",
                         "double-blind crossover, N=15"),
                Citation("Mas-Herrero", 2014,
                         "Musical anhedonia dissociates from monetary reward; "
                         "specific opioid-hedonic circuitry",
                         "behavioral + questionnaire, N=30"),
                Citation("Salimpoor", 2011,
                         "Caudate DA ramps before peak; NAcc DA bursts at "
                         "peak -- anticipatory vs consummatory",
                         "PET [11C]raclopride, N=8"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.92),
            falsification_criteria=(
                "Music-induced mu-opioid release requires intact opioid "
                "circuitry (Putkinen 2025: PET [11C]carfentanil d=4.8)",
                "Pharmacological blockade of opioid system (naltrexone) "
                "eliminates music-evoked pleasure (Mallik 2017: N=15)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 7D mu-opioid receptor reward representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 7)`` -- E(4) + M(1) + P(1) + F(1)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
