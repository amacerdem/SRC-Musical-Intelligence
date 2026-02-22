"""STANM F-Layer -- Forecast (3D).

Forward predictions for attention network dynamics:
  F0: network_state_pred   (predicted network integration state)
  F1: lateral_pred         (predicted lateralization, TANH [-1,1])
  F2: compensation_pred    (predicted compensatory allocation)

H3 demands consumed:
  x_l0l5:  (25,16,1,2)  coupling mean 1s

M-layer inputs:
  M1: local_clustering    (local network clustering)
  M2: lateralization      (hemispheric asymmetry index, tanh-valued)

CRITICAL: F1 is a direct pass-through of M2 (lateralization), which is
already tanh-valued in [-1, 1]. No additional activation is applied.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/stanm/
Fritz 2007: STRF plasticity predicts future attention state.
Mesgarani 2012: coupling dynamics predict network reconfiguration.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_COUPLING_H16_MEAN = (25, 16, 1, 2)      # coupling mean 1s


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for attention network.

    F0 predicts future network integration state from local clustering
    (M1) and sustained coupling. High clustering + high coupling predicts
    continued strong network integration.

    F1 directly passes through M2 (lateralization), which is already
    tanh-valued in [-1, 1]. The predicted lateralization index is the
    current lateralization state -- persistent hemispheric asymmetry.

    F2 predicts compensatory allocation: when local clustering is high
    and coupling is strong, the network can compensate for resource
    imbalances between temporal and spectral processing.

    Mesgarani 2012: ECoG coupling dynamics predict network reconfiguration
    in multi-talker attention tasks.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        m: ``(M0, M1, M2)`` from temporal integration layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
        F0, F2 in [0, 1] (sigmoid); F1 in [-1, 1] (tanh pass-through).
    """
    _m0, m1, m2 = m

    coupling_mean_1s = h3_features[_COUPLING_H16_MEAN]

    # -- F0: Network State Prediction --
    # Predicted network integration state: local clustering (M1) captures
    # current tight coupling; sustained coupling mean (1s) captures
    # stable cross-band interaction. Together they predict whether the
    # attention network will maintain or lose integration.
    # Mesgarani 2012: STG coupling predicts attention state transitions.
    f0 = torch.sigmoid(
        0.50 * m1
        + 0.50 * coupling_mean_1s
    )

    # -- F1: Lateral Prediction --
    # Direct pass-through of M2 (lateralization). The predicted hemispheric
    # asymmetry is the current asymmetry -- lateralization is a slow-changing
    # state variable that persists across short forecast horizons.
    # Already tanh-valued in [-1, 1]; no additional activation needed.
    # Bidet-Caulet 2007: lateralization patterns are sustained during attention.
    f1 = m2

    # -- F2: Compensation Prediction --
    # Predicted compensatory allocation: same features as F0 (clustering +
    # coupling) but interpreted as the network's ability to compensate for
    # imbalanced resource distribution between temporal and spectral streams.
    # Fritz 2007: STRF plasticity enables compensatory reallocation.
    f2 = torch.sigmoid(
        0.50 * m1
        + 0.50 * coupling_mean_1s
    )

    return f0, f1, f2
