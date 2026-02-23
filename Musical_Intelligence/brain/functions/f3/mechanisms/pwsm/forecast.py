"""PWSM F-Layer -- Forecast (2D).

Two forward predictions for precision-weighted salience:

  F0: mmn_presence_pred   -- Predicted MMN presence (deviance detection)
  F1: context_reliability -- Predicted context reliability for future precision

H3 consumed:
    (37, 16, 21, 2)  pitch_height contrast H16 bidi -- pitch range for MMN
    (37, 16, 17, 2)  pitch_height peaks H16 bidi    -- pitch events for context

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/pwsm/PWSM-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PITCH_CONTRAST_H16 = (37, 16, 21, 2)
_PITCH_PEAKS_H16 = (37, 16, 17, 2)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D forecast from H3 + E/M/P outputs.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f19, f20, f21)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1)`` each ``(B, T)``.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    f19, f20, f21 = e_outputs
    m0, m1 = m_outputs
    p0, p1 = p_outputs

    B = f19.shape[0]
    T = f19.shape[1] if f19.dim() > 1 else 1
    device = f19.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    pitch_contrast = h3_features.get(_PITCH_CONTRAST_H16, zero)
    pitch_peaks = h3_features.get(_PITCH_PEAKS_H16, zero)

    # F0: MMN Presence Prediction -- predicted deviance detection
    # Garrido 2009: MMN presence depends on precision and PE magnitude
    f0 = torch.sigmoid(
        0.30 * p0
        + 0.25 * pitch_contrast
        + 0.25 * m0
        + 0.20 * (1.0 - f20)
    )

    # F1: Context Reliability -- predicted future context reliability
    # Friston 2005: precision tracks learned context reliability
    f1 = torch.sigmoid(
        0.30 * p1
        + 0.25 * f21
        + 0.25 * pitch_peaks
        + 0.20 * m1
    )

    return f0, f1
