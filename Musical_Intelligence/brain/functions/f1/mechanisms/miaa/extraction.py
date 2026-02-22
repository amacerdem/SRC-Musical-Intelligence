"""MIAA E-Layer — Extraction (3D).

Auditory cortex imagery features from R³ + H³.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/miaa/MIAA-extraction.md

Uses sigmoid activation following Kraemer et al. 2005 imagery model.
Coefficient saturation rule: |wi| sum ≤ 1.0 per sigmoid.

Outputs:
    E0: imagery_activation        [0, 1]  AC activation during musical imagery
    E1: familiarity_enhancement   [0, 1]  BA22 enhancement for familiar music
    E2: a1_modulation             [0, 1]  Primary AC involvement (instrumental > lyrics)
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
_INHARM = 5           # inharmonicity (A group)
_TONALNESS = 14       # tonalness (C group)
_CLARITY = 15         # clarity (C group, was "spectral_flatness" inverted)
_SPECTRAL_AUTO = 17   # spectral_autocorrelation (C group, replaces x_l5l7)


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: 3D imagery features with sigmoid activation.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.

    Returns:
        Tuple of (E0, E1, E2), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    # ── Tristimulus balance (H³ at H2 gamma-rate, bidirectional) ─────
    # Uniform distribution → balance=1.0; unbalanced → lower
    trist1 = h3(18, 2, 0, 2)    # tristimulus1 fundamental energy
    trist2 = h3(19, 2, 0, 2)    # tristimulus2 mid-harmonic
    trist3 = h3(20, 2, 0, 2)    # tristimulus3 high-harmonic
    trist_stack = torch.stack([trist1, trist2, trist3], dim=-1)  # (B, T, 3)
    trist_balance = 1.0 - torch.std(trist_stack, dim=-1, correction=0)

    # E0: Imagery Activation — AC activation during musical imagery
    #     Kraemer 2005: AC active in silence (F(1,14)=48.92, p<.0001)
    #     Tonalness × instrument identity drive template-based imagery.
    #     Tristimulus balance provides harmonic template structure.
    #     Spectral autocorrelation captures cross-band binding.
    #     Coefficients: 0.40 + 0.30 + 0.30 = 1.0
    tonalness_val = h3(14, 2, 0, 2)   # tonalness at gamma-rate
    e0 = torch.sigmoid(
        0.40 * tonalness_val * trist_balance   # tonal identity
        + 0.30 * trist_balance                 # spectral envelope
        + 0.30 * r3(_SPECTRAL_AUTO)            # cross-band binding
    )

    # E1: Familiarity Enhancement — familiar > unfamiliar in BA22
    #     Kraemer 2005: p<0.0001 (n=15); Halpern 2004: r=0.84 behavioral
    #     Clarity (inv. spectral flatness) × sustained tonalness = strong template.
    #     Warmth contributes to template richness.
    #     Spectral autocorrelation as plasticity proxy (self-similar → memorable).
    #     Coefficients: 0.40 + 0.30 + 0.30 = 1.0
    tonalness_mean = h3(14, 5, 1, 0)  # tonalness mean at alpha-beta
    warmth_mean = h3(12, 5, 1, 0)     # warmth mean at alpha-beta
    e1 = torch.sigmoid(
        0.40 * r3(_CLARITY) * tonalness_mean   # template clarity
        + 0.30 * warmth_mean                   # timbre richness
        + 0.30 * r3(_SPECTRAL_AUTO)            # spectral coherence
    )

    # E2: A1 Modulation — primary AC for instrumentals only
    #     Kraemer 2005: instrumental > lyrics F(1,14)=22.55, p<.0005
    #     Low inharmonicity × high tonalness = acoustic (not semantic) imagery.
    #     Tristimulus balance provides spectral envelope detail.
    #     Loudness context modulates overall activation level.
    #     Coefficients: 0.40 + 0.30 + 0.30 = 1.0
    loudness_mean = h3(10, 8, 1, 0)    # loudness mean at syllable-rate
    e2 = torch.sigmoid(
        0.40 * (1.0 - r3(_INHARM)) * r3(_TONALNESS)  # harmonic + tonal
        + 0.30 * trist_balance                         # spectral envelope
        + 0.30 * loudness_mean                         # intensity context
    )

    return e0, e1, e2
