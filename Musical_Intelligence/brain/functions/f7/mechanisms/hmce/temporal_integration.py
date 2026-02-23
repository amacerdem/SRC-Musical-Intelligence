"""HMCE M-Layer -- Temporal Integration (3D).

Three memory dimensions capturing context dynamics:

  M0: context_depth         -- How deep the hierarchical context extends
  M1: structure_regularity  -- Degree of structural regularity detected
  M2: transition_dynamics   -- Rate and direction of context change

H3 consumed:
    (60, 8, 18, 0)   x_l0l2l5 trend H8     -- context depth direction (medium)
    (60, 16, 18, 0)  x_l0l2l5 trend H16    -- context depth direction (long)
    (51, 8, 1, 0)    x_l5l7 mean H8        -- coupling strength
    (17, 16, 1, 0)   spectral_autocorr mean H16 -- tonal regularity
    (11, 16, 14, 0)  onset_strength period H16   -- structural regularity at beat

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/hmce/HMCE-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_HIER_TREND_H8 = (60, 8, 18, 0)
_HIER_TREND_H16 = (60, 16, 18, 0)
_CONTEXT_MEAN_H8 = (51, 8, 1, 0)
_SPECTRAL_AUTO_MEAN_H16 = (17, 16, 1, 0)
_ONSET_PERIOD_H16 = (11, 16, 14, 0)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from H3 + E-layer.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03)`` each ``(B, T)``.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``.
    """
    f01, f02, f03 = e_outputs

    # Infer B, T, device from E-layer output
    B = f01.shape[0]
    T = f01.shape[1] if f01.dim() > 1 else 1
    device = f01.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    hier_trend_h8 = h3_features.get(_HIER_TREND_H8, zero)
    hier_trend_h16 = h3_features.get(_HIER_TREND_H16, zero)
    context_mean_h8 = h3_features.get(_CONTEXT_MEAN_H8, zero)
    spectral_auto_mean_h16 = h3_features.get(_SPECTRAL_AUTO_MEAN_H16, zero)
    onset_period_h16 = h3_features.get(_ONSET_PERIOD_H16, zero)

    # M0: Context Depth -- how deep the hierarchical context extends
    # Pearce 2018: statistical learning accumulates context at multiple scales
    m0 = torch.sigmoid(
        0.30 * hier_trend_h8
        + 0.30 * hier_trend_h16
        + 0.20 * f02
        + 0.20 * f03
    )

    # M1: Structure Regularity -- degree of structural regularity
    # Tillmann 2003: implicit tonal structure yields automatic priming
    m1 = torch.sigmoid(
        0.35 * spectral_auto_mean_h16
        + 0.35 * onset_period_h16
        + 0.30 * context_mean_h8
    )

    # M2: Transition Dynamics -- rate and direction of context change
    # Koelsch 2009: surprise at structural boundaries modulates ACC
    m2 = torch.sigmoid(
        0.35 * torch.abs(hier_trend_h8 - hier_trend_h16)
        + 0.30 * context_mean_h8
        + 0.20 * f01
        + 0.15 * f03
    )

    return m0, m1, m2
