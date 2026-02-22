"""PCCR P-Layer — Cognitive Present (3D).

Multi-source integration for pitch-class encoding at the perceptual present.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/pccr/PCCR-cognitive-present.md

Dependencies:
    - BCH (Depth 0): E1:harmonicity [idx 1], E2:hierarchy [idx 2]
    - PSCL (Depth 1): P0:pitch_prominence_sig [idx 8], P2:periodicity_clarity [idx 10]

Outputs:
    P0: Chroma Identity Signal          [0, 1]
    P1: Octave Equivalence Index        [0, 1]
    P2: Chroma Salience                 [0, 1]
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_PCE = 38            # pitch_class_entropy

# ── Upstream output indices ──────────────────────────────────────────
_BCH_E1 = 1          # BCH E1:harmonicity
_BCH_E2 = 2          # BCH E2:hierarchy
_PSCL_P0 = 8         # PSCL P0:pitch_prominence_sig
_PSCL_P2 = 10        # PSCL P2:periodicity_clarity


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: 3D cognitive present from R³ + H³ + E + M + upstream.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        e_outputs: Tuple of (E0, E1, E2, E3) from extraction.
        m_outputs: Tuple of (M0,) from temporal integration.
        upstream_outputs: ``{"BCH": (B, T, 16), "PSCL": (B, T, 16)}``.

    Returns:
        Tuple of (P0, P1, P2), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    e0, e1, e2, e3 = e_outputs
    (m0,) = m_outputs

    bch = upstream_outputs["BCH"]
    pscl = upstream_outputs["PSCL"]

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # P0: Chroma Identity Signal
    p0 = (
        0.25 * e0
        + 0.20 * e1
        + 0.15 * e3
        + 0.15 * m0
        + 0.15 * pscl[:, :, _PSCL_P0]
        + 0.10 * pscl[:, :, _PSCL_P2]
    )

    # P1: Octave Equivalence Index
    p1 = (
        0.40 * e2
        + 0.25 * bch[:, :, _BCH_E1]
        + 0.20 * e1
        + 0.15 * (1.0 - h3(_PCE, 6, 0, 2))
    )

    # P2: Chroma Salience
    p2 = (
        0.30 * p0
        + 0.25 * pscl[:, :, _PSCL_P0]
        + 0.25 * e0
        + 0.20 * bch[:, :, _BCH_E2]
    )

    return p0, p1, p2
