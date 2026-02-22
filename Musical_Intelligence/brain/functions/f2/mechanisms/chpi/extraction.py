"""CHPI E-Layer -- Extraction (2D).

Cross-modal harmonic prediction gain and voice-leading parsimony:
  E0: crossmodal_prediction_gain  (harmonic change detection strength)
  E1: voiceleading_parsimony      (smoothness of voice-leading motion)

H3 demands consumed:
  harmonic_change:          (6,0,0,2), (6,3,0,2), (6,3,4,2)
  roughness:                (0,3,0,2)
  sensory_pleasantness:     (4,3,0,2)
  spectral_change:          (21,3,8,0)
  onset_strength:           (10,1,0,2)

R3 direct reads:
  tristimulus[18:21] -- harmonic balance for voice-leading parsimony

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/chpi/
Tillmann 2003: harmonic priming activates STG/IFG for chord transitions.
Koelsch 2005: ERAN amplitude reflects harmonic expectancy violation magnitude.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_TRISTIMULUS_START = 18
_TRISTIMULUS_END = 21

# -- H3 keys consumed ---------------------------------------------------------
_HARM_CHANGE_H0_VAL = (6, 0, 0, 2)
_HARM_CHANGE_H3_VAL = (6, 3, 0, 2)
_HARM_CHANGE_H3_MAX = (6, 3, 4, 2)
_ROUGHNESS_H3_VAL = (0, 3, 0, 2)
_CONSONANCE_H3_VAL = (4, 3, 0, 2)
_SPEC_CHANGE_H3_VEL = (21, 3, 8, 0)
_ONSET_H1_VAL = (10, 1, 0, 2)


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: cross-modal prediction gain and voice-leading parsimony.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    # -- R3 direct reads --
    trist_mean = r3_features[..., _TRISTIMULUS_START:_TRISTIMULUS_END].mean(
        dim=-1
    )  # (B, T) -- harmonic balance for voice-leading context

    # -- H3 features --
    harm_change_25ms = h3_features[_HARM_CHANGE_H0_VAL]
    harm_change_100ms = h3_features[_HARM_CHANGE_H3_VAL]
    harm_change_max = h3_features[_HARM_CHANGE_H3_MAX]
    roughness_100ms = h3_features[_ROUGHNESS_H3_VAL]
    consonance_100ms = h3_features[_CONSONANCE_H3_VAL]
    spec_change_vel = h3_features[_SPEC_CHANGE_H3_VEL]
    onset_50ms = h3_features[_ONSET_H1_VAL]

    # -- E0: Crossmodal Prediction Gain --
    # Cross-modal integration amplifies chord-change detection. Harmonic
    # change at multiple timescales (instantaneous + contextual + peak)
    # plus onset alignment signal.
    # Tillmann 2003: harmonic priming in STG/IFG.
    # Musacchia 2007: cross-modal brainstem enhancement.
    e0 = torch.sigmoid(
        0.30 * harm_change_25ms
        + 0.25 * harm_change_100ms
        + 0.25 * harm_change_max
        + 0.20 * onset_50ms
    )

    # -- E1: Voiceleading Parsimony --
    # Smoothness of voice-leading motion. Low spectral velocity + high
    # consonance + balanced harmonic structure = parsimonious motion.
    # Inverted roughness contributes (less tension = smoother transitions).
    # Koelsch 2005: smooth voice-leading reduces ERAN amplitude.
    e1 = torch.sigmoid(
        0.30 * consonance_100ms
        + 0.25 * trist_mean
        + 0.25 * (1.0 - roughness_100ms)
        + 0.20 * (1.0 - spec_change_vel)
    )

    return e0, e1
