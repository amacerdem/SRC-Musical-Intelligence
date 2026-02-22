"""PSH P-Layer — Cognitive Present (3D).

Present-processing prediction silencing with upstream integration:
  P0: prediction_match      (accuracy of top-down prediction)
  P1: sensory_persistence   (low-level sensory signal that always persists)
  P2: binding_check         (dissociation between silencing and persistence)

This is the core silencing computation where the key formula is applied:
  High-level silencing:  post_high = repr * (1 - accuracy) -> 0 when correct
  Low-level persistence: post_low  = repr * 1.0 -> always persists

Upstream reads:
  HTP  [3]  E3:hierarchy_gradient     — hierarchical prediction quality
  PWUP [2]  M0:weighted_error         — precision-weighted PE
  UDP  [1]  E1:confirmation_reward    — prediction confirmation signal
  WMED [3]  M1:dissociation_index     — WM-entrainment dissociation
  MAA  [3]  M1:appreciation_composite — appreciation modulation

H3 demands consumed:
  amplitude:      (7,0,0,2), (7,1,0,2), (7,3,0,2) from temporal_integration
  onset_strength: (10,0,0,2), (10,3,0,2) from temporal_integration

R3 direct reads:
  [7]  amplitude      (low-level sensory for persistence)
  [11] onset_strength (PE trigger for persistence)

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/psh/
de Vries & Wurm 2023: prediction silencing hierarchy.
Todorovic 2012: repetition suppression as prediction.
Wacongne 2012: two cortical PE systems.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_AMPLITUDE = 7           # amplitude (B group, low-level sensory)
_ONSET_STRENGTH = 11     # onset_strength (B group, PE trigger)

# -- H3 keys consumed (reused from temporal_integration) ----------------------
_AMP_H0_VAL = (7, 0, 0, 2)        # amplitude at 25ms value integration
_AMP_H1_VAL = (7, 1, 0, 2)        # amplitude at 50ms value integration
_AMP_H3_VAL = (7, 3, 0, 2)        # amplitude at 100ms value integration
_ONSET_H0_VAL = (11, 0, 0, 2)     # onset_strength at 25ms value integration
_ONSET_H3_VAL = (11, 3, 0, 2)     # onset_strength at 100ms value integration

# -- Upstream output indices ---------------------------------------------------
_HTP_HIERARCHY = 3      # HTP E3:hierarchy_gradient
_PWUP_WEIGHTED_ERR = 2  # PWUP M0:weighted_error
_UDP_CONFIRM = 1        # UDP E1:confirmation_reward
_WMED_DISSOC = 3        # WMED M1:dissociation_index
_MAA_APPRECIATION = 3   # MAA M1:appreciation_composite


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: prediction match, sensory persistence, binding check.

    The core silencing formula:
      accuracy = sigmoid(0.30*htp_hierarchy + 0.30*pwup_error_inv
                         + 0.20*udp_confirm + 0.20*m0)
      P0 = accuracy (prediction_match — how well prediction explains input)
      P1 = sigmoid(0.40*e1 + 0.30*amp_h3 + 0.30*onset_h3) (sensory_persistence)
      P2 = sigmoid(0.50*(P1 - (1.0 - P0))) (binding_check — dissociation)

    When P0 is high (accurate prediction), high-level representations are
    silenced (explained away). P1 always persists because low-level sensory
    features are not affected by top-down prediction accuracy.
    P2 measures the dissociation: when P1 is high and (1-P0) is low
    (i.e. silencing is strong), the binding check is high.

    de Vries & Wurm 2023: eta_p^2=0.49, F(2)=19.9, p=8.3e-7.
    Todorovic 2012: low-level PE survives repetition suppression.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        upstream_outputs: ``{"HTP": (B,T,12), "PWUP": (B,T,10),
            "WMED": (B,T,11), "UDP": (B,T,10), "MAA": (B,T,10)}``

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    _e0, e1 = e
    m0, _m1 = m

    # -- Upstream relay features --
    htp = upstream_outputs["HTP"]      # (B, T, 12)
    pwup = upstream_outputs["PWUP"]    # (B, T, 10)
    udp = upstream_outputs["UDP"]      # (B, T, 10)

    htp_hierarchy = htp[..., _HTP_HIERARCHY]         # hierarchy_gradient
    pwup_error = pwup[..., _PWUP_WEIGHTED_ERR]       # weighted_error
    udp_confirm = udp[..., _UDP_CONFIRM]             # confirmation_reward

    # Invert PWUP error: low error = high prediction accuracy
    pwup_error_inv = 1.0 - pwup_error

    # -- H3 features for sensory persistence --
    amp_h3 = h3_features[_AMP_H3_VAL]       # amplitude at 100ms
    onset_h3 = h3_features[_ONSET_H3_VAL]   # onset_strength at 100ms

    # -- P0: Prediction Match (Accuracy) --
    # High-level silencing: stronger when prediction is accurate.
    # HTP hierarchy gradient indicates prediction quality at each level.
    # PWUP inverted error: low PE = good match.
    # UDP confirmation: reward for correct prediction.
    # M0 silencing efficiency: temporal context for silencing.
    accuracy = torch.sigmoid(
        0.30 * htp_hierarchy
        + 0.30 * pwup_error_inv
        + 0.20 * udp_confirm
        + 0.20 * m0
    )
    p0 = accuracy  # prediction_match

    # -- P1: Sensory Persistence --
    # Low-level persistence: always persists regardless of prediction.
    # post_low = repr * 1.0 — amplitude and onset continue as PE.
    # E1 (low-level extraction) + H3 amplitude/onset context.
    # de Vries & Wurm 2023: low-level persist post-stimulus.
    # Todorovic 2012: low-level PE survives repetition suppression.
    p1 = torch.sigmoid(
        0.40 * e1
        + 0.30 * amp_h3
        + 0.30 * onset_h3
    )  # sensory_persistence

    # -- P2: Binding Check --
    # Dissociation between silencing and persistence.
    # When prediction is accurate (P0 high -> 1-P0 low -> silencing strong)
    # and sensory persistence is high (P1 high), the dissociation is maximal.
    # P2 = sigmoid(0.50 * (P1 - (1.0 - P0)))
    # = sigmoid(0.50 * (persistence - residual_high_level))
    # de Vries & Wurm 2023: hierarchical dissociation eta_p^2 = 0.49.
    p2 = torch.sigmoid(
        0.50 * (p1 - (1.0 - p0))
    )  # binding_check

    return p0, p1, p2
