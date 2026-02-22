"""SRP F-Layer -- Forecast (3D).

Three forward predictions for reward, chills, and resolution:

  F0: reward_forecast     -- Forward reward signal (5-15s ahead) [0, 1]
  F1: chills_proximity    -- Proximity to chills peak (2-5s ahead) [0, 1]
  F2: resolution_expect   -- Harmonic resolution expectation [0, 1]

H3 consumed (tuples 26-31):
    (7, 22, 4, 1)   amplitude max H22 L1                 -- future peak 15s
    (0, 20, 18, 0)  roughness trend H20 L0               -- dissonance 5s
    (4, 20, 18, 0)  sensory_pleasantness trend H20 L0    -- consonance 5s
    (7, 20, 8, 1)   amplitude velocity H20 L1            -- forward energy
    (0, 18, 19, 2)  roughness stability H18 L2           -- harmonic stability
    (4, 20, 18, 0)  sensory_pleasantness trend H20 L0    -- resolution (F)

F-layer primarily reuses N+C/T+M/P outputs rather than reading many new H3
tuples directly.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 26-31 from demand spec) --------------------------------
_AMP_MAX_15S_FWD = (7, 22, 4, 1)        # #26: future peak energy 15s
_ROUGH_TREND_5S = (0, 20, 18, 0)        # #27: dissonance trajectory 5s
_PLEAS_TREND_5S = (4, 20, 18, 0)        # #28: consonance trend 5s
_AMP_VEL_5S_FWD = (7, 20, 8, 1)         # #29: forward energy velocity
_ROUGH_STAB_2S = (0, 18, 19, 2)         # #30: harmonic stability phrase
# #31 reuses same key as #28: (4, 20, 18, 0) -- consonance trend 5s F-layer


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from N+C/T+M/P outputs + H3 context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(N0, N1, N2, C0, C1, C2)`` each ``(B, T)``.
        m_outputs: ``(T0, T1, T2, T3, M0, M1, M2)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    n0, n1, _n2, c0, _c1, c2 = e_outputs
    t0, _t1, _t2, _t3, m0, m1, m2 = m_outputs
    p0, p1, p2 = p_outputs

    amp_max_15s_fwd = h3_features[_AMP_MAX_15S_FWD]
    rough_trend_5s = h3_features[_ROUGH_TREND_5S]
    pleas_trend_5s = h3_features[_PLEAS_TREND_5S]
    amp_vel_5s_fwd = h3_features[_AMP_VEL_5S_FWD]
    rough_stab_2s = h3_features[_ROUGH_STAB_2S]

    # F0: Reward forecast -- anticipatory reward signal 5-15s ahead
    # Salimpoor 2011: caudate DA ramp predicts upcoming peak reward
    # reward_forecast = f(wanting, peak_energy_future, tension, caudate_da)
    f0 = torch.sigmoid(
        0.30 * p0 + 0.30 * amp_max_15s_fwd * n0
        + 0.20 * t0 + 0.20 * m1 * c0
    )

    # F1: Chills proximity -- proximity to peak chills moment
    # Salimpoor 2011: NAcc DA peaks coincide with chills (r=0.84)
    # Ferreri 2019: levodopa enhances chills frequency
    # chills = f(liking, forward_energy_velocity, peak_detection, pleasure)
    f1 = torch.sigmoid(
        0.30 * p1 + 0.30 * amp_vel_5s_fwd * m2
        + 0.20 * p2 + 0.20 * n1 * m1
    )

    # F2: Resolution expectation -- harmonic resolution prediction
    # Huron 2006 ITPRA: resolution of tension produces reward
    # Blood & Zatorre 2001: dissonance-to-consonance activates NAcc
    # resolution = f(harmonic_tension, consonance_trend, stability, RPE)
    f2 = torch.sigmoid(
        0.30 * m0 * pleas_trend_5s
        + 0.30 * (1.0 - rough_trend_5s) * rough_stab_2s
        + 0.20 * p2 + 0.20 * c2
    )

    return f0, f1, f2
