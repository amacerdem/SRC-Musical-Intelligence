"""MPG P-Layer — Cognitive Present (2D).

Relay output dimensions consumed by the C³ kernel's MPG relay wrapper.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/mpg/MPG-cognitive-present.md

These are the primary outputs read by downstream models:
    P0: onset_state  → kernel relay (SNEM, SDD, EDNR, STU)
    P1: contour_state → kernel relay (CDMR, STU)

Outputs:
    P0: onset_state      [0, 1]  Pitch-processing onset-locked activity
    P1: contour_state    [0, 1]  Pitch-processing contour tracking activity
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_ONSET = 11           # onset_strength
_BEAT_STR = 42        # beat_strength (rhythmic context)


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: 2D relay outputs from E + M layers.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        e_outputs: Tuple of (E0, E1, E2, E3) from extraction.
        m_outputs: Tuple of (M0, M1, M2) from temporal integration.

    Returns:
        Tuple of (P0, P1), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    e0, e1, e2, e3 = e_outputs
    _m0, m1, m2 = m_outputs

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # P0: onset_state — pitch-processing onset-locked activity
    #     High when posterior dominance is strong (gradient_ratio → 1.0)
    #     Rupp 2022: posterior AC response to melodic onset
    p0 = (
        0.35 * e0                           # onset_posterior
        + 0.25 * m1                         # posterior_activity
        + 0.20 * e3                         # gradient_ratio (posterior dominance)
        + 0.20 * h3(_ONSET, 3, 1, 2)       # onset_strength mean ~100ms
    )

    # P1: contour_state — pitch-processing contour tracking activity
    #     High when anterior dominance is strong (gradient_ratio → 0.0)
    #     Rupp 2022: anterior AC response to melodic contour
    p1 = (
        0.35 * e1                           # sequence_anterior
        + 0.25 * m2                         # anterior_activity
        + 0.20 * e2                         # contour_complexity
        + 0.20 * (1.0 - e3)                # inverse gradient (anterior dominance)
    )

    return p0, p1
