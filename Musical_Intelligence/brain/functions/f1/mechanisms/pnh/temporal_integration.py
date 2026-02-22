"""PNH M-Layer — Mathematical Model (2D).

Two computed quantities from the harmonic encoding:

  M0: ratio_complexity   — Normalized log₂(n×d) proxy
  M1: neural_activation  — Predicted BOLD signal (ratio × conflict)

H3 consumed:
    (6, 14, 0, 0)  harmonic_deviation value H14 L0 — template mismatch

R3 consumed:
    [0] roughness         — sensory dissonance
    [5] inharmonicity     — ratio complexity
    [6] harmonic_deviation — error from ideal harmonics

See Docs/C³/Models/IMU-α2-PNH/PNH.md §6.1
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_HARM_DEV_H14 = (6, 14, 0, 0)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_INHARM = 5
_HARM_DEV = 6


def compute_temporal_integration(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D mathematical model from R3/H3 + H-layer.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(H0, H1, H2)`` each ``(B, T)``.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    h0, h1, _h2 = e_outputs

    roughness = r3_features[:, :, _ROUGHNESS]
    inharm = r3_features[:, :, _INHARM]
    harm_dev = r3_features[:, :, _HARM_DEV]
    harm_dev_h14 = h3_features[_HARM_DEV_H14]

    # M0: Ratio Complexity — normalized log₂(n×d) proxy
    # σ((roughness + inharmonicity + harmonic_deviation) / 3)
    m0 = torch.sigmoid(
        (roughness + inharm + 0.50 * harm_dev + 0.50 * harm_dev_h14) / 3.0
    )

    # M1: Neural Activation — predicted BOLD signal
    # Ratio encoding × conflict → IFG/ACC activation
    m1 = (h0 * h1).clamp(0.0, 1.0)

    return m0, m1
