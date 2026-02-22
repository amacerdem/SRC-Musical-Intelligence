"""MCCN P-Layer -- Cognitive Present (2D).

Present-time chills network activation signals:
  network_state  -- Distributed cortical network activation level [0, 1]
  theta_pattern  -- Prefrontal-central theta contrast biomarker [0, 1]

Network State (P0): Overall activation of the distributed cortical chills
network (OFC + bilateral insula + SMA + bilateral STG). Integrates chills
magnitude (f04) and arousal index (f03). When network_state is high, the
full cortical chills circuit is engaged.

Theta Pattern (P1): The defining EEG biomarker of chills -- the theta
oscillation contrast (prefrontal increase + central/temporal decrease).
Combines f01 (theta prefrontal, excitatory) and f02 (theta central, already
inverted). More specific than network state: theta_pattern tracks the
oscillatory signature, while network_state tracks activation magnitude.

H3 demands consumed (6 tuples -- all shared with E-layer):
  (25, 3,  14, 2)  x_l0l5 periodicity H3 L2   -- via f01, f02
  (25, 16, 1,  2)  x_l0l5 mean H16 L2          -- via f01
  (8,  8,  4,  2)  loudness max H8 L2           -- via f04
  (9,  8,  8,  2)  rms_energy velocity H8 L2    -- via f03
  (9,  3,  0,  2)  rms_energy value H3 L2       -- via f03
  (0,  16, 2,  2)  roughness std H16 L2         -- via f02

E-layer features:
  f01 (theta_prefrontal), f02 (theta_central),
  f03 (arousal_index), f04 (chills_magnitude)

Chabin et al. 2020: OFC + insula + SMA + STG co-activation during chills
(LAURA source localization, all p < 1e-05; HD-EEG, N = 18).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/mccn/p_layer.md
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_cognitive_present(
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: present-time chills network state and theta biomarker.

    P0 (network_state) integrates chills magnitude (f04, peak pleasure and
    reward-arousal coupling) with arousal index (f03, physiological
    activation). OFC + bilateral insula + SMA + bilateral STG all
    co-activate during chills (Chabin 2020, all p < 1e-05).

    P1 (theta_pattern) captures the characteristic theta oscillation
    contrast: simultaneous prefrontal increase + central decrease. This
    is the EEG biomarker of chills, distinct from overall network magnitude.
    Chabin 2020: RPF theta up (p = 0.049), central/temporal theta down
    (p = 0.006).

    Args:
        e: ``(f01, f02, f03, f04)`` from extraction layer, each ``(B, T)``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    f01, f02, f03, f04 = e

    # -- P0: Network State --
    # Overall cortical chills network activation.
    # sigma(0.5 * f04 + 0.5 * f03)
    # Chabin 2020: OFC + insula + SMA + STG (LAURA, all p < 1e-05).
    p0 = torch.sigmoid(
        0.50 * f04
        + 0.50 * f03
    )

    # -- P1: Theta Pattern --
    # Prefrontal-central theta contrast biomarker.
    # sigma(0.5 * f01 + 0.5 * f02)
    # Chabin 2020: RPF theta up (p = 0.049), RC/RT theta down (p = 0.006).
    p1 = torch.sigmoid(
        0.50 * f01
        + 0.50 * f02
    )

    return p0, p1
