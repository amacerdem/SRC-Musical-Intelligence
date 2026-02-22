"""PCCR M-Layer — Temporal Integration (1D).

Chroma stability over time via H³ sliding-window morphologies.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/pccr/PCCR-temporal-integration.md

Outputs:
    M0: Chroma Stability        [0, 1]
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_TONAL = 14          # tonalness
_PCE = 38            # pitch_class_entropy
_PITCHSAL = 39       # pitch_salience


def compute_temporal_integration(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor]:
    """Compute M-layer: 1D temporal chroma stability from H³.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.

    Returns:
        Tuple of (M0,), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # M0: Chroma Stability
    m0 = (
        0.30 * (1.0 - h3(_PCE, 12, 1, 0))       # low PCE mean 525ms
        + 0.25 * h3(_TONAL, 6, 0, 2)              # tonalness at 200ms
        + 0.25 * h3(_PITCHSAL, 12, 1, 0)           # pitch_salience mean 525ms
        + 0.20 * h3(_TONAL, 12, 14, 0)             # tonalness periodicity 525ms
    )

    return (m0,)
