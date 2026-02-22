"""AAC P-Layer -- Cognitive Present (3D).

Three present-processing dimensions for autonomic-arousal state:

  P0: current_intensity    -- Current overall arousal intensity [0, 1]
  P1: driving_signal       -- Rhythmic driving signal strength [0, 1]
  P2: perceptual_arousal   -- Perceptual arousal from acoustic features [0, 1]

H3 consumed (reuse of E+A-layer tuples):
    (7, 9, 4, 2)    amplitude max H9 L2             -- current energy
    (10, 9, 14, 2)  spectral_flux periodicity H9 L2 -- driving rhythm
    (10, 16, 14, 2) spectral_flux periodicity H16 L2 -- tempo signal
    (7, 9, 11, 2)   amplitude acceleration H9 L2    -- intensity momentum

R3 consumed:
    [7]   amplitude        -- P2: raw energy for arousal
    [10]  spectral_flux    -- P1: beat entrainment
    [11]  onset_strength   -- P0: event density

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/aac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (reused from E+A-layer) ----------------------------------------
_AMP_MAX_350MS = (7, 9, 4, 2)
_FLUX_PERIOD_350MS = (10, 9, 14, 2)
_FLUX_PERIOD_1S = (10, 16, 14, 2)
_AMP_ACCEL_350MS = (7, 9, 11, 2)

# -- R3 indices ----------------------------------------------------------------
_AMPLITUDE = 7
_SPECTRAL_FLUX_B = 10
_ONSET_STRENGTH = 11


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    ea_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
    i_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3/R3 + E+A/I outputs.

    P-layer outputs are the primary relay exports:
        current_intensity  -> downstream intensity assessment
        driving_signal     -> motor entrainment coupling
        perceptual_arousal -> salience and attention modulation

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        ea_outputs: ``(E0, E1, A0, A1, A2, A3, A4)`` each ``(B, T)``.
        i_outputs: ``(I0, I1)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    e0, _e1, a0, _a1, _a2, _a3, _a4 = ea_outputs
    i0, i1 = i_outputs

    amp_max_350ms = h3_features[_AMP_MAX_350MS]
    flux_period_350ms = h3_features[_FLUX_PERIOD_350MS]
    flux_period_1s = h3_features[_FLUX_PERIOD_1S]
    amp_accel_350ms = h3_features[_AMP_ACCEL_350MS]

    # R3 features
    amplitude = r3_features[..., _AMPLITUDE]       # (B, T)
    flux_b = r3_features[..., _SPECTRAL_FLUX_B]    # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]       # (B, T)

    # P0: Current intensity -- integrated arousal state
    # Craig 2002: anterior insula integrates interoceptive signals into
    # a unified feeling of arousal intensity
    p0 = torch.sigmoid(
        0.30 * e0 + 0.25 * i1 + 0.20 * a0
        + 0.15 * amp_max_350ms + 0.10 * onset
    )

    # P1: Driving signal -- rhythmic entrainment strength
    # Trost 2017: beat periodicity and tempo modulate ANS activation
    # Beat clarity at both 350ms and 1s scales drives the motor signal
    p1 = torch.sigmoid(
        0.35 * flux_period_350ms + 0.30 * flux_period_1s
        + 0.20 * flux_b + 0.15 * amp_accel_350ms
    )

    # P2: Perceptual arousal -- raw acoustic arousal perception
    # Koelsch 2014: amygdala + hypothalamus activation tracks
    # perceived arousal from acoustic features
    p2 = torch.sigmoid(
        0.30 * amp_max_350ms + 0.25 * amplitude
        + 0.20 * i0 + 0.15 * amp_accel_350ms
        + 0.10 * e0
    )

    return p0, p1, p2
