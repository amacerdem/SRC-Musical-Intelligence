"""HGSIC E-Layer -- Extraction (3D).

Three features modeling beat/meter/groove at the oscillatory level:

  f01: beat_gamma        -- Beat-level gamma oscillation strength
  f02: meter_integration -- Metric structure integration
  f03: motor_groove      -- Motor coupling for groove

H3 consumed:
    (7, 6, 0, 0)    amplitude value H6       -- beat-level dynamic envelope
    (7, 6, 4, 0)    amplitude min H6         -- dynamic floor for contrast
    (8, 6, 0, 0)    loudness value H6        -- perceptual intensity at beat
    (10, 6, 0, 0)   spectral_flux value H6   -- onset energy at beat
    (10, 6, 17, 0)  spectral_flux peaks H6   -- onset peak detection
    (11, 6, 0, 0)   onset_strength value H6  -- event salience at beat

Upstream consumed:
    PEOM: period_lock_strength [0], kinematic_smoothness [1]

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hgsic/HGSIC-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_AMPLITUDE_H6 = (7, 6, 0, 0)
_AMPLITUDE_MIN_H6 = (7, 6, 4, 0)
_LOUDNESS_H6 = (8, 6, 0, 0)
_FLUX_H6 = (10, 6, 0, 0)
_FLUX_PEAKS_H6 = (10, 6, 17, 0)
_ONSET_H6 = (11, 6, 0, 0)

# -- R3 indices ----------------------------------------------------------------
_ONSET_STRENGTH = 11
_SPECTRAL_FLUX = 10


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from R3/H3 + PEOM relay.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        relay_outputs: ``{"PEOM": (B, T, 11)}``.

    Returns:
        ``(f01, f02, f03)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    amplitude_h6 = h3_features.get(_AMPLITUDE_H6, zero)
    amplitude_min_h6 = h3_features.get(_AMPLITUDE_MIN_H6, zero)
    loudness_h6 = h3_features.get(_LOUDNESS_H6, zero)
    flux_h6 = h3_features.get(_FLUX_H6, zero)
    flux_peaks_h6 = h3_features.get(_FLUX_PEAKS_H6, zero)
    onset_h6 = h3_features.get(_ONSET_H6, zero)

    # PEOM relay context
    peom = relay_outputs.get("PEOM")
    if peom is not None and peom.dim() >= 2:
        peom_period_lock = peom[:, :, 0]       # period_lock_strength
        peom_smoothness = peom[:, :, 1]         # kinematic_smoothness
    else:
        peom_period_lock = zero
        peom_smoothness = zero

    # f01: Beat Gamma -- beat-level oscillation strength
    # Janata 2012: beat-level dynamics drive groove perception
    f01 = torch.sigmoid(
        0.30 * amplitude_h6
        + 0.25 * onset_h6
        + 0.25 * flux_peaks_h6
        + 0.20 * loudness_h6
    )

    # f02: Meter Integration -- metric structure from beat contrast
    # Madison 2011: dynamic range and event density drive groove
    dynamic_contrast = amplitude_h6 - amplitude_min_h6
    f02 = torch.sigmoid(
        0.35 * dynamic_contrast
        + 0.30 * flux_h6
        + 0.20 * onset_h6
        + 0.15 * peom_period_lock
    )

    # f03: Motor Groove -- motor coupling for groove sensation
    # Witek 2014: groove is the desire to move, linked to motor system
    f03 = torch.sigmoid(
        0.30 * f01 * peom_period_lock
        + 0.25 * f02
        + 0.25 * peom_smoothness
        + 0.20 * flux_peaks_h6
    )

    return f01, f02, f03
