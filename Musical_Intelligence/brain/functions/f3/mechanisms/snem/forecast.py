"""SNEM F-Layer — Forecast (3D).

Three forward predictions for beat onset, meter position, and enhancement:

  F0: beat_onset_pred       — Next beat onset prediction [0, 1]
  F1: meter_position_pred   — Metric position prediction (0=weak, 1=downbeat) [0, 1]
  F2: enhancement_pred      — SS-EP enhancement ~0.75s ahead [0, 1]

H3 consumed (reuses E-layer demands):
    (8, 20, 14, 0)   loudness periodicity H20 L0 — beat periodicity at 5s
    (10, 20, 20, 0)  flux entropy H20 L0         — meter entropy at 5s

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/snem/SNEM-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (reused from extraction) ---------------------------------------
_LOUD_PERIOD_H20 = (8, 20, 14, 0)       # beat periodicity at 5s
_FLUX_ENTROPY_H20 = (10, 20, 20, 0)     # meter entropy at 5s


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/P outputs + H3 context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    e0, e1, e2 = e_outputs
    (_p0, _p1, _p2) = p_outputs

    loud_period_h20 = h3_features[_LOUD_PERIOD_H20]
    flux_entropy_h20 = h3_features[_FLUX_ENTROPY_H20]

    # F0: Beat onset prediction — next beat ~0.5s
    # Vuust 2022: predictive coding generates beat expectations.
    # Loudness periodicity at 5s provides sustained rhythmic context.
    f0 = torch.sigmoid(
        0.50 * e0 + 0.50 * loud_period_h20
    )

    # F1: Meter position prediction — 0=weak beat, 1=downbeat
    # Grahn 2007: metric structure drives position predictions.
    # Flux entropy at 5s reflects accent-pattern diversity.
    f1 = torch.sigmoid(
        0.50 * e1 + 0.50 * flux_entropy_h20
    )

    # F2: Enhancement prediction — SS-EP ~0.75s ahead
    # Nozaradan 2018: enhancement prediction from SS-EP + selective gain.
    f2 = torch.sigmoid(
        0.50 * e2 + 0.50 * loud_period_h20
    )

    return f0, f1, f2
