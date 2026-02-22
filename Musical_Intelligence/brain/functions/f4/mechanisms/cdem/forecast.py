"""CDEM F-Layer -- Forecast (3D).

Forward predictions for context-dependent emotional memory:

  F0: encoding_strength_fc   -- Encoding strength prediction (2-5s) [0, 1]
  F1: retrieval_context_fc   -- Context retrieval prediction (5-10s) [0, 1]
  F2: mood_congruency_fc     -- Mood congruency prediction (1-3s) [0, 1]

H3 consumed:
    (22, 24, 19, 0)  entropy stability H24 L0               -- context stability 36s
    (0, 20, 18, 0)   roughness trend H20 L0                 -- valence trajectory
    (4, 20, 18, 0)   sensory_pleasantness trend H20 L0      -- pleasantness traj.
    (11, 20, 4, 0)   onset_strength max H20 L0              -- peak onset 5s

F-layer also reuses C-layer encoding_strength and M-layer congruency_index.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cdem/CDEM-forecast.md
Janata 2009: dMPFC parametrically tracks autobiographical salience (N=13).
Sachs 2025: same-valence context transitions 6.26s earlier (fMRI, N=39).
Sakakibara 2025: nostalgia enhances memory vividness (EEG, N=33, r=0.88).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from .extraction import ExtractionResult

# -- H3 tuples ----------------------------------------------------------------
_ENTROPY_STAB_36S = (22, 24, 19, 0)
_ROUGH_TREND_5S = (0, 20, 18, 0)
_PLEAS_TREND_5S = (4, 20, 18, 0)
_ONSET_MAX_5S = (11, 20, 4, 0)


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    c: ExtractionResult,
    m: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from C/M/P outputs + H3 context.

    F0 (encoding_strength_fc): predicts trajectory of context-dependent
    encoding over 2-5 seconds. Uses H20 consolidation window plus
    encoding_strength from C-layer and M-layer recall probability.
    Janata 2009: dMPFC tracks autobiographical salience (fMRI, N=13).

    F1 (retrieval_context_fc): predicts context-dependent retrieval
    probability over 5-10 seconds. Uses H24 entropy stability for
    long-range context state and onset peaks for boundary detection.
    Sachs 2025: same-valence context transitions 6.26s earlier (N=39).

    F2 (mood_congruency_fc): predicts music-mood alignment over 1-3
    seconds. Uses H16-scale roughness trend as short-horizon valence
    predictor and M-layer congruency index for current alignment.
    Sakakibara 2025: nostalgia enhances memory vividness (r=0.88).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        c: :class:`ExtractionResult` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    m0, m1 = m
    p0, _p1, p2 = p

    # -- H3 features --
    entropy_stab_36s = h3_features[_ENTROPY_STAB_36S]    # (B, T)
    rough_trend_5s = h3_features[_ROUGH_TREND_5S]        # (B, T)
    pleas_trend_5s = h3_features[_PLEAS_TREND_5S]        # (B, T)
    onset_max_5s = h3_features[_ONSET_MAX_5S]            # (B, T)

    # -- Derived signals from C-layer --
    encoding = c.encoding_strength

    # -- F0: Encoding Strength Forecast (2-5s horizon, H20) --
    # Hippocampal consolidation trajectory: encoding strength + M1 recall
    # probability + pleasantness trajectory (reward trend).
    # Janata 2009: dMPFC parametrically tracks autobiographical salience.
    f0 = torch.sigmoid(
        0.35 * encoding
        + 0.30 * m1
        + 0.20 * pleas_trend_5s
        + 0.15 * entropy_stab_36s
    )

    # -- F1: Retrieval Context Forecast (5-10s horizon, H24) --
    # mPFC context reinstatement trajectory: entropy stability (long-range
    # context state) + P2 synthesis (current encoding-congruency quality)
    # + onset peaks (context boundary detection).
    # Sachs 2025: same-valence context shifts transitions 6.26s earlier.
    f1 = torch.sigmoid(
        0.35 * entropy_stab_36s
        + 0.30 * p2
        + 0.20 * onset_max_5s
        + 0.15 * p0
    )

    # -- F2: Mood Congruency Forecast (1-3s horizon, H16) --
    # Short-horizon congruency prediction: M0 congruency index (current
    # alignment) + roughness trend (valence trajectory) + encoding
    # (context-dependent encoding strength).
    # Sakakibara 2025: nostalgia enhances memory vividness (r=0.88).
    f2 = torch.sigmoid(
        0.40 * m0
        + 0.30 * (1.0 - torch.sigmoid(rough_trend_5s))
        + 0.30 * encoding
    )

    return f0, f1, f2
