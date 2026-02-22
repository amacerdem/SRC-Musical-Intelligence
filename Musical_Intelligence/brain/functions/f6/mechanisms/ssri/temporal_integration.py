"""SSRI M-Layer -- Temporal Integration (2D).

Social Synchrony Reward Integration mathematical model outputs:
  M0: social_prediction_error   -- Social reward prediction error [0, 1]
  M1: synchrony_amplification   -- Social reward amplification ratio [0, 1]

social_prediction_error implements a social extension of reward prediction
error. It compares actual entrainment quality (f04) against an expected
coordination baseline approximated from H3 features (mechanisms do not
have direct belief state access). Positive SPE triggers a reward surge
in downstream mesolimbic targets (NAcc, VTA); negative SPE suppresses
reward. This extends RPEM's individual prediction error to interpersonal
coordination. Cheung et al. 2019: uncertainty x surprise interaction
predicts musical pleasure. Normalized: (tanh(raw) + 1) / 2 maps to [0, 1]
where 0.5 = neutral, >0.5 = positive PE (better than expected), <0.5 =
negative PE (worse than expected).

synchrony_amplification provides a multiplicative scaling factor. Starting
from a solo baseline of 1.0, it adds the product of synchrony_reward
(f01) with the sum of entrainment_quality (f04) and social_bonding_index
(f02). This captures the key empirical finding that group music-making
amplifies hedonic reward by 1.3-1.8x compared to solitary listening,
implemented with kappa_social = 0.60. Normalized: (raw - 1.0) / 2.0 maps
[1.0, 3.0] to [0, 1] where 0 = solo baseline, 1 = maximum amplification.

H3 demands consumed: 0 tuples (operates entirely on E-layer outputs).

Dependencies:
  E-layer f01 (synchrony_reward)
  E-layer f02 (social_bonding_index)
  E-layer f04 (entrainment_quality)
  Upstream relay RPEM (for expected coordination baseline approximation)

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ssri/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- Scaling constant ----------------------------------------------------------
_KAPPA_SOCIAL = 0.60  # social amplification gain (Dunbar 2012)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: social prediction error and synchrony amplification.

    social_prediction_error (SPE) compares actual entrainment quality (f04)
    against an expected coordination baseline. Since mechanism layers lack
    direct access to belief states (expect_surprise[10:20]), we approximate
    the baseline from the upstream RPEM relay output. Positive SPE indicates
    better-than-expected coordination producing a reward surge; negative SPE
    signals coordination breakdown and reward suppression. Raw value bounded
    to [-1, 1] via tanh, then normalized to [0, 1] via (tanh + 1) / 2.

    synchrony_amplification (SA) provides a multiplicative reward boost from
    successful group coordination. SA = 1.0 + kappa_social * f01 * (f04 + f02).
    Raw value ranges from 1.0 (solo baseline) to approximately 3.0 (maximum
    social amplification). Normalized to [0, 1] via (raw - 1.0) / 2.0.
    Implements the 1.3-1.8x range reported for group vs solo music-making
    (Dunbar 2012).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e_outputs: ``(f01, f02, f03, f04, f05)`` from extraction layer.
        relay_outputs: ``{"DAED": ..., "RPEM": ...}``

    Returns:
        ``(social_prediction_error, synchrony_amplification)`` each ``(B, T)``
    """
    f01, f02, _f03, f04, _f05 = e_outputs

    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- Approximate expected coordination baseline from RPEM relay --
    # RPEM provides reward prediction error signals; we use its mean
    # activation as a proxy for expected coordination quality.
    # Graceful fallback if RPEM is not available.
    rpem = relay_outputs.get("RPEM", torch.zeros(B, T, 8, device=device))
    expected_coordination = rpem.mean(dim=-1).clamp(0.0, 1.0)  # (B, T)

    # -- social_prediction_error (SPE) --
    # SPE = (tanh(f04 - expected_coordination) + 1) / 2
    # Positive PE (>0.5): better-than-expected coordination -> reward surge
    # Negative PE (<0.5): coordination breakdown -> reward suppression
    # Neutral (0.5): coordination meets expectation
    # Cheung et al. 2019: uncertainty x surprise interaction predicts pleasure
    spe_raw = f04 - expected_coordination
    social_prediction_error = (torch.tanh(spe_raw) + 1.0) * 0.5  # [0, 1]

    # -- synchrony_amplification (SA) --
    # SA_raw = 1.0 + kappa_social * f01 * (f04 + f02), range [1.0, ~3.0]
    # Normalized: (SA_raw - 1.0) / 2.0, range [0, 1]
    # 0 = solo baseline (no amplification), 1 = maximum social amplification
    # Dunbar 2012: synchronized music-making amplifies reward 1.3-1.8x
    sa_raw = (
        1.0 + _KAPPA_SOCIAL * f01 * (f04 + f02)
    ).clamp(1.0, 3.0)
    synchrony_amplification = (sa_raw - 1.0) * 0.5  # [0, 1]

    return social_prediction_error, synchrony_amplification
