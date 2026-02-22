"""IACM M-Layer — Temporal Integration (3D).

Three composite signals integrating E-layer with temporal context:

  M0: attention_capture      — Inharmonicity-driven attention strength [0, 1]
  M1: approx_entropy         — Spectral entropy / noise estimate [0, 1]
  M2: object_perception_or   — Object-level perception override [0, 1]

H3 consumed:
    (14, 1, 1, 2)   tonalness mean H1 L2           — smoothed tonal state 50ms
    (16, 0, 0, 2)   spectral_flatness value H0 L2  — noise proxy (reused)
    (14, 0, 0, 2)   tonalness value H0 L2          — instant tonal/noisy (reused)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/iacm/IACM-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_TONALNESS_MEAN_50 = (14, 1, 1, 2)
_FLATNESS_H0 = (16, 0, 0, 2)
_TONALNESS_H0 = (14, 0, 0, 2)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from E-layer + H3.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``.
    """
    e0, e1, _e2 = e_outputs

    tonalness_mean_50 = h3_features[_TONALNESS_MEAN_50]
    flatness_25ms = h3_features[_FLATNESS_H0]
    tonalness_25ms = h3_features[_TONALNESS_H0]

    # M0: Attention capture — inharmonicity-driven capture strength
    # Albouy 2017: pitch deviance triggers automatic attention
    m0 = torch.sigmoid(
        0.50 * e0 + 0.50 * (1.0 - tonalness_mean_50)
    )

    # M1: Approximate entropy — spectral noise / irregularity estimate
    # Koelsch 2019: entropy-based salience computation
    m1 = torch.sigmoid(
        0.50 * flatness_25ms + 0.50 * (1.0 - tonalness_25ms)
    )

    # M2: Object perception override — scene parsing from segregation + entropy
    # Herrmann 2015: object segregation modulated by spectral regularity
    m2 = torch.sigmoid(
        0.50 * e1 + 0.50 * m1
    )

    return m0, m1, m2
