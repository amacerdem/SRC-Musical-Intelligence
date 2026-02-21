"""BCH P-Layer — Cognitive Present (4D).

Multi-source integration for the perceptual present moment.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/BCH-cognitive-present.md

Outputs:
    P0: Consonance Signal       [0, 1]
    P1: Template Match          [0, 1]
    P2: Neural Pitch            [0, 1]
    P3: Tonal Context           [0, 1]
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_ROUGH = 0
_SETH = 1           # sethares_dissonance
_PLEAS = 4          # sensory_pleasantness
_INHARM = 5
_HDEV = 6           # harmonic_deviation
_TONAL = 14
_AUTOCORR = 17
_PCE = 38
_PITCHSAL = 39
_KEYCLAR = 51
_TONALSTAB = 60


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute P-layer: 4D cognitive present from R³ + H³ + E-layer.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        e_outputs: Tuple of (E0, E1, E2, E3) from extraction layer.

    Returns:
        Tuple of (P0, P1, P2, P3), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    e0, _e1, _e2, _e3 = e_outputs

    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # P0: Consonance Signal
    p0 = (
        0.20 * (1.0 - r3(_ROUGH))
        + 0.15 * (1.0 - r3(_SETH))
        + 0.15 * (1.0 - h3(_ROUGH, 3, 1, 2))
        + 0.10 * r3(_PLEAS)
        + 0.10 * (1.0 - r3(_HDEV))
        + 0.10 * (1.0 - h3(_ROUGH, 6, 18, 0))
        + 0.10 * h3(_KEYCLAR, 6, 0, 2)
        + 0.10 * (1.0 - h3(_PCE, 3, 1, 2))
    )

    # P1: Template Match
    p1 = (
        0.15 * h3(2, 0, 0, 2)      # helmholtz_kang
        + 0.15 * h3(2, 3, 1, 2)
        + 0.15 * h3(3, 0, 0, 2)    # stumpf_fusion
        + 0.10 * h3(3, 6, 1, 0)
        + 0.15 * (1.0 - h3(_HDEV, 0, 0, 2))
        + 0.10 * (1.0 - r3(_HDEV))
        + 0.10 * h3(_KEYCLAR, 3, 0, 2)
        + 0.10 * r3(_TONALSTAB)
    )

    # P2: Neural Pitch
    p2 = (
        0.25 * e0
        + 0.15 * r3(_TONAL)
        + 0.15 * (1.0 - h3(_INHARM, 0, 0, 2))
        + 0.10 * r3(_AUTOCORR)
        + 0.10 * (1.0 - h3(_INHARM, 3, 18, 0))
        + 0.15 * h3(_PITCHSAL, 0, 0, 2)
        + 0.10 * (1.0 - r3(_PCE))
    )

    # P3: Tonal Context
    p3 = (
        0.25 * h3(_KEYCLAR, 3, 0, 2)
        + 0.25 * h3(_KEYCLAR, 6, 0, 2)
        + 0.25 * h3(_TONALSTAB, 3, 0, 2)
        + 0.25 * r3(_TONALSTAB)
    )

    return p0, p1, p2, p3
