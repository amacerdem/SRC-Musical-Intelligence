"""MORMR F-Layer -- Forecast (1D).

One forward prediction for chills onset:

  chills_onset_pred  -- Chills onset prediction (2-5s ahead) [0, 1]

H3 consumed: 0 new tuples (reuses E/M/P outputs).

The F-layer produces a forward-looking prediction of chills onset by
combining the current opioid release trajectory with chills-predictive
features. Key predictive signals:
    - Rising opioid release (f01 increasing) signals approach to pleasure peak
    - Reward sensitivity (f04) captures individual prediction threshold
    - Opioid tone trajectory indicates sustained build-up
    - Current opioid state provides present-moment hedonic level

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/mormr/f_layer.md
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_forecast(
    h3_features: dict,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
    p_outputs: Tuple[Tensor],
) -> Tuple[Tensor]:
    """F-layer: 1D forecast from E/M/P outputs (no new H3).

    Predicts chills onset probability on a 2-5s forward horizon,
    corresponding to the anticipatory window observed in Salimpoor (2011)
    where caudate DA release precedes peak emotion.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
            Not consumed directly -- included for interface consistency.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        m_outputs: ``(opioid_tone,)`` each ``(B, T)``.
        p_outputs: ``(current_opioid_state,)`` each ``(B, T)``.

    Returns:
        ``(chills_onset_pred,)`` -- single tensor ``(B, T)`` wrapped in 1-tuple.
    """
    f01, f02, _f03, f04 = e_outputs
    (opioid_tone,) = m_outputs
    (current_opioid_state,) = p_outputs

    # chills_onset_pred: Chills onset prediction (2-5s ahead)
    # Putkinen 2025: chills frequency correlates with NAcc MOR binding (r = -0.52).
    # Salimpoor 2011: caudate DA release precedes peak emotion.
    # Rising f01 + sustained opioid tone + high sensitivity = impending chills.
    chills_onset_pred = torch.sigmoid(
        0.30 * f01
        + 0.25 * f02
        + 0.20 * opioid_tone
        + 0.15 * current_opioid_state
        + 0.10 * f04
    )

    return (chills_onset_pred,)
