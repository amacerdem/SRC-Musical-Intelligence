"""PSCL F-Layer — Forecast (4D).

Trend extrapolation for pitch salience signals.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/PSCL-forecast.md

Outputs:
    F0: Pitch Continuation       [0, 1]
    F1: Salience Direction       [-1, 1]  (signed)
    F2: Melody Propagation       [0, 1]
    F3: Register Trajectory      [0, 1]
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_TONAL = 14
_CONC = 24
_PITCH_H = 37
_PITCHSAL = 39

# ── BCH relay output indices ─────────────────────────────────────────
_BCH_F1 = 13        # F1:pitch_forecast


def compute_forecast(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    bch_output: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute F-layer: 4D forecast from P+M outputs + H³ + BCH.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        p_outputs: Tuple of (P0, P1, P2, P3).
        m_outputs: Tuple of (M0, M1, M2, M3).
        bch_output: ``(B, T, 16)`` BCH relay output.

    Returns:
        Tuple of (F0, F1, F2, F3), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    p0, _p1, _p2, _p3 = p_outputs
    _m0, _m1, m2, _m3 = m_outputs

    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # F0: Pitch Continuation
    f0 = (
        0.30 * h3(_TONAL, 6, 18, 0)
        + 0.25 * h3(_PITCHSAL, 6, 18, 0)
        + 0.20 * h3(_TONAL, 6, 1, 1)
        + 0.15 * h3(_PITCHSAL, 6, 1, 1)
        + 0.10 * bch_output[:, :, _BCH_F1]
    )

    # F1: Salience Direction (signed, [-1, 1])
    f1_raw = (
        0.35 * h3(_PITCHSAL, 6, 18, 0)
        + 0.30 * h3(_TONAL, 6, 18, 0)
        + 0.20 * h3(_CONC, 6, 18, 1)
        + 0.15 * h3(_PITCH_H, 6, 8, 0)
    )
    f1 = torch.tanh(f1_raw)

    # F2: Melody Propagation
    f2 = (
        0.30 * p0
        + 0.25 * h3(_PITCH_H, 6, 1, 1)
        + 0.25 * h3(_PITCH_H, 6, 8, 0)
        + 0.20 * m2
    )

    # F3: Register Trajectory
    f3 = (
        0.40 * h3(_PITCH_H, 6, 8, 0)
        + 0.30 * h3(_PITCH_H, 6, 1, 1)
        + 0.30 * r3(_PITCH_H)
    )

    return f0, f1, f2, f3
