"""IGFE M-Layer -- Temporal Integration (2D).

Executive enhancement and dose-response accumulation over time:
  M0: executive_enhancement  (sustained gamma entrainment for executive control)
  M1: dose_response          (cumulative stimulation effect)

H3 demands consumed:
  periodicity:     (5,0,0,2), (5,1,0,2), (5,3,1,2), (5,16,1,0)
  tonalness:       (14,3,0,2), (14,16,1,0)
  amplitude:       (7,3,0,2), (7,16,1,2)
  onset_strength:  (11,0,0,2), (11,1,14,2), (11,3,1,2)

Temporal integration builds multi-scale gamma entrainment from H3 features:
gamma-scale (25-50ms) captures instantaneous entrainment, alpha-beta
(100ms) captures sustained gamma synchronization, and beat-scale (1s)
captures stable dosage accumulation.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/igfe/
Herrmann 2016: sustained gamma entrainment requires 100ms+ exposure.
Bolland 2025: dose-response relationship in gamma stimulation studies.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PERIOD_H0_VAL = (5, 0, 0, 2)       # periodicity 25ms value integration
_PERIOD_H1_VAL = (5, 1, 0, 2)       # periodicity 50ms value integration
_PERIOD_H3_MEAN = (5, 3, 1, 2)      # periodicity 100ms mean integration
_PERIOD_H16_MEAN = (5, 16, 1, 0)    # periodicity 1s mean memory

_TONAL_H3_VAL = (14, 3, 0, 2)       # tonalness 100ms value integration
_TONAL_H16_MEAN = (14, 16, 1, 0)    # tonalness 1s mean memory

_AMPL_H3_VAL = (7, 3, 0, 2)         # amplitude 100ms value integration
_AMPL_H16_MEAN = (7, 16, 1, 2)      # amplitude 1s mean integration

_ONSET_H0_VAL = (11, 0, 0, 2)       # onset_strength 25ms value integration
_ONSET_H1_PERIOD = (11, 1, 14, 2)   # onset_strength 50ms periodicity integration
_ONSET_H3_MEAN = (11, 3, 1, 2)      # onset_strength 100ms mean integration


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: executive enhancement and dose-response.

    Executive enhancement integrates gamma-scale entrainment signals with
    E-layer match to assess sustained cognitive benefit. Dose-response
    tracks cumulative intensity and modulation at longer timescales.

    Polanía et al. 2012: tACS at individual gamma frequency enhances
    working memory capacity via fronto-parietal coupling (p<0.05).
    Bolland 2025: meta-analysis shows dose-response saturation pattern.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1 = e

    # Gamma-scale features
    period_25ms = h3_features[_PERIOD_H0_VAL]
    period_50ms = h3_features[_PERIOD_H1_VAL]
    period_100ms = h3_features[_PERIOD_H3_MEAN]
    period_1s = h3_features[_PERIOD_H16_MEAN]

    tonal_100ms = h3_features[_TONAL_H3_VAL]
    tonal_1s = h3_features[_TONAL_H16_MEAN]

    ampl_100ms = h3_features[_AMPL_H3_VAL]
    ampl_1s = h3_features[_AMPL_H16_MEAN]

    onset_25ms = h3_features[_ONSET_H0_VAL]
    onset_50ms_period = h3_features[_ONSET_H1_PERIOD]
    onset_100ms = h3_features[_ONSET_H3_MEAN]

    # -- M0: Executive Enhancement --
    # Sustained gamma entrainment that supports executive control.
    # Fast gamma-scale periodicity (25-50ms) combined with sustained
    # harmonic match indicates ongoing frequency-specific entrainment.
    # Polanía 2012: fronto-parietal gamma coupling enhances WM.
    gamma_entrain = 0.30 * period_25ms + 0.30 * period_50ms + 0.40 * period_100ms
    m0 = torch.sigmoid(
        0.40 * gamma_entrain
        + 0.30 * e0
        + 0.15 * tonal_100ms
        + 0.15 * onset_50ms_period
    )

    # -- M1: Dose Response --
    # Cumulative stimulation effect: longer-timescale features capture
    # sustained exposure. Intensity (amplitude) and regularity (periodicity)
    # at 1s scale reflect dosage accumulation.
    # Bolland 2025: dose-response in gamma stimulation meta-analysis.
    sustained_dose = 0.35 * period_1s + 0.35 * ampl_1s + 0.30 * tonal_1s
    m1 = torch.sigmoid(
        0.40 * sustained_dose
        + 0.30 * e1
        + 0.15 * ampl_100ms
        + 0.15 * onset_100ms
    )

    return m0, m1
