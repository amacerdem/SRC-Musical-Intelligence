"""BCH F-Layer — Forecast (4D).

Trend extrapolation combining E+M+P outputs with H³ forward demands.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/BCH-forecast.md

Outputs:
    F0: Consonance Forecast     [0, 1]
    F1: Pitch Forecast          [0, 1]
    F2: Tonal Forecast          [0, 1]
    F3: Interval Forecast       [0, 1]
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_ROUGH = 0
_PLEAS = 4
_INHARM = 5
_PCE = 38
_PITCHSAL = 39
_KEYCLAR = 51
_TONALSTAB = 60
_COUPLING = 41


def compute_forecast(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute F-layer: 4D forecast from E+M+P outputs + H³.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        e_outputs: Tuple of (E0, E1, E2, E3).
        m_outputs: Tuple of (M0, M1, M2, M3).
        p_outputs: Tuple of (P0, P1, P2, P3).

    Returns:
        Tuple of (F0, F1, F2, F3), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    e0, e1, _e2, e3 = e_outputs
    m0, m1, m2, _m3 = m_outputs
    p0, _p1, p2, p3 = p_outputs

    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # Coupling
    coupling = h3(_COUPLING, 3, 0, 2)

    # E1 trist_balance (recompute for F3)
    trist_std = torch.stack(
        [r3_features[:, :, 18], r3_features[:, :, 19],
         r3_features[:, :, 20]], dim=-1,
    ).std(dim=-1)
    trist_balance = (1.0 - trist_std).clamp(0, 1)

    # F0: Consonance Forecast
    f0 = (
        0.15 * e1
        + 0.15 * m0
        + 0.20 * p0
        + 0.10 * coupling
        + 0.10 * e3
        + 0.10 * r3(_PLEAS)
        + 0.10 * h3(_KEYCLAR, 12, 1, 0)
        + 0.10 * h3(_TONALSTAB, 6, 1, 0)
    )

    # F1: Pitch Forecast
    f1 = (
        0.20 * e0
        + 0.20 * m1
        + 0.20 * p2
        + 0.15 * h3(_ROUGH, 6, 14, 2)
        + 0.15 * h3(_PITCHSAL, 6, 0, 2)
        + 0.10 * (1.0 - h3(_PCE, 0, 0, 2))
    )

    # F2: Tonal Forecast
    f2 = (
        0.25 * m2
        + 0.25 * p3
        + 0.15 * h3(_KEYCLAR, 12, 1, 0)
        + 0.15 * h3(_TONALSTAB, 18, 1, 0)
        + 0.10 * h3(_KEYCLAR, 6, 1, 1)
        + 0.10 * h3(_TONALSTAB, 6, 1, 1)
    )

    # F3: Interval Forecast
    f3 = (
        0.20 * h3(2, 12, 1, 0)     # helmholtz memory 525ms
        + 0.15 * h3(3, 6, 1, 0)    # stumpf memory 200ms
        + 0.15 * (1.0 - h3(_ROUGH, 6, 18, 0))
        + 0.10 * (1.0 - h3(_INHARM, 3, 18, 0))
        + 0.10 * trist_balance
        + 0.10 * coupling
        + 0.10 * h3(_KEYCLAR, 6, 0, 2)
        + 0.10 * h3(_TONALSTAB, 6, 1, 0)
    )

    return f0, f1, f2, f3
