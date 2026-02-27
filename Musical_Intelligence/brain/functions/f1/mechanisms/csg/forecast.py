"""CSG F-Layer — Forecast (3D).

Three forward predictions for consonance-salience dynamics:

  F0: valence_pred       — Predicted valence [-1, 1] (tanh)
  F1: processing_pred    — Predicted processing load [0, 1]
  F2: aesthetic_pred     — Predicted aesthetic appreciation [0, 1]

H3 consumed:
    (4, 16, 1, 2)   sensory_pleas mean H16 L2    — sustained pleasantness (reused)
    (4, 3, 8, 2)    sensory_pleas velocity H3 L2 — pleasantness direction (reused)
    (1, 8, 8, 0)    sethares velocity H8 L0      — dissonance dynamics (reused)
    (0, 3, 1, 2)    roughness mean H3 L2          — roughness context (reused)

R3 consumed:
    [4] sensory_pleasantness — consonance proxy

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/csg/CSG-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PLEAS_MEAN_1S = (4, 16, 1, 2)
_PLEAS_VEL = (4, 3, 8, 2)
_SETHARES_VEL = (1, 8, 8, 0)
_ROUGHNESS_MEAN = (0, 3, 1, 2)

# -- R3 indices ----------------------------------------------------------------
_PLEAS = 4


def compute_forecast(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/M outputs + H3/R3 context.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``. F0 is tanh-valued ``[-1, 1]``.
    """
    _e0, e1, e2 = e_outputs
    (_m0, _m1, m2) = m_outputs

    pleas_mean_1s = h3_features[_PLEAS_MEAN_1S]
    pleas_vel = h3_features[_PLEAS_VEL]
    sethares_vel = h3_features[_SETHARES_VEL]
    roughness_mean = h3_features[_ROUGHNESS_MEAN]

    consonance = r3_features[:, :, _PLEAS]
    ambiguity = 1.0 - torch.abs(consonance - 0.5) * 2

    # Velocity morphs are H³ signed, already [-1, 1] with 0 at origin

    # F0: Valence prediction [-1, 1]
    # Cheung: amygdala/hippocampus integrate uncertainty x surprise
    # Diversified: reduced E2 echo (0.25), added velocity trend (0.25)
    # and dissonance dynamics (0.15) for temporal prediction
    centered_pleas = (pleas_mean_1s - 0.5) * 2.0
    f0 = torch.tanh(
        0.25 * e2
        + 0.25 * pleas_vel
        + 0.35 * centered_pleas
        - 0.15 * sethares_vel
    )

    # F1: Processing load prediction
    # Bravo 2017: intermediate dissonance = highest processing demand
    f1 = torch.sigmoid(
        0.40 * e1 + 0.30 * ambiguity + 0.30 * roughness_mean
    )

    # F2: Aesthetic appreciation prediction
    # Sarasso 2019: consonance -> aesthetic preference (d=2.008)
    f2 = torch.sigmoid(0.50 * m2 + 0.50 * consonance)

    return f0, f1, f2
