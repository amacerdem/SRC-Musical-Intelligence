"""TSCP F-Layer -- Forecast (3D).

Timbre-Specific Cortical Plasticity forward predictions:
  timbre_continuation       (idx 7)  -- Note-by-note timbre prediction [0, 1]
  cortical_enhancement_pred (idx 8)  -- Long-term plasticity prediction [0, 1]
  generalization_pred       (idx 9)  -- Transfer to related timbres [0, 1]

timbre_continuation uses warmth and tonalness means at 46ms (alpha-beta
timescale) to predict upcoming timbre characteristics. Implements the
imagery-perception overlap from Halpern et al. 2004: posterior PT overlaps
with perception (R STG imagery t=4.66, perception t=6.89). Zatorre &
Halpern 2005: auditory cortex supports veridical timbre imagery.

cortical_enhancement_pred combines plasticity magnitude (f03) with timbre
change trends at 300ms to predict the trajectory of cortical enhancement.
Leipold et al. 2021: robust musicianship effects on functional/structural
networks replicable across AP/non-AP (n=153).

generalization_pred combines recognition quality, consonance-timbre coupling
(x_l5l7 at 300ms), and timbre identity to predict how much trained enhancement
generalizes to acoustically similar timbres. Pantev 2001: trained > similar
> dissimilar > pure tone hierarchy implies graded generalization.

H3 demands consumed (4 tuples):
  (12, 5, 1, 0)   warmth mean H5 L0         -- mean warmth over 46ms
  (14, 5, 1, 0)   tonalness mean H5 L0      -- mean tonalness over 46ms
  (24, 8, 1, 0)   timbre_change mean H8 L0  -- mean timbre flux 300ms
  (41, 8, 0, 2)   x_l5l7[0] value H8 L2     -- consonance x timbre coupling 300ms

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/tscp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (4 tuples) ----------------------------------------------
_WARMTH_MEAN_H5 = (12, 5, 1, 0)          # warmth mean H5 L0
_TONALNESS_MEAN_H5 = (14, 5, 1, 0)       # tonalness mean H5 L0
_TIMBRE_MEAN_H8 = (24, 8, 1, 0)          # timbre_change mean H8 L0
_X_L5L7_VALUE_H8 = (41, 8, 0, 2)         # x_l5l7[0] value H8 L2


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
    ednr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: predictions about upcoming timbre processing.

    timbre_continuation (idx 7): sigma(0.50 * warmth_mean_46ms + 0.50 *
    tonalness_mean_46ms). Note-by-note timbre prediction at alpha-beta
    timescale. Halpern et al. 2004: imagery activates posterior PT
    overlapping with perception. Maps to right posterior STG / left PT.

    cortical_enhancement_pred (idx 8): sigma(0.60 * f03 + 0.40 *
    timbre_change_mean_300ms). Predicts enhancement trajectory from current
    plasticity magnitude and timbre change trends. Leipold et al. 2021:
    robust musicianship effects (n=153). Maps to expansion-renormalization
    pathway.

    generalization_pred (idx 9): sigma(0.50 * recognition_quality + 0.30 *
    x_l5l7_300ms + 0.20 * timbre_identity). Predicts graded generalization
    of trained enhancement to acoustically similar timbres. Pantev 2001:
    trained > similar > dissimilar > pure tone hierarchy. Maps to auditory
    association cortex BA22.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e_outputs: ``(f01, f02, f03)`` from extraction layer.
        m_outputs: ``(enhancement_function,)`` from temporal integration layer.
        p_outputs: ``(recognition_quality, enhanced_response, timbre_identity)``
            from cognitive present layer.
        ednr: ``(B, T, 10)`` from upstream EDNR relay.

    Returns:
        ``(timbre_continuation, cortical_enhancement_pred, generalization_pred)``
        each ``(B, T)``
    """
    _f01, _f02, f03 = e_outputs
    recognition_quality, _enhanced_response, timbre_identity = p_outputs

    # -- H3 features --
    warmth_mean = h3_features[_WARMTH_MEAN_H5]         # (B, T)
    tonalness_mean = h3_features[_TONALNESS_MEAN_H5]   # (B, T)
    timbre_mean = h3_features[_TIMBRE_MEAN_H8]         # (B, T)
    x_l5l7_300ms = h3_features[_X_L5L7_VALUE_H8]      # (B, T)

    # -- timbre_continuation (idx 7) --
    # sigma(0.50 * warmth_mean_46ms + 0.50 * tonalness_mean_46ms)
    # Halpern 2004: R STG imagery t=4.66, perception t=6.89
    # Zatorre & Halpern 2005: veridical timbre imagery
    timbre_continuation = torch.sigmoid(
        0.50 * warmth_mean.clamp(0.0, 1.0)
        + 0.50 * tonalness_mean.clamp(0.0, 1.0)
    )

    # -- cortical_enhancement_pred (idx 8) --
    # sigma(0.60 * f03 + 0.40 * timbre_change_mean_300ms)
    # Leipold et al. 2021: robust musicianship effects (n=153)
    cortical_enhancement_pred = torch.sigmoid(
        0.60 * f03
        + 0.40 * timbre_mean.clamp(0.0, 1.0)
    )

    # -- generalization_pred (idx 9) --
    # sigma(0.50 * recognition_quality + 0.30 * x_l5l7_300ms + 0.20 * timbre_identity)
    # Pantev 2001: trained > similar > dissimilar > pure tone hierarchy
    generalization_pred = torch.sigmoid(
        0.50 * recognition_quality
        + 0.30 * x_l5l7_300ms.clamp(0.0, 1.0)
        + 0.20 * timbre_identity
    )

    return timbre_continuation, cortical_enhancement_pred, generalization_pred
