"""DGTP M-Layer -- Temporal Integration (2D).

Temporal dynamics of domain correlation and shared variance:
  M0: domain_correlation  (product interaction of music and speech timing)
  M1: shared_variance     (stability of shared mechanism over time)

M0 captures the cross-domain interaction: when both music timing (E0)
and speech timing (E1) are active, timing circuits are shared.
Coupling mean at 1s provides sustained integration context.

M1 captures the stability of the shared mechanism (E2) over time,
modulated by coupling stability which reflects consistent timing
precision across domains.

H3 demands consumed:
  x_l0l5: (25,16,1,0)  coupling mean 1s memory
  x_l0l5: (25,16,19,0) coupling stability 1s memory

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/dgtp/
Patel 2011: OPERA hypothesis -- shared neural resources.
Grahn 2012: BG-cortical coupling for beat processing.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_COUPLING_H16_MEAN = (25, 16, 1, 0)   # x_l0l5 mean 1s memory
_COUPLING_H16_STAB = (25, 16, 19, 0)  # x_l0l5 stability 1s memory


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: domain correlation and shared variance.

    M0 integrates the product interaction of E0 (music) and E1 (speech)
    with coupling mean to estimate the degree of cross-domain temporal
    correlation. High M0 = music and speech timing circuits overlap.

    M1 captures the stability of the shared mechanism (E2) over time,
    reflecting how consistently the shared timing infrastructure is
    engaged. Coupling stability provides the multi-scale anchor.

    Patel 2011: OPERA hypothesis predicts high correlation when both
    domains engage overlapping circuits.
    Grahn 2012: BG-cortical coupling strength reflects timing integration.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1, e2 = e

    coupling_mean_1s = h3_features[_COUPLING_H16_MEAN]       # (B, T)
    coupling_stability_1s = h3_features[_COUPLING_H16_STAB]  # (B, T)

    # -- M0: Domain Correlation --
    # Cross-domain temporal correlation: product interaction of music
    # and speech timing (E0 * E1) reflects shared activation, plus
    # coupling mean provides sustained integration context.
    # Patel 2011: OPERA overlap predicts correlated timing.
    m0 = torch.sigmoid(
        0.50 * e0 * e1
        + 0.50 * coupling_mean_1s
    )

    # -- M1: Shared Variance --
    # Stability of shared mechanism over time: E2 (geometric mean proxy)
    # reflects instantaneous shared variance, coupling stability provides
    # the sustained timing precision anchor.
    m1 = torch.sigmoid(
        0.50 * e2
        + 0.50 * coupling_stability_1s
    )

    return m0, m1
