"""DDSMI F-Layer -- Forecast (3D).

Dyadic Dance Social Motor Integration forward predictions:
  F0: coordination_pred  -- Social coordination prediction [0, 1]
  F1: music_pred         -- Music tracking prediction [0, 1]
  F2: social_pred        -- Overall social process prediction [0, 1]

F0 predicts near-future social coordination quality. Combines current social
tracking (f13) with sustained social periodicity (1s timescale). When both
are high, the dyadic dance coordination is predicted to continue successfully.
Sabharwal 2024: Granger causality directional coupling predicts leader/follower.

F1 predicts near-future music tracking strength. Combines current music
tracking (f14) with sustained music coupling periodicity (1s). Regular
rhythmic patterns with strong current tracking predict continued auditory
entrainment.

F2 predicts the overall social processing state including both direct partner
coordination and the visual modulation effect. Integrates f13 (social
coordination) with f15 (visual modulation) to forecast whether social
processing will dominate in the near future.
Yoneta et al. 2022: leader/follower roles modulate inter-brain coupling.

H3 demands consumed: 0 new tuples (reuses E-layer tuples):
  - social_period_1s: (33, 16, 14, 2) from E-layer
  - music_period_1s: (25, 16, 14, 2) from E-layer

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ddsmi/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys reused from E-layer ---------------------------------------------
_SOCIAL_PERIOD_1S = (33, 16, 14, 2)    # x_l4l5[0] periodicity H16 L2
_MUSIC_COUPLING_P1S = (25, 16, 14, 2)  # x_l0l5[0] periodicity H16 L2


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for dyadic dance system.

    F0 (coordination_pred) predicts social coordination quality. Averages
    current social coordination (f13) with sustained social periodicity (1s).
    Interpersonal coordination is predicted by both current partner tracking
    state and regularity of the social coupling signal.
    Sabharwal 2024: Granger causality predicts leader/follower dynamics.

    F1 (music_pred) predicts music tracking strength. Averages current music
    tracking (f14) with sustained music coupling periodicity (1s). Highly
    periodic music with strong current entrainment predicts continued
    auditory tracking. Interacts with resource competition: strong music_pred
    + strong coordination_pred = resource allocation challenge.

    F2 (social_pred) predicts overall social processing dominance. Integrates
    social coordination (f13) with visual modulation (f15), forecasting
    whether social-dominant or music-dominant processing will persist.
    Yoneta 2022: leader/follower roles modulate inter-brain coupling.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer -- f13, f14, f15.
        m: ``(M0, M1, M2)`` from temporal integration layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    f13, f14, f15 = e
    _m0, _m1, _m2 = m
    _p0, _p1 = p

    # -- H3 features (reused from E-layer demands) --
    social_period_1s = h3_features[_SOCIAL_PERIOD_1S]      # (B, T)
    music_period_1s = h3_features[_MUSIC_COUPLING_P1S]     # (B, T)

    # -- F0: Coordination Prediction --
    # Predicts near-future social coordination quality. Current social
    # tracking (f13) anchored by sustained social periodicity (1s).
    # Consistent, periodic social coupling predicts continued coordination.
    # Sabharwal 2024: directional coupling predicts leader/follower.
    f0 = torch.sigmoid(
        0.50 * f13
        + 0.50 * social_period_1s
    )

    # -- F1: Music Prediction --
    # Predicts near-future music tracking strength. Current music tracking
    # (f14) anchored by sustained music coupling periodicity (1s).
    # Regular rhythmic patterns + strong current tracking = continued
    # auditory entrainment.
    f1 = torch.sigmoid(
        0.50 * f14
        + 0.50 * music_period_1s
    )

    # -- F2: Social Process Prediction --
    # Predicts overall social processing dominance. Combines social
    # coordination (f13) with visual modulation (f15). When both social
    # coordination is strong and visual modulation indicates resource
    # shift toward social processing, predicts continued social dominance.
    # Yoneta 2022: leader/follower roles modulate inter-brain coupling.
    f2 = torch.sigmoid(
        0.50 * f13
        + 0.50 * f15
    )

    return f0, f1, f2
