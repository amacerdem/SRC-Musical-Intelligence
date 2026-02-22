"""UDP E-Layer -- Extraction (2D).

Uncertainty level and confirmation reward from instantaneous R3 features:
  E0: uncertainty_level      (inverse tonal certainty -- high = uncertain context)
  E1: confirmation_reward    (hedonic value when prediction confirmed under uncertainty)

R3 direct reads:
  sensory_pleasantness:  [4]     -- hedonic baseline
  periodicity:           [5]     -- tonal certainty (inverted for uncertainty)
  tonalness:             [14]    -- key clarity proxy (inverted for uncertainty)
  tristimulus1-3:        [18:21] -- harmonic balance for reward signal

No H3 or upstream dependencies -- pure R3 extraction.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/udp/
Gold et al. 2019: pleasure from prediction confirmation in uncertain contexts.
Cheung et al. 2019: uncertainty x surprise interaction drives pleasure.
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_SENSORY_PLEAS = 4
_PERIODICITY = 5
_TONALNESS = 14
_TRISTIMULUS_START = 18
_TRISTIMULUS_END = 21


def compute_extraction(
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: uncertainty level and confirmation reward.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    # -- R3 direct reads --
    pleasantness = r3_features[..., _SENSORY_PLEAS]       # (B, T)
    periodicity = r3_features[..., _PERIODICITY]           # (B, T)
    tonalness = r3_features[..., _TONALNESS]               # (B, T)
    trist_mean = r3_features[..., _TRISTIMULUS_START:_TRISTIMULUS_END].mean(
        dim=-1
    )  # (B, T) -- harmonic balance

    # -- E0: Uncertainty Level --
    # High when tonalness and periodicity are low (atonal, aperiodic context).
    # Inverted tonal features: uncertainty = 1 - tonal_certainty.
    # Cheung et al. 2019: NAc encodes uncertainty level.
    e0 = torch.sigmoid(
        0.50 * (1.0 - tonalness)
        + 0.50 * (1.0 - periodicity)
    )

    # -- E1: Confirmation Reward --
    # Hedonic value gated by uncertainty. When uncertainty is high,
    # any hedonic signal (pleasantness + harmonic balance) is amplified.
    # Gold et al. 2019: correct predictions under uncertainty are more rewarding.
    e1 = torch.sigmoid(
        0.40 * pleasantness
        + 0.30 * trist_mean
        + 0.30 * e0
    )

    return e0, e1
