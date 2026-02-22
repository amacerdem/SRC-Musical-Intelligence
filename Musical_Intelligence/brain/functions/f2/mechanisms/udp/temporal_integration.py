"""UDP M-Layer -- Temporal Integration (2D).

Error reward and pleasure index from H3 temporal features + E-layer:
  M0: error_reward    (reward signal from prediction errors under uncertainty)
  M1: pleasure_index  (integrated pleasure from uncertainty resolution)

H3 demands consumed:
  sensory_pleasantness:  (4,3,0,2), (4,16,1,0), (4,16,20,0)
  tonalness:             (14,8,1,0), (14,16,1,0)
  periodicity:           (5,8,1,0), (5,16,18,0)
  spectral_change:       (21,1,0,2), (21,3,0,2)
  H_coupling:            (41,8,0,0), (41,16,1,0), (41,16,20,0)

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/udp/
Cheung et al. 2019: uncertainty x surprise -> pleasure (saddle-shaped).
Pearce 2005: IDyOM entropy tracks tonal uncertainty over time.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PLEAS_H3_VAL = (4, 3, 0, 2)
_PLEAS_H16_MEAN = (4, 16, 1, 0)
_PLEAS_H16_ENTROPY = (4, 16, 20, 0)
_TONAL_H8_MEAN = (14, 8, 1, 0)
_TONAL_H16_MEAN = (14, 16, 1, 0)
_PERIOD_H8_MEAN = (5, 8, 1, 0)
_PERIOD_H16_TREND = (5, 16, 18, 0)
_SPEC_CHANGE_H1_VAL = (21, 1, 0, 2)
_SPEC_CHANGE_H3_VAL = (21, 3, 0, 2)
_H_COUPLING_H8_VAL = (41, 8, 0, 0)
_H_COUPLING_H16_MEAN = (41, 16, 1, 0)
_H_COUPLING_H16_ENTROPY = (41, 16, 20, 0)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: error reward and pleasure index.

    Integrates H3 temporal morphologies with E-layer uncertainty signals
    to track reward from prediction errors and sustained pleasure from
    uncertainty resolution.

    Cheung et al. 2019: amygdala/hippocampus encode uncertainty x surprise.
    Pearce 2005: entropy over multiple horizons tracks tonal uncertainty.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1 = e

    # -- H3 features --
    pleas_100ms = h3_features[_PLEAS_H3_VAL]
    pleas_mean_1s = h3_features[_PLEAS_H16_MEAN]
    pleas_entropy_1s = h3_features[_PLEAS_H16_ENTROPY]
    tonal_mean_500ms = h3_features[_TONAL_H8_MEAN]
    tonal_mean_1s = h3_features[_TONAL_H16_MEAN]
    period_mean_500ms = h3_features[_PERIOD_H8_MEAN]
    spec_change_50ms = h3_features[_SPEC_CHANGE_H1_VAL]
    spec_change_100ms = h3_features[_SPEC_CHANGE_H3_VAL]
    h_coupling_500ms = h3_features[_H_COUPLING_H8_VAL]
    h_coupling_mean_1s = h3_features[_H_COUPLING_H16_MEAN]
    h_coupling_entropy_1s = h3_features[_H_COUPLING_H16_ENTROPY]

    # -- M0: Error Reward --
    # Reward from prediction errors under uncertainty. When uncertainty
    # (E0) is high and spectral change indicates surprise, the error
    # itself becomes rewarding (model improvement signal).
    # Cheung 2019: amygdala codes uncertainty x surprise.
    m0 = torch.sigmoid(
        0.25 * e0
        + 0.20 * spec_change_50ms
        + 0.20 * spec_change_100ms
        + 0.20 * h_coupling_entropy_1s
        + 0.15 * (1.0 - tonal_mean_500ms)
    )

    # -- M1: Pleasure Index --
    # Integrated pleasure from uncertainty resolution. Combines hedonic
    # context (pleasantness temporal) with tonal certainty recovery and
    # harmonic coupling stability.
    # Gold 2019: inverted-U for IC on liking.
    m1 = torch.sigmoid(
        0.25 * pleas_100ms
        + 0.20 * pleas_mean_1s
        + 0.15 * pleas_entropy_1s
        + 0.15 * h_coupling_500ms
        + 0.15 * h_coupling_mean_1s
        + 0.10 * period_mean_500ms
    )

    return m0, m1
