"""TPIO P-Layer -- Cognitive Present (2D).

Two present-processing dimensions for timbre perception-imagery state:

  P0: pstg_activation  -- Current posterior STG activation for timbre
  P1: sma_activation   -- Current SMA activation for motor imagery

H3 consumed:
    (17, 8, 1, 0)   spectral_autocorr mean H8  -- periodicity of timbre
    (21, 8, 1, 0)   spectral_change mean H8    -- flux dynamics
    (21, 8, 8, 0)   spectral_change vel H8     -- rate of flux change
    (24, 8, 1, 0)   timbre_change mean H8      -- composite dynamics
    (14, 14, 3, 0)  tonalness std H14          -- tonal variability
    (18, 20, 22, 0) tristimulus1 autocorr H20  -- recurrence of spectral shape

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/tpio/TPIO-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_SPECTRAL_AUTO_MEAN_H8 = (17, 8, 1, 0)
_SPECTRAL_CHANGE_MEAN_H8 = (21, 8, 1, 0)
_SPECTRAL_CHANGE_VEL_H8 = (21, 8, 8, 0)
_TIMBRE_CHANGE_MEAN_H8 = (24, 8, 1, 0)
_TONALNESS_STD_H14 = (14, 14, 3, 0)
_TRIST1_AUTOCORR_H20 = (18, 20, 22, 0)


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from H3 + E/M outputs.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        m_outputs: ``(M0,)`` each ``(B, T)``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    f01, _f02, f03, f04 = e_outputs
    (m0,) = m_outputs

    B, T = r3_features.shape[:2]
    device = r3_features.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    spectral_auto_mean = h3_features.get(_SPECTRAL_AUTO_MEAN_H8, zero)
    spectral_change_mean = h3_features.get(_SPECTRAL_CHANGE_MEAN_H8, zero)
    spectral_change_vel = h3_features.get(_SPECTRAL_CHANGE_VEL_H8, zero)
    timbre_change_mean = h3_features.get(_TIMBRE_CHANGE_MEAN_H8, zero)
    tonalness_std = h3_features.get(_TONALNESS_STD_H14, zero)
    trist1_autocorr = h3_features.get(_TRIST1_AUTOCORR_H20, zero)

    # P0: pSTG Activation -- perception-imagery convergence in posterior STG
    # Halpern 2004: pSTG shows overlapping activation patterns
    p0 = torch.sigmoid(
        0.25 * f01
        + 0.20 * spectral_auto_mean
        + 0.20 * timbre_change_mean
        + 0.15 * spectral_change_mean
        + 0.10 * trist1_autocorr
        + 0.10 * m0
    )

    # P1: SMA Activation -- motor imagery contribution to timbre state
    # Zatorre 2005: SMA involved in auditory imagery generation
    p1 = torch.sigmoid(
        0.30 * f04
        + 0.25 * spectral_change_vel
        + 0.20 * tonalness_std
        + 0.15 * f03
        + 0.10 * m0
    )

    return p0, p1
