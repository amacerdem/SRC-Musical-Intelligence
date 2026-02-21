"""BCH M-Layer — Temporal Integration (4D).

Multi-scale temporal consolidation via H³ sliding-window morphologies.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/BCH-temporal-integration.md

Outputs:
    M0: Consonance Memory       [0, 1]
    M1: Pitch Memory            [0, 1]
    M2: Tonal Memory            [0, 1]
    M3: Spectral Memory         [0, 1]
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_ROUGH = 0
_PLEAS = 4          # sensory_pleasantness
_INHARM = 5
_HDEV = 6           # harmonic_deviation
_TRIST1 = 18
_TRIST2 = 19
_TRIST3 = 20
_PCE = 38
_PITCHSAL = 39
_KEYCLAR = 51       # key_clarity
_TONALSTAB = 60     # tonal_stability
_COUPLING = 41      # cross-domain coupling


def compute_temporal_integration(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute M-layer: 4D temporal integration from H³ + R³.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.

    Returns:
        Tuple of (M0, M1, M2, M3), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # Coupling (consonance × timbre interaction)
    coupling = h3(_COUPLING, 3, 0, 2)

    # M0: Consonance Memory
    m0 = (
        0.20 * (1.0 - h3(_ROUGH, 0, 0, 2))
        + 0.15 * (1.0 - h3(_ROUGH, 3, 1, 2))
        + 0.10 * (1.0 - h3(_ROUGH, 6, 18, 0))
        + 0.10 * r3(_PLEAS)
        + 0.10 * coupling
        + 0.05 * h3(_ROUGH, 6, 14, 2)
        + 0.15 * h3(_PITCHSAL, 3, 0, 2)
        + 0.15 * (1.0 - h3(_PCE, 0, 0, 2))
    )

    # M1: Pitch Memory
    m1 = (
        0.25 * h3(_PITCHSAL, 0, 0, 2)
        + 0.20 * h3(_PITCHSAL, 3, 0, 2)
        + 0.15 * h3(_PITCHSAL, 6, 0, 2)
        + 0.15 * (1.0 - h3(_INHARM, 0, 0, 2))
        + 0.10 * (1.0 - h3(_INHARM, 3, 18, 0))
        + 0.15 * (1.0 - h3(_PCE, 3, 1, 2))
    )

    # M2: Tonal Memory
    m2 = (
        0.20 * h3(_KEYCLAR, 3, 0, 2)
        + 0.20 * h3(_KEYCLAR, 3, 1, 2)
        + 0.20 * h3(_KEYCLAR, 6, 0, 2)
        + 0.20 * h3(_TONALSTAB, 3, 0, 2)
        + 0.20 * h3(_TONALSTAB, 6, 1, 0)
    )

    # M3: Spectral Memory
    trist1_h = h3(_TRIST1, 0, 0, 2)
    trist2_h = h3(_TRIST2, 0, 0, 2)
    trist3_h = h3(_TRIST3, 0, 0, 2)
    trist_balance_h = (1.0 - torch.stack(
        [trist1_h, trist2_h, trist3_h], dim=-1,
    ).std(dim=-1)).clamp(0, 1)
    m3 = (
        0.25 * trist_balance_h
        + 0.25 * (1.0 - h3(_HDEV, 0, 0, 2))
        + 0.25 * (1.0 - h3(_HDEV, 3, 1, 0))
        + 0.25 * (1.0 - h3(_INHARM, 12, 1, 0))
    )

    return m0, m1, m2, m3
