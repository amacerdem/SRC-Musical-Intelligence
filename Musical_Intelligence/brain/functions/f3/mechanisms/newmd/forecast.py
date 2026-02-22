"""NEWMD F-Layer -- Forecast (2D).

Forward predictions for entrainment-WM dissociation dynamics:
  F0: performance_pred   (predicted performance from WM capacity and paradox)
  F1: adaptation_pred    (predicted adaptation from cross-stream stability and WM)

F0 predicts overall performance: high WM capacity (E1) + low paradox (1-M0)
+ balanced dual-route (M1) + cross-stream stability. When paradox is low
and WM is high, performance is predicted to be strong (Tierney 2014).

F1 predicts adaptation ability: high cross-stream stability + WM capacity
+ dual-route balance. Stable cross-stream coupling means the system can
adapt to changing rhythmic patterns (Grahn 2009).

H3 demands consumed:
  x_l4l5: (33,20,19,0) -- cross-stream stability 5s L0 (long stability)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/newmd/
Tierney 2014: behavioral+EEG, N=30.
Grahn 2009: fMRI, N=18.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CROSS_STREAM_STABILITY_5S = (33, 20, 19, 0)  # x_l4l5 stability 5s L0


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: performance and adaptation predictions.

    F0 predicts performance from WM capacity (E1), inverted paradox
    magnitude (1-M0), dual-route balance (M1), and cross-stream
    stability. Low paradox + high WM + high stability = strong
    predicted performance (Tierney 2014).

    F1 predicts adaptation from cross-stream stability (primary driver),
    WM capacity (E1), and dual-route balance (M1). High stability
    enables flexible adaptation to rhythmic changes (Grahn 2009).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``
    """
    _e0, e1, _e2, _e3 = e
    m0, m1 = m

    cross_stream_stability_5s = h3_features[_CROSS_STREAM_STABILITY_5S]  # (B, T)

    # -- F0: Performance Prediction --
    # Predicted performance: high WM capacity + low paradox + balanced routes
    # + stable cross-stream coupling. Tierney 2014: beat synchronization
    # accuracy predicted by combination of entrainment and WM measures.
    f0 = torch.sigmoid(
        0.35 * e1
        + 0.30 * (1.0 - m0)
        + 0.20 * m1
        + 0.15 * cross_stream_stability_5s
    )

    # -- F1: Adaptation Prediction --
    # Predicted adaptation ability: cross-stream stability is the primary
    # driver, supported by WM capacity and dual-route balance.
    # Grahn 2009: SMA and putamen activation predict rhythmic adaptation.
    f1 = torch.sigmoid(
        0.40 * cross_stream_stability_5s
        + 0.30 * e1
        + 0.30 * m1
    )

    return f0, f1
