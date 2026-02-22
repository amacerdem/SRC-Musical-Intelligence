"""CLAM P-Layer -- Cognitive Present (2D).

Present-time closed-loop affective modulation signals:
  P0: arousal_modulation     — Real-time arousal steering state [0, 1]
  P1: valence_tracking       — Real-time valence tracking accuracy [0, 1]

P0 captures the moment-by-moment arousal modulation driven by the
closed-loop BCI system. Combines instantaneous arousal velocity
(loudness dynamics), dynamic rate (velocity_A), and the control output
from the B+C layer. High P0 indicates the loop is actively and
successfully steering arousal toward the target. This feeds the
affective_control appraisal belief.

P1 captures how accurately the system tracks valence changes. Combines
hedonic state (sensory pleasantness at 525ms), valence-related roughness
dynamics, and the decoded affect signal. High P1 indicates reliable
valence tracking even though valence is harder to decode than arousal
(Ehrlich 2019: r=0.52 vs r=0.74).

H3 demands consumed (2 tuples -- shared key with E-layer + new):
  (10, 7, 8, 0)   loudness velocity H7 L0           -- arousal velocity
  (8, 7, 8, 0)    velocity_A velocity H7 L0         -- dynamic rate
  Note: (10, 7, 8, 0) shared with E-layer.

Additional P-layer tuple:
  (4, 12, 0, 0)   sensory_pleasantness value H12 L0 -- hedonic state

R3 features:
  [0] roughness, [4] sensory_pleasantness, [8] velocity_A, [10] loudness

Ehrlich et al. 2019: arousal tracking r=0.74, valence tracking r=0.52.
Daly et al. 2019: frontal EEG arousal-valence classification.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_LOUD_VEL_H7 = (10, 7, 8, 0)           # loudness velocity H7 L0
_VELA_VEL_H7 = (8, 7, 8, 0)            # velocity_A velocity H7 L0
_PLEAS_VAL_H12 = (4, 12, 0, 0)         # sensory_pleasantness value H12 L0

# -- R3 feature indices -------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_VELOCITY_A = 8
_LOUDNESS = 10


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: present-time arousal modulation and valence tracking.

    P0 (arousal_modulation) captures real-time arousal steering. Combines
    instantaneous arousal velocity, dynamic rate from velocity_A, and
    the control output (C0) gated by loop coherence (E1). When the loop
    is coherent and control is active, arousal modulation is high.

    P1 (valence_tracking) captures valence tracking accuracy. Combines
    hedonic state (pleasantness at 525ms), roughness dynamics (inverted
    for valence), and decoded affect quality. Valence tracking is
    inherently harder (r=0.52 vs r=0.74 for arousal).

    Ehrlich et al. 2019: arousal tracking r=0.74, valence r=0.52 (N=5).
    Daly et al. 2019: frontal asymmetry maps to valence dimension.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(B0, B1, B2, C0, C1)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, e1 = e
    b0, _b1, b2, c0, _c1 = m

    # -- H3 features --
    loud_vel = h3_features[_LOUD_VEL_H7]        # (B, T)
    vela_vel = h3_features[_VELA_VEL_H7]        # (B, T)
    pleas_val = h3_features[_PLEAS_VAL_H12]      # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]               # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    velocity_a = r3_features[..., _VELOCITY_A]             # (B, T)
    loudness = r3_features[..., _LOUDNESS]                 # (B, T)

    # -- Derived signals --
    # Arousal dynamics: instantaneous change in arousal-related features
    arousal_dynamics = 0.50 * loud_vel.abs() + 0.50 * vela_vel.abs()

    # Valence quality: hedonic state x inverted roughness
    valence_quality = pleas_val * (1.0 - roughness.clamp(0.0, 1.0))

    # -- P0: Arousal Modulation --
    # Real-time arousal steering. Active control (C0) x loop coherence (E1)
    # x arousal dynamics. High values = loop is successfully steering arousal.
    # Ehrlich 2019: arousal tracking r=0.74 via closed-loop EEG.
    p0 = torch.sigmoid(
        0.35 * arousal_dynamics * c0.clamp(min=0.1)
        + 0.35 * e0 * loudness * velocity_a.clamp(min=0.1)
        + 0.30 * e1 * (1.0 - b2.clamp(0.0, 1.0))
    )

    # -- P1: Valence Tracking --
    # Valence tracking accuracy. Hedonic quality (pleasantness) x decoded
    # affect (B0) x loop coherence (E1). Harder than arousal -- valence
    # requires integration of roughness, pleasantness, and hedonic state.
    # Ehrlich 2019: valence tracking r=0.52; Daly 2019: frontal asymmetry.
    p1 = torch.sigmoid(
        0.35 * valence_quality * b0.clamp(min=0.1)
        + 0.35 * pleasantness * pleas_val
        + 0.30 * e1 * (1.0 - roughness.clamp(0.0, 1.0))
    )

    return p0, p1
