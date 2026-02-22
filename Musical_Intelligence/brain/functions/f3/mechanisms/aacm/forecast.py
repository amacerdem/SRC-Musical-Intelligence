"""AACM F-Layer -- Forecast (3D).

Forward predictions for aesthetic-attention dynamics:
  F0: behavioral_pred     (predicted behavioral response to aesthetic stimulus)
  F1: n2p3_pred           (predicted N2/P3 ERP component magnitude)
  F2: aesthetic_pred       (predicted aesthetic appreciation trajectory)

H3 demands consumed:
  x_l0l5:      (25,16,1,0) coupling mean at 1s L0 -- reused
  pleasant:    (3,16,8,2)  pleasant velocity at 1s -- reused

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/aacm/
Sarasso 2019: N2/P3 components predict later aesthetic judgments (N=22).
Brattico 2013: vmPFC predicts aesthetic appreciation trajectories (N=18).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_COUPLING_MEAN_1S = (25, 16, 1, 0)  # coupling mean at 1s L0 (reused)
_PLEAS_VEL_1S = (3, 16, 8, 2)       # pleasant velocity at 1s (reused)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for aesthetic-attention dynamics.

    F0 predicts behavioral response using savoring (E2) and integration
    coupling. F1 predicts N2/P3 ERP magnitude from motor inhibition (E1)
    and pleasant dynamics. F2 predicts aesthetic appreciation trajectory
    from sustained engagement (M0) and pleasant dynamics.

    Sarasso 2019: N2/P3 amplitudes correlated with subsequent aesthetic
    ratings (r=0.42, p<0.05, N=22).
    Brattico 2013: vmPFC BOLD signal predicts aesthetic trajectory (N=18).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    _e0, e1, e2 = e
    m0, _m1 = m

    coupling_mean_1s = h3_features[_COUPLING_MEAN_1S]
    pleasant_vel_1s = h3_features[_PLEAS_VEL_1S]

    # -- F0: Behavioral Prediction --
    # Predicted behavioral response to aesthetic stimulus. Savoring (E2)
    # projects forward as sustained engagement tendency; coupling provides
    # integration context for action readiness.
    # Brattico 2013: behavioral liking ratings predicted by vmPFC activation.
    f0 = torch.sigmoid(
        0.50 * e2
        + 0.50 * coupling_mean_1s
    )

    # -- F1: N2/P3 Prediction --
    # Predicted magnitude of late ERP components (N2/P3) reflecting
    # evaluative attention. Motor inhibition (E1) drives the inhibitory
    # component (N2); pleasant dynamics drive the evaluative component (P3).
    # Sarasso 2019: N2/P3 predict aesthetic judgment accuracy.
    f1 = torch.sigmoid(
        0.50 * e1
        + 0.50 * pleasant_vel_1s
    )

    # -- F2: Aesthetic Prediction --
    # Predicted aesthetic appreciation trajectory. Sustained engagement
    # (M0) provides the base; pleasant dynamics (velocity) predict
    # whether appreciation is rising, stable, or declining.
    # Brattico 2013: vmPFC trajectory predicts subsequent aesthetic ratings.
    f2 = torch.sigmoid(
        0.50 * m0
        + 0.50 * pleasant_vel_1s
    )

    return f0, f1, f2
