"""DGTP F-Layer -- Forecast (2D).

Forward predictions for cross-domain transfer and training effects:
  F0: cross_domain_pred        (predicted cross-domain timing transfer)
  F1: training_transfer_pred   (predicted training-induced improvement)

H3 demands consumed:
  x_l0l5: (25,16,1,0)  coupling mean 1s memory

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/dgtp/
Patel 2011: OPERA hypothesis predicts bidirectional transfer.
Grahn 2012: beat processing predicts domain-general timing.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_COUPLING_H16_MEAN = (25, 16, 1, 0)  # x_l0l5 mean 1s memory


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: cross-domain and training transfer predictions.

    F0 predicts cross-domain timing transfer from the shared mechanism
    (E2) and coupling mean at 1s. When E2 is high (shared variance
    active) and coupling is sustained, cross-domain transfer is predicted
    to be strong.

    F1 predicts training-induced improvement from domain correlation
    (M0) and shared variance (M1). High correlation + high shared
    variance = training in one domain should transfer to the other.

    Patel 2011: OPERA hypothesis predicts bidirectional transfer
    when overlap, precision, and repetition conditions are met.
    Grahn 2012: beat processing engages domain-general circuits.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``
    """
    _e0, _e1, e2 = e
    m0, m1 = m

    coupling_mean_1s = h3_features[_COUPLING_H16_MEAN]  # (B, T)

    # -- F0: Cross-Domain Prediction --
    # Predicted cross-domain timing transfer: shared mechanism (E2)
    # + coupling mean (sustained integration context).
    # Patel 2011: overlap of neural resources enables transfer.
    f0 = torch.sigmoid(
        0.50 * e2
        + 0.50 * coupling_mean_1s
    )

    # -- F1: Training Transfer Prediction --
    # Predicted training-induced improvement: domain correlation (M0)
    # + shared variance (M1) reflects the degree to which training
    # in one domain will improve the other.
    # Patel 2011: precision + repetition + overlap = transfer.
    f1 = torch.sigmoid(
        0.50 * m0
        + 0.50 * m1
    )

    return f0, f1
