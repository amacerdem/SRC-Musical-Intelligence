"""MIAA F-Layer — Forecast (3D).

Imagery predictions for upcoming musical events.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/miaa/MIAA-forecast.md

Uses sigmoid activation: predictions are probability-like values
for upcoming imagery content, AC activation, and recognition.

Outputs:
    F0: melody_continuation_pred  [0, 1]  Predicted imagery content for next phrase
    F1: ac_activation_pred        [0, 1]  Predicted AC activation during upcoming gap
    F2: recognition_pred          [0, 1]  Predicted familiar-match probability
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor


def compute_forecast(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: 3D imagery predictions from E + P + H³.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        e_outputs: Tuple of (E0, E1, E2) from extraction.
        p_outputs: Tuple of (P0, P1, P2) from cognitive_present.

    Returns:
        Tuple of (F0, F1, F2), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    e0, e1, _e2 = e_outputs
    p0, p1, _p2 = p_outputs

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # F0: melody_continuation_pred — predicted imagery content for next phrase
    #     Combines current imagery activation, melody retrieval, and continuation.
    #     Coefficients: 0.50 + 0.30 + 0.20 = 1.0
    f0 = torch.sigmoid(
        0.50 * e0                          # imagery activation
        + 0.30 * p0                        # melody retrieval
        + 0.20 * p1                        # continuation prediction
    )

    # F1: ac_activation_pred — predicted AC activation during upcoming gap
    #     Familiarity drives sustained AC activity during silence.
    #     Kraemer 2005: AC active in silence, especially for familiar music.
    #     Coefficients: 0.60 + 0.40 = 1.0
    f1 = torch.sigmoid(
        0.60 * e1                          # familiarity enhancement
        + 0.40 * e0                        # base imagery activation
    )

    # F2: recognition_pred — predicted familiar-match probability at gap resolution
    #     Spectral autocorrelation (cross-band coherence) and tonal quality
    #     predict whether upcoming sound will match stored template.
    #     Coefficients: 0.50 + 0.30 + 0.20 = 1.0
    spectral_auto_mean = h3(17, 8, 1, 0)  # spectral_auto mean at 300ms
    tonalness_mean = h3(14, 5, 1, 0)      # tonalness mean at alpha-beta
    f2 = torch.sigmoid(
        0.50 * e1                          # familiarity enhancement
        + 0.30 * spectral_auto_mean        # cross-band coherence
        + 0.20 * tonalness_mean            # tonal quality context
    )

    return f0, f1, f2
