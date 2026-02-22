"""SSRI E-Layer -- Extraction (5D).

Social Synchrony Reward Integration extraction signals:
  f01: synchrony_reward       -- Reward from interpersonal synchrony [0, 1]
  f02: social_bonding_index   -- Social bonding strength proxy [0, 1]
  f03: group_flow_state       -- Group flow / collective absorption [0, 1]
  f04: entrainment_quality    -- Temporal entrainment precision [0, 1]
  f05: collective_pleasure    -- Shared hedonic experience [0, 1]

f01 is the core reward signal from interpersonal coordination. It combines
onset periodicity at 500ms (beat-level coordination), mean pleasantness at
1s (hedonic quality of the shared stimulus), and coupling trend at 1s
(whether consonance-energy interaction is strengthening).

f02 accumulates over longer timescales (5s LTI coupling mean, 5s loudness
trend) and depends on f01, reflecting that bonding builds on synchrony
reward. Mean warmth at 1s contributes timbral blend quality.

f03 combines f01 with beat-level dynamics (mean amplitude 500ms, spectral
entropy 500ms) to capture collective absorption during coordinated
performance.

f04 is the most temporally precise feature, drawing on fast-scale onset
alignment (100ms, 125ms periodicity) and medium-scale periodicity (500ms).
Energy velocity adds dynamic coordination tracking.

f05 integrates f02 and f03 with mean pleasantness 500ms, providing a
summary hedonic signal that reflects the social amplification of individual
pleasure.

H3 demands consumed (12 tuples):
  (10, 3, 0, 2)   onset at 100ms alpha L2         -- micro-timing alignment
  (10, 4, 14, 2)  beat periodicity 125ms L2        -- rhythmic entrainment
  (10, 8, 14, 2)  onset periodicity 500ms L2       -- phrase-level coordination
  (7, 8, 1, 2)    mean amplitude 500ms L2          -- shared dynamic envelope
  (4, 8, 1, 2)    mean pleasantness 500ms L2       -- shared hedonic quality
  (4, 16, 1, 2)   mean pleasantness 1s L2          -- sustained positive affect
  (22, 8, 8, 0)   energy velocity 500ms L0         -- dynamic coordination
  (12, 16, 1, 2)  mean warmth 1s L2                -- timbral blending quality
  (21, 8, 20, 2)  spectral entropy 500ms L2        -- structural coordination
  (25, 16, 18, 2) coupling trend 1s L2             -- consonance-energy trajectory
  (25, 20, 1, 0)  coupling mean 5s LTI L0          -- sustained emotional synchrony
  (8, 20, 18, 0)  loudness trend 5s LTI L0         -- long-range dynamic trajectory

R3 features:
  [10] spectral_flux (onset proxy), [7] amplitude, [4] sensory_pleasantness,
  [8] loudness, [12] warmth, [22] energy_change, [21] spectral_change,
  [25] x_l0l5[0]

Upstream reads:
  DAED relay, RPEM relay (via relay_outputs)

Kokal et al. 2011: joint drumming activates caudate with synchrony quality.
Ni et al. 2024: social bonding increases prefrontal neural synchronization
(fNIRS hyperscanning, N=528, d=0.85).
Williamson & Bonshor 2019: brass band group music produces flow and
cognitive engagement.
Wohltjen et al. 2023: beat entrainment ability is stable individual
difference (d=1.37).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ssri/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ONSET_VAL_H3 = (10, 3, 0, 2)           # onset at 100ms alpha L2
_BEAT_PERIOD_H4 = (10, 4, 14, 2)        # beat periodicity 125ms L2
_ONSET_PERIOD_H8 = (10, 8, 14, 2)       # onset periodicity 500ms L2
_AMP_MEAN_H8 = (7, 8, 1, 2)            # mean amplitude 500ms L2
_PLEAS_MEAN_H8 = (4, 8, 1, 2)          # mean pleasantness 500ms L2
_PLEAS_MEAN_H16 = (4, 16, 1, 2)        # mean pleasantness 1s L2
_ENERGY_VEL_H8 = (22, 8, 8, 0)         # energy velocity 500ms L0
_WARMTH_MEAN_H16 = (12, 16, 1, 2)      # mean warmth 1s L2
_SPECTRAL_ENT_H8 = (21, 8, 20, 2)      # spectral entropy 500ms L2
_COUPLING_TREND_H16 = (25, 16, 18, 2)  # coupling trend 1s L2
_COUPLING_MEAN_H20 = (25, 20, 1, 0)    # coupling mean 5s LTI L0
_LOUDNESS_TREND_H20 = (8, 20, 18, 0)   # loudness trend 5s LTI L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_SPECTRAL_FLUX = 10    # onset_strength (R3 naming: spectral_flux -> onset_strength)
_AMPLITUDE = 7         # velocity_A
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 8          # velocity_D
_WARMTH = 12
_ENERGY_CHANGE = 22    # distribution_entropy
_SPECTRAL_CHANGE = 21  # spectral_flux
_X_L0L5_0 = 25        # first cross-domain feature


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: five social synchrony reward extraction signals.

    f01 (synchrony_reward) captures interpersonal coordination reward from
    onset periodicity, pleasantness, and coupling trend. Kokal et al. 2011:
    joint drumming activates caudate with synchrony quality.

    f02 (social_bonding_index) accumulates bonding from long-timescale
    coupling and loudness trends, building on f01. Ni et al. 2024: social
    bonding increases prefrontal synchronization (d=0.85).

    f03 (group_flow_state) captures collective absorption from coordinated
    dynamics. Williamson & Bonshor 2019: group music produces flow.

    f04 (entrainment_quality) measures temporal entrainment precision from
    fast-scale onset alignment. Wohltjen et al. 2023: beat entrainment
    ability (d=1.37).

    f05 (collective_pleasure) integrates f02 and f03 with hedonic signals
    for social amplification of pleasure.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        relay_outputs: ``{"DAED": (B, T, D), "RPEM": (B, T, D)}``

    Returns:
        ``(f01, f02, f03, f04, f05)`` each ``(B, T)``
    """
    # -- H3 features --
    onset_period_500 = h3_features[_ONSET_PERIOD_H8]      # (B, T)
    pleas_mean_1s = h3_features[_PLEAS_MEAN_H16]          # (B, T)
    coupling_trend_1s = h3_features[_COUPLING_TREND_H16]  # (B, T)
    coupling_mean_5s = h3_features[_COUPLING_MEAN_H20]    # (B, T)
    loudness_trend_5s = h3_features[_LOUDNESS_TREND_H20]  # (B, T)
    warmth_mean_1s = h3_features[_WARMTH_MEAN_H16]        # (B, T)
    amp_mean_500 = h3_features[_AMP_MEAN_H8]              # (B, T)
    spectral_ent_500 = h3_features[_SPECTRAL_ENT_H8]      # (B, T)
    onset_100ms = h3_features[_ONSET_VAL_H3]              # (B, T)
    beat_period_125 = h3_features[_BEAT_PERIOD_H4]         # (B, T)
    energy_vel_500 = h3_features[_ENERGY_VEL_H8]           # (B, T)
    pleas_mean_500 = h3_features[_PLEAS_MEAN_H8]          # (B, T)

    # -- f01: Synchrony Reward --
    # Core reward from interpersonal coordination: onset periodicity at 500ms
    # (phrase-level coordination), mean pleasantness at 1s (sustained positive
    # affect), and coupling trend at 1s (consonance-energy trajectory).
    # Kokal et al. 2011: joint drumming activates caudate with synchrony.
    f01 = torch.sigmoid(
        0.25 * onset_period_500
        + 0.15 * pleas_mean_1s
        + 0.15 * coupling_trend_1s
    )

    # -- f02: Social Bonding Index --
    # Slow-building bonding from sustained coordination: coupling mean at 5s
    # (sustained emotional synchrony), f01 (synchrony reward drives bonding),
    # loudness trend at 5s (shared dynamic trajectory), warmth mean at 1s
    # (timbral blending quality). Ni et al. 2024: bonding increases rDLPFC
    # synchronization (d=0.85).
    f02 = torch.sigmoid(
        0.25 * coupling_mean_5s
        + 0.20 * f01
        + 0.15 * loudness_trend_5s
        + 0.15 * warmth_mean_1s
    )

    # -- f03: Group Flow State --
    # Collective absorption from coordinated dynamics: f01 (synchrony reward
    # grounds flow), mean amplitude at 500ms (shared dynamic envelope),
    # spectral entropy at 500ms (structural coordination demand).
    # Williamson & Bonshor 2019: brass band group music produces flow.
    f03 = torch.sigmoid(
        0.25 * f01
        + 0.15 * amp_mean_500
        + 0.15 * spectral_ent_500
    )

    # -- f04: Entrainment Quality --
    # Temporal entrainment precision from fast-scale alignment: onset
    # periodicity at 500ms (0.30), beat periodicity at 125ms (0.25),
    # onset at 100ms (0.25), energy velocity at 500ms (0.20).
    # Wohltjen et al. 2023: beat entrainment ability (d=1.37).
    f04 = torch.sigmoid(
        0.30 * onset_period_500
        + 0.25 * beat_period_125
        + 0.25 * onset_100ms
        + 0.20 * energy_vel_500
    )

    # -- f05: Collective Pleasure --
    # Shared hedonic experience integrating group flow, social bonding, and
    # mean pleasantness at 500ms. Social amplification exceeds individual
    # hedonic responses.
    f05 = torch.sigmoid(
        0.25 * pleas_mean_500
        + 0.20 * f03
        + 0.15 * f02
    )

    return f01, f02, f03, f04, f05
