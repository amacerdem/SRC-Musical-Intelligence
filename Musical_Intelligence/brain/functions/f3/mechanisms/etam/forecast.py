"""ETAM F-Layer -- Forecast (3D).

Forward predictions for tracking, attention sustain, and segregation:
  F0: tracking_prediction   (predicted next-beat tracking accuracy)
  F1: attention_sustain     (predicted attentional maintenance over time)
  F2: segregation_predict   (predicted stream segregation quality)

H3 demands consumed:
  x_l4l5:           (33,16,18,0)  -- cross-stream trend 1s (trajectory)
  loudness:         (8,14,1,0)    -- mean ~900ms (sustained level)
  loudness:         (8,20,18,0)   -- trend 5s (long dynamics)
  x_l5l7:           (41,14,13,0)  -- cognitive coupling entropy ~900ms

Dependencies on E-layer and M-layer:
  E0: early_window            -- transient tracking for beat prediction
  E2: late_window             -- cognitive grouping for segregation
  E3: instrument_asymmetry    -- timbral cues for segregation prediction
  M0: attention_gain          -- current attention for sustain projection
  M1: entrainment_index       -- entrainment strength for tracking prediction

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/etam/
Tierney & Kraus 2015: EEG entrainment predicts sustained attention.
London 2012: temporal attention sustains across metric hierarchy.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_CROSS_STREAM_TREND_1S = (33, 16, 18, 0)    # cross-stream trend 1s (memory)
_LOUD_MEAN_900MS = (8, 14, 1, 0)            # loudness mean ~900ms (memory)
_LOUD_TREND_5S = (8, 20, 18, 0)             # loudness trend 5s (memory)
_COG_COUPLING_ENT_900MS = (41, 14, 13, 0)   # cognitive coupling entropy ~900ms


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: forward predictions for tracking, attention, segregation.

    Each dimension predicts a different aspect of upcoming entrainment-
    attention dynamics: next-beat tracking accuracy, sustained attentional
    maintenance, and stream segregation quality.

    Tierney & Kraus 2015: EEG phase-locking predicts sustained attention
    to tempo envelope (N=24, p<0.01).
    London 2012: temporal attention is maintained across metric hierarchy
    based on entrainment strength and metric regularity.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``
    """
    e0, _e1, e2, e3 = e
    m0, m1 = m

    cross_stream_trend_1s = h3_features[_CROSS_STREAM_TREND_1S]
    loud_mean_900ms = h3_features[_LOUD_MEAN_900MS]
    loud_trend_5s = h3_features[_LOUD_TREND_5S]
    cog_coupling_ent_900ms = h3_features[_COG_COUPLING_ENT_900MS]

    # -- F0: Tracking Prediction --
    # Predicted next-beat tracking accuracy. Early window (E0) provides
    # current transient detection quality, cross-stream trend extrapolates
    # multi-stream coherence trajectory, and entrainment index (M1) gives
    # oscillatory prediction strength.
    # Grahn 2012: putamen activity predicts upcoming beat tracking.
    f0 = torch.sigmoid(
        0.50 * e0
        + 0.30 * cross_stream_trend_1s
        + 0.20 * m1
    )

    # -- F1: Attention Sustain --
    # Predicted attentional maintenance over time. Attention gain (M0)
    # projects forward, loudness mean provides sustained energy context,
    # and loudness trend captures long-range dynamic trajectory -- rising
    # energy sustains attention, falling energy predicts disengagement.
    # Tierney 2015: sustained EEG entrainment predicts attention.
    f1 = torch.sigmoid(
        0.40 * m0
        + 0.30 * loud_mean_900ms
        + 0.30 * loud_trend_5s
    )

    # -- F2: Segregation Predict --
    # Predicted stream segregation quality. Instrument asymmetry (E3)
    # projects timbral distinctiveness forward, late window (E2) provides
    # cognitive grouping context, and coupling entropy captures metric
    # complexity -- higher entropy may impair segregation.
    # London 2012: metric hierarchy supports perceptual grouping predictions.
    f2 = torch.sigmoid(
        0.40 * e3
        + 0.30 * e2
        + 0.30 * cog_coupling_ent_900ms
    )

    return f0, f1, f2
