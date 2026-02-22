"""SDNPS P-Layer — Cognitive Present (3D).

Three present-processing dimensions for brainstem pitch salience:

  P0: ffr_encoding         — Brainstem phase-locking strength
  P1: harmonicity_proxy    — Harmonic template match weighted by spectra
  P2: roughness_interference — Invariant roughness signal (stimulus-independent)

H3 consumed:
    (14, 0, 0, 2) tonalness value H0 L2         — pitch clarity (FFR proxy)
    (17, 3, 14, 2) spectral_auto periodicity H3  — harmonic periodicity 100ms

R3 consumed:
    [0] roughness        — roughness signal
    [1] sethares         — psychoacoustic dissonance
    [5] inharmonicity    — spectral deviation

See Docs/C³/Models/SPU-γ1-SDNPS/SDNPS.md §6.1 (Layer P)
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_TONALNESS_H0 = (14, 0, 0, 2)
_AUTOCORR_PERIOD = (17, 3, 14, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SETHARES = 1
_INHARM = 5


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
    trist_balance: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0,)`` each ``(B, T)``.
        trist_balance: ``(B, T)`` pre-computed tristimulus balance.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    # H3 features
    tonalness_h0 = h3_features[_TONALNESS_H0]
    autocorr_period = h3_features[_AUTOCORR_PERIOD]

    # R3 features
    roughness = r3_features[:, :, _ROUGHNESS]
    sethares = r3_features[:, :, _SETHARES]
    inharm = r3_features[:, :, _INHARM]

    # P0: FFR Encoding — brainstem phase-locking strength
    # FFR magnitude correlates with tonalness and harmonic periodicity
    # Bidelman & Krishnan 2009: FFR magnitude ↔ pitch salience
    p0 = torch.sigmoid(0.50 * tonalness_h0 + 0.50 * autocorr_period)

    # P1: Harmonicity Proxy — harmonic template match
    # (1 - inharmonicity) × tristimulus balance
    p1 = (1.0 - inharm) * trist_balance

    # P2: Roughness Interference — stimulus-invariant signal
    # NPS ↔ roughness: r=-0.57 across ALL stimulus types
    # 1 - (roughness + sethares)/2 → high when low roughness
    p2 = 1.0 - (roughness + sethares) / 2.0

    return p0, p1, p2
