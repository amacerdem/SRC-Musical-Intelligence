"""SNEM F-Layer — Forecast (3D).

Three forward predictions for beat onset, meter position, and enhancement:

  F0: beat_onset_pred       — Next beat onset prediction [0, 1]
  F1: meter_position_pred   — Metric position prediction (0=weak, 1=downbeat) [0, 1]
  F2: enhancement_pred      — SS-EP enhancement ~0.75s ahead [0, 1]

H3 consumed:
    (10, 16, 14, 2)  flux periodicity H16 L2       — beat periodicity 1s (reused)
    (25, 16, 14, 2)  coupling periodicity H16 L2   — metric structure 1s (reused)

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/snem/SNEM-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_FLUX_PERIOD_1S = (10, 16, 14, 2)
_COUPLING_PERIOD_1S = (25, 16, 14, 2)


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

    flux_period_1s = h3_features[_FLUX_PERIOD_1S]
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]

    # F0: Beat onset prediction — next beat ~0.5s
    # Vuust 2022: predictive coding generates beat expectations
    f0 = torch.sigmoid(
        0.50 * e0 + 0.50 * flux_period_1s
    )

    # F1: Meter position prediction — 0=weak beat, 1=downbeat
    # Grahn 2007: metric structure from coupling drives position predictions
    f1 = torch.sigmoid(
        0.50 * e1 + 0.50 * coupling_period_1s
    )

    # F2: Enhancement prediction — SS-EP ~0.75s ahead
    # Nozaradan 2018: enhancement prediction from SS-EP + selective gain
    f2 = torch.sigmoid(
        0.50 * e2 + 0.50 * flux_period_1s
    )

    return f0, f1, f2
