"""ICEM E-Layer — Extraction (4D).

Information content and emotional response features:
  E0: information_content   (event unexpectedness — IC proxy)
  E1: arousal_response      (physiological activation from IC)
  E2: valence_response      (emotional valence change from IC)
  E3: defense_cascade       (threat appraisal activation)

H3 demands consumed:
  spectral_flux:          (21,3,0,2), (21,3,13,2)
  distribution_entropy:   (22,3,8,0)
  onset_strength:         (11,3,0,2)
  loudness:               (10,16,8,2)
  sensory_pleasantness:   (4,3,0,2)
  pitch_salience:         (39,4,8,0)
  tonal_stability:        (60,16,1,0)

See Docs/C3/Models/PCU-a3-ICEM/ICEM.md §7.2 formulas.
Egermann 2013: IC peaks → arousal↑, valence↓, SCR↑, HR↓.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_SPECTRAL_FLUX_H3_VAL = (21, 3, 0, 2)
_SPECTRAL_FLUX_H3_ENTROPY = (21, 3, 13, 2)
_ENTROPY_VEL_H3 = (22, 3, 8, 0)
_ONSET_H3_VAL = (11, 3, 0, 2)
_LOUDNESS_H16_VEL = (10, 16, 8, 2)
_CONSONANCE_H3_VAL = (4, 3, 0, 2)
_PITCH_SAL_H4_VEL = (39, 4, 8, 0)
_TONAL_STAB_H16_MEAN = (60, 16, 1, 0)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: information content and emotional features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``
    """
    spectral_flux_100ms = h3_features[_SPECTRAL_FLUX_H3_VAL]
    spectral_flux_entropy = h3_features[_SPECTRAL_FLUX_H3_ENTROPY]
    entropy_vel_100ms = h3_features[_ENTROPY_VEL_H3]
    onset_100ms = h3_features[_ONSET_H3_VAL]
    loudness_vel_1s = h3_features[_LOUDNESS_H16_VEL]
    consonance_100ms = h3_features[_CONSONANCE_H3_VAL]
    pitch_sal_vel = h3_features[_PITCH_SAL_H4_VEL]
    tonal_stab_mean_1s = h3_features[_TONAL_STAB_H16_MEAN]

    # -- E0: Information Content --
    # Event unexpectedness proxy: spectral change entropy (distributional
    # unpredictability) + spectral flux (raw change) + energy change velocity.
    # Egermann 2013: IDyOM IC peaks predict emotional responses (p<0.001).
    e0 = torch.sigmoid(
        0.35 * spectral_flux_entropy
        + 0.35 * spectral_flux_100ms
        + 0.30 * entropy_vel_100ms
    )

    # -- E1: Arousal Response --
    # Physiological activation: IC drives arousal via mid-level dynamics
    # (pitch salience velocity) + onset detection.
    # Egermann 2013: high IC → arousal↑, SCR↑ (p<0.001).
    e1 = torch.sigmoid(
        0.40 * e0 + 0.30 * pitch_sal_vel + 0.30 * onset_100ms
    )

    # -- E2: Valence Response --
    # Emotional valence: INVERSE of IC. Low IC → high valence (expected
    # events feel good). Consonance + tonal stability contribute positively.
    # Egermann 2013: high IC → valence↓ (p<0.001).
    e2 = torch.sigmoid(
        0.40 * (1.0 - e0)
        + 0.30 * tonal_stab_mean_1s
        + 0.30 * consonance_100ms
    )

    # -- E3: Defense Cascade --
    # Threat appraisal: multiplicative IC×arousal product + loudness
    # velocity (sudden loud events trigger orienting response).
    # Egermann 2013: subjective unexpected → RespR↑ (p<0.001).
    e3 = torch.sigmoid(
        0.50 * e0 * e1 + 0.50 * loudness_vel_1s
    )

    return e0, e1, e2, e3
