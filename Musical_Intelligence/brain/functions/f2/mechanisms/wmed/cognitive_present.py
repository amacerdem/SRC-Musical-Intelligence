"""WMED P-Layer -- Cognitive Present (3D).

Present-processing integration for rhythm perception via dual routes:
  P0: phase_locking_strength   (current SS-EP phase-locking quality)
  P1: pattern_segmentation     (rhythmic pattern boundary detection)
  P2: rhythmic_engagement      (overall rhythmic engagement combining both routes)

This layer reads upstream PWUP (Encoder, depth 1) to incorporate
precision-weighted prediction error into rhythm processing:
  PWUP[2] = M0:weighted_error       -- prediction error magnitude
  PWUP[3] = M1:uncertainty_index    -- prediction uncertainty
  PWUP[4] = P0:tonal_precision_weight -- precision weighting

H3 demands consumed:
  chroma_C:         (25,3,14,2)   -- 100ms periodicity integration
  chroma_C:         (25,16,14,2)  -- 1s periodicity integration
  chroma_C:         (25,16,21,2)  -- 1s M21 integration
  H_coupling:       (41,16,1,0)   -- 1s mean memory
  onset_strength:   (10,16,14,2)  -- 1s periodicity integration
  spectral_change:  (21,16,19,0)  -- 1s M19 memory

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/wmed/
Large 2008: Neural resonance theory.
Nozaradan 2011: SS-EP at beat frequency.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CHROMA_C_H3_PERIOD = (25, 3, 14, 2)    # chroma_C at 100ms periodicity integration
_CHROMA_C_H16_PERIOD = (25, 16, 14, 2)  # chroma_C at 1s periodicity integration
_CHROMA_C_H16_M21 = (25, 16, 21, 2)     # chroma_C at 1s M21 integration
_H_COUPLING_H16_MEAN = (41, 16, 1, 0)   # H_coupling at 1s mean memory
_ONSET10_H16_PERIOD = (10, 16, 14, 2)   # onset_strength at 1s periodicity integration
_SPEC_CHANGE_H16_M19 = (21, 16, 19, 0)  # spectral_change at 1s M19 memory

# -- PWUP upstream output indices (Encoder, 10D) ------------------------------
_PWUP_M0_WEIGHTED_ERROR = 2       # M0:weighted_error
_PWUP_M1_UNCERTAINTY = 3          # M1:uncertainty_index
_PWUP_P0_PRECISION_WEIGHT = 4     # P0:tonal_precision_weight


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: present-processing rhythm perception integration.

    P0 captures phase-locking quality from entrainment (E0), chroma
    periodicity, and onset periodicity at 1s scale. Modulated by PWUP
    precision weighting.

    P1 captures rhythmic pattern segmentation from WM contribution (E1),
    dissociation (M1), and spectral change M19 (pattern boundary proxy).

    P2 captures overall rhythmic engagement combining both routes with
    prediction error from PWUP to assess active engagement quality.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        upstream_outputs: ``{"PWUP": (B, T, 10)}``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    e0, e1 = e
    m0, m1 = m

    pwup = upstream_outputs["PWUP"]  # (B, T, 10)
    pwup_error = pwup[..., _PWUP_M0_WEIGHTED_ERROR]         # (B, T)
    pwup_uncertainty = pwup[..., _PWUP_M1_UNCERTAINTY]       # (B, T)
    pwup_precision = pwup[..., _PWUP_P0_PRECISION_WEIGHT]    # (B, T)

    chroma_period_100ms = h3_features[_CHROMA_C_H3_PERIOD]   # (B, T)
    chroma_period_1s = h3_features[_CHROMA_C_H16_PERIOD]     # (B, T)
    chroma_m21_1s = h3_features[_CHROMA_C_H16_M21]           # (B, T)
    h_coupling_mean_1s = h3_features[_H_COUPLING_H16_MEAN]   # (B, T)
    onset10_period_1s = h3_features[_ONSET10_H16_PERIOD]     # (B, T)
    spec_change_m19_1s = h3_features[_SPEC_CHANGE_H16_M19]   # (B, T)

    # -- P0: Phase Locking Strength --
    # SS-EP phase-locking quality: entrainment + onset periodicity at beat scale
    # + chroma periodicity (harmonic regularity supports entrainment).
    # Precision-weighted by PWUP to reflect confidence in phase lock.
    # Large 2008: neural resonance at beat frequency.
    p0 = torch.sigmoid(
        0.30 * e0
        + 0.20 * onset10_period_1s
        + 0.20 * chroma_period_1s
        + 0.15 * h_coupling_mean_1s
        + 0.15 * pwup_precision
    )

    # -- P1: Pattern Segmentation --
    # Rhythmic boundary detection: WM contribution + dissociation index
    # + spectral change M19 (temporal pattern boundary proxy).
    # Higher uncertainty from PWUP signals pattern transitions.
    # Nozaradan 2011: meter tagging reveals pattern structure.
    p1 = torch.sigmoid(
        0.25 * e1
        + 0.25 * m1
        + 0.20 * spec_change_m19_1s
        + 0.15 * chroma_m21_1s
        + 0.15 * pwup_uncertainty
    )

    # -- P2: Rhythmic Engagement --
    # Overall engagement combining both routes. Tapping accuracy (M0)
    # + chroma periodicity + prediction error as engagement amplifier.
    # Strong PE means active prediction = high engagement.
    p2 = torch.sigmoid(
        0.25 * m0
        + 0.20 * e0
        + 0.20 * chroma_period_100ms
        + 0.20 * pwup_error
        + 0.15 * e1
    )

    return p0, p1, p2
