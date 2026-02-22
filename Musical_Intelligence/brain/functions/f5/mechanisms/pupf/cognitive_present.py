"""PUPF P-Layer -- Cognitive Present (3D).

Present-time pleasure-uncertainty prediction signals:
  P0: surprise_pleasure    — Real-time surprise-pleasure coupling [0, 1]
  P1: affective_outcome    — Current affective valence outcome [0, 1]
  P2: tempo_pred_error     — Temporal prediction error for rhythm [0, 1]

P0 captures the moment-by-moment coupling between surprise and pleasure.
When the Goldilocks zone is active (G1 high), surprise events produce
pleasure rather than aversion. This is the real-time readout of whether
surprising events are experienced as pleasurable or aversive. Amygdala
and hippocampus activation scales with this coupling (Cheung 2019).

P1 integrates the Goldilocks pleasure signal (G0) with current hedonic
context to produce an overall affective outcome. Sensory pleasantness
(hedonic baseline) modulates the pleasure signal from the H x S function.
NAcc dopamine release tracks this combined signal.

P2 captures temporal (rhythmic) prediction errors. Velocity_A trend at 1s
combined with harmonic deviation velocity measures how well the brain
predicts upcoming temporal and pitch events. Tempo prediction errors
contribute to surprise and thus to the Goldilocks function.

H3 demands consumed (4 tuples -- shared with E/M layers):
  (8, 16, 18, 0)  velocity_A trend H16 L0              -- tempo trend 1s
  (4, 12, 18, 0)  sensory_pleasantness trend H12 L0    -- hedonic trajectory
  (22, 7, 8, 0)   distribution_entropy velocity H7 L0  -- uncertainty rate
  (6, 12, 8, 0)   harmonic_deviation velocity H12 L0   -- harmonic PE rate

R3 features:
  [4] sensory_pleasantness, [8] velocity_A, [21] spectral_flux,
  [33:41] x_l4l5

Cheung et al. 2019: surprise-pleasure coupling in amygdala/hippocampus
(fMRI, N=39, d=3.8-4.16).
Koelsch 2014: tension-resolution in auditory cortex and striatum.
Salimpoor et al. 2011: dopamine release in NAcc during peak pleasure.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/pupf/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_VELA_TREND_H16 = (8, 16, 18, 0)          # velocity_A trend H16 L0
_PLEAS_TREND_H12 = (4, 12, 18, 0)         # sensory_pleasantness trend H12 L0
_ENTROPY_VEL_H7 = (22, 7, 8, 0)           # distribution_entropy velocity H7 L0
_HARM_VEL_H12 = (6, 12, 8, 0)             # harmonic_deviation velocity H12 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_SENSORY_PLEASANTNESS = 4
_VELOCITY_A = 8
_SPECTRAL_FLUX = 21
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: present-time surprise-pleasure and affective outcome.

    P0 (surprise_pleasure) captures the real-time coupling between surprise
    and pleasure. Goldilocks zone (G1) gates whether surprise produces
    pleasure or aversion. E0 (prediction error) modulated by G1 (Goldilocks)
    produces the coupling signal. Amygdala/hippocampus activation scales
    with this (Cheung 2019, d=3.8-4.16).

    P1 (affective_outcome) integrates Goldilocks pleasure (G0) with hedonic
    context. Sensory pleasantness trend provides trajectory. H x S
    interaction (U2) provides the interaction context. NAcc dopamine release
    tracks this combined signal.

    P2 (tempo_pred_error) captures temporal prediction errors. Velocity_A
    trend (tempo trajectory at 1s) combined with harmonic deviation velocity
    (pitch prediction errors) measures how well temporal and pitch
    predictions are fulfilled.

    Cheung et al. 2019: H x S interaction drives amygdala (d=3.8-4.16).
    Salimpoor et al. 2011: NAcc dopamine during peak pleasure.
    Koelsch 2014: tension-resolution cycle.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(U0, U1, U2, G0, G1)`` from temporal integration layer.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    e0, _e1 = e
    u0, _u1, u2, g0, g1 = m

    # -- H3 features --
    vela_trend = h3_features[_VELA_TREND_H16]       # (B, T)
    pleas_trend = h3_features[_PLEAS_TREND_H12]     # (B, T)
    entropy_vel = h3_features[_ENTROPY_VEL_H7]      # (B, T)
    harm_vel = h3_features[_HARM_VEL_H12]           # (B, T)

    # -- R3 features --
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]   # (B, T)
    velocity_a = r3_features[..., _VELOCITY_A]               # (B, T)
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]         # (B, T)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]    # (B, T, 8)
    x_l4l5_mean = x_l4l5.mean(dim=-1)                       # (B, T)

    # -- P0: Surprise-Pleasure Coupling --
    # Real-time coupling between surprise (E0) and pleasure (G0/G1).
    # Goldilocks zone (G1) gates whether surprise -> pleasure or aversion.
    # When G1 is high (low H, high S), surprise produces pleasure.
    # Cheung 2019: amygdala/hippocampus respond to H x S (d=3.8-4.16).
    p0 = torch.sigmoid(
        0.35 * e0 * g1.clamp(min=0.1)
        + 0.35 * g0 * spectral_flux.clamp(min=0.1)
        + 0.30 * u2 * x_l4l5_mean.clamp(min=0.1)
    )

    # -- P1: Affective Outcome --
    # Current affective valence integrating Goldilocks pleasure (G0),
    # hedonic trajectory (pleasantness trend), and interaction context (U2).
    # Salimpoor et al. 2011: NAcc dopamine tracks peak pleasure.
    p1 = torch.sigmoid(
        0.35 * g0 * pleasantness.clamp(min=0.1)
        + 0.35 * pleas_trend * u2.clamp(min=0.1)
        + 0.30 * p0
    )

    # -- P2: Tempo Prediction Error --
    # Temporal PE from velocity_A trend (tempo trajectory) combined with
    # harmonic deviation velocity (pitch PE). Entropy velocity provides
    # uncertainty change rate for temporal context.
    # Koelsch 2014: temporal predictions and their violations.
    p2 = torch.sigmoid(
        0.35 * vela_trend * velocity_a.clamp(min=0.1)
        + 0.35 * harm_vel * entropy_vel.clamp(min=0.1)
        + 0.30 * e0 * u0.clamp(min=0.1)
    )

    return p0, p1, p2
