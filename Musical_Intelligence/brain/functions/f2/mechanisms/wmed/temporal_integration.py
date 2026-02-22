"""WMED M-Layer -- Temporal Integration (2D).

Temporal dynamics of tapping accuracy and dissociation:
  M0: tapping_accuracy    (integrated motor-timing precision)
  M1: dissociation_index  (degree of WM-entrainment paradox)

M0 combines amplitude mean over 1s with onset value at 100ms and
entrainment strength (E0) to estimate motor timing accuracy.

M1 captures the paradoxical dissociation: when E0 (entrainment) is high
but E1 (WM) is low, tapping degrades -- the Noboa 2025 paradox where
stronger SS-EP entrainment to simple rhythms predicts worse performance
(beta=-0.418).

H3 demands consumed:
  amplitude:        (7,16,1,2)   -- mean over 1s integration
  onset_strength:   (10,3,0,2)   -- value at 100ms integration
  onset_strength:   (11,3,0,2)   -- value at 100ms integration
  spectral_change:  (21,3,0,2)   -- value at 100ms integration
  spectral_change:  (21,16,2,0)  -- std over 1s memory
  H_coupling:       (41,8,0,0)   -- value at 500ms memory

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/wmed/
Noboa 2025: beta=-0.418, R2adj=0.27.
Grahn 2007: BG-SMA timing loop, fMRI N=14.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_AMP_H16_MEAN = (7, 16, 1, 2)         # amplitude mean over 1s integration
_ONSET10_H3_VAL = (10, 3, 0, 2)       # onset_strength value at 100ms integration
_ONSET11_H3_VAL = (11, 3, 0, 2)       # onset_strength value at 100ms integration
_SPEC_CHANGE_H3_VAL = (21, 3, 0, 2)   # spectral_change value at 100ms integration
_SPEC_CHANGE_H16_STD = (21, 16, 2, 0) # spectral_change std over 1s memory
_H_COUPLING_H8_VAL = (41, 8, 0, 0)    # H_coupling value at 500ms memory


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: tapping accuracy and dissociation index.

    M0 integrates multi-scale onset and amplitude features with
    entrainment strength (E0) to estimate motor timing precision.

    M1 captures the paradox strength: E0 high + E1 low = strong
    dissociation. Modulated by spectral change variability (timing
    irregularity at 1s scale) and tonal coupling stability.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1 = e

    amp_mean_1s = h3_features[_AMP_H16_MEAN]             # (B, T)
    onset10_val_100ms = h3_features[_ONSET10_H3_VAL]      # (B, T)
    onset11_val_100ms = h3_features[_ONSET11_H3_VAL]      # (B, T)
    spec_change_100ms = h3_features[_SPEC_CHANGE_H3_VAL]  # (B, T)
    spec_change_std_1s = h3_features[_SPEC_CHANGE_H16_STD]  # (B, T)
    h_coupling_500ms = h3_features[_H_COUPLING_H8_VAL]    # (B, T)

    # -- M0: Tapping Accuracy --
    # Motor timing precision: entrainment + amplitude stability + onset strength.
    # Grahn 2007: BG-SMA loop underpins beat-based timing.
    m0 = torch.sigmoid(
        0.30 * e0
        + 0.25 * amp_mean_1s
        + 0.20 * onset10_val_100ms
        + 0.15 * onset11_val_100ms
        + 0.10 * h_coupling_500ms
    )

    # -- M1: Dissociation Index --
    # Paradox strength: high entrainment (E0) + low WM (1-E1) + timing variability.
    # Noboa 2025: stronger SS-EP entrainment predicts worse tapping (beta=-0.418).
    # Higher spectral change std = more timing irregularity = stronger paradox.
    dissociation_raw = e0 * (1.0 - e1)  # paradox: entrained but no WM support
    m1 = torch.sigmoid(
        0.40 * dissociation_raw
        + 0.25 * spec_change_std_1s
        + 0.20 * spec_change_100ms
        + 0.15 * (1.0 - h_coupling_500ms)
    )

    return m0, m1
