"""STAI F-Layer -- Forecast (3D).

Forward predictions for spectral-temporal aesthetic integration:
  F0: aesthetic_rating_pred    — Predicted aesthetic rating trajectory [0, 1]
  F1: reward_response_pred     — Predicted reward circuit response [0, 1]
  F2: connectivity_pred        — Predicted vmPFC-IFG connectivity [0, 1]

F0 forecasts the aesthetic rating trajectory based on current aesthetic
response, spectral-temporal interaction strength, and the stability of
both dimensions. This predicts how the listener's aesthetic judgment will
evolve -- will the music maintain, increase, or decrease its aesthetic
appeal?

F1 predicts the reward circuit response based on current aesthetic value,
temporal quality, and interaction strength. NAcc/caudate/putamen reward
signals for temporal integrity (Menon & Levitin 2005). This forecasts
whether the music will continue to produce reward responses.

F2 predicts the evolution of vmPFC-IFG connectivity based on current
connectivity state, aesthetic integration, and binding quality. This
forecasts whether the interaction locus will strengthen or weaken.

H3 demands consumed (0 new tuples -- F-layer derives all signals from
E/M/P layer outputs and R3 features).

R3 features:
  [0] roughness, [4] sensory_pleasantness, [7] amplitude,
  [33:41] x_l4l5

Koelsch 2014: vmPFC/OFC for aesthetic value prediction.
Menon & Levitin 2005: NAcc/caudate reward prediction signal.
Kim et al. 2019: vmPFC-IFG connectivity evolution.
Blood & Zatorre 2001: reward circuit anticipation from aesthetic stimuli.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/stai/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 feature indices -------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for aesthetic integration.

    F0 (aesthetic_rating_pred) forecasts the aesthetic rating trajectory.
    Current aesthetic response (P2) + spectral-temporal interaction (M1) +
    aesthetic value (M0) project forward. Predicts whether the aesthetic
    appeal will be maintained.

    F1 (reward_response_pred) predicts reward circuit response. Aesthetic
    value (M0) + temporal quality (P1) + interaction (E2) project expected
    NAcc/caudate activation.
    Menon & Levitin 2005: reward circuit tracks aesthetic value.

    F2 (connectivity_pred) predicts vmPFC-IFG connectivity evolution.
    Current connectivity (E3) + aesthetic integration (E2) + binding
    quality project whether the interaction locus will strengthen.
    Kim et al. 2019: vmPFC-IFG connectivity is the interaction locus.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    e0, e1, e2, e3 = e
    m0, m1 = m
    p0, p1, p2 = p

    # -- F0: Aesthetic Rating Prediction --
    # Forecasts aesthetic rating trajectory. Current aesthetic response (P2)
    # is the anchor. Interaction strength (M1) and spectral quality (P0)
    # modulate the prediction -- strong interaction + good spectral quality
    # = high predicted rating.
    # Koelsch 2014: vmPFC/OFC value prediction for aesthetic stimuli.
    f0 = torch.sigmoid(
        0.40 * p2 * m1.clamp(min=0.1)
        + 0.30 * m0 * p0.clamp(min=0.1)
        + 0.30 * e2 * p1
    )

    # -- F1: Reward Response Prediction --
    # Predicts reward circuit (NAcc/caudate/putamen) response trajectory.
    # Aesthetic value (M0) as the primary reward driver. Temporal quality
    # (P1) provides forward flow prediction. Interaction (E2) gates the
    # reward -- requires both dimensions for full reward.
    # Third term gates aesthetic response by spectral integrity (E0) rather
    # than temporal integrity (E1) alone, because NAcc activation requires
    # musically structured (spectrally coherent) stimuli, not mere temporal
    # stationarity. Blood & Zatorre 2001: NAcc correlates with consonance.
    # Menon & Levitin 2005: NAcc activation tracks aesthetic value.
    f1 = torch.sigmoid(
        0.35 * m0 * p1.clamp(min=0.1)
        + 0.35 * e2 * m1
        + 0.30 * p2 * e0
    )

    # -- F2: Connectivity Prediction --
    # Predicts vmPFC-IFG connectivity evolution. Current connectivity (E3)
    # anchors the prediction. Aesthetic integration (E2) and interaction
    # strength (M1) modulate -- strong integration = expected connectivity
    # maintenance.
    # Kim et al. 2019: vmPFC-IFG connectivity is the interaction locus.
    f2 = torch.sigmoid(
        0.40 * e3 * e2.clamp(min=0.1)
        + 0.30 * m1 * e0.clamp(min=0.1)
        + 0.30 * p2 * m0
    )

    return f0, f1, f2
