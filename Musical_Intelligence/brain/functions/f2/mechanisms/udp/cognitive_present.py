"""UDP P-Layer -- Cognitive Present (3D).

Context assessment, prediction accuracy, and reward computation at the
perceptual present, integrating upstream PWUP and WMED outputs:
  P0: context_assessment    (uncertainty context evaluation)
  P1: prediction_accuracy   (accuracy of prediction in current context)
  P2: reward_computation    (reward inversion: uncertainty x confirmation)

Dependencies:
    - PWUP (Depth 1): M1:uncertainty_index [idx 3]
    - WMED (Depth 2): E1:wm_contribution   [idx 1]

H3 demands consumed:
  spectral_change:   (21,3,4,2) max integration
  onset_strength:    (10,3,0,2), (10,3,8,2)
  tonalness:         (14,8,1,0) reused
  H_coupling:        (41,16,6,0) skew

R3 direct reads:
  tristimulus[18:21] -- harmonic balance for reward computation

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/udp/
Cheung et al. 2019: uncertainty x surprise -> pleasure (saddle-shaped).
Gold et al. 2019: inverted-U for IC and entropy on liking.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_TRISTIMULUS_START = 18
_TRISTIMULUS_END = 21

# -- H3 keys consumed ---------------------------------------------------------
_SPEC_CHANGE_H3_MAX = (21, 3, 4, 2)
_ONSET_H3_VAL = (11, 3, 0, 2)
_ONSET_H3_VEL = (11, 3, 8, 2)
_TONAL_H8_MEAN = (14, 8, 1, 0)
_H_COUPLING_H16_SKEW = (41, 16, 6, 0)

# -- Upstream output indices ---------------------------------------------------
_PWUP_M1 = 3         # PWUP M1:uncertainty_index
_WMED_E1 = 1         # WMED E1:wm_contribution


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: context assessment, prediction accuracy, reward.

    Integrates upstream uncertainty (PWUP) and working memory (WMED)
    with local E/M signals and H3 features to compute the reward
    inversion characteristic of uncertainty-driven pleasure.

    Cheung et al. 2019: saddle-shaped pleasure surface --
    low uncertainty + high surprise = pleasure,
    high uncertainty + correct prediction = pleasure.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        upstream_outputs: ``{"PWUP": (B, T, 10), "WMED": (B, T, 11)}``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    e0, e1 = e
    m0, m1 = m

    # -- R3 direct reads --
    trist_mean = r3_features[..., _TRISTIMULUS_START:_TRISTIMULUS_END].mean(
        dim=-1
    )

    # -- Upstream reads --
    pwup = upstream_outputs["PWUP"]    # (B, T, 10)
    wmed = upstream_outputs["WMED"]    # (B, T, 11)
    uncertainty_index = pwup[:, :, _PWUP_M1]    # (B, T)
    wm_contribution = wmed[:, :, _WMED_E1]      # (B, T)

    # -- H3 features --
    spec_change_max = h3_features[_SPEC_CHANGE_H3_MAX]
    onset_100ms = h3_features[_ONSET_H3_VAL]
    onset_vel_100ms = h3_features[_ONSET_H3_VEL]
    tonal_mean_500ms = h3_features[_TONAL_H8_MEAN]
    h_coupling_skew = h3_features[_H_COUPLING_H16_SKEW]

    # -- P0: Context Assessment --
    # Evaluates the current uncertainty context by combining upstream
    # precision-weighted uncertainty with local tonal/coupling signals.
    # Koelsch 2019: musical syntax expectations modulate emotional context.
    # abs() on skewness: coupling asymmetry magnitude, not direction
    p0 = torch.sigmoid(
        0.30 * uncertainty_index
        + 0.25 * e0
        + 0.20 * (1.0 - tonal_mean_500ms)
        + 0.15 * torch.abs(h_coupling_skew)
        + 0.10 * wm_contribution
    )

    # -- P1: Prediction Accuracy --
    # How accurate the current prediction is, given onset events and
    # spectral change. Low spectral change + low onset velocity = high
    # accuracy (prediction confirmed). Gated by working memory.
    # Pearce 2005: IC = -log2(P(event|context)).
    # abs() on velocity: low MAGNITUDE of change = accurate prediction
    p1 = torch.sigmoid(
        0.30 * (1.0 - spec_change_max)
        + 0.25 * (1.0 - torch.abs(onset_vel_100ms))
        + 0.20 * wm_contribution
        + 0.15 * m1
        + 0.10 * trist_mean
    )

    # -- P2: Reward Computation --
    # Core reward inversion: when uncertainty (P0) is high AND prediction
    # is accurate (P1), reward is amplified. This is the saddle-shaped
    # interaction from Cheung 2019: uncertainty x confirmation = pleasure.
    # Multiplicative interaction captures the nonlinear reward surface.
    uncertainty_x_accuracy = p0 * p1  # (B, T) -- interaction term
    p2 = torch.sigmoid(
        0.30 * uncertainty_x_accuracy
        + 0.25 * e1
        + 0.20 * m0
        + 0.15 * onset_100ms
        + 0.10 * m1
    )

    return p0, p1, p2
