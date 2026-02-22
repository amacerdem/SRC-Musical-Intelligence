"""MAA P-Layer — Cognitive Present (3D).

Present-processing integration for atonal aesthetic evaluation:
  P0: pattern_search        (active search for structure in atonal material)
  P1: context_assessment    (contextual evaluation with upstream signals)
  P2: aesthetic_evaluation  (integrated aesthetic judgment)

Dependencies:
  - PWUP (upstream): M1:uncertainty_index [idx 3]
  - UDP  (upstream): M1:pleasure_index    [idx 3]
  - IGFE (upstream): P0:gamma_synchronization [idx 4]

H3 demands consumed:
  sensory_pleasantness: (4,3,0,2) — instantaneous consonance
  roughness:            (0,3,0,2) — instantaneous dissonance
  periodicity:          (5,16,1,0) — tonal certainty memory
  tonalness:            (14,8,1,0) reused

See Brattico 2013: mPFC for aesthetic judgment, OFC for framing.
See Greenberg 2015: openness moderates complex music appreciation.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_SENSORY_PLEAS_H3_VAL = (4, 3, 0, 2)
_ROUGHNESS_H3_VAL = (0, 3, 0, 2)
_PERIODICITY_H16_MEAN = (5, 16, 1, 0)
_TONALNESS_H8_MEAN = (14, 8, 1, 0)

# -- Upstream output indices ---------------------------------------------------
_PWUP_M1 = 3             # PWUP M1:uncertainty_index
_UDP_M1 = 3              # UDP M1:pleasure_index
_IGFE_P0 = 4             # IGFE P0:gamma_synchronization


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: present-processing aesthetic evaluation.

    Integrates E/M internal representations with upstream signals from
    PWUP (uncertainty), UDP (pleasure), and IGFE (gamma synchronization)
    to produce an active pattern search, contextual assessment, and
    final aesthetic evaluation of atonal material.

    Brattico et al. 2013: mPFC engagement for aesthetic judgment.
    Greenberg et al. 2015: personality × complexity interaction.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        upstream_outputs: ``{"PWUP": (B, T, 10), "UDP": (B, T, 10),
                             "IGFE": (B, T, 9)}``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    e0, e1 = e
    m0, m1 = m

    pleas_h3 = h3_features[_SENSORY_PLEAS_H3_VAL]
    roughness_h3 = h3_features[_ROUGHNESS_H3_VAL]
    period_mean_1s = h3_features[_PERIODICITY_H16_MEAN]
    tonal_mean_500ms = h3_features[_TONALNESS_H8_MEAN]

    pwup = upstream_outputs["PWUP"]   # (B, T, 10)
    udp = upstream_outputs["UDP"]     # (B, T, 10)
    igfe = upstream_outputs["IGFE"]   # (B, T, 9)

    uncertainty = pwup[:, :, _PWUP_M1]      # PWUP M1:uncertainty_index
    pleasure = udp[:, :, _UDP_M1]           # UDP M1:pleasure_index
    gamma_sync = igfe[:, :, _IGFE_P0]       # IGFE P0:gamma_synchronization

    # -- P0: Pattern Search --
    # Active search for structure within atonal material. Driven by
    # complexity tolerance (E0), modulated by gamma synchronization
    # (IGFE) which indicates neural binding of disparate elements.
    # Berlyne 1971: exploration drive for novel/complex stimuli.
    p0 = torch.sigmoid(
        0.30 * e0
        + 0.25 * gamma_sync
        + 0.20 * (1.0 - period_mean_1s)
        + 0.15 * roughness_h3
        + 0.10 * m0
    )

    # -- P1: Context Assessment --
    # Contextual evaluation integrating uncertainty (PWUP) and pleasure
    # (UDP) with tonal anchoring and familiarity. Low tonalness + high
    # uncertainty signals challenging atonal context; pleasure moderates.
    # Brattico 2013: amygdala for affective evaluation.
    p1 = torch.sigmoid(
        0.25 * uncertainty
        + 0.25 * pleasure
        + 0.20 * tonal_mean_500ms
        + 0.15 * e1
        + 0.15 * m1
    )

    # -- P2: Aesthetic Evaluation --
    # Integrated aesthetic judgment combining framing effect (M0),
    # appreciation composite (M1), instantaneous consonance, and
    # upstream pleasure signal. This is the convergence point.
    # Brattico 2013: mPFC differentiates liked vs disliked aesthetic judgments.
    # Greenberg 2015: openness × complexity → preference.
    p2 = torch.sigmoid(
        0.25 * m0
        + 0.25 * m1
        + 0.20 * pleas_h3
        + 0.15 * pleasure
        + 0.15 * p0
    )

    return p0, p1, p2
