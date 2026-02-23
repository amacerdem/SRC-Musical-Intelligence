"""PWSM M-Layer -- Temporal Integration (2D).

Two memory dimensions for precision-weighted error dynamics:

  M0: pe_weighted -- Precision-weighted prediction error strength
  M1: precision   -- Current precision estimate (inverse variance)

H3 consumed:
    (10, 3, 0, 2)   spectral_flux value H3 bidi    -- instant onset for PE
    (22, 3, 0, 2)    entropy value H3 bidi          -- instant complexity
    (37, 3, 0, 2)    pitch_height value H3 bidi     -- pitch for PE baseline
    (10, 0, 0, 2)    spectral_flux value H0 bidi    -- fast onset at brainstem
    (10, 1, 1, 2)    spectral_flux mean H1 bidi     -- sustained fast onset
    (10, 4, 17, 2)   spectral_flux peaks H4 bidi    -- beta-rate peaks for PE

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/pwsm/PWSM-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_FLUX_H3 = (10, 3, 0, 2)
_ENTROPY_H3 = (22, 3, 0, 2)
_PITCH_H3 = (37, 3, 0, 2)
_FLUX_H0 = (10, 0, 0, 2)
_FLUX_MEAN_H1 = (10, 1, 1, 2)
_FLUX_PEAKS_H4 = (10, 4, 17, 2)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from H3 + E-layer.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f19, f20, f21)`` each ``(B, T)``.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    f19, f20, f21 = e_outputs

    B = f19.shape[0]
    T = f19.shape[1] if f19.dim() > 1 else 1
    device = f19.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    flux_h3 = h3_features.get(_FLUX_H3, zero)
    entropy_h3 = h3_features.get(_ENTROPY_H3, zero)
    pitch_h3 = h3_features.get(_PITCH_H3, zero)
    flux_h0 = h3_features.get(_FLUX_H0, zero)
    flux_mean_h1 = h3_features.get(_FLUX_MEAN_H1, zero)
    flux_peaks_h4 = h3_features.get(_FLUX_PEAKS_H4, zero)

    # M0: PE Weighted -- precision-weighted prediction error
    # Garrido 2009: PE = precision * (observation - prediction)
    # Here approximated as precision_weighting * deviation signals
    m0 = torch.sigmoid(
        0.30 * f19 * flux_h3
        + 0.20 * pitch_h3
        + 0.20 * entropy_h3
        + 0.15 * flux_h0
        + 0.15 * (1.0 - f20)
    )

    # M1: Precision -- current precision estimate
    # Friston 2005: precision = 1/variance, estimated from context stability
    m1 = torch.sigmoid(
        0.30 * f21
        + 0.25 * (1.0 - entropy_h3)
        + 0.20 * flux_mean_h1
        + 0.15 * flux_peaks_h4
        + 0.10 * f19
    )

    return m0, m1
