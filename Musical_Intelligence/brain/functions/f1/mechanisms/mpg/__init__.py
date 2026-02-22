"""MPG — Melodic Processing Gradient.

Relay nucleus (depth 0) in NDU, Function F1. Transforms raw R³ spectral
features and H³ temporal morphologies into a 10D posterior-to-anterior
cortical gradient representation for melodic processing.

Dependency chain:
    MPG is a Relay (Depth 0) — reads R³/H³ directly, no upstream dependencies.
    Runs in parallel with BCH at Phase 0a of the kernel scheduler.

R³ Ontology Mapping (v1 → 97D freeze):
    spectral_flux: [10] → [21]   (Group B→D)
    loudness:      [8]  → [10]   (shifted within B)
    brightness:    [13] → [13]   (renamed to "sharpness")
    pitch_change:  [23] → DISSOLVED → pitch_height [37] replacement
    x_l0l5:        [25:33] → DISSOLVED → beat_strength [42] replacement
    x_l4l5:        [33:41] → DISSOLVED → pitch_salience [39] replacement
    amplitude:     [7]  → [7]    (unchanged)
    onset_strength:[11] → [11]   (unchanged)

Output structure: E(4) + M(3) + P(2) + F(1) = 10D
  E-layer [0:4]   Extraction    (sigmoid activation)      scope=internal
  M-layer [4:7]   Memory        (gradient dynamics)        scope=internal
  P-layer [7:9]   Present       (relay outputs)            scope=hybrid
  F-layer [9:10]  Forecast      (phrase boundary)          scope=external

See Building/C³-Brain/F1-Sensory-Processing/mechanisms/mpg/MPG-*.md
See Docs/C³/Models/NDU-α1-MPG/MPG.md (original model specification)
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

# ── Horizon labels ────────────────────────────────────────────────────
_H_LABELS = {
    0: "5.8ms (instant)",
    1: "12ms (gamma)",
    3: "23ms (onset)",
    4: "57ms (theta)",
    16: "1s (measure)",
}

# ── Morph labels ──────────────────────────────────────────────────────
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    14: "periodicity", 18: "trend",
}

# ── Law labels ────────────────────────────────────────────────────────
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


# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
_AMPLITUDE = 7        # amplitude
_ONSET = 11           # onset_strength
_SHARPNESS = 13       # sharpness (was "brightness" in v1)
_SPECTRAL_FLUX = 21   # spectral_flux (was at [10] in v1)
_PITCH_HEIGHT = 37    # pitch_height (replaces dissolved pitch_change)
_PCE = 38             # pitch_class_entropy
_PITCH_SAL = 39       # pitch_salience (replaces dissolved x_l4l5)
_BEAT_STR = 42        # beat_strength (replaces dissolved x_l0l5)


# ── 16 H³ Demand Specifications ──────────────────────────────────────
# Ordered: L2 (integration, 13) → L0 (memory, 3)

_MPG_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === L2 Integration (13 tuples) ===
    # -- Onset detection (posterior AC) --
    _h3(_SPECTRAL_FLUX, "spectral_flux", 0, 0, 2,
        "Spectral flux value instant (onset detection)", "Rupp 2022"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 1, 1, 2,
        "Spectral flux mean ~50ms (sustained onset)", "Rupp 2022"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Spectral flux value ~100ms (alpha-band onset)", "Rupp 2022"),
    _h3(_ONSET, "onset_strength", 0, 0, 2,
        "Onset strength instant (note boundary)", "Patterson 2002"),
    _h3(_ONSET, "onset_strength", 3, 1, 2,
        "Onset strength mean ~100ms (sustained onset)", "Patterson 2002"),
    _h3(_ONSET, "onset_strength", 16, 14, 2,
        "Onset periodicity ~1s (rhythmic regularity)", "Samiee 2022"),
    # -- Pitch/contour (anterior AC) --
    _h3(_SHARPNESS, "sharpness", 3, 0, 2,
        "Sharpness value ~100ms (pitch brightness)", "Briley 2013"),
    _h3(_SHARPNESS, "sharpness", 3, 2, 2,
        "Sharpness std ~100ms (brightness variability)", "Briley 2013"),
    _h3(_PITCH_HEIGHT, "pitch_height", 3, 0, 2,
        "Pitch height value ~100ms (register context)", "Norman-Haignere 2013"),
    _h3(_PITCH_HEIGHT, "pitch_height", 16, 1, 2,
        "Pitch height mean ~1s (register memory)", "Norman-Haignere 2013"),
    _h3(_PCE, "pitch_class_entropy", 4, 0, 2,
        "Pitch class entropy ~125ms (chroma distribution)", "Cheung 2019"),
    # -- Scene/coupling --
    _h3(_AMPLITUDE, "amplitude", 3, 0, 2,
        "Amplitude value ~100ms (energy context)", "Patterson 2002"),
    _h3(_BEAT_STR, "beat_strength", 3, 14, 2,
        "Beat strength periodicity ~100ms (metric structure)", "Samiee 2022"),

    # === L0 Memory (3 tuples) ===
    _h3(_SHARPNESS, "sharpness", 4, 8, 0,
        "Sharpness velocity ~125ms (pitch contour rate)", "Foo 2016"),
    _h3(_PITCH_HEIGHT, "pitch_height", 4, 18, 2,
        "Pitch height trend ~125ms (contour direction)", "Rupp 2022"),
    _h3(_PITCH_SAL, "pitch_salience", 3, 8, 0,
        "Pitch salience velocity ~100ms (pitch presence dynamics)", "Bidelman 2009"),
)

assert len(_MPG_H3_DEMANDS) == 16


class MPG(Relay):
    """Melodic Processing Gradient — NDU Relay (depth 0, 10D).

    Models the posterior-to-anterior cortical gradient for melodic
    processing. Posterior regions process sequence onset, anterior regions
    process subsequent notes and pitch variation (Rupp et al. 2022).

    Dependency chain:
        MPG is a Relay (Depth 0) — reads R³/H³ directly.
        No upstream mechanism dependencies.

    Downstream feeds (relay outputs):
        → SNEM (onset context for salience)
        → SDD (gradient context for deviance detection)
        → CDMR (contour for melodic mismatch)
        → STU (onset timing + phrase segmentation)
    """

    NAME = "MPG"
    FULL_NAME = "Melodic Processing Gradient"
    UNIT = "NDU"
    FUNCTION = "F1"
    OUTPUT_DIM = 10

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:onset_posterior", "E1:sequence_anterior",
             "E2:contour_complexity", "E3:gradient_ratio"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 7,
            ("M0:activity_x", "M1:posterior_activity",
             "M2:anterior_activity"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 7, 9,
            ("P0:onset_state", "P1:contour_state"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 10,
            ("F0:phrase_boundary_pred",),
            scope="external",
        ),
    )

    # ── Abstract property implementations ─────────────────────────────

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _MPG_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:onset_posterior", "E1:sequence_anterior",
            "E2:contour_complexity", "E3:gradient_ratio",
            "M0:activity_x", "M1:posterior_activity",
            "M2:anterior_activity",
            "P0:onset_state", "P1:contour_state",
            "F0:phrase_boundary_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Medial Heschl's Gyrus — onset pitch detection (posterior)
            RegionLink("E0:onset_posterior", "A1_HG", 0.80,
                       "Patterson 2002"),
            RegionLink("M1:posterior_activity", "A1_HG", 0.70,
                       "Briley 2013"),
            # Superior Temporal Gyrus — melodic contour
            RegionLink("E1:sequence_anterior", "STG", 0.75,
                       "Rupp 2022"),
            RegionLink("P1:contour_state", "STG", 0.70,
                       "Foo 2016"),
            RegionLink("M2:anterior_activity", "STG", 0.55,
                       "Norman-Haignere 2013"),
            # Onset state → A1_HG + STG dual
            RegionLink("P0:onset_state", "A1_HG", 0.60,
                       "Patterson 2002"),
            RegionLink("P0:onset_state", "STG", 0.40,
                       "Rupp 2022"),
            # Phrase boundary → IFG (frontal integration)
            RegionLink("F0:phrase_boundary_pred", "IFG", 0.35,
                       "Cheung 2019"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Onset novelty → weak norepinephrine (alerting)
            NeuroLink("P0:onset_state", 1, "amplify", 0.15,
                      "Samiee 2022"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Rupp", 2022,
                         "Posterior→anterior gradient for melodic contours vs "
                         "fixed-pitch in MEG",
                         "MEG, n=20, spatial pattern"),
                Citation("Patterson", 2002,
                         "Activity moves anterolaterally from HG to STG/PP "
                         "for melody vs pitch",
                         "fMRI, ~n=10"),
                Citation("Norman-Haignere", 2013,
                         "Pitch-sensitive regions in anterior nonprimary AC",
                         "fMRI+tonotopy"),
                Citation("Briley", 2013,
                         "IRN sources 7mm lateral/anterior to pure-tone; "
                         "pitch chroma representation",
                         "EEG, F(1,28)=29.865"),
                Citation("Foo", 2016,
                         "Anterior STG = dissonant-sensitive; posterior STG "
                         "= non-selective",
                         "ECoG, n=8, p=0.003"),
                Citation("Samiee", 2022,
                         "Delta bottom-up AC→IFG; beta bursts top-down; "
                         "delta-beta PAC at pitch change",
                         "MEG+EEG, n=16, F(1)=49.7"),
                Citation("Zatorre", 2022,
                         "Right AC specialization for spectral/pitch",
                         "mini-review"),
                Citation("Cheung", 2019,
                         "AC uncertainty×surprise interaction for harmonic "
                         "sequences",
                         "fMRI, n=40, β=-0.182"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.80, 0.92),
            falsification_criteria=(
                "Single notes should primarily activate posterior regions; "
                "complex melodies should show stronger anterior activation "
                "(Rupp 2022 confirmed)",
                "Fixed-pitch sequences should show reduced anterior activity "
                "compared to melodic contours (Rupp 2022 confirmed)",
            ),
            version="1.0.0",
        )

    # ── Compute ───────────────────────────────────────────────────────

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R³/H³ into 10D melodic gradient representation.

        Delegates to 4 layer functions (extraction → temporal_integration
        → cognitive_present → forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 10)`` — E(4) + M(3) + P(2) + F(1)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(r3_features, h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(r3_features, h3_features, p, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
