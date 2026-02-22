"""SDL M-Layer -- Temporal Integration (2D).

Lateralization integration and salience demand over temporal windows:
  M0: lateralization_index  (integrated hemispheric asymmetry, TANH [-1, 1])
  M1: salience_demand       (salience-driven processing demand, sigmoid [0, 1])

H3 demands consumed:
  spectral_centroid: (15,3,0,2)   centroid value 100ms (reused)
  spectral_flux:     (10,3,0,2)   flux value 100ms (reused)
  loudness:          (8,16,20,2)  loudness entropy 1s (reused)

E-layer inputs:
  E0: dynamic_lateral  (lateralization index, tanh [-1, 1])
  E1: local_clustering (network clustering, sigmoid [0, 1])

CRITICAL: M0 uses torch.tanh, producing values in [-1, 1].
  Positive = spectral-dominant (right hemisphere bias)
  Negative = temporal-dominant (left hemisphere bias)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/sdl/
Poeppel 2003: asymmetric sampling in time.
Zatorre 2002: hemispheric specialization review.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CENTROID_H3_VAL = (15, 3, 0, 2)       # centroid value 100ms -- spectral focus
_FLUX_H3_VAL = (10, 3, 0, 2)           # flux value 100ms -- temporal focus
_LOUD_H16_ENT = (8, 16, 20, 2)         # loudness entropy 1s -- salience demand


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: lateralization integration and salience demand.

    M0 integrates E0 (dynamic lateralization) with the raw spectral-temporal
    contrast (centroid - flux) to produce a smoothed lateralization index.
    Uses tanh to maintain [-1, 1] range. The 50/50 weighting balances
    the E-layer lateralization estimate with the direct spectral-temporal
    contrast from H3 features.

    M1 captures salience-driven processing demand by combining loudness
    entropy (acoustic salience at 1s scale) with E1 (local clustering),
    reflecting how much processing resource the current scene demands.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
        M0 in [-1, 1] (tanh); M1 in [0, 1] (sigmoid).
    """
    e0, e1, _e2 = e

    centroid_100ms = h3_features[_CENTROID_H3_VAL]
    flux_100ms = h3_features[_FLUX_H3_VAL]
    loudness_entropy_1s = h3_features[_LOUD_H16_ENT]

    # -- M0: Lateralization Index --
    # Integrated hemispheric asymmetry: E0 (E-layer lateralization) combined
    # with raw spectral-temporal contrast (centroid - flux).
    # Positive = spectral-dominant (right hemisphere bias)
    # Negative = temporal-dominant (left hemisphere bias)
    # Poeppel 2003: lateralization reflects asymmetric temporal windows.
    m0 = torch.tanh(
        0.50 * e0
        + 0.50 * (centroid_100ms - flux_100ms)
    )

    # -- M1: Salience Demand --
    # Processing demand driven by acoustic salience: loudness entropy (1s)
    # captures unpredictability of intensity (high entropy = salient);
    # E1 (local clustering) captures network engagement level.
    # Zatorre 2002: salience modulates degree of lateralization.
    m1 = torch.sigmoid(
        0.50 * loudness_entropy_1s
        + 0.50 * e1
    )

    return m0, m1
