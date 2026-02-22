"""DDSMI E-Layer -- Extraction (3D).

Dyadic Dance Social Motor Integration extraction signals:
  E0: f13_social_coordination  -- Partner tracking and social coordination [0, 1]
  E1: f14_music_tracking       -- Auditory entrainment during social movement [0, 1]
  E2: f15_visual_modulation    -- Resource shift from music to social processing [0, 1]

E0 captures social coordination strength across three timescales: 1s (sustained
partner coordination), 500ms (mid-range synchronization), and 100ms (fast
partner tracking). The multi-scale combination reflects temporal hierarchies
in interpersonal dance coordination -- from micro-adjustments to sustained
coupling.

E1 captures auditory entrainment strength during dyadic dance. Music coupling
periodicity at 1s and 500ms with music onset value at 100ms. Self-movement
tracking is autonomous from social context (Bigand 2025: all ps>.224).

E2 captures the resource competition between auditory and social processing.
The (f13 - f14) difference is the key innovation: positive values indicate
social-dominant processing (visual contact condition). Loudness entropy adds
auditory complexity and social variability adds partner unpredictability.

H3 demands consumed (11 tuples):
  (10, 3, 0, 2)   onset_strength value H3 L2        -- music onset 100ms
  (10, 16, 14, 2)  onset_strength periodicity H16 L2 -- music periodicity 1s
  (25, 3, 0, 2)   x_l0l5[0] value H3 L2             -- music coupling 100ms
  (25, 3, 14, 2)  x_l0l5[0] periodicity H3 L2       -- music coupling period 100ms
  (25, 8, 14, 2)  x_l0l5[0] periodicity H8 L2       -- music coupling period 500ms
  (25, 16, 14, 2) x_l0l5[0] periodicity H16 L2      -- music coupling period 1s
  (33, 3, 0, 2)   x_l4l5[0] value H3 L2             -- social coupling 100ms
  (33, 3, 2, 2)   x_l4l5[0] std H3 L2               -- social variability 100ms
  (33, 8, 14, 2)  x_l4l5[0] periodicity H8 L2       -- social period 500ms
  (33, 16, 14, 2) x_l4l5[0] periodicity H16 L2      -- social period 1s
  (8, 3, 20, 2)   loudness entropy H3 L2             -- loudness entropy 100ms

R3 features:
  [8] loudness, [10] onset_strength, [25:33] x_l0l5, [33:41] x_l4l5

Upstream reads:
  PEOM relay (11D) -- period entrainment context
  ASAP encoder (11D) -- beat prediction context

Bigand et al. 2025: social coordination mTRF F(1,57)=249.75, p<.001.
Bigand et al. 2025: music tracking mTRF F(1,57)=30.22, p<.001.
Bigand et al. 2025: visual contact reduces music tracking F(1,57)=7.48, p=.033.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ddsmi/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_MUSIC_ONSET_100MS = (10, 3, 0, 2)         # onset_strength value H3 L2
_MUSIC_PERIOD_1S = (10, 16, 14, 2)         # onset_strength periodicity H16 L2
_MUSIC_COUPLING_100MS = (25, 3, 0, 2)      # x_l0l5[0] value H3 L2
_MUSIC_COUPLING_P100 = (25, 3, 14, 2)      # x_l0l5[0] periodicity H3 L2
_MUSIC_COUPLING_P500 = (25, 8, 14, 2)      # x_l0l5[0] periodicity H8 L2
_MUSIC_COUPLING_P1S = (25, 16, 14, 2)      # x_l0l5[0] periodicity H16 L2
_SOCIAL_COUPLING_100MS = (33, 3, 0, 2)     # x_l4l5[0] value H3 L2
_SOCIAL_VAR_100MS = (33, 3, 2, 2)          # x_l4l5[0] std H3 L2
_SOCIAL_PERIOD_500MS = (33, 8, 14, 2)      # x_l4l5[0] periodicity H8 L2
_SOCIAL_PERIOD_1S = (33, 16, 14, 2)        # x_l4l5[0] periodicity H16 L2
_LOUDNESS_ENT_100MS = (8, 3, 20, 2)        # loudness entropy H3 L2

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_LOUDNESS = 8
_ONSET_STRENGTH = 10
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: social coordination, music tracking, visual modulation.

    E0 (f13_social_coordination) combines social coupling periodicity at
    three timescales: 1s (sustained partner coordination), 500ms (mid-range
    synchronization), and 100ms (fast partner tracking). Multi-scale
    combination reflects temporal hierarchies in interpersonal coordination.
    Bigand 2025: social coordination mTRF F(1,57)=249.75.

    E1 (f14_music_tracking) combines music coupling periodicity at 1s and
    500ms with music onset value at 100ms. Captures neural tracking of the
    musical stimulus during dyadic dance. Self-movement tracking is
    autonomous (all ps>.224). Bigand 2025: music tracking F(1,57)=30.22.

    E2 (f15_visual_modulation) captures the resource competition. The
    (f13 - f14) difference signals resource shift: positive = social-dominant,
    negative = music-dominant. Loudness entropy adds auditory complexity,
    social variability adds partner unpredictability.
    Bigand 2025: visual contact reduces music tracking F(1,57)=7.48.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        relay_outputs: ``{"PEOM": (B, T, 11), "ASAP": (B, T, 11)}``

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``
    """
    B, T = r3_features.shape[:2]

    # -- H3 features --
    social_period_1s = h3_features[_SOCIAL_PERIOD_1S]          # (B, T)
    social_period_500ms = h3_features[_SOCIAL_PERIOD_500MS]    # (B, T)
    social_coupling_100ms = h3_features[_SOCIAL_COUPLING_100MS]  # (B, T)
    music_period_1s = h3_features[_MUSIC_COUPLING_P1S]         # (B, T)
    music_period_500ms = h3_features[_MUSIC_COUPLING_P500]     # (B, T)
    music_onset_100ms = h3_features[_MUSIC_ONSET_100MS]        # (B, T)
    loudness_entropy = h3_features[_LOUDNESS_ENT_100MS]        # (B, T)
    social_variability = h3_features[_SOCIAL_VAR_100MS]        # (B, T)

    # -- E0: Social Coordination (f13) --
    # Multi-scale social coupling periodicity: 1s (sustained), 500ms
    # (mid-range), 100ms (fast tracking). Weighted combination reflects
    # temporal hierarchy of interpersonal coordination in dance.
    # Bigand 2025: social coordination mTRF F(1,57)=249.75, p<.001.
    e0 = torch.sigmoid(
        0.40 * social_period_1s
        + 0.30 * social_period_500ms
        + 0.30 * social_coupling_100ms
    )

    # -- E1: Music Tracking (f14) --
    # Music coupling periodicity at 1s and 500ms with onset value at 100ms.
    # Captures auditory entrainment strength during social interaction.
    # Bigand 2025: music tracking mTRF F(1,57)=30.22, p<.001.
    e1 = torch.sigmoid(
        0.40 * music_period_1s
        + 0.30 * music_period_500ms
        + 0.30 * music_onset_100ms
    )

    # -- E2: Visual Modulation (f15) --
    # Resource competition: (f13 - f14) = social vs. music processing shift.
    # Loudness entropy adds auditory complexity (complex = harder to track).
    # Social variability adds partner unpredictability (variable = more
    # demanding social tracking).
    # Bigand 2025: visual contact reduces music tracking F(1,57)=7.48.
    e2 = torch.sigmoid(
        0.35 * loudness_entropy
        + 0.35 * social_variability
        + 0.30 * (e0 - e1)
    )

    return e0, e1, e2
