"""STANM M-Layer -- Temporal Integration (3D).

Network integration and lateralization over temporal windows:
  M0: network_topology_m  (integrated attention network state)
  M1: local_clustering     (local network clustering coefficient)
  M2: lateralization       (hemispheric asymmetry index, TANH [-1,1])

H3 demands consumed:
  energy_change:  (22,8,2,0) energy variability 500ms (reused for M1)

E-layer inputs:
  E0: temporal_attention   (temporal stream strength)
  E1: spectral_attention   (spectral stream strength)
  E2: network_topology     (network integration state)

CRITICAL: M2 uses torch.tanh, producing values in [-1, 1].
  Positive = spectral-dominant (right hemisphere bias)
  Negative = temporal-dominant (left hemisphere bias)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/stanm/
Fritz 2007: asymmetric STRF plasticity across hemispheres.
Bidet-Caulet 2007: lateralized MEG attention effects.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ENERGY_H8_STD = (22, 8, 2, 0)           # energy variability 500ms


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: network integration and lateralization.

    M0 integrates temporal and spectral attention streams with network
    topology to compute the overall attention network state. Both streams
    contribute equally, with topology as a modulator.

    M1 captures local clustering by combining network topology (E2) with
    energy variability -- high clustering indicates tightly coupled local
    attention networks.

    M2 computes lateralization as the difference between spectral (E1)
    and temporal (E0) attention, using tanh to produce a [-1, 1] index.
    Positive = spectral-dominant (right hemisphere); negative = temporal-
    dominant (left hemisphere). Fritz 2007 and Bidet-Caulet 2007 both
    show hemispheric asymmetry in spectrotemporal processing.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``
        M0, M1 in [0, 1] (sigmoid); M2 in [-1, 1] (tanh).
    """
    e0, e1, e2 = e

    energy_var_500ms = h3_features[_ENERGY_H8_STD]

    # -- M0: Network Topology (Memory) --
    # Integrated attention network state: balanced mix of temporal (E0)
    # and spectral (E1) stream strengths, modulated by network topology (E2).
    # Fritz 2007: attention reshapes STRFs across the temporal-spectral network.
    m0 = torch.sigmoid(
        0.40 * e0
        + 0.40 * e1
        + 0.20 * e2
    )

    # -- M1: Local Clustering --
    # Local network clustering coefficient: network topology (E2) indicates
    # connectivity structure; energy variability captures dynamic range
    # within local ensembles. High clustering = tightly coupled attention.
    # Mesgarani 2012: ECoG shows clustered neural populations in STG.
    m1 = torch.sigmoid(
        0.50 * e2
        + 0.50 * energy_var_500ms
    )

    # -- M2: Lateralization --
    # Hemispheric asymmetry index using tanh: (E1 - E0) scaled by 0.50.
    # When spectral attention (E1) > temporal attention (E0): positive
    # (right hemisphere bias for spectral processing).
    # When temporal attention (E0) > spectral attention (E1): negative
    # (left hemisphere bias for temporal processing).
    # Bidet-Caulet 2007: lateralized MEG patterns during selective attention.
    m2 = torch.tanh(0.50 * (e1 - e0))

    return m0, m1, m2
