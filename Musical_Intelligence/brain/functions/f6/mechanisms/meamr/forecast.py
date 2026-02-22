"""MEAMR F-Layer -- Forecast (1D).

Forward prediction for nostalgia response:
  F0: nostalgia_response_pred -- Predicted nostalgia response [0, 1]

Projects likelihood of a sustained nostalgia experience based on current
positive affect (E3/f04) and autobiographical salience (E1/f02). High
positive affect combined with strong autobiographical salience predicts an
emerging nostalgia response -- the bittersweet pleasure of music-evoked
personal memories. tau_decay = 10.0s reflects the slow, sustained nature
of nostalgic responses.

Nostalgia prediction requires both emotional reward (positive affect from
remembering) and autobiographical specificity (personal significance of
the memory).

H3 demands consumed: None new -- reuses E-layer outputs (f02, f04).
  The F-layer doc lists 4 tuples already in the E-layer demand set:
    (41, 16, 18, 2)  memory-structure trend 1s -- via f02 autobio trajectory
    (41, 16, 1, 2)   mean memory-structure 1s -- via f02 sustained salience
    (4, 16, 18, 2)   pleasantness trend 1s -- via f01 -> f04 hedonic trajectory
    (12, 16, 1, 2)   mean warmth 1s -- via f01 -> f04 timbral trajectory
  These are consumed via E-layer outputs, not directly.

Janata 2009: Sustained dMPFC during autobiographical music
(P < 0.001, FDR P < 0.025, fMRI, N = 13).
Salimpoor 2011: Anticipatory caudate DA for familiar music
(PET, N = 8, r = 0.71).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/meamr/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_forecast(
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor],
) -> Tuple[Tensor]:
    """Compute F-layer: 1D nostalgia response prediction.

    F0 (nostalgia_response_pred): Projects emerging nostalgia from positive
    affect (E3/f04) and autobiographical salience (E1/f02). Nostalgia is
    the sustained emotional reward following music-evoked autobiographical
    memory retrieval.

    sigma(0.5 * f04 + 0.5 * f02)

    The f04 + f02 combination ensures nostalgia prediction requires both
    emotional reward (the positive affect of remembering) and autobiographical
    specificity (the personal significance of the memory).

    Janata 2009: Sustained dMPFC during autobio music (P < 0.001).
    Salimpoor 2011: Anticipatory caudate DA for familiar music (r = 0.71).

    Args:
        e: ``(E0, E1, E2, E3)`` from extraction layer, each ``(B, T)``.
        p: ``(P0,)`` from cognitive present layer, each ``(B, T)``.

    Returns:
        ``(F0,)`` each ``(B, T)``.
    """
    _e0, e1, _e2, e3 = e
    (p0,) = p

    # -- F0: Nostalgia Response Prediction --
    # sigma(0.5 * f04 + 0.5 * f02)
    # Janata 2009: sustained dMPFC requires both familiarity + autobio
    # Salimpoor 2011: anticipatory DA for familiar music
    f0 = torch.sigmoid(
        0.40 * e3
        + 0.35 * e1
        + 0.25 * p0
    )

    return (f0,)
