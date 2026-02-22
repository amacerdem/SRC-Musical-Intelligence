"""HTP F-Layer — Forecast (2D).

Forward predictions for upcoming musical structure:
  F0: abstract_future_500ms   (high-level structure ~500ms ahead)
  F1: midlevel_future_200ms   (mid-level features ~200ms ahead)

H3 demands consumed:
  tonal_stability:  (60,16,1,0) reused
  sharpness:        (13,4,8,0) reused

See Docs/C3/Models/PCU-a1-HTP/HTP.md §6.1 Layer F.
Cheung et al. 2019: amygdala/hippocampus integrate uncertainty x surprise.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_TONAL_STAB_H16_MEAN = (60, 16, 1, 0)
_SHARPNESS_H4_VEL = (13, 4, 8, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: forward predictions for upcoming structure.

    Abstract future uses high-level prediction lead (E0) + sustained
    tonal stability context. Mid-level future uses mid-level lead (E1)
    + brightness velocity for pitch extrapolation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``
    """
    e0, e1, _e2, _e3 = e

    tonal_stab_mean_1s = h3_features[_TONAL_STAB_H16_MEAN]
    sharpness_vel_125ms = h3_features[_SHARPNESS_H4_VEL]

    # -- F0: Abstract Future (~500ms) --
    # Predicted high-level structure based on current abstract prediction
    # lead and long-range tonal stability context.
    f0 = torch.sigmoid(0.50 * e0 + 0.50 * tonal_stab_mean_1s)

    # -- F1: Midlevel Future (~200ms) --
    # Predicted mid-level features based on current perceptual prediction
    # lead and brightness velocity (extrapolated pitch/timbre trajectory).
    f1 = torch.sigmoid(0.50 * e1 + 0.50 * sharpness_vel_125ms)

    return f0, f1
