"""SDL F-Layer -- Forecast (2D).

Forward predictions for lateralization dynamics:
  F0: network_config_pred   (predicted network configuration, sigmoid [0, 1])
  F1: processing_eff_pred   (predicted processing efficiency, sigmoid [0, 1])

H3 demands consumed:
  x_l0l5:  (25,8,1,0) coupling mean 500ms L0 -- medium binding (for F0)

E/M-layer inputs:
  E2: hemispheric_osc       (oscillatory state, sigmoid)
  M1: salience_demand       (salience demand, sigmoid)

F-layer outputs are purely external (sigmoid [0, 1]) -- no tanh dims.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/sdl/
Poeppel 2003: asymmetric sampling in time.
Zatorre 2002: hemispheric specialization review.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_COUPLING_H8_MEAN = (25, 8, 1, 0)      # coupling mean 500ms L0 -- medium binding


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    m: Tuple[Tensor, Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: forward predictions for lateralization.

    F0 predicts the upcoming network configuration: salience demand (M1)
    combined with coupling mean at 500ms to predict how bilateral
    processing resources will be configured. High salience demand +
    strong coupling -> distributed bilateral network predicted.

    F1 predicts processing efficiency: inverse salience demand (1-M1)
    combined with hemispheric oscillatory state (E2) to predict how
    efficiently the lateralized network will process. Low demand +
    strong oscillatory state -> high efficiency predicted.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        m: ``(M0, M1)`` from temporal integration layer.
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)`` in [0, 1] (sigmoid).
    """
    _m0, m1 = m
    _e0, _e1, e2 = e

    coupling_mean_500ms = h3_features[_COUPLING_H8_MEAN]

    # -- F0: Network Configuration Prediction --
    # Predicted bilateral network configuration: salience demand drives
    # resource allocation; coupling mean captures sustained cross-band
    # binding. High values -> distributed bilateral processing predicted.
    # Zatorre 2002: salience drives hemispheric recruitment.
    f0 = torch.sigmoid(
        0.50 * m1
        + 0.50 * coupling_mean_500ms
    )

    # -- F1: Processing Efficiency Prediction --
    # Predicted processing efficiency: inverse salience demand (low demand
    # = high efficiency) + oscillatory readiness (E2).
    # Poeppel 2003: efficient lateralization when oscillatory state matches
    # input timescale.
    f1 = torch.sigmoid(
        0.50 * (1.0 - m1)
        + 0.50 * e2
    )

    return f0, f1
