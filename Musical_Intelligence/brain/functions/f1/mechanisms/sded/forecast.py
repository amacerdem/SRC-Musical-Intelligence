"""SDED F-Layer — Forecast (3D).

Three forward predictions for dissonance processing:

  F0: dissonance_detection_pred  — Predicted dissonance detection
  F1: behavioral_accuracy_pred   — Predicted behavioral accuracy
  F2: training_effect_pred       — Training effect prediction

H3 consumed:
    (2, 3, 1, 2) helmholtz mean H3 L2 — consonance context (reused)

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/sded/SDED-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_HELMHOLTZ_MEAN = (2, 3, 1, 2)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/M outputs + H3 context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0,)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    e0, e1, _e2 = e_outputs
    (m0,) = m_outputs

    helmholtz_mean = h3_features[_HELMHOLTZ_MEAN]

    # F0: Predicted dissonance detection
    # Current detection + consonance context predicts next detection
    f0 = torch.sigmoid(0.60 * e0 + 0.40 * helmholtz_mean)

    # F1: Predicted behavioral accuracy
    # Combined early detection + MMN signal predicts behavioral output
    f1 = torch.sigmoid(0.50 * e0 + 0.50 * e1)

    # F2: Training effect prediction
    # Neural-behavioral dissociation: neural (M0) stays constant,
    # behavioral (E1) improves with training
    f2 = torch.sigmoid(0.70 * e1 + 0.30 * m0)

    return f0, f1, f2
