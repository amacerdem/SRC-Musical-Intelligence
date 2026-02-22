"""HTP E-Layer — Extraction (4D).

Hierarchical prediction latency across three abstraction levels:
  E0: high_level_lead    (~500ms, abstract patterns, STG/aIPL)
  E1: mid_level_lead     (~200ms, perceptual features, belt cortex)
  E2: low_level_lead     (~110ms, sensory features, A1)
  E3: hierarchy_gradient  (gradient strength = f(E0 - E2))

H3 demands consumed:
  tonal_stability: (60,8,0,0), (60,8,1,0), (60,16,1,0)
  sharpness:       (13,4,8,0), (13,8,1,0)
  amplitude:       (7,0,0,2)
  onset_strength:  (11,3,14,2)
  spectral_auto:   (17,3,0,2)
  pitch_salience:  (39,4,8,0)

R3 direct reads:
  tristimulus1-3:  [18:21] — averaged for high-level abstract signal

See Docs/C3/Models/PCU-a1-HTP/HTP.md §6.1 Layer E, §7.2 formulas.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_TRISTIMULUS_START = 18
_TRISTIMULUS_END = 21

# -- H3 keys consumed ---------------------------------------------------------
_TONAL_STAB_H8_VAL = (60, 8, 0, 0)
_TONAL_STAB_H8_MEAN = (60, 8, 1, 0)
_TONAL_STAB_H16_MEAN = (60, 16, 1, 0)
_SHARPNESS_H4_VEL = (13, 4, 8, 0)
_SHARPNESS_H8_MEAN = (13, 8, 1, 0)
_AMPLITUDE_H0_VAL = (7, 0, 0, 2)
_ONSET_H3_PERIOD = (11, 3, 14, 2)
_SPECTRAL_AUTO_H3_VAL = (17, 3, 0, 2)
_PITCH_SAL_H4_VEL = (39, 4, 8, 0)


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: hierarchical prediction leads.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``
    """
    # -- R3 direct reads --
    trist_mean = r3_features[..., _TRISTIMULUS_START:_TRISTIMULUS_END].mean(
        dim=-1
    )  # (B, T) — harmonic balance as high-level abstract signal

    # -- H3 features --
    tonal_stab_mean_1s = h3_features[_TONAL_STAB_H16_MEAN]
    tonal_stab_500ms = h3_features[_TONAL_STAB_H8_VAL]
    sharpness_vel_125ms = h3_features[_SHARPNESS_H4_VEL]
    sharpness_mean_500ms = h3_features[_SHARPNESS_H8_MEAN]
    amplitude_h0 = h3_features[_AMPLITUDE_H0_VAL]
    onset_period_100ms = h3_features[_ONSET_H3_PERIOD]
    spectral_auto_100ms = h3_features[_SPECTRAL_AUTO_H3_VAL]
    pitch_sal_vel = h3_features[_PITCH_SAL_H4_VEL]

    # -- E0: High-Level Lead (~500ms) --
    # Abstract prediction: harmonic balance + tonal stability over long windows.
    # de Vries & Wurm 2023: view-invariant (abstract) predicted ~500ms ahead.
    e0 = torch.sigmoid(
        0.40 * trist_mean
        + 0.35 * tonal_stab_mean_1s
        + 0.25 * tonal_stab_500ms
    )

    # -- E1: Mid-Level Lead (~200ms) --
    # Perceptual prediction: brightness dynamics + pitch salience velocity.
    # de Vries & Wurm 2023: view-dependent predicted ~200ms ahead.
    e1 = torch.sigmoid(
        0.40 * sharpness_mean_500ms
        + 0.30 * sharpness_vel_125ms
        + 0.30 * pitch_sal_vel
    )

    # -- E2: Low-Level Lead (~110ms) --
    # Sensory prediction: amplitude + onset periodicity + spectral coupling.
    # de Vries & Wurm 2023: optical flow / sensory predicted ~110ms ahead.
    e2 = torch.sigmoid(
        0.40 * amplitude_h0
        + 0.35 * onset_period_100ms
        + 0.25 * spectral_auto_100ms
    )

    # -- E3: Hierarchy Gradient --
    # Strength of hierarchical prediction gradient. When high-level leads
    # are strong and low-level leads are weak, the predictive hierarchy
    # is maximally engaged. de Vries & Wurm 2023: ηp² = 0.49.
    e3 = torch.sigmoid(0.50 * (e0 - e2))

    return e0, e1, e2, e3
