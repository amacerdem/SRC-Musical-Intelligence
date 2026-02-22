"""HTP M-Layer — Temporal Integration (3D).

Latency-normalized prediction strength at each hierarchy level:
  M0: latency_high   (500ms normalized lead time)
  M1: latency_mid    (200ms normalized lead time)
  M2: latency_low    (110ms normalized lead time)

H3 demands consumed:
  tonal_stability:   (60,16,1,0) reused from E-layer
  sharpness:         (13,8,1,0) reused from E-layer
  onset_strength:    (11,1,1,2)

See Docs/C3/Models/PCU-a1-HTP/HTP.md §6.1 Layer M, §7.1 latency function.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_TONAL_STAB_H16_MEAN = (60, 16, 1, 0)
_SHARPNESS_H8_MEAN = (13, 8, 1, 0)
_ONSET_H1_MEAN = (11, 1, 1, 2)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: latency-normalized prediction strengths.

    Each latency dimension integrates the E-layer prediction lead with
    its corresponding sustained feature. Higher values indicate stronger
    prediction at that hierarchy level.

    Golesorkhi et al. 2021: intrinsic neural timescales follow core-periphery
    hierarchy (η² = 0.86). Longer timescales in higher-level areas (DMN/FPN)
    than sensory cortex.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``
    """
    e0, e1, e2, _e3 = e

    tonal_stab_mean_1s = h3_features[_TONAL_STAB_H16_MEAN]
    sharpness_mean_500ms = h3_features[_SHARPNESS_H8_MEAN]
    onset_mean_50ms = h3_features[_ONSET_H1_MEAN]

    # -- M0: Latency High (500ms) --
    # α·pred_high + β·template_match.
    # High-level prediction + long-range tonal stability as template.
    m0 = torch.sigmoid(0.50 * e0 + 0.50 * tonal_stab_mean_1s)

    # -- M1: Latency Mid (200ms) --
    # α·pred_mid + β·pitch_pred.
    # Mid-level prediction + sustained brightness as pitch proxy.
    m1 = torch.sigmoid(0.50 * e1 + 0.50 * sharpness_mean_500ms)

    # -- M2: Latency Low (110ms) --
    # α·pred_low + β·onset_pred.
    # Low-level prediction + onset detection mean.
    m2 = torch.sigmoid(0.50 * e2 + 0.50 * onset_mean_50ms)

    return m0, m1, m2
