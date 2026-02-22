"""CHPI F-Layer -- Forecast (4D).

Forward predictions for harmonic progressions:
  F0: next_chord_prediction       (predicted next chord identity/quality)
  F1: crossmodal_anticipation     (cross-modal anticipatory signal strength)
  F2: harmonic_trajectory         (predicted harmonic path direction)
  F3: integration_confidence      (confidence in cross-modal prediction)

H3 demands consumed:
  sensory_pleasantness:     (4,16,1,0) reused
  tonalness:                (14,8,1,0) reused
  chroma_I:                 (33,8,0,0)
  periodicity:              (5,16,18,0)
  spectral_change:          (21,3,8,0) reused
  chroma_C:                 (25,3,0,2) reused

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/chpi/
Tillmann 2003: harmonic priming predicts upcoming chord identity.
Vuust 2022: predictive framework for music perception and anticipation.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CONSONANCE_H16_MEAN = (4, 16, 1, 0)
_TONALNESS_H8_MEAN = (14, 8, 1, 0)
_CHROMA_I_H8_VAL = (33, 8, 0, 0)
_PERIODICITY_H16_TREND = (5, 16, 18, 0)
_SPEC_CHANGE_H3_VEL = (21, 3, 8, 0)
_CHROMA_C_H3_VAL = (25, 3, 0, 2)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for harmonic progressions.

    Each dimension predicts a different aspect of upcoming harmonic events:
    chord identity, cross-modal anticipation, trajectory direction, and
    overall integration confidence.

    Tillmann et al. 2003: harmonic priming facilitates processing of
    harmonically related chords (p<0.05, N=12).
    Vuust et al. 2022: predictive processing framework for anticipatory
    music perception across modalities.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2, F3)`` each ``(B, T)``
    """
    e0, e1 = e
    p0, p1, p2 = p

    consonance_mean_1s = h3_features[_CONSONANCE_H16_MEAN]
    tonalness_mean_500ms = h3_features[_TONALNESS_H8_MEAN]
    pitch_height_500ms = h3_features[_CHROMA_I_H8_VAL]
    periodicity_trend_1s = h3_features[_PERIODICITY_H16_TREND]
    spec_change_vel = h3_features[_SPEC_CHANGE_H3_VEL]
    chroma_100ms = h3_features[_CHROMA_C_H3_VAL]

    # -- F0: Next Chord Prediction --
    # Predicted next chord identity based on harmonic context strength (P0),
    # tonal grounding (tonalness), chroma context (current tonal identity),
    # and consonance baseline (harmonic norm).
    # Tillmann 2003: STG/IFG generate harmonic predictions from context.
    f0 = torch.sigmoid(
        0.30 * p0
        + 0.25 * tonalness_mean_500ms
        + 0.25 * chroma_100ms
        + 0.20 * consonance_mean_1s
    )

    # -- F1: Crossmodal Anticipation --
    # Anticipated cross-modal benefit for next harmonic event. Cross-modal
    # convergence (P1) + prediction gain (E0) + periodicity trend (rhythmic
    # predictability enables timing of cross-modal cues).
    # Musacchia 2007: cross-modal training enhances anticipatory responses.
    f1 = torch.sigmoid(
        0.35 * p1
        + 0.30 * e0
        + 0.20 * periodicity_trend_1s
        + 0.15 * pitch_height_500ms
    )

    # -- F2: Harmonic Trajectory --
    # Predicted direction of harmonic path. Voice-leading smoothness (P2)
    # projects forward, modulated by spectral change velocity (motion
    # direction) and pitch height (registral trajectory).
    # Koelsch 2005: harmonic expectations follow voice-leading rules.
    f2 = torch.sigmoid(
        0.30 * p2
        + 0.25 * spec_change_vel
        + 0.25 * pitch_height_500ms
        + 0.20 * e1
    )

    # -- F3: Integration Confidence --
    # Overall confidence in cross-modal harmonic prediction. Strong harmonic
    # context + strong convergence + smooth voice-leading = high confidence.
    # Combines P-layer signals as a meta-estimate of prediction quality.
    # Vuust 2022: precision-weighted prediction confidence.
    f3 = torch.sigmoid(
        0.30 * p0
        + 0.25 * p1
        + 0.25 * p2
        + 0.20 * consonance_mean_1s
    )

    return f0, f1, f2, f3
