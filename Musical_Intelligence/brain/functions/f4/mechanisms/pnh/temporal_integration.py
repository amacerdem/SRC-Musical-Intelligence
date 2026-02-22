"""PNH M-Layer — Temporal Integration (2D).

Two composite signals integrating H-layer with temporal context:

  M0: ratio_complexity_norm  — Normalized log2(n*d) proxy [0, 1]
  M1: neural_activation      — Predicted BOLD signal across ratio-sensitive ROIs [0, 1]

H3 consumed:
    (0, 18, 18, 0)  roughness trend H18 L0            — dissonance trajectory (2s)
    (3, 14, 1, 2)   stumpf_fusion mean H14 L2         — fusion stability (700ms)
    (4, 10, 0, 2)   sensory_pleasantness value H10 L2 — current consonance (400ms)
    (14, 14, 2, 0)  tonalness std H14 L0              — purity variation (700ms)
    (6, 14, 0, 0)   harmonic_deviation value H14 L0   — template mismatch (700ms)

R3 consumed:
    [0]  roughness            — critical-band beating
    [5]  inharmonicity        — deviation from harmonic series
    [6]  harmonic_deviation   — partial misalignment

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pnh/PNH-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_TREND_2S = (0, 18, 18, 0)
_FUSION_MEAN_700MS = (3, 14, 1, 2)
_PLEASANT_VAL_400MS = (4, 10, 0, 2)
_TONALNESS_STD_700MS = (14, 14, 2, 0)
_HARMDEV_VAL_700MS = (6, 14, 0, 0)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_INHARMONICITY = 5
_HARMONIC_DEV = 6


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    h_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from H-layer + H3 + R3.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h_outputs: ``(H0, H1, H2)`` each ``(B, T)``.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    h0, _h1, h2 = h_outputs

    # -- R3 slices -------------------------------------------------------------
    roughness = r3_features[..., _ROUGHNESS]           # (B, T)
    inharmonicity = r3_features[..., _INHARMONICITY]   # (B, T)
    harmonic_dev = r3_features[..., _HARMONIC_DEV]     # (B, T)

    # -- H3 lookups ------------------------------------------------------------
    roughness_trend = h3_features[_ROUGHNESS_TREND_2S]     # (B, T)
    fusion_mean = h3_features[_FUSION_MEAN_700MS]          # (B, T)
    consonance_val = h3_features[_PLEASANT_VAL_400MS]      # (B, T)
    tonalness_std = h3_features[_TONALNESS_STD_700MS]      # (B, T)
    harmdev_val = h3_features[_HARMDEV_VAL_700MS]          # (B, T)

    # -- M0: Ratio complexity (normalized) ------------------------------------
    # Bidelman & Krishnan 2009: NPS ordering matches log2(n*d)
    # Plomp & Levelt 1965: roughness proportional to ratio complexity
    m0 = torch.sigmoid(
        (roughness + inharmonicity + harmonic_dev) / 3.0
    )

    # -- M1: Neural activation (predicted BOLD) --------------------------------
    # Sarasso et al. 2019: aesthetic judgment eta_p^2=0.685; N1 eta_p^2=0.225
    # harmony = fusion stability as harmonic context proxy
    # training = expertise modulation from H2
    harmony = fusion_mean
    ratio_complexity = h0
    inverse_consonance = 1.0 - consonance_val
    training_level = h2

    m1 = torch.sigmoid(
        harmony * ratio_complexity * inverse_consonance * training_level
    )

    return m0, m1
