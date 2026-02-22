"""DAP F-Layer -- Forecast (2D).

Forward predictions for adult hedonic capacity and preference stability:
  F0: adult_hedonic_pred   -- Predicted adult hedonic response capacity [0, 1]
  F1: preference_stab      -- Predicted preference stability [0, 1]

Adult hedonic prediction (F0) projects the capacity for hedonic
response in adulthood based on developmental trajectory. Combines
exposure history (D2), plasticity coefficient (D1), and current affect
(P0). Higher developmental exposure and ongoing plasticity predict
stronger adult hedonic responses. Peretz et al. 2001: congenital
amusia shows impaired hedonic response from disrupted development.

Preference stability (F1) estimates how stable current preferences
will be over time. High exposure history (D2) and neural maturation
(D3) with moderate learning rate (P2) predict stable preferences.
North & Hargreaves 2008: preference stability increases with
repeated exposure and developmental consolidation.

H3 demands consumed: None new (uses D-layer and P-layer outputs).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/dap/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_forecast(
    h3_features: dict,
    e_outputs: Tuple[Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: adult hedonic prediction and preference stability.

    F0 (adult_hedonic_pred): Projects adult hedonic response capacity
    from developmental trajectory. High exposure + plasticity + current
    affect = strong future hedonic capacity.
    Peretz et al. 2001: developmental disruption -> impaired hedonic.

    F1 (preference_stab): Estimates preference stability over time.
    High exposure + maturation + moderate learning rate = stable prefs.
    North & Hargreaves 2008: stability from repeated exposure.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0,)`` from extraction layer.
        m_outputs: ``(D0, D1, D2, D3)`` from temporal integration layer.
        p_outputs: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    (e0,) = e_outputs
    _d0, d1, d2, d3 = m_outputs
    p0, _p1, p2 = p_outputs

    # -- F0: Adult Hedonic Prediction --
    # sigma(0.35*d2 + 0.30*d1 + 0.20*p0 + 0.15*e0)
    # Peretz et al. 2001: developmental exposure -> adult hedonic capacity
    # Sloboda 1991: early musical experiences predict adult emotional responses
    f0 = torch.sigmoid(
        0.35 * d2
        + 0.30 * d1
        + 0.20 * p0
        + 0.15 * e0
    )

    # -- F1: Preference Stability --
    # sigma(0.35*d2 + 0.30*d3 + 0.20*(1-p2) + 0.15*d1)
    # North & Hargreaves 2008: preference stability from exposure repetition
    # High maturation (D3) + high exposure (D2) + LOW learning rate (stable)
    f1 = torch.sigmoid(
        0.35 * d2
        + 0.30 * d3
        + 0.20 * (1.0 - p2)
        + 0.15 * d1
    )

    return f0, f1
