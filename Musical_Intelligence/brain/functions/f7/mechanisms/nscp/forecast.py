"""NSCP F-Layer -- Forecast (3D).

Forward-looking predictions for the neural synchrony commercial pathway:
  F0: synchrony_pred  -- Neural synchrony trajectory prediction [0, 1]
  F1: popularity_pred -- Commercial success trajectory prediction [0, 1]
  F2: catchiness_pred -- Catchiness trajectory prediction [0, 1]

Synchrony prediction (F0) forecasts upcoming ISC levels by combining
current neural synchrony (f22) with coherence periodicity trend.
Leeuwis 2021: ISC stability (early R^2=0.404 vs late R^2=0.393)
supports temporal prediction of synchrony.

Popularity prediction (F1) forecasts commercial success trajectory
by combining current commercial prediction (f23) with binding
periodicity. Leeuwis 2021: combined model R^2=0.619.

Catchiness prediction (F2) forecasts motor entrainment trajectory
by combining current catchiness (f24) with onset periodicity.
Spiech 2022: groove has stable temporal dynamics.

H3 demands consumed (5):
  (25, 16, 14, 2) coherence periodicity 1s L2    -- synchrony prediction
  (33, 16, 14, 2) binding periodicity 1s L2       -- popularity prediction
  (10, 16, 14, 2) onset periodicity 1s L2         -- catchiness prediction
  (25, 4, 14, 2)  coherence periodicity 125ms L2  -- short-term trend
  (10, 4, 2, 2)   onset variability 125ms L2      -- catchiness stability

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/nscp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_COHERENCE_PERIOD_1S = (25, 16, 14, 2)    # x_l0l5 periodicity H16 L2
_BINDING_PERIOD_1S = (33, 16, 14, 2)      # x_l4l5 periodicity H16 L2
_ONSET_PERIOD_1S = (10, 16, 14, 2)        # spectral_flux periodicity H16 L2
_COHERENCE_PERIOD_125MS = (25, 4, 14, 2)  # x_l0l5 periodicity H4 L2
_ONSET_STD_125MS = (10, 4, 2, 2)          # spectral_flux std H4 L2


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: 3D forward predictions for ISC-commercial pathway.

    F0 (synchrony_pred): Forecasts ISC trajectory. Combines current ISC
    estimate (f22) with 1s coherence periodicity. Regular coherence
    periodicity with high current synchrony predicts sustained ISC.
    Leeuwis 2021: ISC temporally stable.

    F1 (popularity_pred): Forecasts commercial success trajectory.
    Combines current commercial prediction (f23) with binding
    periodicity at 1s. Stable binding = sustained multi-feature
    coherence = continued listener engagement.
    Leeuwis 2021: combined model R^2=0.619.

    F2 (catchiness_pred): Forecasts groove/motor entrainment trajectory.
    Combines current catchiness (f24) with onset periodicity at 1s.
    Beat-regular passages with sustained catchiness predict extended
    motor engagement driving repeated listening.
    Spiech 2022: groove stable temporal dynamics.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` from extraction layer.
        m_outputs: ``(M0, M1, M2)`` from temporal integration layer.
        p_outputs: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    e0, e1, e2 = e_outputs

    # -- H3 features --
    coherence_period = h3_features[_COHERENCE_PERIOD_1S]       # (B, T)
    binding_period = h3_features[_BINDING_PERIOD_1S]            # (B, T)
    onset_period = h3_features[_ONSET_PERIOD_1S]                # (B, T)
    _coherence_125ms = h3_features[_COHERENCE_PERIOD_125MS]    # (B, T)
    _onset_std_125ms = h3_features[_ONSET_STD_125MS]           # (B, T)

    # -- F0: Synchrony Prediction --
    # sigma(0.5 * f22 + 0.5 * coherence_period_1s)
    # Leeuwis 2021: ISC temporally stable (early vs late R^2 drop 0.011)
    f0 = torch.sigmoid(
        0.50 * e0
        + 0.50 * coherence_period
    )

    # -- F1: Popularity Prediction --
    # sigma(0.5 * f23 + 0.5 * binding_period_1s)
    # Leeuwis 2021: combined model R^2=0.619
    f1 = torch.sigmoid(
        0.50 * e1
        + 0.50 * binding_period
    )

    # -- F2: Catchiness Prediction --
    # sigma(0.5 * f24 + 0.5 * onset_period_1s)
    # Spiech 2022: groove perception stable temporal dynamics
    f2 = torch.sigmoid(
        0.50 * e2
        + 0.50 * onset_period
    )

    return (f0, f1, f2)
