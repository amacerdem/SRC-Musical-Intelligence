"""VRIAP P-Layer -- Cognitive Present (2D).

Present-processing motor-pain state and S1 connectivity estimation:
  P0: motor_pain_state   -- Current motor-pain gating activation [0, 1]
  P1: s1_connectivity    -- S1 connectivity proxy (higher = more gating) [0, 1]

Motor-pain state (P0) is the product of memory encoding state and motor
engagement (E0). Only active when both memory encoding is engaged AND
the motor system is coupled with musical structure. Reflects gate
control: efference copies from active motor engagement suppress pain
through S1. Liang 2025: VRMS enhances S1-motor connectivity (t=4.023).

S1 connectivity (P1) provides a running estimate of S1 connectivity
reduction. Higher values = greater pain gating (less S1 connectivity
to pain matrix). Derived from pain gate (E1) mean. Liang 2025: VRMS >
VRAO for RS1 FC (t=4.023, p=0.002 FDR).

H3 demands consumed (shared with E-layer, plus 1 new):
  (11, 16, 0, 2) onset_strength value H16 L2   -- motor cueing
  (10, 16, 0, 2) loudness value H16 L2         -- engagement intensity
  (7, 16, 8, 0)  amplitude velocity H16 L0     -- motor dynamics
  (21, 16, 0, 2) spectral_flux value H16 L2    -- event salience

R3 inputs: amplitude[7], loudness[10], onset_strength[11],
           spectral_flux[21], x_l0l5[25:33]

See Building/C3-Brain/F4-Memory-Systems/mechanisms/vriap/VRIAP-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_ONSET_VAL_H16 = (11, 16, 0, 2)       # onset_strength value H16 L2
_LOUD_VAL_H16 = (10, 16, 0, 2)        # loudness value H16 L2
_AMP_VEL_H16 = (7, 16, 8, 0)          # amplitude velocity H16 L0
_SFLUX_VAL_H16 = (21, 16, 0, 2)       # spectral_flux value H16 L2

# -- R3 feature indices -------------------------------------------------------
_AMPLITUDE = 7
_LOUDNESS = 10
_ONSET = 11
_SPECTRAL_FLUX = 21
_X_L0L5_START = 25
_X_L0L5_END = 33


def _encoding_state(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tensor:
    """Encoding state for motor-pain gating.

    Combines onset cueing, loudness, amplitude velocity, and spectral
    flux to estimate the current strength of mnemonic encoding. Uses
    R3 x_l0l5 for motor-sensory binding context.

    Returns (B, T) in [0, 1] via sigmoid.
    """
    onset_val = h3_features[_ONSET_VAL_H16]            # (B, T)
    loud_val = h3_features[_LOUD_VAL_H16]              # (B, T)
    amp_vel = h3_features[_AMP_VEL_H16]                # (B, T)
    sflux_val = h3_features[_SFLUX_VAL_H16]            # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)

    return torch.sigmoid(
        0.25 * onset_val
        + 0.25 * loud_val * amp_vel
        + 0.25 * sflux_val
        + 0.25 * x_l0l5.mean(dim=-1)
    )


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: motor-pain state and S1 connectivity proxy.

    P0 (motor_pain_state): Product of encoding state and motor engagement
    (E0). Gate control mechanism — active motor engagement generates
    efference copies that suppress pain through S1.
    Liang 2025: VRMS enhances S1-motor connectivity (t=4.023, p=0.002).

    P1 (s1_connectivity): Running estimate of S1 connectivity reduction.
    Derived from pain gate (E1) signal. Higher = more pain gating
    (less S1 connectivity to pain matrix).
    Liang 2025: VRMS > VRAO RS1 FC (t=4.023, p=0.002 FDR).

    Args:
        r3_features: ``(B, T, 97)`` R3 spectral features.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    e0, e1, _e2 = e
    _m0, _m1 = m

    # -- Encoding state for motor-pain interaction --
    enc_state = _encoding_state(r3_features, h3_features)  # (B, T)

    # -- P0: Motor-Pain State --
    # Product of encoding state and engagement: active only when both
    # memory encoding is engaged AND motor system is coupled.
    # Liang 2025: VRMS S1-motor connectivity (t=4.023, p=0.002)
    # Melzack & Wall 1965: gate control via non-nociceptive input
    p0 = (enc_state * e0).clamp(0.0, 1.0)

    # -- P1: S1 Connectivity --
    # Running estimate of S1 connectivity reduction from pain gate.
    # Higher values = greater pain gating (reduced S1 connectivity).
    # Liang 2025: VRMS > VRAO RS1 FC (t=4.023, p=0.002 FDR)
    p1 = e1.clamp(0.0, 1.0)

    return p0, p1
