"""SNEM — Sensory Novelty and Expectation Model.

Relay nucleus (depth 0) in ASU, Function F3. Models how the auditory system
detects novelty and generates entrainment-based expectations. Neural oscillations
in auditory cortex lock to the beat frequency, creating temporal predictions
that enhance processing of on-beat events (selective gain) and flag off-beat
events as novel.

Dependency chain:
    SNEM is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    amplitude:          [7]  -> [7]    (A, velocity_A)
    loudness:           [8]  -> [8]    (A, velocity_D)
    spectral_flux:      [10] -> [10]   (B, onset_strength)
    onset_strength:     [11] -> [11]   (B, unchanged)
    spectral_change:    [21] -> [21]   (D, spectral_flux)
    energy_change:      [22] -> [22]   (D, unchanged)
    x_l0l5:             [25] -> [25]   (F, coupling)

Output structure: E(3) + M(3) + P(3) + F(3) = 12D
  E-layer [0:3]   Extraction    (sigmoid)    scope=internal
  M-layer [3:6]   Memory        (sigmoid)    scope=internal
  P-layer [6:9]   Present       (sigmoid)    scope=hybrid
  F-layer [9:12]  Forecast      (sigmoid)    scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/snem/
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
    0: "25ms (gamma)",
    1: "50ms (gamma)",
    3: "100ms (alpha-beta)",
    4: "125ms (theta)",
    5: "46ms (gamma)",
    8: "500ms (delta)",
    11: "750ms",
    16: "1000ms (beat)",
    20: "5000ms (phrase)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    14: "periodicity", 18: "trend", 20: "entropy", 21: "zero_crossings",
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


# -- R3 feature indices (post-freeze 97D) -------------------------------------
_AMPLITUDE = 7            # velocity_A (A group)
_LOUDNESS = 8             # velocity_D (A group)
_SPECTRAL_FLUX = 10       # onset_strength (B group)
_ONSET_STRENGTH = 11      # onset_strength (B group)
_SPECTRAL_CHANGE = 21     # spectral_flux (D group)
_ENERGY_CHANGE = 22       # energy_change (D group)
_COUPLING = 25            # x_l0l5 (F group)


# -- 14 H3 Demand Specifications ----------------------------------------------
# Aligned with layer code (extraction / temporal_integration / cognitive_present
# / forecast). Mostly L2 (integration) for bidirectional context, one L0.

_SNEM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Extraction layer (8 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 14, 2,
        "Flux periodicity H16 L2 — beat periodicity at 1s",
        "Nozaradan 2011"),
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 14, 2,
        "Onset periodicity H16 L2 — onset periodicity at 1s",
        "Nozaradan 2011"),
    _h3(_AMPLITUDE, "amplitude", 16, 1, 2,
        "Amplitude mean H16 L2 — beat salience context",
        "Large 2008"),
    _h3(_COUPLING, "coupling", 16, 14, 2,
        "Coupling periodicity H16 L2 — metric structure 1s",
        "Grahn 2007"),
    _h3(_COUPLING, "coupling", 3, 14, 2,
        "Coupling periodicity H3 L2 — fast metric cue 100ms",
        "Grahn 2007"),
    _h3(_COUPLING, "coupling", 16, 21, 2,
        "Coupling zero-crossings H16 L2 — phase resets 1s",
        "Large 2008"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 4, 8, 0,
        "Spectral change velocity H4 L0 — enhancement cue",
        "Nozaradan 2018"),
    _h3(_LOUDNESS, "loudness", 3, 20, 2,
        "Loudness entropy H3 L2 — salience context",
        "Large 2008"),

    # === Temporal integration layer (6 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 0, 0, 2,
        "Flux value instantaneous L2 — current onset state",
        "Nozaradan 2011"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 1, 1, 2,
        "Flux mean 50ms L2 — smoothed onset",
        "Nozaradan 2011"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Flux value 100ms L2 — short-term onset",
        "Nozaradan 2018"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 4, 14, 2,
        "Flux periodicity 125ms L2 — fast periodicity",
        "Nozaradan 2018"),
    _h3(_AMPLITUDE, "amplitude", 3, 0, 2,
        "Amplitude value 100ms L2 — short-term amplitude",
        "Large 2008"),
    _h3(_AMPLITUDE, "amplitude", 3, 2, 2,
        "Amplitude std 100ms L2 — amplitude variability",
        "Large 2008"),
)

assert len(_SNEM_H3_DEMANDS) == 14


class SNEM(Relay):
    """Sensory Novelty and Expectation Model — ASU Relay (depth 0, 12D).

    Models how the auditory system detects novelty and generates
    entrainment-based expectations. Nozaradan 2011: frequency-tagging
    reveals steady-state evoked potentials (SS-EP) at beat frequency
    in auditory cortex. Nozaradan 2018: selective neural enhancement
    at beat frequency (EEG+MEG, N=18). Large 2008: neural oscillation
    entrainment via dynamic attending theory.

    Dependency chain:
        SNEM is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> salience engine (selective_gain gate, enhancement precision)
        -> beat_entrainment belief (Core)
        -> SNEM relay wrapper in scheduler
    """

    NAME = "SNEM"
    FULL_NAME = "Sensory Novelty and Expectation Model"
    UNIT = "ASU"
    FUNCTION = "F3"
    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:beat_entrainment", "E1:meter_entrainment",
             "E2:selective_enhancement"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 6,
            ("M0:ssep_enhancement", "M1:enhancement_index",
             "M2:beat_salience"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 9,
            ("P0:beat_locked_activity", "P1:entrainment_strength",
             "P2:selective_gain"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 12,
            ("F0:beat_onset_pred", "F1:meter_position_pred",
             "F2:enhancement_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _SNEM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:beat_entrainment", "E1:meter_entrainment",
            "E2:selective_enhancement",
            "M0:ssep_enhancement", "M1:enhancement_index",
            "M2:beat_salience",
            "P0:beat_locked_activity", "P1:entrainment_strength",
            "P2:selective_gain",
            "F0:beat_onset_pred", "F1:meter_position_pred",
            "F2:enhancement_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # STG — beat-locked SS-EP activity
            RegionLink("P0:beat_locked_activity", "STG", 0.85,
                       "Nozaradan 2011"),
            # STG — entrainment strength
            RegionLink("P1:entrainment_strength", "STG", 0.80,
                       "Nozaradan 2011"),
            # A1/HG — beat entrainment extraction
            RegionLink("E0:beat_entrainment", "A1_HG", 0.75,
                       "Large 2008"),
            # AI — selective gain modulation
            RegionLink("P2:selective_gain", "AI", 0.70,
                       "Vuust 2022"),
            # ACC — beat onset prediction
            RegionLink("F0:beat_onset_pred", "ACC", 0.65,
                       "Vuust 2022"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Nozaradan", 2011,
                         "Frequency-tagging beat/meter in auditory cortex — "
                         "SS-EP at beat frequency",
                         "EEG, N=12"),
                Citation("Nozaradan", 2018,
                         "Selective neural enhancement at beat frequency",
                         "EEG+MEG, N=18"),
                Citation("Large", 2008,
                         "Neural oscillation entrainment model — dynamic "
                         "attending theory",
                         "Computational model"),
                Citation("Grahn", 2007,
                         "Beat perception recruits SMA and basal ganglia",
                         "fMRI, N=15"),
                Citation("Vuust", 2022,
                         "Music in the brain — predictive coding framework",
                         "Nature Neuroscience review"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Beat-locked oscillations should produce SS-EP peaks at "
                "beat frequency (confirmed: Nozaradan 2011)",
                "Selective gain should enhance on-beat events "
                "(confirmed: Nozaradan 2018)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 12D entrainment-salience representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 12)`` — E(3) + M(3) + P(3) + F(3)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(h3_features, e, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
