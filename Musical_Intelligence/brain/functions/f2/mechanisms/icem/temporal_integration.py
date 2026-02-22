"""ICEM M-Layer — Temporal Integration (5D).

Mathematical model outputs for IC-emotion mapping:
  M0: ic_value       (refined IC computation)
  M1: arousal_pred   (arousal = α·IC + β)
  M2: valence_pred   (valence = -γ·IC + δ)
  M3: scr_pred       (SCR = ε·IC + ζ)
  M4: hr_pred        (HR = -η·IC + θ)

H3 demands consumed:
  spectral_flux:        (21,3,2,2)
  sensory_pleasantness: (4,8,2,0)
  pitch_class_entropy:  (38,3,0,2)
  tonal_stability:      (60,16,13,0)

See Docs/C3/Models/PCU-a3-ICEM/ICEM.md §7.1 information content function.
Cheung 2019: uncertainty × surprise → pleasure (R²=0.654).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_SPECTRAL_FLUX_H3_STD = (21, 3, 2, 2)
_CONSONANCE_H8_STD = (4, 8, 2, 0)
_PITCH_CLASS_ENTROPY_H3 = (38, 3, 0, 2)
_TONAL_STAB_H16_ENTROPY = (60, 16, 13, 0)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Compute M-layer: IC-emotion mathematical model outputs.

    Each dimension maps IC to a specific physiological/emotional response
    following the linear relations from Egermann 2013.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(M0, M1, M2, M3, M4)`` each ``(B, T)``
    """
    e0, e1, e2, e3 = e

    spectral_flux_std = h3_features[_SPECTRAL_FLUX_H3_STD]
    consonance_std_500ms = h3_features[_CONSONANCE_H8_STD]
    pitch_class_entropy = h3_features[_PITCH_CLASS_ENTROPY_H3]
    tonal_stab_entropy_1s = h3_features[_TONAL_STAB_H16_ENTROPY]

    # -- M0: IC Value --
    # Refined information content: E0 IC proxy + pitch class entropy
    # (melodic unpredictability) + spectral flux variability + tonal
    # structural uncertainty.
    # Cheung 2019: IC × entropy interaction (β_interaction=-0.124, p<0.001).
    m0 = torch.sigmoid(
        0.40 * e0
        + 0.25 * pitch_class_entropy
        + 0.20 * spectral_flux_std
        + 0.15 * tonal_stab_entropy_1s
    )

    # -- M1: Arousal Prediction --
    # Arousal = α·IC + β. IC (surprise) directly drives arousal.
    # Egermann 2013: IC → arousal (p<0.001).
    m1 = torch.sigmoid(0.50 * e0 + 0.50 * e1)

    # -- M2: Valence Prediction --
    # Valence = -γ·IC + δ. High IC suppresses valence.
    # Egermann 2013: IC → valence↓ (p<0.001).
    m2 = torch.sigmoid(0.50 * (1.0 - e0) + 0.50 * e2)

    # -- M3: SCR Prediction --
    # SCR = ε·IC + ζ. Arousal + defense cascade predict SCR.
    # Egermann 2013: IC → SCR↑ (p<0.001).
    m3 = torch.sigmoid(0.50 * e1 + 0.50 * e3)

    # -- M4: HR Prediction --
    # HR = -η·IC + θ. Low IC + positive valence + consonance stability.
    # Egermann 2013: IC → HR↓ (deceleration, p<0.001).
    m4 = torch.sigmoid(
        0.40 * (1.0 - e0) + 0.30 * e2 + 0.30 * consonance_std_500ms
    )

    return m0, m1, m2, m3, m4
