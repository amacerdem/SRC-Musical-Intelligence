"""CSSL F-Layer -- Forecast (3D).

Forward predictions for song learning trajectory and binding strength:
  F0: learning_trajectory      (learning trajectory prediction, 2-5s ahead)
  F1: binding_prediction       (binding strength prediction, 5-36s ahead)
  F2: reserved                 (reserved for future expansion, outputs zeros)

F0 predicts the direction of song learning using familiarity trend from
the H20 window. During the sensitive period, this trajectory is steep;
post-sensitive period, it flattens.

F1 predicts all-shared binding strength using retrieval dynamics from
the H24 horizon. High binding prediction means the hippocampus is
actively consolidating rhythm + melody into a unified song representation.

F2 is held for future expansion (sensitive-period gating or cross-species
divergence index).

H3 demands consumed:
    (22, 24, 19, 0) entropy stability H24 L0  -- pattern stability over 36s
    (12, 20, 1, 0)  warmth mean H20 L0        -- sustained voice warmth

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cssl/CSSL-forecast.md
Burchardt et al. 2025: all-shared binding r=0.94 (N=54, zebra finch).
Sensitive period study 2018: critical window d=0.61 (N=48).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ENTROPY_STAB_H24_L0 = (22, 24, 19, 0)  # entropy stability H24 L0
_WARMTH_MEAN_H20_L0 = (12, 20, 1, 0)    # warmth mean H20 L0


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: learning trajectory, binding prediction, reserved.

    F0 predicts the direction of song learning over the next 2-5s. Uses
    template fidelity (M1) as the core learning signal, modulated by
    sustained voice warmth from H20. High trajectory means the listener
    is converging toward the template.

    F1 predicts all-shared binding strength over a 5-36s window. Uses
    all-shared binding (E2) plus entropy stability from H24. High binding
    prediction means hippocampus is actively consolidating the song.

    F2 is reserved for future expansion (currently zeros).

    Burchardt et al. 2025: all-shared binding r=0.94 (N=54, zebra finch).
    Sensitive period study 2018: critical window for song template
    acquisition; d=0.61 (N=48).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    _e0, _e1, e2 = e
    _m0, m1 = m
    p0, _p1 = p

    # -- H3 reads --
    entropy_stab = h3_features[_ENTROPY_STAB_H24_L0]  # (B, T)
    warmth_h20 = h3_features[_WARMTH_MEAN_H20_L0]     # (B, T)

    # -- F0: Learning Trajectory --
    # Predicts direction of song learning (2-5s ahead). Template fidelity
    # (M1) reflects current learning state; warmth provides sustained
    # voice quality context; entrainment state (P0) provides motor coupling.
    # Sensitive period study 2018: critical window d=0.61 (N=48).
    f0 = torch.sigmoid(
        0.40 * m1
        + 0.30 * warmth_h20
        + 0.30 * p0
    )

    # -- F1: Binding Prediction --
    # Predicts all-shared binding strength (5-36s ahead). All-shared
    # binding (E2) provides current binding state; entropy stability
    # from H24 provides the long-term consolidation context.
    # Burchardt et al. 2025: all-shared binding r=0.94 (N=54).
    f1 = torch.sigmoid(
        0.50 * e2
        + 0.50 * entropy_stab
    )

    # -- F2: Reserved --
    # Currently outputs zeros. Future expansion: sensitive-period gating
    # signal or cross-species divergence index.
    f2 = torch.zeros_like(e2)

    return f0, f1, f2
