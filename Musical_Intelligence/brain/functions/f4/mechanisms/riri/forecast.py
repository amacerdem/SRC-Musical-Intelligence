"""RIRI F-Layer -- Forecast (3D).

Forward predictions for rehabilitation trajectory:
  F0: recovery_trajectory  (direction of functional recovery)
  F1: connectivity_pred    (functional connectivity restoration prediction)
  F2: consolidation_pred   (motor memory consolidation prediction)

F-layer combines long-horizon H3 tuples (H16 = 1s) with M-layer
integration synergy for trajectory prediction.  These feed downstream
into F8 Learning (adaptive difficulty), F6 Reward (session success), and
the precision engine.

H3 consumed (F-layer):
  (41, 16, 18, 0)  x_l5l7[0] trend H16 L0        -- connectivity trajectory
  (41, 16, 14, 2)  x_l5l7[0] periodicity H16 L2   -- connectivity regularity
  (41, 16, 1, 0)   x_l5l7[0] mean H16 L0          -- current connectivity level (shared with E)
  (25, 16, 19, 0)  x_l0l5[0] stability H16 L0     -- entrainment stability (shared with M)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/riri/RIRI-forecast.md
Blasi 2025: structural + functional neuroplasticity from music/dance rehab.
Fang 2017: music therapy preserves encoding in neurodegeneration.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (F-layer) ------------------------------------------------
_CONN_H16_TREND = (41, 16, 18, 0)      # x_l5l7[0] trend H16 L0
_CONN_H16_PERIOD = (41, 16, 14, 2)     # x_l5l7[0] periodicity H16 L2
_CONN_H16_MEAN = (41, 16, 1, 0)        # x_l5l7[0] mean H16 L0  (shared w/ E)
_COUPLING_L0L5_H16_STAB = (25, 16, 19, 0)  # x_l0l5 stability H16 L0 (shared w/ M)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for rehabilitation trajectory.

    F0 (recovery_trajectory) predicts the direction of functional recovery
    based on connectivity trends and entrainment stability.
    Blasi 2025: structural neuroplasticity across sessions.

    F1 (connectivity_pred) predicts upcoming functional connectivity
    restoration based on current level and periodicity.
    Blasi 2025: enhanced FC within language and motor networks.

    F2 (consolidation_pred) predicts session-to-session motor learning
    consolidation.  Combines connectivity coupling, temporal coherence,
    and encoding state.
    Fang 2017: music therapy preserves encoding in neurodegeneration.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    _e0, _e1, e2 = e
    m0, m1 = m
    _p0, _p1 = p

    # -- H3 features -------------------------------------------------------
    conn_trend = h3_features[_CONN_H16_TREND]          # (B, T)
    conn_period = h3_features[_CONN_H16_PERIOD]        # (B, T)
    conn_mean = h3_features[_CONN_H16_MEAN]            # (B, T)
    stability = h3_features[_COUPLING_L0L5_H16_STAB]   # (B, T)

    # -- F0: Recovery Trajectory -------------------------------------------
    # "Is rehabilitation moving in the right direction?"
    # sigma(0.40 * connectivity_trend + 0.30 * stability + 0.30 * synergy)
    # Blasi 2025: structural neuroplasticity from music/dance rehab.
    f0 = torch.sigmoid(
        0.40 * conn_trend
        + 0.30 * stability
        + 0.30 * m0
    )

    # -- F1: Connectivity Prediction ---------------------------------------
    # Predicts near-future functional connectivity restoration.
    # sigma(0.50 * connectivity_mean + 0.50 * connectivity_period)
    # Stable, periodic connectivity signals predict continued restoration.
    f1 = torch.sigmoid(
        0.50 * conn_mean
        + 0.50 * conn_period
    )

    # -- F2: Consolidation Prediction --------------------------------------
    # Predicts session-to-session motor memory consolidation.
    # sigma(0.40 * connectivity_mean + 0.30 * temporal_coherence + 0.30 * encoding)
    # Fang 2017: music therapy preserves encoding in neurodegeneration.
    f2 = torch.sigmoid(
        0.40 * conn_mean
        + 0.30 * m1
        + 0.30 * e2
    )

    return f0, f1, f2
