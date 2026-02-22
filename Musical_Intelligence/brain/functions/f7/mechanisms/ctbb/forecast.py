"""CTBB F-Layer -- Forecast (3D).

Forward predictions for cerebellar motor timing state:
  F0: timing_pred      -- Timing enhancement prediction [0, 1]
  F1: balance_pred     -- Postural control prediction [0, 1]
  F2: modulation_pred  -- M1 modulation prediction [0, 1]

Timing prediction (F0) forecasts expected cerebellar timing precision at
the next time step by combining f25 with coupling stability at 1s.
Highest-confidence prediction, supported by sustained iTBS effects
(Sansare 2025: >= 30 min).

Balance prediction (F1) forecasts expected balance state by combining
f27 with coupling periodicity at 1s. Periodicity provides oscillatory
regularity supporting prediction. Sansare 2025: POST1-6 time series
shows stable postural improvement within 30-min window.

Modulation prediction (F2) forecasts expected M1 modulation. Carries
highest uncertainty due to CBI null result (Sansare 2025, eta-sq=0.045
n.s.), suggesting direct cerebellar-M1 pathway may not be the primary
mediator.

H3 demands consumed: 0 new (shares E-layer tuples for coupling stability
and periodicity at H16).

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ctbb/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- Shared H3 tuple keys (from E-layer demands) ------------------------------
_COUPLING_STAB_H16 = (25, 16, 19, 0)   # coupling stability 1s L0
_COUPLING_PERIOD_H16 = (25, 16, 14, 2) # coupling periodicity 1s L2


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: timing, balance, and modulation predictions.

    F0 (timing_pred): Next-step cerebellar timing precision from f25 +
    coupling stability at 1s. Stability captures the slow-varying
    reliability of the cerebellar timing circuit.
    Sansare 2025: sustained iTBS effects >= 30 min.

    F1 (balance_pred): Next-step postural control from f27 + coupling
    periodicity at 1s. Oscillatory regularities in coupling support
    balance prediction. Sansare 2025: stable within 30-min POST window.

    F2 (modulation_pred): Next-step M1 modulation from f26. Highest
    uncertainty due to CBI null (Sansare 2025, eta-sq=0.045 n.s.).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` from extraction layer.
        m_outputs: ``(M0, M1, M2)`` from temporal integration layer.
        p_outputs: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    e0, e1, e2 = e_outputs   # f25, f26, f27
    _m0, _m1, _m2 = m_outputs
    _p0, _p1 = p_outputs

    # Determine shape/device from e0
    B, T = e0.shape
    device = e0.device

    # -- Shared H3 features (from E-layer demands) --
    coupling_stab = h3_features.get(
        _COUPLING_STAB_H16, torch.zeros(B, T, device=device),
    )
    coupling_period = h3_features.get(
        _COUPLING_PERIOD_H16, torch.zeros(B, T, device=device),
    )

    # -- F0: Timing Prediction --
    # timing_pred = sigma(0.5 * f25 + 0.5 * coupling_stability_1s)
    # Sansare 2025: sustained cerebellar timing enhancement
    f0 = torch.sigmoid(
        0.50 * e0
        + 0.50 * coupling_stab
    )

    # -- F1: Balance Prediction --
    # balance_pred = sigma(0.5 * f27 + 0.5 * coupling_period_1s)
    # Periodicity supports oscillatory prediction for balance
    f1 = torch.sigmoid(
        0.50 * e2
        + 0.50 * coupling_period
    )

    # -- F2: Modulation Prediction --
    # modulation_pred: extrapolates f26 forward
    # CBI null (Sansare 2025): highest uncertainty prediction
    f2 = torch.sigmoid(
        0.50 * e1
        + 0.50 * coupling_stab
    )

    return f0, f1, f2
