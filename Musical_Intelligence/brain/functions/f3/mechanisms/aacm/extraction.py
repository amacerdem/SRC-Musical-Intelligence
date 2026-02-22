"""AACM E-Layer -- Extraction (3D).

Aesthetic-attention coupling features from sensory signals:
  E0: attentional_engage     (engagement driven by consonance and dissonance)
  E1: motor_inhibition       (response suppression during aesthetic listening)
  E2: savoring_effect        (prolonged aesthetic experience from dynamics)

H3 demands consumed:
  pleasant:    (3,3,0,2)   consonance value at 100ms
  roughness:   (0,16,1,2)  roughness mean over 1s
  loudness:    (8,3,0,2)   loudness value at 100ms
  x_l0l5:      (25,3,0,2)  coupling value at 100ms
  pleasant:    (3,16,8,2)  pleasant velocity at 1s
  x_l0l5:      (25,16,1,0) coupling mean at 1s L0
  pleasant:    (3,6,6,2)   pleasant periodicity at 150ms

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/aacm/
Sarasso 2019: consonant > dissonant aesthetic appreciation (EEG ERP, N=22).
Brattico 2013: fMRI evidence for aesthetic processing network (N=18).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_PLEAS_H3 = (3, 3, 0, 2)           # pleasant value at 100ms
_ROUGH_MEAN_1S = (0, 16, 1, 2)     # roughness mean over 1s
_PLEAS_VEL_1S = (3, 16, 8, 2)      # pleasant velocity at 1s
_COUPLING_MEAN_1S = (25, 16, 1, 0)  # coupling mean at 1s L0
_LOUD_H3 = (8, 3, 0, 2)            # loudness value at 100ms
_COUPLING_H3 = (25, 3, 0, 2)       # coupling value at 100ms (fast integration)
_PLEAS_PERIOD_150 = (3, 6, 6, 2)   # pleasant periodicity at 150ms


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: aesthetic-attention coupling extraction features.

    E0 models attentional engagement driven by consonance level minus
    sustained dissonance, modulated by loudness and integration coupling.
    E1 models motor inhibition (stillness) during aesthetic listening,
    reflecting the suppression of motor activity when attending to beauty.
    E2 models the savoring effect, prolonged aesthetic experience driven
    by pleasant dynamics and coupling.

    Sarasso 2019: N1/P2 enhanced for consonant intervals (80-194ms).
    Brattico 2013: vmPFC/NAcc activation for liked music (N=18).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``
    """
    pleasant_100ms = h3_features[_PLEAS_H3]
    roughness_mean_1s = h3_features[_ROUGH_MEAN_1S]
    loudness_100ms = h3_features[_LOUD_H3]
    coupling_100ms = h3_features[_COUPLING_H3]
    pleasant_vel_1s = h3_features[_PLEAS_VEL_1S]
    coupling_mean_1s = h3_features[_COUPLING_MEAN_1S]
    pleasant_period_150ms = h3_features[_PLEAS_PERIOD_150]

    # -- E0: Attentional Engage --
    # Engagement driven by consonance (pleasant) minus sustained dissonance
    # (inverted roughness), with loudness providing intensity context and
    # coupling providing integration context.
    # Sarasso 2019: consonant intervals capture attention (N1/P2 enhancement).
    e0 = torch.sigmoid(
        0.35 * pleasant_100ms
        + 0.30 * (1.0 - roughness_mean_1s)
        + 0.20 * loudness_100ms
        + 0.15 * coupling_100ms
    )

    # -- E1: Motor Inhibition --
    # Suppression of motor activity during aesthetic listening. Pleasant
    # stimuli + loudness intensity + integration coupling drive stillness.
    # Brattico 2013: aesthetic listening produces motor cortex deactivation.
    e1 = torch.sigmoid(
        0.35 * pleasant_100ms
        + 0.35 * loudness_100ms
        + 0.30 * coupling_100ms
    )

    # -- E2: Savoring Effect --
    # Prolonged aesthetic experience from pleasant dynamics (velocity),
    # sustained coupling, and rhythmic beauty (pleasant periodicity).
    # Brattico 2013: sustained vmPFC activation during liked passages.
    e2 = torch.sigmoid(
        0.35 * pleasant_vel_1s
        + 0.35 * coupling_mean_1s
        + 0.30 * pleasant_period_150ms
    )

    return e0, e1, e2
