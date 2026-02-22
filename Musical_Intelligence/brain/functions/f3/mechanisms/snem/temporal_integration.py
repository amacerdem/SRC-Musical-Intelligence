"""SNEM M-Layer — Temporal Integration (3D).

Three composite signals integrating E-layer with temporal context:

  M0: ssep_enhancement      — Beat-salience proxy from SS-EP [0, 1]
  M1: enhancement_index     — Onset novelty relative to smoothed baseline [0, 1]
  M2: beat_salience          — Periodicity + amplitude variability [0, 1]

H3 consumed:
    (10, 0, 0, 2)   flux value H0 L2           — instant flux
    (10, 1, 1, 2)   flux mean H1 L2            — smoothed onset 50ms
    (10, 3, 0, 2)   flux value H3 L2           — beat-scale onset 100ms
    (10, 4, 14, 2)  flux periodicity H4 L2     — beat rhythm 125ms
    (7, 3, 0, 2)    amplitude value H3 L2      — beat amplitude 100ms
    (7, 3, 2, 2)    amplitude std H3 L2        — beat variability 100ms

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/snem/SNEM-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_FLUX_VAL_INST = (10, 0, 0, 2)
_FLUX_MEAN_50MS = (10, 1, 1, 2)
_FLUX_VAL_100MS = (10, 3, 0, 2)
_FLUX_PERIOD_125MS = (10, 4, 14, 2)
_AMP_VAL_100MS = (7, 3, 0, 2)
_AMP_STD_100MS = (7, 3, 2, 2)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from E-layer + H3.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``.
    """
    _e0, e1, _e2 = e_outputs

    flux_mean_50ms = h3_features[_FLUX_MEAN_50MS]
    flux_val_100ms = h3_features[_FLUX_VAL_100MS]
    flux_period_125ms = h3_features[_FLUX_PERIOD_125MS]
    amp_val_100ms = h3_features[_AMP_VAL_100MS]
    amp_std_100ms = h3_features[_AMP_STD_100MS]

    # Beat-salience proxy: periodicity modulated by amplitude
    beat_salience_proxy = flux_period_125ms * amp_val_100ms

    # M0: SS-EP enhancement — beat-salience modulated by meter
    # Nozaradan 2011: SS-EP peaks at beat frequency in auditory cortex
    m0 = torch.sigmoid(
        1.0 * beat_salience_proxy + 0.8 * e1 - 0.5 * flux_mean_50ms
    )

    # M1: Enhancement index — novelty relative to smoothed baseline
    # Nozaradan 2018: enhanced response at beat vs off-beat positions
    m1 = torch.sigmoid(
        0.50 * m0 + 0.50 * (flux_val_100ms - flux_mean_50ms)
    )

    # M2: Beat salience — periodicity and variability
    # Large 2008: oscillation entrainment tracks beat salience
    m2 = torch.sigmoid(
        0.50 * flux_period_125ms + 0.50 * amp_std_100ms
    )

    return m0, m1, m2
