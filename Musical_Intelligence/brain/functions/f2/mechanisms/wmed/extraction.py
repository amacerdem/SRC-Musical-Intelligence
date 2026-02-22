"""WMED E-Layer -- Extraction (2D).

Dual-route extraction for working memory-entrainment dissociation:
  E0: entrainment_strength  (neural entrainment proxy from onset periodicity)
  E1: wm_contribution       (working memory proxy from entropy + change)

Route 1 (Entrainment): SS-EP-based motor coupling extracted from onset
periodicity and beat strength. Stronger entrainment to simple rhythms
paradoxically predicts worse tapping (Noboa 2025, beta=-0.418).

Route 2 (WM): Cognitive-control route extracted from distribution entropy
(syncopation) and spectral change (timing variability). Higher WM capacity
predicts better tapping via standard cognitive control.

R3 direct reads:
  [7]  amplitude          -- beat strength
  [10] onset_strength     -- loudness proxy (renamed from spectral_flux)
  [11] onset_strength     -- beat marker
  [22] distribution_entropy -- syncopation detection
  [21] spectral_change    -- timing variability

H3 demands consumed:
  onset_strength: (10,3,14,2), (11,16,14,2)
  amplitude:      (7,3,2,2)

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/wmed/
Noboa 2025: WM-entrainment paradox, EEG N=60.
Nozaradan 2011: Tagging meter with EEG, N=12.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_AMPLITUDE = 7              # beat strength (B group)
_ONSET_LOUD = 10            # onset_strength / loudness proxy (B group)
_ONSET_BEAT = 11            # onset_strength / beat marker (B group)
_SPECTRAL_CHANGE = 21       # spectral_change / timing variability (D group)
_DIST_ENTROPY = 22          # distribution_entropy / syncopation (D group)

# -- H3 keys consumed ---------------------------------------------------------
_ONSET10_H3_PERIOD = (10, 3, 14, 2)   # onset_strength at 100ms periodicity integration
_ONSET11_H16_PERIOD = (11, 16, 14, 2)  # onset_strength at 1s periodicity integration
_AMP_H3_STD = (7, 3, 2, 2)            # amplitude at 100ms std integration


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: dual-route entrainment and WM proxies.

    E0 captures neural entrainment strength via onset periodicity and
    amplitude variability -- the SS-EP route that paradoxically predicts
    worse tapping accuracy for simple rhythms (Noboa 2025).

    E1 captures working memory contribution via entropy and spectral change
    -- the cognitive control route that predicts standard tapping improvement.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    # -- R3 direct reads --
    amplitude = r3_features[..., _AMPLITUDE]           # (B, T)
    onset_loud = r3_features[..., _ONSET_LOUD]         # (B, T)
    dist_entropy = r3_features[..., _DIST_ENTROPY]     # (B, T)
    spectral_change = r3_features[..., _SPECTRAL_CHANGE]  # (B, T)

    # -- H3 features --
    onset10_period_100ms = h3_features[_ONSET10_H3_PERIOD]   # (B, T)
    onset11_period_1s = h3_features[_ONSET11_H16_PERIOD]     # (B, T)
    amp_std_100ms = h3_features[_AMP_H3_STD]                 # (B, T)

    # -- E0: Entrainment Strength --
    # Route 1: SS-EP motor coupling from onset periodicity + beat strength.
    # Nozaradan 2011: SS-EP tagging reveals beat frequency peaks.
    # Stronger periodicity + lower amplitude variability = stronger entrainment.
    e0 = torch.sigmoid(
        0.30 * onset10_period_100ms
        + 0.25 * onset11_period_1s
        + 0.25 * onset_loud
        + 0.20 * (amplitude - amp_std_100ms)
    )

    # -- E1: WM Contribution --
    # Route 2: cognitive control from entropy and spectral change.
    # Higher entropy signals syncopation complexity requiring WM.
    # Higher spectral change signals timing variability requiring WM.
    e1 = torch.sigmoid(
        0.40 * dist_entropy
        + 0.35 * spectral_change
        + 0.25 * amp_std_100ms
    )

    return e0, e1
