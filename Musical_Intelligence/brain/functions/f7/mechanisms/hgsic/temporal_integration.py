"""HGSIC M-Layer -- Temporal Integration (2D).

Two memory dimensions capturing groove state dynamics:

  M0: groove_index     -- Overall groove strength (inverted-U with syncopation)
  M1: coupling_strength -- Motor-auditory coupling strength for groove

H3 consumed:
    (22, 11, 1, 0)    entropy mean H11        -- spectral complexity at measure
    (22, 11, 14, 2)   entropy periodicity H11 -- complexity cycling
    (21, 11, 1, 0)    spectral_change mean H11 -- flux dynamics at measure
    (8, 11, 1, 0)     loudness mean H11        -- sustained loudness baseline

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hgsic/HGSIC-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ENTROPY_MEAN_H11 = (22, 11, 1, 0)
_ENTROPY_PERIOD_H11 = (22, 11, 14, 2)
_SPECTRAL_CHANGE_MEAN_H11 = (21, 11, 1, 0)
_LOUDNESS_MEAN_H11 = (8, 11, 1, 0)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from H3 + E-layer.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03)`` each ``(B, T)``.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    f01, f02, f03 = e_outputs

    B = f01.shape[0]
    T = f01.shape[1] if f01.dim() > 1 else 1
    device = f01.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    entropy_mean = h3_features.get(_ENTROPY_MEAN_H11, zero)
    entropy_period = h3_features.get(_ENTROPY_PERIOD_H11, zero)
    spectral_change_mean = h3_features.get(_SPECTRAL_CHANGE_MEAN_H11, zero)
    loudness_mean = h3_features.get(_LOUDNESS_MEAN_H11, zero)

    # M0: Groove Index -- overall groove strength
    # Madison 2011: inverted-U function -- medium complexity maximizes groove
    # Beat gamma * meter integration captures syncopation level
    m0 = torch.sigmoid(
        0.30 * f01 * f02
        + 0.25 * entropy_period
        + 0.25 * loudness_mean
        + 0.20 * spectral_change_mean
    )

    # M1: Coupling Strength -- motor-auditory coupling for groove
    # Janata 2012: motor cortex coupling with auditory processing
    m1 = torch.sigmoid(
        0.35 * f03
        + 0.25 * entropy_mean
        + 0.20 * f01
        + 0.20 * loudness_mean
    )

    return m0, m1
