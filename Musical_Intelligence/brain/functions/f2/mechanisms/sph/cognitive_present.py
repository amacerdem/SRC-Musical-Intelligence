"""SPH P-Layer — Cognitive Present (3D).

Present-processing memory match and prediction error:
  P0: memory_match        (positive memory match — memorised response)
  P1: prediction_error    (negative prediction error — varied response)
  P2: deviation_detection (error magnitude at deviation point)

H3 demands consumed:
  amplitude:            (7,3,0,2)
  onset_strength:       (11,3,0,2)
  spectral_flux:        (21,3,0,2) reused
  distribution_entropy: (22,4,8,0)
  pitch_height:         (37,3,0,2)
  pitch_salience:       (39,3,0,2)

See Docs/C3/Models/PCU-a2-SPH/SPH.md §6.1 Layer P.
Bonetti 2024: hippocampus memory match/mismatch comparison.
Carbajal & Malmierca 2018: prediction error IC→MGB→AC hierarchy.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_AMPLITUDE_H3_VAL = (7, 3, 0, 2)
_ONSET_H3_VAL = (11, 3, 0, 2)
_SPECTRAL_FLUX_H3_VAL = (21, 3, 0, 2)
_ENTROPY_VEL_H4 = (22, 4, 8, 0)
_PITCH_HEIGHT_H3_VAL = (37, 3, 0, 2)
_PITCH_SAL_H3_VAL = (39, 3, 0, 2)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: memory match, prediction error, deviation detection.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        m: ``(M0, M1, M2, M3)`` from temporal integration layer.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    m0, m1, m2, m3 = m

    amplitude_100ms = h3_features[_AMPLITUDE_H3_VAL]
    onset_100ms = h3_features[_ONSET_H3_VAL]
    spectral_flux_100ms = h3_features[_SPECTRAL_FLUX_H3_VAL]
    entropy_vel_125ms = h3_features[_ENTROPY_VEL_H4]
    pitch_height_100ms = h3_features[_PITCH_HEIGHT_H3_VAL]
    pitch_sal_100ms = h3_features[_PITCH_SAL_H3_VAL]

    # -- P0: Memory Match --
    # Positive memory match in hippocampus. Match response + gamma power
    # + pitch salience (clarity of encoded pitch element).
    # Bonetti 2024: hippocampus memory match/mismatch comparison.
    p0 = torch.sigmoid(
        0.40 * m0 + 0.30 * m2 + 0.30 * pitch_sal_100ms
    )

    # -- P1: Prediction Error --
    # Negative prediction error. Varied response + alpha-beta power
    # + entropy velocity (rate of distributional change).
    # Carbajal & Malmierca 2018: prediction error propagates IC→MGB→AC.
    p1 = torch.sigmoid(
        0.40 * m1 + 0.30 * m3 + 0.30 * entropy_vel_125ms
    )

    # -- P2: Deviation Detection --
    # Error magnitude at the deviation point (tone introducing variation).
    # Raw spectral/onset/amplitude/pitch change at 100ms timescale.
    # Bonetti 2024: prediction error strongest at deviation tone.
    p2 = torch.sigmoid(
        0.35 * spectral_flux_100ms
        + 0.25 * onset_100ms
        + 0.20 * amplitude_100ms
        + 0.20 * pitch_height_100ms
    )

    return p0, p1, p2
