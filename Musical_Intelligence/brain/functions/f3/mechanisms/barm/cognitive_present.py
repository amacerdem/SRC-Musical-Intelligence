"""BARM P-Layer -- Cognitive Present (2D).

Present-time brainstem modulation integrating upstream SNEM relay:
  P0: beat_alignment_accuracy   (accuracy of beat-locked brainstem response)
  P1: regularization_strength   (strength of temporal regularization)

This layer reads SNEM relay output (same ASU unit) to integrate cortical
entrainment context with brainstem modulation signals. SNEM P1 index 7
provides entrainment_strength which modulates the accuracy of brainstem
beat alignment.

Upstream reads:
  SNEM[7]  P1:entrainment_strength -- cortical entrainment context

H3 demands consumed:
  amplitude:  (7,16,1,2)  mean at 1s integration

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/barm/
Tierney & Kraus 2013: beat sync ability predicts ABR consistency (r=0.65).
Skoe & Kraus 2010: cortical modulation enhances subcortical encoding.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_AMPLITUDE_H16_MEAN = (7, 16, 1, 2)         # amplitude mean 1s integration

# -- Upstream relay index ------------------------------------------------------
_SNEM_ENTRAINMENT = 7   # SNEM P1:entrainment_strength


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: present-time brainstem modulation with SNEM context.

    P0 (beat_alignment_accuracy) integrates beat alignment (E1), veridical
    perception (M0), and SNEM entrainment strength. When cortical
    entrainment is strong, brainstem responses become more precisely
    aligned to beat structure via top-down modulation.

    P1 (regularization_strength) combines regularization effect (M1),
    regularization tendency (E0), and sustained amplitude level. Stronger
    regularization arises when the brainstem compensates for temporal
    irregularity under cortical guidance.

    Tierney & Kraus 2013: participants with stronger beat synchronization
    (motor-auditory coupling) show more consistent brainstem responses
    (r=0.65, p<0.001, N=30).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        relay_outputs: ``{"SNEM": (B, T, 12)}``

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, e1, _e2 = e
    m0, m1 = m

    # -- Upstream relay features --
    snem = relay_outputs["SNEM"]                             # (B, T, 12)
    snem_entrainment = snem[..., _SNEM_ENTRAINMENT]          # (B, T)

    # -- H3 features --
    amplitude_mean_1s = h3_features[_AMPLITUDE_H16_MEAN]     # (B, T)

    # -- P0: Beat Alignment Accuracy --
    # Accurate beat alignment requires: (1) good beat alignment from E1,
    # (2) veridical perception from M0, and (3) cortical entrainment
    # context from SNEM. Top-down entrainment sharpens brainstem timing.
    # Tierney 2013: beat sync predicts ABR consistency (r=0.65).
    p0 = torch.sigmoid(
        0.35 * e1
        + 0.35 * m0
        + 0.30 * snem_entrainment
    )

    # -- P1: Regularization Strength --
    # Net regularization strength integrates the temporal regularization
    # effect (M1), the innate tendency to regularize (E0), and sustained
    # amplitude level (louder stimuli elicit stronger brainstem responses).
    # Musacchia 2007: ABR amplitude enhanced in musicians (d=0.8).
    p1 = torch.sigmoid(
        0.40 * m1
        + 0.30 * e0
        + 0.30 * amplitude_mean_1s
    )

    return p0, p1
