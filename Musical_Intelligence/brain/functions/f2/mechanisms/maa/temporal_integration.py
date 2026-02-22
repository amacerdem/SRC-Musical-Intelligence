"""MAA M-Layer — Temporal Integration (2D).

Temporal context for aesthetic framing and appreciation composite:
  M0: framing_effect          (how temporal context shapes aesthetic framing)
  M1: appreciation_composite  (multi-scale appreciation integration)

H3 demands consumed:
  sensory_pleasantness: (4,16,1,0), (4,16,20,0)
  tonalness:            (14,8,1,0), (14,16,1,0)
  roughness:            (0,16,1,0)
  spectral_change:      (21,8,1,0), (21,16,20,0)
  H_coupling:           (41,8,0,0), (41,16,1,0), (41,16,20,0)

See Hargreaves 1984: familiarity and complexity interact over time.
See Berlyne 1971: arousal potential accumulates through temporal exposure.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_SENSORY_PLEAS_H16_MEAN = (4, 16, 1, 0)
_SENSORY_PLEAS_H16_ENT = (4, 16, 20, 0)
_TONALNESS_H8_MEAN = (14, 8, 1, 0)
_TONALNESS_H16_MEAN = (14, 16, 1, 0)
_ROUGHNESS_H16_MEAN = (0, 16, 1, 0)
_SPECTRAL_CHANGE_H8_MEAN = (21, 8, 1, 0)
_SPECTRAL_CHANGE_H16_ENT = (21, 16, 20, 0)
_H_COUPLING_H8_VAL = (41, 8, 0, 0)
_H_COUPLING_H16_MEAN = (41, 16, 1, 0)
_H_COUPLING_H16_ENT = (41, 16, 20, 0)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: temporal context for aesthetic framing and appreciation.

    Integrates H3 temporal morphologies at multiple scales to build a
    sustained context for aesthetic evaluation. Framing effect captures
    how temporal variety (entropy) in consonance and complexity shapes
    the aesthetic frame. Appreciation composite integrates tonal anchoring
    with cross-band coupling for an overall appreciation readiness signal.

    Brattico et al. 2013: OFC engages for aesthetic framing.
    Hargreaves 1984: repeated exposure shifts preference curve.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1 = e

    pleas_mean_1s = h3_features[_SENSORY_PLEAS_H16_MEAN]
    pleas_ent_1s = h3_features[_SENSORY_PLEAS_H16_ENT]
    tonal_mean_500ms = h3_features[_TONALNESS_H8_MEAN]
    tonal_mean_1s = h3_features[_TONALNESS_H16_MEAN]
    roughness_mean_1s = h3_features[_ROUGHNESS_H16_MEAN]
    spec_change_mean_500ms = h3_features[_SPECTRAL_CHANGE_H8_MEAN]
    spec_change_ent_1s = h3_features[_SPECTRAL_CHANGE_H16_ENT]
    h_coupling_500ms = h3_features[_H_COUPLING_H8_VAL]
    h_coupling_mean_1s = h3_features[_H_COUPLING_H16_MEAN]
    h_coupling_ent_1s = h3_features[_H_COUPLING_H16_ENT]

    # -- M0: Framing Effect --
    # Aesthetic framing is shaped by temporal variety in consonance and
    # complexity. High entropy in pleasantness and spectral change signals
    # a varied passage where cognitive framing matters most.
    # Berlyne 1971: arousal potential from collative variables.
    # Brattico 2013: OFC framing for aesthetic judgment.
    m0 = torch.sigmoid(
        0.25 * pleas_ent_1s
        + 0.25 * spec_change_ent_1s
        + 0.20 * roughness_mean_1s
        + 0.15 * spec_change_mean_500ms
        + 0.15 * e0
    )

    # -- M1: Appreciation Composite --
    # Multi-scale appreciation readiness: sustained consonance context,
    # tonal anchoring across scales, and cross-band coupling integration.
    # Hargreaves 1984: familiarity + complexity → inverted-U preference.
    # Greenberg 2015: openness moderates complexity preference.
    m1 = torch.sigmoid(
        0.25 * pleas_mean_1s
        + 0.20 * tonal_mean_1s
        + 0.15 * tonal_mean_500ms
        + 0.15 * h_coupling_mean_1s
        + 0.10 * h_coupling_500ms
        + 0.10 * h_coupling_ent_1s
        + 0.05 * e1
    )

    return m0, m1
