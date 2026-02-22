"""SLEE P-Layer -- Cognitive Present (3D).

Statistical Learning Expertise Enhancement present-state estimates:
  expectation_formation  -- Current distribution model state [0, 1]
  cross_modal_binding    -- Current multisensory integration strength [0, 1]
  pattern_segmentation   -- Current boundary detection [0, 1]

expectation_formation represents the instantaneous expectation formed from
the statistical model, combining the E-layer distribution estimate (f01)
with accumulated exposure (M-layer exposure_model). Under the Bayesian
predictive coding framework (Fong et al. 2020), this represents the prior
that generates predictions about upcoming auditory events. MMN as prediction
error under the Bayesian framework with hierarchical processing.

cross_modal_binding reflects the real-time strength of multisensory
integration, drawing from f03 (multisensory integration) and current
interaction feature values. This captures the ongoing activity of the IFG
supramodal hub in binding auditory, visual, and proprioceptive streams.
Paraskevopoulos 2022: IFG area 47m highest node degree in 5/6 network
states. Porfyri et al. 2025: left MFG, IFS, and insula show greatest
effective connectivity reorganization.

pattern_segmentation detects statistical boundaries using spectral change
at 100ms (H3 tuple 0), spectral trend at 125ms (H3 tuple 1), pitch change
at 100ms (H3 tuple 2), and mean pitch change over 1s (H3 tuple 3). When
spectral or pitch dynamics shift sharply relative to their running
baselines, a segment boundary is identified, signaling a transition
between statistical contexts. Bridwell 2017: cortical sensitivity
distinguishes patterned from random sequences (45% amplitude reduction).

H3 demands consumed (4 tuples):
  (21, 3, 0, 2)    spectral_flux value H3 L2     -- spectral change 100ms
  (21, 4, 18, 0)   spectral_flux trend H4 L0     -- spectral trend 125ms
  (23, 3, 0, 2)    pitch_change value H3 L2      -- pitch change 100ms
  (23, 16, 1, 2)   pitch_change mean H16 L2      -- mean pitch change 1s

Dependencies:
  E-layer f01 (statistical_model)
  E-layer f03 (multisensory_integration)
  M-layer exposure_model
  R3[21] spectral_change
  R3[23] pitch_change

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/slee/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_SPECTRAL_CHANGE_H3 = (21, 3, 0, 2)       # spectral change 100ms
_SPECTRAL_TREND_H4 = (21, 4, 18, 0)       # spectral trend 125ms
_PITCH_CHANGE_H3 = (23, 3, 0, 2)          # pitch change 100ms
_PITCH_CHANGE_MEAN_H16 = (23, 16, 1, 2)   # mean pitch change 1s


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    ednr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: instantaneous cognitive state of statistical learning.

    expectation_formation combines E-layer statistical model (f01) with
    M-layer exposure history to produce the current expectation state.
    Under Bayesian predictive coding (Fong et al. 2020), this represents
    the prior that generates predictions about upcoming auditory events.

    cross_modal_binding reflects real-time multisensory integration from
    E-layer f03 and the spectral change signal. Paraskevopoulos 2022:
    IFG area 47m is the primary supramodal hub. Porfyri et al. 2025:
    left MFG, IFS, and insula reorganization.

    pattern_segmentation detects statistical boundaries using spectral
    change at 100ms, spectral trend at 125ms, pitch change at 100ms,
    and mean pitch change over 1s. Sharp shifts relative to running
    baselines signal segment boundaries. Bridwell 2017: cortical
    sensitivity distinguishes patterned from random (45% reduction).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e_outputs: ``(f01, f02, f03, f04)`` from extraction layer.
        m_outputs: ``(exposure_model, pattern_memory, expertise_state)``
            from temporal integration layer.
        ednr: ``(B, T, 10)`` -- upstream EDNR relay output.

    Returns:
        ``(expectation_formation, cross_modal_binding, pattern_segmentation)``
        each ``(B, T)``
    """
    f01, _f02, f03, _f04 = e_outputs
    exposure_model, _pattern_memory, _expertise_state = m_outputs

    # -- H3 features --
    spectral_change_100 = h3_features[_SPECTRAL_CHANGE_H3]       # (B, T)
    spectral_trend_125 = h3_features[_SPECTRAL_TREND_H4]         # (B, T)
    pitch_change_100 = h3_features[_PITCH_CHANGE_H3]             # (B, T)
    pitch_change_mean_1s = h3_features[_PITCH_CHANGE_MEAN_H16]   # (B, T)

    # -- expectation_formation --
    # Combines E-layer statistical model (f01) with accumulated exposure
    # to produce the current expectation state.
    # sigma(0.50 * f01 + 0.50 * exposure_model)
    # Fong et al. 2020: MMN as prediction error under Bayesian framework
    expectation_formation = torch.sigmoid(
        0.50 * f01
        + 0.50 * exposure_model
    )

    # -- cross_modal_binding --
    # Real-time multisensory integration from f03 and spectral dynamics.
    # sigma(0.40 * f03 + 0.30 * spectral_change_100ms)
    # Paraskevopoulos 2022: IFG area 47m supramodal hub (5/6 states)
    # Porfyri et al. 2025: MFG, IFS, insula reorganization
    cross_modal_binding = torch.sigmoid(
        0.40 * f03
        + 0.30 * spectral_change_100
    )

    # -- pattern_segmentation --
    # Segment boundary detection from spectral and pitch dynamics.
    # sigma(0.25 * spectral_change_100ms + 0.25 * spectral_trend_125ms
    #      + 0.25 * pitch_change_100ms + 0.25 * pitch_change_mean_1s)
    # Bridwell 2017: cortical sensitivity patterned vs random (45% reduction)
    pattern_segmentation = torch.sigmoid(
        0.25 * spectral_change_100
        + 0.25 * spectral_trend_125
        + 0.25 * pitch_change_100
        + 0.25 * pitch_change_mean_1s
    )

    return expectation_formation, cross_modal_binding, pattern_segmentation
