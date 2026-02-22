"""PCCR F-Layer — Forecast (3D).

Trend extrapolation for pitch-class chroma signals.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/pccr/PCCR-forecast.md

Outputs:
    F0: Chroma Continuation Signal      [0, 1]
    F1: Chroma Transition Likelihood    [0, 1]
    F2: Chroma Resolution Direction     [0, 1]
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_TONAL = 14          # tonalness
_PITCH_H = 37        # pitch_height
_PCE = 38            # pitch_class_entropy
_PITCHSAL = 39       # pitch_salience


def compute_forecast(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: 3D forecast from P+M outputs + H³.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        p_outputs: Tuple of (P0, P1, P2).
        m_outputs: Tuple of (M0,).

    Returns:
        Tuple of (F0, F1, F2), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    p0, _p1, _p2 = p_outputs
    (m0,) = m_outputs

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # F0: Chroma Continuation Signal
    f0 = (
        0.30 * (1.0 - h3(_PCE, 6, 18, 0))         # low PCE trend → stable
        + 0.25 * h3(_TONAL, 6, 1, 1)                # expected tonalness
        + 0.25 * h3(_PITCHSAL, 6, 1, 1)             # expected pitch salience
        + 0.20 * m0                                   # current stability
    )

    # F1: Chroma Transition Likelihood
    f1 = (
        0.35 * h3(_PCE, 6, 18, 0)                   # PCE trend ↑ = change
        + 0.30 * h3(_PITCH_H, 6, 8, 0)              # pitch height velocity
        + 0.20 * (1.0 - h3(_PCE, 6, 1, 1))          # high expected PCE
        + 0.15 * h3(_PCE, 6, 0, 2)                   # current PCE level
    )

    # F2: Chroma Resolution Direction
    f2 = (
        0.30 * (1.0 - h3(_PCE, 6, 1, 1))            # expected lower PCE
        + 0.25 * h3(_TONAL, 6, 1, 1)                 # expected tonalness
        + 0.25 * p0                                    # current identity strength
        + 0.20 * h3(_PITCH_H, 6, 1, 1)               # register prediction
    )

    return f0, f1, f2
