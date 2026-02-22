"""PMIM F-Layer -- Forecast (2D).

Two forward prediction signals:

  F0: eran_forecast_fc   -- ERAN prediction 1-2 s ahead [0, 1]
  F1: mmn_forecast_fc    -- MMN prediction 0.5-1 s ahead [0, 1]

ERAN forecast (F0) projects the expected syntax violation signal based on
harmony trajectory and entropy trend at H18 (2 s phrase window). When
harmony trends toward an unusual key area, ERAN forecast increases. This
implements the top-down prediction arm of hierarchical predictive coding.

MMN forecast (F1) projects the expected deviance detection signal based on
prediction-error trajectory and flux trend at H14 (700 ms progression
window). Rapid flux acceleration predicts upcoming deviant events within
the echoic memory timescale.

H3 demands consumed (from F-layer doc -- 3 of the 5 tuples):
  roughness:              (0,18,18,0)   trend H18 L0       -- dissonance trajectory
  spectral_flux:          (21,14,8,0)   velocity H14 L0    -- change acceleration
  tonalness:              (14,14,18,0)  trend H14 L0       -- tonal trajectory

Note: (0,18,18,0) and (14,14,18,0) are shared with S-layer / M-layer
respectively, reducing unique H3 demand count.

R3 consumed:
  [0]  roughness      -- F0: dissonance trajectory for syntax forecast
  [14] tonalness      -- F0: tonal trend for ERAN projection
  [21] spectral_flux  -- F1: change trend for MMN forecast

Scientific basis:
  Koelsch 2014: hierarchical predictive coding for music syntax
  Garrido et al. 2009: forward PE + backward predictions (DCM/fMRI N=16)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pmim/PMIM-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_TREND_H18 = (0, 18, 18, 0)       # dissonance trajectory for ERAN
_FLUX_VEL_H14 = (21, 14, 8, 0)              # change acceleration for MMN
_TONALNESS_TREND_H14 = (14, 14, 18, 0)      # tonal trajectory for ERAN


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
    s_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: 2D forecast from P/S layers + H3 context.

    Computes ERAN forecast (F0) and MMN forecast (F1) using upstream
    prediction-error signals, present-state context, and multi-scale
    temporal trends.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)`` from extraction.
        s_outputs: ``(S0, S1, S2)`` each ``(B, T)`` from cognitive present.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    p0, p1, _p2 = p_outputs
    s0, s1, _s2 = s_outputs

    # -- H3 features --
    roughness_trend = h3_features[_ROUGHNESS_TREND_H18]       # (B, T)
    flux_vel = h3_features[_FLUX_VEL_H14]                     # (B, T)
    tonalness_trend = h3_features[_TONALNESS_TREND_H14]       # (B, T)

    # -- F0: ERAN Forecast --
    # Projects syntax violation signal 1-2 s ahead. Combines current
    # ERAN response (P0), syntax state (S0 inverted -- low stability
    # predicts upcoming violations), roughness trend, and tonalness trend.
    # Koelsch 2014: brain predicts upcoming chords from tonal context.
    f0 = torch.sigmoid(
        0.30 * p0
        + 0.25 * (1.0 - s0)
        + 0.25 * roughness_trend
        + 0.20 * (1.0 - tonalness_trend)
    )

    # -- F1: MMN Forecast --
    # Projects deviance detection signal 0.5-1 s ahead. Combines current
    # MMN response (P1), deviance state (S1), and flux velocity (change
    # acceleration predicts upcoming deviants).
    # Garrido et al. 2009: forward connections carry PE.
    f1 = torch.sigmoid(
        0.35 * p1
        + 0.30 * s1
        + 0.35 * flux_vel
    )

    return f0, f1
