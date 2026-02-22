"""STANM P-Layer -- Cognitive Present (2D).

Present-state resource allocation across temporal and spectral dimensions:
  P0: temporal_alloc   (resource allocation to temporal processing)
  P1: spectral_alloc   (resource allocation to spectral processing)

H3 demands consumed:
  spectral_flux:  (10,16,14,2) temporal periodicity 1s (reused)
  tonalness:      (14,16,1,2)  tonalness mean 1s (reused)

E-layer inputs:
  E0: temporal_attention  (temporal stream strength)
  E1: spectral_attention  (spectral stream strength)

M-layer inputs:
  M0: network_topology_m  (integrated network state)

The P-layer computes how attention resources are currently distributed
between temporal and spectral processing. Both dimensions combine
bottom-up E-layer salience with M-layer network integration and
long-timescale H3 context features.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/stanm/
Fritz 2007: dynamic resource allocation in STRF plasticity.
Bidet-Caulet 2007: sustained attention allocation in MEG.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_FLUX_H16_PERIOD = (10, 16, 14, 2)       # temporal periodicity 1s
_TONAL_H16_MEAN = (14, 16, 1, 2)         # tonalness mean 1s


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: present-state attention resource allocation.

    P0 (temporal allocation) combines temporal attention (E0) with
    network integration (M0) and long-range temporal periodicity. High
    temporal periodicity at 1s scale provides a stable temporal scaffold
    for resource allocation.

    P1 (spectral allocation) combines spectral attention (E1) with
    network integration (M0) and sustained tonalness. High tonalness
    indicates rich spectral content deserving increased allocation.

    Fritz 2007: STRFs show rapid reallocation of processing resources
    between temporal and spectral features during active listening.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1, M2)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, e1, _e2 = e
    m0, _m1, _m2 = m

    temporal_period_1s = h3_features[_FLUX_H16_PERIOD]
    tonalness_mean_1s = h3_features[_TONAL_H16_MEAN]

    # -- P0: Temporal Allocation --
    # Resource allocation to temporal processing: temporal attention (E0)
    # provides the bottom-up drive; network integration (M0) gates
    # overall allocation capacity; temporal periodicity at 1s adds
    # context-dependent scaffolding from beat-scale regularity.
    # Fritz 2007: temporal attention enhances temporal modulation STRFs.
    p0 = torch.sigmoid(
        0.40 * e0
        + 0.30 * m0
        + 0.30 * temporal_period_1s
    )

    # -- P1: Spectral Allocation --
    # Resource allocation to spectral processing: spectral attention (E1)
    # provides the bottom-up drive; network integration (M0) gates
    # capacity; sustained tonalness (1s mean) indicates rich spectral
    # structure worth allocating resources to.
    # Bidet-Caulet 2007: spectral attention enhances gamma for tonal features.
    p1 = torch.sigmoid(
        0.40 * e1
        + 0.30 * m0
        + 0.30 * tonalness_mean_1s
    )

    return p0, p1
