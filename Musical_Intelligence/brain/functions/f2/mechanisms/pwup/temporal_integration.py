"""PWUP M-Layer -- Temporal Integration (2D).

Precision-weighted error and uncertainty index over temporal windows:
  M0: weighted_error     (PE magnitude weighted by current precision)
  M1: uncertainty_index  (contextual uncertainty from entropy + variability)

H3 demands consumed:
  consonance:        (4,3,0,2)   value at 100ms integration
  consonance:        (4,16,20,0) entropy at 1s memory
  tonalness:         (14,8,1,0)  mean at 500ms memory
  spectral_change:   (21,3,0,2)  value at 100ms integration
  spectral_change:   (21,3,2,2)  std at 100ms integration
  onset_strength:    (10,3,0,2)  value at 100ms integration
  tonal_stability:   (41,8,0,0)  value at 500ms memory

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/pwup/
Garrido et al. 2009: precision-weighted PE in predictive coding (fMRI, N=16).
Friston 2005: PE is weighted by inverse variance (precision) of the generative model.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CONSONANCE_H3_VAL = (4, 3, 0, 2)           # consonance at 100ms value integration
_CONSONANCE_H16_ENT = (4, 16, 20, 0)        # consonance entropy at 1s memory
_TONALNESS_H8_MEAN = (14, 8, 1, 0)          # tonalness mean at 500ms memory
_SPEC_CHANGE_H3_VAL = (21, 3, 0, 2)         # spectral_change at 100ms value integration
_SPEC_CHANGE_H3_STD = (21, 3, 2, 2)         # spectral_change std at 100ms integration
_ONSET_H3_VAL = (10, 3, 0, 2)               # onset_strength at 100ms value integration
_TONAL_STAB_H8_VAL = (41, 8, 0, 0)          # tonal_stability at 500ms value memory


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: precision-weighted error and uncertainty.

    M0 combines prediction error proxies (spectral change, onset events)
    weighted by the E-layer precision estimates. High precision attenuates
    expected signals; low precision passes errors through.

    M1 captures contextual uncertainty from consonance entropy and
    spectral variability -- reflecting the inverse of precision in the
    generative model (Friston 2005).

    Garrido et al. 2009: fMRI evidence that PE signals in STG are
    modulated by precision context (predictable vs random, N=16).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1 = e

    # -- H3 features --
    consonance_100ms = h3_features[_CONSONANCE_H3_VAL]
    consonance_ent_1s = h3_features[_CONSONANCE_H16_ENT]
    tonalness_500ms = h3_features[_TONALNESS_H8_MEAN]
    spec_change_100ms = h3_features[_SPEC_CHANGE_H3_VAL]
    spec_change_std = h3_features[_SPEC_CHANGE_H3_STD]
    onset_100ms = h3_features[_ONSET_H3_VAL]
    tonal_stab_500ms = h3_features[_TONAL_STAB_H8_VAL]

    # -- M0: Weighted Error --
    # PE magnitude = spectral change + onset surprise, weighted down by
    # precision (E0 for tonal, E1 for rhythmic). When precision is high,
    # expected events are attenuated; unexpected events persist.
    # Garrido 2009: STG PE amplitude scales inversely with context precision.
    raw_error = 0.40 * spec_change_100ms + 0.30 * onset_100ms + 0.30 * consonance_100ms
    precision_gate = 0.55 * e0 + 0.45 * e1  # combined precision
    m0 = torch.sigmoid(raw_error * (1.0 - 0.5 * precision_gate))

    # -- M1: Uncertainty Index --
    # High entropy of consonance + high spectral variability + low tonal
    # stability = high uncertainty (atonal / unpredictable context).
    # Friston 2005: uncertainty = inverse precision of generative model.
    m1 = torch.sigmoid(
        0.35 * consonance_ent_1s
        + 0.25 * spec_change_std
        + 0.20 * (1.0 - tonal_stab_500ms)
        + 0.20 * (1.0 - tonalness_500ms)
    )

    return m0, m1
