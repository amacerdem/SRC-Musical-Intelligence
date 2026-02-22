"""SLEE F-Layer -- Forecast (3D).

Statistical Learning Expertise Enhancement forward predictions:
  next_probability         -- Predicted next event probability [0, 1]
  regularity_continuation  -- Model updating prediction [0, 1]
  detection_predict        -- Behavioral output prediction [0, 1]

next_probability predicts the probability of the next auditory event based
on the learned statistical model (f01) and detection accuracy (f02).
sigma(0.50 * f01 + 0.50 * f02). Reflects the predictive coding output:
given the statistical model and detection sensitivity, what is the expected
probability of the next event conforming to learned regularities. Carbajal
& Malmierca 2018: top-down prediction component of predictive coding.

regularity_continuation predicts whether the current statistical regularity
will persist, combining f01 with accumulated exposure.
sigma(0.50 * f01 + 0.50 * exposure_model). Bridwell 2017: pattern-specific
cortical entrainment predicts continuation of statistical structure.

detection_predict predicts detection performance for upcoming irregularities
based on current pattern segmentation, expertise state, and cross-modal
binding strength. Paraskevopoulos 2022: musicians predict irregularities
with higher accuracy, suggesting the system generates forward predictions
about detection likelihood.

H3 demands consumed (4 tuples):
  (7, 3, 0, 2)    amplitude value H3 L2         -- amplitude at 100ms
  (8, 8, 5, 0)    loudness range H8 L0          -- loudness range 500ms
  (33, 3, 0, 2)   x_l4l5 value H3 L2            -- pattern coupling 100ms
  (41, 3, 2, 2)   x_l5l6 std H3 L2              -- binding variability 100ms

Dependencies:
  E-layer f01 (statistical_model)
  E-layer f02 (detection_accuracy)
  M-layer exposure_model
  M-layer expertise_state
  P-layer pattern_segmentation
  P-layer cross_modal_binding

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/slee/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_AMP_VAL_H3 = (7, 3, 0, 2)               # amplitude at 100ms
_LOUDNESS_RANGE_H8 = (8, 8, 5, 0)        # loudness range 500ms
_COUPLING_VAL_H3 = (33, 3, 0, 2)         # pattern coupling 100ms
_BINDING_STD_H3 = (41, 3, 2, 2)          # binding variability 100ms


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
    ednr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: three forward predictions for statistical learning.

    next_probability combines the statistical model (f01) and detection
    accuracy (f02) to predict the probability of the next event matching
    learned regularities. Carbajal & Malmierca 2018: top-down prediction
    in predictive coding hierarchy.

    regularity_continuation combines the statistical model (f01) with the
    exposure model (M-layer) to predict whether regularity persists.
    Bridwell 2017: cortical entrainment predicts continuation.

    detection_predict predicts upcoming detection performance by integrating
    pattern segmentation (P-layer), expertise state (M-layer), and current
    binding dynamics. Paraskevopoulos 2022: musicians predict irregularities
    with higher accuracy.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e_outputs: ``(f01, f02, f03, f04)`` from extraction layer.
        m_outputs: ``(exposure_model, pattern_memory, expertise_state)``
            from temporal integration layer.
        p_outputs: ``(expectation_formation, cross_modal_binding,
            pattern_segmentation)`` from P-layer.
        ednr: ``(B, T, 10)`` -- upstream EDNR relay output.

    Returns:
        ``(next_probability, regularity_continuation, detection_predict)``
        each ``(B, T)``
    """
    f01, f02, _f03, _f04 = e_outputs
    exposure_model, _pattern_memory, expertise_state = m_outputs
    _expectation_formation, cross_modal_binding, pattern_segmentation = p_outputs

    # -- H3 features --
    amp_100ms = h3_features[_AMP_VAL_H3]                 # (B, T)
    loudness_range_500 = h3_features[_LOUDNESS_RANGE_H8]  # (B, T)
    coupling_100ms = h3_features[_COUPLING_VAL_H3]        # (B, T)
    binding_std_100 = h3_features[_BINDING_STD_H3]        # (B, T)

    # -- next_probability --
    # sigma(0.50 * f01 + 0.50 * f02)
    # Carbajal & Malmierca 2018: top-down prediction in predictive coding
    next_probability = torch.sigmoid(
        0.50 * f01
        + 0.50 * f02
    )

    # -- regularity_continuation --
    # sigma(0.50 * f01 + 0.50 * exposure_model)
    # Bridwell 2017: pattern-specific cortical entrainment predicts continuation
    regularity_continuation = torch.sigmoid(
        0.50 * f01
        + 0.50 * exposure_model
    )

    # -- detection_predict --
    # Integrates pattern segmentation, expertise state, and binding dynamics.
    # sigma(0.30 * pattern_segmentation + 0.30 * expertise_state
    #      + 0.20 * cross_modal_binding + 0.20 * coupling_100ms)
    # Paraskevopoulos 2022: musicians predict with higher accuracy
    detection_predict = torch.sigmoid(
        0.30 * pattern_segmentation
        + 0.30 * expertise_state
        + 0.20 * cross_modal_binding
        + 0.20 * coupling_100ms
    )

    return next_probability, regularity_continuation, detection_predict
