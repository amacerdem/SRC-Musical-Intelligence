"""PWUP P-Layer -- Cognitive Present (3D).

Precision weights integrating upstream relay outputs with current state:
  P0: tonal_precision_weight     (weight for tonal prediction errors)
  P1: rhythmic_precision_weight  (weight for rhythmic prediction errors)
  P2: attenuated_response        (precision-gated PE attenuation)

This is the integration layer where upstream HTP and ICEM relay outputs
modulate the precision weights. HTP provides hierarchical prediction
quality; ICEM provides information content (surprise magnitude).

Upstream reads:
  HTP [3]  E3:hierarchy_gradient  -- hierarchical prediction quality
  HTP [7]  P0:sensory_match       -- low-level prediction accuracy
  ICEM [0] E0:information_content -- surprise magnitude
  ICEM [3] E3:defense_cascade     -- emotional defense activation

H3 demands consumed:
  consonance:      (4,16,1,0)  mean at 1s memory
  tonalness:       (14,16,1,0) mean at 1s memory
  tonal_stability: (41,16,1,0) mean at 1s memory
  periodicity:     (5,8,1,0)   mean at 500ms memory

R3 direct reads:
  [18:21] tristimulus1-3  (harmonic structure for tonal context)

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/pwup/
Quiroga-Martinez 2019: tonal vs atonal context modulates MMN (d=3, N=40).
Sedley et al. 2016: precision in auditory cortex modulates PE propagation.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_TRISTIMULUS_START = 18
_TRISTIMULUS_END = 21

# -- H3 keys consumed ---------------------------------------------------------
_CONSONANCE_H16_MEAN = (4, 16, 1, 0)        # consonance mean at 1s memory
_TONALNESS_H16_MEAN = (14, 16, 1, 0)        # tonalness mean at 1s memory
_TONAL_STAB_H16_MEAN = (41, 16, 1, 0)       # tonal_stability mean at 1s memory
_PERIODICITY_H8_MEAN = (5, 8, 1, 0)         # periodicity mean at 500ms memory

# -- Upstream relay indices ---------------------------------------------------
_HTP_HIERARCHY = 3      # HTP E3:hierarchy_gradient
_HTP_SENSORY = 7        # HTP P0:sensory_match
_ICEM_IC = 0            # ICEM E0:information_content
_ICEM_DEFENSE = 3       # ICEM E3:defense_cascade


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: precision weights for present-time PE processing.

    P0 (tonal precision weight) is high in tonal contexts where HTP
    hierarchy is strong and tonal features are stable. In atonal music,
    P0 drops, attenuating tonal PE (Quiroga-Martinez 2019: d=3).

    P1 (rhythmic precision weight) is high when rhythmic periodicity
    is reliable and sensory match from HTP confirms event timing.

    P2 (attenuated response) represents the net PE after precision gating:
    high IC (ICEM surprise) is suppressed when precision is high (expected
    context) but amplified when precision is low (uncertain context).

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        relay_outputs: ``{"HTP": (B, T, 12), "ICEM": (B, T, 13)}``

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    e0, e1 = e
    m0, m1 = m

    # -- Upstream relay features --
    htp = relay_outputs["HTP"]    # (B, T, 12)
    icem = relay_outputs["ICEM"]  # (B, T, 13)

    htp_hierarchy = htp[..., _HTP_HIERARCHY]     # hierarchy_gradient
    htp_sensory = htp[..., _HTP_SENSORY]         # sensory_match
    icem_ic = icem[..., _ICEM_IC]                # information_content
    icem_defense = icem[..., _ICEM_DEFENSE]      # defense_cascade

    # -- R3 direct reads --
    trist_mean = r3_features[..., _TRISTIMULUS_START:_TRISTIMULUS_END].mean(
        dim=-1
    )  # (B, T) -- harmonic structure proxy

    # -- H3 features --
    consonance_1s = h3_features[_CONSONANCE_H16_MEAN]
    tonalness_1s = h3_features[_TONALNESS_H16_MEAN]
    tonal_stab_1s = h3_features[_TONAL_STAB_H16_MEAN]
    periodicity_500ms = h3_features[_PERIODICITY_H8_MEAN]

    # -- P0: Tonal Precision Weight --
    # High in tonal contexts (high tonalness, consonance, stability, HTP
    # hierarchy). Drops in atonal contexts, reducing PE propagation.
    # Quiroga-Martinez 2019: tonal precision d=3 effect (0.8 tonal vs 0.5 atonal).
    p0 = torch.sigmoid(
        0.30 * e0
        + 0.25 * m0
        + 0.25 * htp_hierarchy
        + 0.20 * tonal_stab_1s
    )

    # -- P1: Rhythmic Precision Weight --
    # High when rhythmic context is predictable (periodicity + sensory
    # match from HTP). Drops during metric ambiguity or irregular rhythm.
    # Sedley 2016: auditory cortex precision gates timing predictions.
    p1 = torch.sigmoid(
        0.30 * e1
        + 0.25 * periodicity_500ms
        + 0.25 * htp_sensory
        + 0.20 * consonance_1s
    )

    # -- P2: Attenuated Response --
    # Net PE after precision gating. High IC (surprise) is suppressed when
    # combined precision is high (expected context) and amplified when
    # precision is low (uncertain context). Defense cascade adds bottom-up
    # urgency that partially bypasses precision gating.
    # Friston 2005: precision-weighted PE = precision * error.
    combined_precision = 0.50 * p0 + 0.50 * p1
    p2 = torch.sigmoid(
        0.35 * icem_ic * (1.0 - 0.5 * combined_precision)
        + 0.25 * m1
        + 0.20 * icem_defense
        + 0.20 * trist_mean
    )

    return p0, p1, p2
