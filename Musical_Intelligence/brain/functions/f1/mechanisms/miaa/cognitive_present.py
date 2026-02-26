"""MIAA P-Layer — Cognitive Present (3D).

Relay output dimensions for melody retrieval and continuation.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/miaa/MIAA-cognitive-present.md

These are the primary outputs consumed by downstream models and beliefs:
    P0: melody_retrieval        → timbral_character belief, MEAMN relay
    P1: continuation_prediction → imagery_recognition context
    P2: phrase_structure        → MPG phrase context

Outputs:
    P0: melody_retrieval          [0, 1]  Melody template retrieval strength
    P1: continuation_prediction   [0, 1]  Next-note prediction from template
    P2: phrase_structure          [0, 1]  Phrase boundary awareness during imagery
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_TRIST1 = 18          # tristimulus1
_TRIST2 = 19          # tristimulus2
_TRIST3 = 20          # tristimulus3


def _wsig(x: Tensor) -> Tensor:
    """Wide sigmoid — full [0, 1] dynamic range (gain=5, center=0.35)."""
    return (1.0 + torch.exp(-5.0 * (x - 0.35))).reciprocal()


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: 3D relay outputs from E + M + H³.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        e_outputs: Tuple of (E0, E1, E2) from extraction.
        m_outputs: Tuple of (M0, M1) from temporal integration.

    Returns:
        Tuple of (P0, P1, P2), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    _e0, e1, _e2 = e_outputs
    m0, _m1 = m_outputs

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    # P0: melody_retrieval — template retrieval strength
    #     Combines composite activation, familiarity enhancement,
    #     harmonic instrument identity, and signal clarity.
    #     Halpern 2004: perception-imagery overlap in posterior PT
    #     Coefficients: 0.35 + 0.25 + 0.20 + 0.20 = 1.0
    inharm_val = h3(5, 5, 0, 2)        # inharmonicity at alpha-beta
    clarity_mean = h3(15, 8, 1, 0)     # clarity mean at syllable-rate
    p0 = (
        0.35 * m0                       # composite AC activation
        + 0.25 * e1                     # familiarity enhancement
        + 0.20 * (1.0 - inharm_val)     # harmonic instrument identity
        + 0.20 * clarity_mean           # signal clarity over 300ms
    )

    # P1: continuation_prediction — next-note prediction from template
    #     Tonalness trend × tristimulus stability.
    #     Di Liberto 2021: imagery pitch encoding comparable to perception
    #     Coefficients: 0.50 + 0.50 = 1.0 (inside sigmoid)
    tonalness_mean = h3(14, 5, 1, 0)   # tonalness mean at alpha-beta
    trist_stack = torch.stack([r3(_TRIST1), r3(_TRIST2), r3(_TRIST3)], dim=-1)
    trist_balance = 1.0 - torch.std(trist_stack, dim=-1, correction=0)
    p1 = _wsig(
        0.50 * tonalness_mean
        + 0.50 * trist_balance
    )

    # P2: phrase_structure — phrase boundary awareness during imagery
    #     Spectral change entropy proxies for structural transitions.
    #     High entropy = uncertain spectral evolution = boundary approaching.
    spectral_flux_entropy = h3(21, 8, 13, 0)  # spectral flux entropy at 300ms
    p2 = _wsig(spectral_flux_entropy)

    return p0, p1, p2
