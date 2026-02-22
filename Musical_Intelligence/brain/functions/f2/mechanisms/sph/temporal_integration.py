"""SPH M-Layer — Temporal Integration (4D).

Match/mismatch response signals and oscillatory power signatures:
  M0: match_response     (confirmed prediction timing ~350ms, positive)
  M1: varied_response    (prediction error timing ~250ms, negative)
  M2: gamma_power        (matched sequence oscillatory signature)
  M3: alpha_beta_power   (varied sequence oscillatory signature)

H3 demands consumed:
  sensory_pleasantness: (4,3,0,2) reused from E-layer
  amplitude:            (7,3,2,2)
  spectral_flux:        (21,3,2,2) reused from E-layer
  tonal_stability:      (60,8,1,0)

R3 direct reads:
  sensory_pleasantness: [4] — modulates gamma/alpha-beta balance

See Docs/C3/Models/PCU-a2-SPH/SPH.md §6.1 Layer M.
Bonetti 2024: memorised=positive ~350ms, varied=negative ~250ms.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_SENSORY_PLEAS = 4

# -- H3 keys consumed ---------------------------------------------------------
_CONSONANCE_H3_VAL = (4, 3, 0, 2)
_AMPLITUDE_H3_STD = (7, 3, 2, 2)
_SPECTRAL_FLUX_H3_STD = (21, 3, 2, 2)
_TONAL_STAB_H8_MEAN = (60, 8, 1, 0)


def compute_temporal_integration(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute M-layer: match/mismatch responses and oscillatory power.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(M0, M1, M2, M3)`` each ``(B, T)``
    """
    e0, e1, _e2, _e3 = e

    sensory_pleas = r3_features[..., _SENSORY_PLEAS]
    consonance_100ms = h3_features[_CONSONANCE_H3_VAL]
    amplitude_std_100ms = h3_features[_AMPLITUDE_H3_STD]
    spectral_flux_std_100ms = h3_features[_SPECTRAL_FLUX_H3_STD]
    tonal_stab_mean_500ms = h3_features[_TONAL_STAB_H8_MEAN]

    # -- M0: Match Response (~350ms) --
    # Confirmed prediction timing. Positive polarity at ~350ms latency.
    # Gamma match + consonance context + long-range tonal stability.
    # Bonetti 2024: memorised sequences → positive components at ~350ms.
    m0 = torch.sigmoid(
        0.40 * e0 + 0.30 * consonance_100ms + 0.30 * tonal_stab_mean_500ms
    )

    # -- M1: Varied Response (~250ms) --
    # Prediction error timing. Negative polarity at ~250ms (faster than match).
    # Alpha-beta error + amplitude variability + spectral flux variability.
    # Bonetti 2024: varied sequences → negative components at ~250ms.
    m1 = torch.sigmoid(
        0.40 * e1 + 0.30 * amplitude_std_100ms + 0.30 * spectral_flux_std_100ms
    )

    # -- M2: Gamma Power --
    # Oscillatory signature for matched/memorised sequences.
    # Gamma power enhanced when prediction confirmed (high sensory pleasantness).
    # Bonetti 2024: gamma power M > N.
    m2 = torch.sigmoid(0.50 * e0 + 0.50 * sensory_pleas)

    # -- M3: Alpha-Beta Power --
    # Oscillatory signature for varied/prediction-error sequences.
    # Alpha-beta enhanced when prediction violated (low sensory pleasantness).
    # Bonetti 2024: alpha-beta power N > M.
    m3 = torch.sigmoid(0.50 * e1 + 0.50 * (1.0 - sensory_pleas))

    return m0, m1, m2, m3
