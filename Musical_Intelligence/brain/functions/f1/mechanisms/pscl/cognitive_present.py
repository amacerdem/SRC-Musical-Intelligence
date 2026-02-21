"""PSCL P-Layer — Cognitive Present (4D).

Cortical integration of pitch salience signals for the present moment.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/PSCL-cognitive-present.md

Outputs:
    P0: Pitch Prominence Signal      [0, 1]
    P1: HG Cortical Response         [0, 1]
    P2: Periodicity Clarity          [0, 1]
    P3: Salience Hierarchy           [0, 1]
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_INHARM = 5
_TONAL = 14
_CLARITY = 15
_PITCHSAL = 39
_CONC = 24
_AUTOCORR = 17


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute P-layer: 4D cognitive present from R³ + H³ + E + M.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        e_outputs: Tuple of (E0, E1, E2, E3) from extraction.
        m_outputs: Tuple of (M0, M1, M2, M3) from temporal integration.

    Returns:
        Tuple of (P0, P1, P2, P3), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    e0, e1, e2, e3 = e_outputs
    m0, m1, m2, m3 = m_outputs

    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # P0: Pitch Prominence Signal
    p0 = (
        0.25 * e0
        + 0.25 * m0
        + 0.20 * m3
        + 0.15 * r3(_PITCHSAL)
        + 0.15 * h3(_PITCHSAL, 6, 0, 2)
    )

    # P1: HG Cortical Response
    p1 = (
        0.30 * e1
        + 0.25 * m1
        + 0.20 * h3(_PITCHSAL, 3, 0, 2)
        + 0.15 * (1.0 - h3(_INHARM, 3, 0, 2))
        + 0.10 * h3(_CLARITY, 3, 0, 2)
    )

    # P2: Periodicity Clarity
    p2 = (
        0.30 * e3
        + 0.25 * h3(_CONC, 6, 14, 0)
        + 0.25 * h3(_AUTOCORR, 3, 0, 2)
        + 0.20 * r3(_TONAL)
    )

    # P3: Salience Hierarchy
    p3 = (
        0.35 * e2
        + 0.25 * m2
        + 0.25 * m0
        + 0.15 * e0
    )

    return p0, p1, p2, p3
