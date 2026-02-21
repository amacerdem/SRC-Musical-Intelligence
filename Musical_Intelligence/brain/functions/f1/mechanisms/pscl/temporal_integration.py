"""PSCL M-Layer — Temporal Integration (4D).

Multi-scale temporal consolidation at cortical pitch processing timescales.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/PSCL-temporal-integration.md

M3 is the BCH integration channel — where brainstem pitch meets cortical processing.

Outputs:
    M0: Salience Sustained       [0, 1]
    M1: Spectral Coherence       [0, 1]
    M2: Tonal Salience Context   [0, 1]
    M3: BCH Integration          [0, 1]
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_TONAL = 14
_AUTOCORR = 17
_TRIST1 = 18
_ENTROPY = 22
_CONC = 24
_CHROMA_START = 25
_CHROMA_END = 37
_PITCH_H = 37       # pitch_height
_PITCHSAL = 39

# ── BCH relay output indices ─────────────────────────────────────────
_BCH_E0 = 0         # E0:nps
_BCH_E1 = 1         # E1:harmonicity
_BCH_P0 = 8         # P0:consonance_signal
_BCH_F1 = 13        # F1:pitch_forecast


def compute_temporal_integration(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    bch_output: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute M-layer: 4D temporal integration from H³ + R³ + BCH.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        bch_output: ``(B, T, 16)`` BCH relay output.

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

    # M0: Salience Sustained
    m0 = (
        0.25 * h3(_TONAL, 6, 1, 0)
        + 0.25 * h3(_PITCHSAL, 6, 1, 0)
        + 0.20 * h3(_AUTOCORR, 6, 1, 0)
        + 0.15 * h3(_TRIST1, 6, 1, 0)
        + 0.15 * h3(_CONC, 6, 14, 0)
    )

    # M1: Spectral Coherence
    m1 = (
        0.30 * h3(_AUTOCORR, 3, 0, 2)
        + 0.30 * h3(_TONAL, 3, 0, 2)
        + 0.20 * h3(_TRIST1, 3, 0, 2)
        + 0.20 * (1.0 - h3(_ENTROPY, 6, 1, 0))
    )

    # M2: Tonal Salience Context
    chroma = r3_features[:, :, _CHROMA_START:_CHROMA_END]  # (B, T, 12)
    chroma_peak = chroma.max(dim=-1).values  # (B, T)
    m2 = (
        0.35 * chroma_peak
        + 0.30 * r3(_PITCHSAL)
        + 0.20 * (1.0 - r3(_ENTROPY))
        + 0.15 * r3(_PITCH_H)
    )

    # M3: BCH Integration
    m3 = (
        0.40 * bch_output[:, :, _BCH_E0]
        + 0.30 * bch_output[:, :, _BCH_E1]
        + 0.20 * bch_output[:, :, _BCH_P0]
        + 0.10 * bch_output[:, :, _BCH_F1]
    )

    return m0, m1, m2, m3
