"""BARM F-Layer -- Forecast (3D).

Forward predictions for brainstem response modulation:
  F0: beat_accuracy_pred     (predicted beat alignment accuracy at next step)
  F1: sync_benefit_pred      (predicted synchronization benefit)
  F2: individual_diff_pred   (predicted individual difference in brainstem response)

H3 demands consumed:
  spectral_flux:  (10,16,14,2) periodicity at 1s integration
  x_l0l5:         (25,16,14,2) periodicity at 1s integration

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/barm/
Skoe & Kraus 2010: ABR enhancement predicts future temporal encoding.
Tierney & Kraus 2013: motor timing precision predicts brainstem consistency.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_FLUX_H16_PERIOD = (10, 16, 14, 2)          # spectral_flux periodicity 1s integration
_COUPLING_H16_PERIOD = (25, 16, 14, 2)      # x_l0l5 periodicity 1s integration


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for brainstem modulation.

    F0 predicts the accuracy of beat alignment at the next time step,
    combining current P0 (beat alignment accuracy) with long-range beat
    periodicity (1s). Stable beat periodicity predicts continued accurate
    alignment.

    F1 predicts the synchronization benefit, combining E2 (current sync
    benefit) with coupling periodicity (1s). Stable coupling indicates
    persistent motor-auditory engagement.

    F2 predicts individual difference effects on brainstem responses,
    combining P1 (regularization strength) with M1 (regularization effect).
    Stronger regularization predicts more pronounced individual differences
    in brainstem enhancement.

    Skoe & Kraus 2010: temporal encoding quality at one time point predicts
    encoding at subsequent points within a stimulus.
    Tierney & Kraus 2013: motor timing precision is a stable individual
    trait that predicts brainstem response consistency.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    _e0, _e1, e2 = e
    p0, p1 = p

    # -- H3 features --
    beat_period_1s = h3_features[_FLUX_H16_PERIOD]           # (B, T)
    coupling_period_1s = h3_features[_COUPLING_H16_PERIOD]   # (B, T)

    # -- F0: Beat Accuracy Prediction --
    # Current beat alignment accuracy + stable beat periodicity = predicted
    # continued accurate alignment. Skoe 2010: ABR encoding quality
    # persists within a stimulus at beat-aligned time points.
    f0 = torch.sigmoid(
        0.50 * p0
        + 0.50 * beat_period_1s
    )

    # -- F1: Sync Benefit Prediction --
    # Current sync benefit + stable coupling periodicity = predicted
    # continued motor-auditory interaction benefit.
    # Tierney 2013: sensorimotor coupling is a stable trait (r=0.65).
    f1 = torch.sigmoid(
        0.50 * e2
        + 0.50 * coupling_period_1s
    )

    # -- F2: Individual Difference Prediction --
    # Regularization strength + effect predict the magnitude of individual
    # differences in brainstem enhancement. Stronger regulators show more
    # pronounced ABR enhancement (Musacchia 2007, Tierney 2013).
    f2 = torch.sigmoid(
        0.50 * p1
        + 0.50 * p0
    )

    return f0, f1, f2
