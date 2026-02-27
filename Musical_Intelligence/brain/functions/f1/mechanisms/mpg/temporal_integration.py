"""MPG M-Layer — Temporal Integration (3D).

Cortical gradient dynamics from posterior-to-anterior processing.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/mpg/MPG-temporal-integration.md

Uses the cortical gradient function: Activity(x) = α·Posterior + β·Anterior
where α = 0.7 (posterior weighting), β = 0.3 (anterior weighting).

Outputs:
    M0: activity_x           [0, 1]  Cortical gradient function
    M1: posterior_activity    [0, 1]  Onset strength encoding
    M2: anterior_activity     [0, 1]  Contour processing strength
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
_AMPLITUDE = 7        # amplitude
_ONSET = 11           # onset_strength
_SPECTRAL_FLUX = 21   # spectral_flux
_SHARPNESS = 13       # sharpness
_PITCH_HEIGHT = 37    # pitch_height
_BEAT_STR = 42        # beat_strength (replaces dissolved x_l0l5)

# ── Gradient parameters (Rupp 2022) ──────────────────────────────────
_ALPHA = 0.70         # posterior weighting
_BETA = 0.30          # anterior weighting


def _wsig(x: Tensor) -> Tensor:
    """Wide sigmoid — full [0, 1] dynamic range (gain=5, center=0.35)."""
    return (1.0 + torch.exp(-5.0 * (x - 0.35))).reciprocal()


def compute_temporal_integration(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: 3D gradient dynamics from E-layer + H³.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        e_outputs: Tuple of (E0, E1, E2, E3) from extraction.

    Returns:
        Tuple of (M0, M1, M2), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    e0, e1, e2, _e3 = e_outputs

    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # M0: Activity_x — cortical gradient function
    #     Weighted combination of posterior onset and anterior contour
    #     α=0.7 emphasizes onset processing (Patterson 2002: HG pitch center)
    m0 = _ALPHA * e0 + _BETA * e1

    # M1: Posterior Activity — onset-locked processing in posterior AC
    #     Briley 2013: medial HG responds to onset/pitch extraction
    m1 = _wsig(
        0.40 * h3(_ONSET, 0, 0, 2)           # onset_strength instant
        + 0.30 * h3(_SPECTRAL_FLUX, 0, 0, 2)  # spectral_flux instant
        + 0.30 * r3(_AMPLITUDE)               # raw amplitude energy
    )

    # M2: Anterior Activity — contour processing in anterior AC
    #     Norman-Haignere 2013: anterior nonprimary AC for pitch sensitivity
    #     abs() on velocity: contour activation is direction-agnostic
    m2 = _wsig(
        0.35 * torch.abs(h3(_SHARPNESS, 4, 8, 0))  # |sharpness velocity| ~125ms
        + 0.35 * h3(_PITCH_HEIGHT, 3, 0, 2)          # pitch_height value ~100ms
        + 0.30 * e2                                   # contour_complexity from E-layer
    )

    return m0, m1, m2
