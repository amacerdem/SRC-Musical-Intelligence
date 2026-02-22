"""MEAMN F-Layer -- Forecast (4D).

Four forward predictions for memory vividness, emotion, self-reference, and reserved:

  F0: mem_vividness_fc   -- Memory vividness prediction (2-5s ahead) [0, 1]
  F1: emo_response_fc    -- Emotional response prediction (1-3s ahead) [0, 1]
  F2: self_ref_fc        -- Self-referential prediction (5-10s ahead) [0, 1]
  F3: (reserved)         -- Future expansion, outputs zeros [0, 1]

H3 consumed:
    (7, 20, 4, 0)    amplitude max H20 L0      -- peak energy over 5s (vividness)
    (10, 24, 2, 0)   loudness std H24 L0       -- arousal variability 36s (self-ref)
    (22, 24, 19, 0)  entropy stability H24 L0  -- pattern stability 36s (familiarity)

F-layer primarily reuses E+M+P outputs rather than reading new H3 tuples directly.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/meamn/MEAMN-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_AMP_MAX_5S = (7, 20, 4, 0)
_LOUD_STD_36S = (10, 24, 2, 0)
_ENTROPY_STAB_36S = (22, 24, 19, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """F-layer: 4D forecast from E/M/P outputs + H3 context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2, F3)`` each ``(B, T)``.
    """
    e0, _e1, e2 = e_outputs
    m0, m1 = m_outputs
    p0, p1, _p2 = p_outputs

    amp_max_5s = h3_features[_AMP_MAX_5S]
    loud_std_36s = h3_features[_LOUD_STD_36S]
    entropy_stab_36s = h3_features[_ENTROPY_STAB_36S]

    # F0: Memory vividness prediction -- hippocampal trajectory over H20 (5s)
    # Janata 2009: imagery vividness strong vs weak autobiographical
    # (t(9)=5.784, p<0.0003)
    f0 = torch.sigmoid(
        0.35 * p0 + 0.30 * m0 + 0.20 * amp_max_5s
        + 0.15 * entropy_stab_36s
    )

    # F1: Emotional response prediction -- amygdala trajectory over H16 (1s)
    # Janata 2009: emotional evocation strong vs weak (t(9)=3.442, p<0.008)
    f1 = torch.sigmoid(
        0.40 * p1 + 0.30 * e2 + 0.30 * m1
    )

    # F2: Self-referential prediction -- mPFC trajectory over H24 (36s)
    # Janata 2009: mPFC self-referential processing
    f2 = torch.sigmoid(
        0.35 * e0 + 0.30 * p0 + 0.20 * loud_std_36s
        + 0.15 * entropy_stab_36s
    )

    # F3: Reserved -- future expansion (reminiscence bump, Janata 2007)
    f3 = torch.zeros_like(f0)

    return f0, f1, f2, f3
